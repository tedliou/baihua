#!/usr/bin/env python3
"""zh-tw-prose 的機械檢查：標點、中英空格、對岸用語、專案用詞表與常見 AI 腔片語。

只用 Python 標準函式庫，可在 Claude Code、claude.ai 與 Claude API 的容器中執行。

用法：
  python check.py 文章.md [其他檔案 ...]
  python check.py - < 草稿.txt
  python check.py 文章.md --glossary GLOSSARY.md --allow-semicolon

輸出每個問題一行：<檔案>:<行號>: <error|warning> [<規則>] <說明>
有 error 時結束碼為 1。warning 是 AI 腔的提示，要依語境判斷，預設不影響結束碼，
加上 --strict 時 warning 也會讓結束碼為 1。
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
USAGE_TABLE = SCRIPT_DIR.parent / "references" / "taiwan-usage.md"

HAN = "㐀-䶿一-鿿豈-﫿"
LATIN = "A-Za-z0-9"
MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdx"}


@dataclass
class Issue:
    path: str
    line: int
    level: str  # "error" 或 "warning"
    rule: str
    message: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: {self.level} [{self.rule}] {self.message}"


@dataclass
class Term:
    avoid: str
    use: str
    exceptions: tuple[str, ...]
    source: str  # "usage" 或 "glossary"


# AI 腔片語：只做提示，因為同樣的字在有內容支撐時可以保留。編號對應 references/patterns.md 與 translationese.md。
AI_PHRASES: list[tuple[str, str, str]] = [
    (r"值得(?:一提|注意|留意)的是|需要(?:注意|留意)的是", "P07", "提醒腔，改寫成後果或條件"),
    (r"綜上所述|總而言之|總的來說|總結來說|總結而言", "P17", "套話結尾，改成具體結論或直接結束"),
    (r"希望(?:本文|這篇|以上|這些)?(?:內容|文章|說明)?(?:能)?對(?:你|您|大家)有(?:所)?幫助", "P17", "套話結尾，直接刪除"),
    (r"在當今|瞬息萬變|隨著[^。！？\n]{0,12}(?:快速|迅速|蓬勃|飛速)發展", "P14", "公式化開場，從讀者的問題開始"),
    (r"至關重要|不可或缺|舉足輕重|關鍵所在", "P10", "評價詞，改寫成後果或數字"),
    (r"標誌著|新紀元|里程碑", "P13", "過度強調意義，寫實際改變了什麼"),
    (r"不是[^。！？\n]{1,40}?而是", "P02", "假對比，確認讀者真的有這個誤解，否則直接寫它是什麼"),
    (r"與其說[^。！？\n]{1,40}?不如說", "P02", "假對比，直接寫它是什麼"),
    (r"不(?:僅|只是|單是)[^。！？\n]{1,40}?更", "P02", "遞進式假對比，保留有證據的那一半"),
    (r"扮演(?:著)?[^。！？\n]{0,15}?角色", "T03", "迴避「是」，改用「是、負責、會」"),
    (r"(?:進行|加以|予以|作出|做出)(?:了)?(?:深入的?)?(?:討論|探討|分析|驗證|處理|說明|優化|調整|回應|決定)", "T01", "虛動詞加名詞，直接用動詞"),
    (r"深入探討|深度解析|全方位", "P09", "空泛的強調，寫具體內容"),
    (r"讓我們", "P15", "自我導覽，刪掉或直接寫內容"),
    (r"本(?:文|篇|頁|節)(?:將|會|要)(?:介紹|說明|探討|帶(?:你|您|大家))", "P15", "自我導覽，開頭直接給答案"),
    (r"無限可能|輕鬆上手|事半功倍|更上一層樓|如虎添翼", "P09", "推銷與空泛好處，寫具體結果"),
    (r"說真的|老實說|好問題", "P11", "假真誠與附和，直接回答"),
    (r"很多人(?:認為|覺得|都)|業界普遍|專家(?:指出|認為)", "P12", "模糊歸因，寫出來源或改成具體情境"),
]


def read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8-sig")


def parse_tables(markdown: str) -> list[list[dict[str, str]]]:
    """把 Markdown 表格解析成以表頭為鍵的列。"""
    tables: list[list[dict[str, str]]] = []
    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    for raw in markdown.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            if header is not None:
                tables.append(rows)
            header, rows = None, []
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if header is None:
            header = cells
            continue
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append({header[i]: cells[i] if i < len(cells) else "" for i in range(len(header))})
    if header is not None:
        tables.append(rows)
    return tables


def load_usage_terms(path: Path) -> list[Term]:
    terms: list[Term] = []
    for table in parse_tables(path.read_text(encoding="utf-8")):
        for row in table:
            if row.get("檢查") != "是" or not row.get("不要用"):
                continue
            exceptions = tuple(e.strip() for e in row.get("例外", "").split("、") if e.strip())
            terms.append(Term(row["不要用"], row.get("改用", ""), exceptions, "usage"))
    return terms


def load_glossary_terms(path: Path) -> list[Term]:
    terms: list[Term] = []
    for table in parse_tables(path.read_text(encoding="utf-8-sig")):
        for row in table:
            avoid_cell = row.get("不要用", "")
            use = next(iter(row.values()), "")
            for word in avoid_cell.split("、"):
                word = word.strip()
                # 括弧裡寫了例外的寫法只是提醒，不檢查。
                if not word or word in {"—", "-", "無"} or re.search(r"[（(]", word):
                    continue
                terms.append(Term(word, use, (), "glossary"))
    return terms


def prose_lines(text: str, markdown: bool) -> list[tuple[int, str]]:
    """回傳要檢查的 (行號, 文字)，去掉程式碼、網址與 Markdown 標記。

    行內程式碼與網址換成拉丁字母佔位，這樣「使用`npm`安裝」仍會被抓到缺少空格。
    """
    lines = text.splitlines()
    out: list[tuple[int, str]] = []
    in_fence = False
    fence_mark = ""
    start = 0
    if markdown and lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    for index in range(start, len(lines)):
        line = lines[index]
        stripped = line.lstrip()
        if markdown:
            fence = re.match(r"(`{3,}|~{3,})", stripped)
            if fence:
                if not in_fence:
                    in_fence, fence_mark = True, fence.group(1)[0]
                elif fence.group(1)[0] == fence_mark:
                    in_fence = False
                continue
            if in_fence or line.startswith("    ") and not stripped.startswith(("-", "*", "|", ">")):
                continue
            line = re.sub(r"`[^`]+`", "C", line)
            line = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", line)
            line = re.sub(r"<(https?://[^>]+)>", "U", line)
            line = re.sub(r"<!--.*?-->|</?[A-Za-z][^>]*>", "", line)
        line = re.sub(r"https?://[^\s)\]」，。]+", "U", line)
        out.append((index + 1, line))
    return out


def check_text(text: str, path: str, terms: list[Term], *, markdown: bool,
               allow_semicolon: bool = False, check_space: bool = True,
               hints: bool = True) -> list[Issue]:
    issues: list[Issue] = []

    def add(line_no: int, level: str, rule: str, message: str) -> None:
        issues.append(Issue(path, line_no, level, rule, message))

    for line_no, line in prose_lines(text, markdown):
        has_han = re.search(f"[{HAN}]", line) is not None
        if not has_han:
            continue

        for term in terms:
            for m in re.finditer(re.escape(term.avoid), line):
                if any(_covered(line, m.start(), m.end(), ex) for ex in term.exceptions):
                    continue
                if term.source == "usage":
                    add(line_no, "error", "taiwan-usage", f"「{term.avoid}」改用「{term.use}」")
                else:
                    add(line_no, "error", "glossary", f"用詞表不用「{term.avoid}」，改用「{term.use}」")
                break

        if not allow_semicolon and re.search(f"；|(?<=[{HAN}]);|;(?=[{HAN}])", line):
            add(line_no, "error", "semicolon", "不用分號，改成句號或逗號並確認前後銜接")

        half = re.search(f"(?<=[{HAN}])[,:!?]|[,:!?](?=[{HAN}])|(?<=[{HAN}])\\.(?=\\s|$|[{HAN}])", line)
        if half:
            add(line_no, "error", "fullwidth", f"中文句子裡的「{half.group(0)}」改用全形標點")

        if re.search("[“”‘’]", line) or re.search(f'(?<=[{HAN}])"|"(?=[{HAN}])', line):
            add(line_no, "error", "quotes", "中文引號用「」與『』，不用 “” 或 \"")

        if re.search(f"(?<=[{HAN}])\\.{{3}}|\\.{{3}}(?=[{HAN}])|。。。", line):
            add(line_no, "error", "ellipsis", "刪節號用「……」")

        if check_space:
            gap = re.search(f"[{HAN}][{LATIN}]|[{LATIN}][{HAN}]", line)
            if gap:
                add(line_no, "error", "spacing", f"中文與英文、數字之間加半形空格：「{gap.group(0)}」")

        if re.search("(?<!—)—(?!—)", line) or re.search(f"(?<=[{HAN}])\\s?--\\s?(?=[{HAN}])", line):
            add(line_no, "warning", "dash", "破折號寫成「——」並少用，補充說明多半可以改成另一句")

        if re.search("[！？]{2,}", line):
            add(line_no, "warning", "exclamation", "不連用驚嘆號或問號")

        if hints:
            for pattern, ref, message in AI_PHRASES:
                m = re.search(pattern, line)
                if m:
                    add(line_no, "warning", f"ai-{ref}", f"「{m.group(0)}」：{message}")

    return issues


def _covered(line: str, start: int, end: int, exception: str) -> bool:
    """這次比對到的詞是不是某個例外詞的一部分，例如「演算法」裡的「算法」。"""
    for m in re.finditer(re.escape(exception), line):
        if m.start() <= start and end <= m.end():
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="檢查正體中文文字的標點、空格、用語與常見 AI 腔片語。")
    parser.add_argument("paths", nargs="+", help="要檢查的檔案，用 - 代表標準輸入")
    parser.add_argument("--glossary", action="append", default=[], help="專案用詞表（Markdown 表格，含「不要用」欄），可重複指定")
    parser.add_argument("--allow-semicolon", action="store_true", help="允許分號")
    parser.add_argument("--no-spacing", action="store_true", help="不檢查中英之間的空格")
    parser.add_argument("--no-hints", action="store_true", help="不列出 AI 腔片語的提示")
    parser.add_argument("--strict", action="store_true", help="warning 也讓結束碼為 1")
    parser.add_argument("--markdown", action="store_true", help="把標準輸入當成 Markdown 處理")
    args = parser.parse_args(argv)

    terms = load_usage_terms(USAGE_TABLE)
    for glossary in args.glossary:
        path = Path(glossary)
        if not path.is_file():
            print(f"找不到用詞表：{glossary}", file=sys.stderr)
            return 2
        terms.extend(load_glossary_terms(path))

    all_issues: list[Issue] = []
    for path in args.paths:
        try:
            text = read_text(path)
        except (OSError, UnicodeDecodeError) as error:
            print(f"無法讀取 {path}：{error}", file=sys.stderr)
            return 2
        markdown = args.markdown if path == "-" else Path(path).suffix.lower() in MARKDOWN_SUFFIXES
        all_issues.extend(check_text(
            text, path, terms, markdown=markdown,
            allow_semicolon=args.allow_semicolon,
            check_space=not args.no_spacing,
            hints=not args.no_hints,
        ))

    for issue in all_issues:
        print(issue.format())
    errors = sum(1 for i in all_issues if i.level == "error")
    warnings = len(all_issues) - errors
    print(f"共 {errors} 個 error、{warnings} 個 warning。")
    if errors or (args.strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

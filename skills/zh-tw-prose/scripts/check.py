#!/usr/bin/env python3
"""zh-tw-prose 的機械檢查：標點、中英空格、對岸用語、專案用詞表與常見 AI 腔片語。

只用 Python 標準函式庫，可在 Claude Code、claude.ai 與 Claude API 的容器中執行。

用法：
  python check.py 文章.md [其他檔案 ...]
  python check.py - < 草稿.txt
  python check.py 文章.md --glossary GLOSSARY.md --allow-semicolon
  python check.py --compare 改前.md 改後.md [--stage structure|style]

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
    (r"(?:舊|網路上的|常見的|一般的)教學|很多(?:文章|教學)", "P12", "讀者沒看過的來源，改寫成讀者做過的事或版本差異"),
    (r"要(?:先)?(?:看|等)[^，。！？\n]{1,24}(?:，[^，。！？\n]{0,12})?才(?:會|能)", "P26", "鋪陳句，條件在前、結果在後一次講完"),
    (r"(\S)不\1[^，。！？\n]{0,12}，要(?:先)?看", "P26", "鋪陳句，刪掉問句，直接寫結果"),
    (r"因為[^。！？\n]{1,60}。\s*因此", "P27", "「因為」開頭的句子，下一句不用「因此」開頭"),
    (r"，而(?:且)?[^，。！？\n]{1,20}也", "P27", "「而」和「也」疊在一起，留「也」就好"),
]


# 文體輪廓用的計數項。依據見 docs/theory.md：翻譯中文與模型中文的連接詞、主語代名詞、
# 限定詞、「的」字修飾與「被」字句都比母語中文多，句長也比較平均。
PROFILE_ITEMS: list[tuple[str, str, str]] = [
    ("connectives", "連接詞", r"因此|所以|但是|然而|而且|並且|此外|同時|另外|因為|由於|如果|雖然|不過|因而|從而|進而|以及|甚至|換句話說|也就是說|總之|首先|其次"),
    ("pronouns", "代名詞", r"它們|它|他們|她們|我們|你們|你|您"),
    ("determiners", "限定詞", r"一個|這個|這些|(?<!應)該(?=[^死不會要怎])"),
    ("bei", "被字句", r"被(?![子單褥])"),
    ("light_verbs", "虛動詞", r"進行|作出|做出|加以|予以"),
]
# 小標結尾是動作名詞化的「X 的 Y」（T12）。「設定、更新、判斷」常當名詞用，不放進來。
NOMINAL_HEADING = (r"^\s{0,3}#{1,6}\s+\S.*的(選擇|複製|確認|處理|安裝|修改|建立|檢查|啟動|移除|下載|執行|切換|搬移|轉換|調整|還原|停用)"
                   r"\s*#*\s*$")
DE_PARTICLE = r"的(?!確|話|士|是)(?<!目的)(?<!標的)"
CLAUSE_SPLIT = r"[，。！？；：,.!?;:\n「」『』（）()]"


def profile_text(text: str, markdown: bool = True) -> dict[str, float]:
    """計算文體輪廓：每千字的各項次數、「的」的密度、句長的平均與變異係數。

    這些數字沒有對錯的門檻，用途是和同一語域的人寫文字比較，或比較改稿前後。
    """
    body = "\n".join(line for _, line in prose_lines(text, markdown))
    han = len(re.findall(f"[{HAN}]", body)) or 1
    result: dict[str, float] = {"han_chars": han}
    for key, _, pattern in PROFILE_ITEMS:
        result[key] = round(len(re.findall(pattern, body)) * 1000 / han, 2)
    result["de"] = round(len(re.findall(DE_PARTICLE, body)) * 100 / han, 2)
    sentences = [len(re.findall(f"[{HAN}]", s)) for s in re.split(r"[。！？\n]", body)]
    sentences = [n for n in sentences if n >= 2]
    if sentences:
        mean = sum(sentences) / len(sentences)
        var = sum((n - mean) ** 2 for n in sentences) / len(sentences)
        result["sent_mean"] = round(mean, 1)
        result["sent_cv"] = round((var ** 0.5) / mean, 2) if mean else 0.0
    return result


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
            add(line_no, "warning", "semicolon", "段落裡的分號改成句號或逗號，介面字串與數值欄位可以保留")

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

        for clause in re.split(CLAUSE_SPLIT, line):
            if len(re.findall(DE_PARTICLE, clause)) >= 3:
                add(line_no, "warning", "ai-T05", f"「{clause.strip()[:24]}」一個分句裡有三個以上的「的」，把修飾語拆成另一句")
                break

        if re.search("[！？]{2,}", line):
            add(line_no, "warning", "exclamation", "不連用驚嘆號或問號")

        if hints:
            for pattern, ref, message in AI_PHRASES:
                m = re.search(pattern, line)
                if m:
                    add(line_no, "warning", f"ai-{ref}", f"「{m.group(0)}」：{message}")
            m = re.search(NOMINAL_HEADING, line) if markdown else None
            if m:
                add(line_no, "warning", "ai-T12", f"小標「的{m.group(1)}」：讀者要動手的小節改成動詞加受詞，說明性的小節可以保留")

    return issues


def _covered(line: str, start: int, end: int, exception: str) -> bool:
    """這次比對到的詞是不是某個例外詞的一部分，例如「演算法」裡的「算法」。"""
    for m in re.finditer(re.escape(exception), line):
        if m.start() <= start and end <= m.end():
            return True
    return False


# 交接檢查（--compare）：比較同一份稿件改稿前後，抓出事實消失、文風階段動到結構，
# 以及句子被壓短或連接詞補過頭。虛詞是交代分句關係的單字與短詞，精簡過頭時會一起下降。
GLUE = r"會|就|才|也|再|而|如果|因此|這時|但|讓|並|時"
NUMBER = (r"\d+(?:[.,]\d+)*(?:\s?(?:GB|MB|KB|TB|ms|fps|Hz|px|%|秒|分鐘|小時|天|次|個|字元|萬|倍|元|美元"
          r"|埠|欄|行|筆|頁|張|篇|題|版))?")
GLUE_DROP = 0.95  # 改後的虛詞密度低於改前的 95%
GLUE_RISE = 1.2   # 改後的虛詞密度高於改前的 120%
FACT_LABELS = {"fences": "程式碼區塊", "inline": "行內程式碼", "links": "連結", "images": "圖片", "numbers": "數字"}


def extract_facts(markdown: str) -> dict:
    """取出交接檢查要比對的事實元素、結構與虛詞密度。"""
    text = markdown.replace("\r\n", "\n")
    m = re.match(r"^---\n.*?\n---\n", text, re.S)
    if m:
        text = text[m.end():]
    # 先切出程式碼區塊，區塊裡的 <!-- 與連結寫法不算正文。列表裡縮排的區塊也算，
    # 關閉的圍欄要用同一種字元、長度不短於開頭。沒有關閉的區塊延伸到檔尾。
    fences: list[str] = []
    kept: list[str] = []
    block: list[str] | None = None
    opener = ""
    for line in text.split("\n"):
        if block is None:
            m = re.match(r"^\s*(`{3,}|~{3,})", line)
            if m:
                block, opener = [line.strip()], m.group(1)
                kept.append("")
            else:
                kept.append(line)
            continue
        block.append(line.strip())
        if re.fullmatch(rf"\s*{re.escape(opener[0])}{{{len(opener)},}}\s*", line):
            fences.append("\n".join(block))
            block = None
    if block is not None:
        fences.append("\n".join(block))
    body = re.sub(r"<!--.*?-->", "", "\n".join(kept), flags=re.S)
    inline = re.findall(r"`([^`\n]+)`", body)
    body = re.sub(r"`[^`\n]+`", " C ", body)
    images = re.findall(r"!\[[^\]]*\]\(([^)\s]+)", body)
    # 圖片換成替代文字後再找連結，包住圖片的連結（徽章）才抓得到外層網址。
    unimaged = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", body)
    links = re.findall(r"\[[^\]]*\]\((\S+?)(?:\s+\"[^\"]*\")?\)", unimaged)
    lines = body.split("\n")
    headings = [ln.strip() for ln in lines if re.match(r"^#{1,6}\s+\S", ln)]
    tables = table_rows = 0
    for i, ln in enumerate(lines):
        if not re.match(r"^\s*\|", ln):
            continue
        if i == 0 or not re.match(r"^\s*\|", lines[i - 1]):
            tables += 1
        if not re.fullmatch(r"\s*\|[\s:|-]+\|\s*", ln):
            table_rows += 1
    prose = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", unimaged)
    prose = re.sub(r"</?[A-Za-z][^>]*>", "", prose)
    prose = re.sub(r"https?://\S+", " ", prose)
    numbers = [n.replace(" ", "") for n in re.findall(NUMBER, prose)]
    numbers = [n for n in numbers if len(n) > 1 or not n.isdigit()]
    # 虛詞只算段落與條列，表格與小標多是名詞片語，算進去會稀釋。
    paragraphs = "\n".join(ln for ln in prose.split("\n") if not re.match(r"^\s*\||^#{1,6}\s", ln))
    para_han = len(re.findall(f"[{HAN}]", paragraphs))
    return {
        "fences": fences, "inline": inline, "links": links, "images": images, "numbers": numbers,
        "headings": headings, "tables": tables, "table_rows": table_rows,
        "han": len(re.findall(f"[{HAN}]", prose)),
        "glue": round(len(re.findall(GLUE, paragraphs)) * 1000 / para_han, 1) if para_han else 0.0,
    }


def _missing(a: list[str], b: list[str]) -> list[str]:
    seen = set(b)
    return [x for x in dict.fromkeys(a) if x not in seen]


def compare_texts(before: str, after: str, stage: str = "any") -> dict:
    """比較改稿前後。stage 是 structure（可以刪改結構）、style（只改句子）或 any。"""
    b, a = extract_facts(before), extract_facts(after)
    removed = {k: _missing(b[k], a[k]) for k in FACT_LABELS}
    added = {k: _missing(a[k], b[k]) for k in ("links", "numbers")}
    flags: list[str] = []
    if any(removed.values()):
        if stage == "style":
            flags.append("fact-removed：只改句子時不應刪掉任何事實元素")
        else:
            flags.append("fact-removed：有事實元素消失，每一項都要能說出刪除的理由，例如重複或超出範圍")
    if stage == "style" and any(added.values()):
        flags.append("fact-added：只改句子時新增了數字或連結，確認不是補上素材沒有的事實")
    if stage == "style" and (len(b["headings"]), b["tables"], b["table_rows"]) != (len(a["headings"]), a["tables"], a["table_rows"]):
        flags.append("structure-changed：只改句子時動到小標或表格的數量，這屬於結構的範圍")
    if b["glue"] and a["glue"] < b["glue"] * GLUE_DROP:
        flags.append(f"glue-drop：虛詞每千字從 {b['glue']} 降到 {a['glue']}，句子可能被壓短。精簡只刪重複的資訊與整句，不刪「會、就、如果、這時」這類交代關係的詞")
    if b["glue"] and a["glue"] > b["glue"] * GLUE_RISE:
        flags.append(f"glue-rise：虛詞每千字從 {b['glue']} 升到 {a['glue']}，確認連接詞沒有補過頭")
    return {
        "stage": stage,
        "han": (b["han"], a["han"]),
        "glue": (b["glue"], a["glue"]),
        "headings": (len(b["headings"]), len(a["headings"])),
        "tables": (b["tables"], a["tables"]),
        "table_rows": (b["table_rows"], a["table_rows"]),
        "removed_headings": _missing(b["headings"], a["headings"]),
        "added_headings": _missing(a["headings"], b["headings"]),
        "removed": removed,
        "added": added,
        "flags": flags,
    }


def format_compare(r: dict) -> str:
    before, after = r["han"]
    change = round((after - before) * 100 / before) if before else 0
    out = [f"交接檢查（{r['stage']}）",
           f"漢字數：{before} → {after}（{change:+d}%）",
           f"小標：{r['headings'][0]} → {r['headings'][1]}，表格：{r['tables'][0]} → {r['tables'][1]}，表格列：{r['table_rows'][0]} → {r['table_rows'][1]}",
           f"虛詞每千字：{r['glue'][0]} → {r['glue'][1]}"]
    for key, items in r["removed"].items():
        if items:
            out.append(f"消失的{FACT_LABELS[key]}：" + "、".join(x.split("\n")[0][:80] for x in items))
    for key, items in r["added"].items():
        if items:
            out.append(f"新增的{FACT_LABELS[key]}：" + "、".join(items))
    if r["removed_headings"]:
        out.append("刪除或改名的小標：" + "、".join(r["removed_headings"]))
    if r["added_headings"]:
        out.append("新增或改名後的小標：" + "、".join(r["added_headings"]))
    out.append("需要確認：\n- " + "\n- ".join(r["flags"]) if r["flags"] else "沒有需要確認的項目。")
    return "\n".join(out)


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
    parser.add_argument("--compare", action="store_true", help="交接檢查：比較兩個檔案（改前、改後），回報消失的事實、結構變動與虛詞密度變化")
    parser.add_argument("--stage", choices=["any", "structure", "style"], default="any", help="--compare 用：style 表示只改句子，結構與事實都不該變")
    parser.add_argument("--profile", action="store_true", help="另外印出文體輪廓：每千字的連接詞、代名詞、限定詞、被字句、虛動詞，「的」的密度與句長變化")
    args = parser.parse_args(argv)

    if args.compare:
        if len(args.paths) != 2 or "-" in args.paths:
            print("--compare 需要兩個檔案：改前與改後", file=sys.stderr)
            return 2
        try:
            before, after = (read_text(p) for p in args.paths)
        except (OSError, UnicodeDecodeError) as error:
            print(f"無法讀取：{error}", file=sys.stderr)
            return 2
        report = compare_texts(before, after, args.stage)
        print(format_compare(report))
        return 1 if args.strict and report["flags"] else 0

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
        if args.profile:
            p = profile_text(text, markdown)
            labels = {key: label for key, label, _ in PROFILE_ITEMS}
            parts = [f"{labels[k]} {p[k]}" for k in labels]
            parts.append(f"「的」每百字 {p['de']}")
            if "sent_mean" in p:
                parts.append(f"句長平均 {p['sent_mean']} 字、變異係數 {p['sent_cv']}")
            print(f"{path}: profile 每千字：" + "，".join(parts))

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

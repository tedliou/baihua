"""check.py 的單元測試。執行：python -m unittest discover -s tests"""

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "zh-tw-prose" / "scripts" / "check.py"

spec = importlib.util.spec_from_file_location("check", SCRIPT)
check = importlib.util.module_from_spec(spec)
sys.modules["check"] = check
spec.loader.exec_module(check)

TERMS = check.load_usage_terms(check.USAGE_TABLE)


def rules(text, markdown=True, **kwargs):
    issues = check.check_text(text, "t.md", TERMS, markdown=markdown, **kwargs)
    return [(i.level, i.rule) for i in issues]


class UsageTableTest(unittest.TestCase):
    def test_table_loads_checked_terms_only(self):
        avoid = {t.avoid for t in TERMS}
        self.assertIn("視頻", avoid)
        self.assertIn("算法", avoid)
        self.assertNotIn("菜單", avoid)
        self.assertNotIn("程序", avoid)

    def test_exception_word_is_skipped(self):
        self.assertNotIn(("error", "taiwan-usage"), rules("這個演算法的時間複雜度是 O(n)。"))
        self.assertIn(("error", "taiwan-usage"), rules("這個算法的時間複雜度是 O(n)。"))

    def test_mainland_terms(self):
        self.assertIn(("error", "taiwan-usage"), rules("系統默認會緩存資料。"))
        self.assertEqual(rules("系統預設會快取資料。"), [])


class PunctuationTest(unittest.TestCase):
    def test_semicolon(self):
        self.assertIn(("warning", "semicolon"), rules("先安裝套件；再執行指令。"))
        self.assertNotIn(("warning", "semicolon"), rules("先安裝套件；再執行指令。", allow_semicolon=True))

    def test_halfwidth_punctuation(self):
        self.assertIn(("error", "fullwidth"), rules("先安裝套件,再執行指令。"))
        self.assertIn(("error", "fullwidth"), rules("安裝完成."))
        self.assertNotIn(("error", "fullwidth"), rules("版本是 v1.2.0，請先升級。"))

    def test_quotes(self):
        self.assertIn(("error", "quotes"), rules("按下“儲存”按鈕。"))
        self.assertNotIn(("error", "quotes"), rules("按下「儲存」按鈕。"))

    def test_ellipsis(self):
        self.assertIn(("error", "ellipsis"), rules("等待中...請稍候。"))
        self.assertNotIn(("error", "ellipsis"), rules("等待中……請稍候。"))

    def test_dash_is_warning(self):
        self.assertIn(("warning", "dash"), rules("這個設計—簡單直接—很好用。", hints=False))
        self.assertNotIn(("warning", "dash"), rules("這個設計——簡單直接——很好用。", hints=False))


class SpacingTest(unittest.TestCase):
    def test_missing_space(self):
        self.assertIn(("error", "spacing"), rules("使用Docker執行3個容器。"))
        self.assertEqual(rules("使用 Docker 執行 3 個容器。"), [])

    def test_inline_code_counts_as_latin(self):
        self.assertIn(("error", "spacing"), rules("執行`npm install`安裝套件。"))
        self.assertEqual(rules("執行 `npm install` 安裝套件。"), [])

    def test_code_block_is_ignored(self):
        text = "安裝方式如下：\n\n```bash\necho 中文abc；視頻\n```\n"
        self.assertEqual(rules(text), [])

    def test_link_url_is_ignored(self):
        self.assertEqual(rules("詳見 [官方文件](https://example.com/中文abc) 的說明。"), [])

    def test_front_matter_is_ignored(self):
        self.assertEqual(rules("---\ntitle: 標題abc；\n---\n\n正文。"), [])

    def test_spacing_can_be_disabled(self):
        self.assertEqual(rules("使用Docker。", check_space=False), [])


class HintTest(unittest.TestCase):
    def test_ai_phrases_are_warnings(self):
        found = rules("值得注意的是，快取不是加速手段，而是架構決策。")
        self.assertIn(("warning", "ai-P07"), found)
        self.assertIn(("warning", "ai-P02"), found)
        self.assertFalse(any(level == "error" for level, _ in found))

    def test_hints_can_be_disabled(self):
        self.assertEqual(rules("綜上所述，這樣設定就好。", hints=False), [])

    def test_plain_prose_has_no_hints(self):
        text = "容器裡的程式寫不進掛載目錄，多半是使用者 ID 對不上。把容器的使用者改成和主機相同的 UID 就能寫入。"
        self.assertEqual(rules(text), [])


class GlossaryTest(unittest.TestCase):
    def test_glossary_avoid_column(self):
        glossary = (
            "| 術語 | English | 定義 | 不要用 |\n"
            "| --- | --- | --- | --- |\n"
            "| 工作區 | Workspace | 最上層資料夾。 | 工作空間、空間（只在儲存容量的語境） |\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "GLOSSARY.md"
            path.write_text(glossary, encoding="utf-8")
            terms = check.load_glossary_terms(path)
        self.assertEqual([t.avoid for t in terms], ["工作空間"])
        issues = check.check_text("打開工作空間。", "t.md", terms, markdown=True)
        self.assertEqual([(i.rule, i.message) for i in issues], [("glossary", "用詞表不用「工作空間」，改用「工作區」")])


class CliTest(unittest.TestCase):
    def test_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "good.md"
            bad = Path(tmp) / "bad.md"
            hint = Path(tmp) / "hint.md"
            good.write_text("系統預設會快取資料。\n", encoding="utf-8")
            bad.write_text("系統默認會緩存資料。\n", encoding="utf-8")
            hint.write_text("綜上所述，系統預設會快取資料。\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(check.main([str(good)]), 0)
                self.assertEqual(check.main([str(bad)]), 1)
                self.assertEqual(check.main([str(hint)]), 0)
                self.assertEqual(check.main([str(hint), "--strict"]), 1)


if __name__ == "__main__":
    unittest.main()

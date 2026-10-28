"""不花額度的結構檢查（L0）：skill 檔案、eval 題目與題庫的格式。

執行：python -m unittest discover -s tests
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "zh-tw-prose"
REFS = SKILL / "references"
FIXED_DIR = ROOT / "evals"
BANK_DIR = ROOT / "eval-bank"

sys.path.insert(0, str(ROOT / "scripts"))
import eval as runner  # noqa: E402

FIELDS = ["模式", "理由", "改法", "前", "後", "保留"]


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else None


def sections(path, prefix):
    text = path.read_text(encoding="utf-8")
    parts = re.split(rf"^### ({prefix}\d\d) .*$|^## ({prefix}\d\d) .*$", text, flags=re.M)
    out = {}
    for i in range(1, len(parts), 3):
        key = parts[i] or parts[i + 1]
        body = parts[i + 2].split("\n## ")[0]
        out[key] = body
    return out


def case_dirs(directory):
    return [p for p in sorted(directory.iterdir()) if (p / "prompt.md").is_file()]


class SkillTest(unittest.TestCase):
    def test_description_fits_claude_ai(self):
        fm = frontmatter((SKILL / "SKILL.md").read_text(encoding="utf-8"))
        desc = re.search(r"^description:\s*(.*)$", fm, re.M).group(1).strip()
        self.assertLessEqual(len(desc), 200)

    def check_patterns(self, path, prefix, count):
        found = sections(path, prefix)
        self.assertEqual(sorted(found), [f"{prefix}{i:02d}" for i in range(1, count + 1)])
        for key, body in found.items():
            labels = re.findall(r"^- ([^：\n]+)：", body, re.M)
            with self.subTest(pattern=key):
                self.assertEqual(sorted(set(labels)), sorted(FIELDS))
                self.assertEqual(labels[-1], "保留")
                self.assertLess(labels.index("前"), labels.index("後"))

    def test_patterns(self):
        self.check_patterns(REFS / "patterns.md", "P", 25)

    def test_translationese(self):
        self.check_patterns(REFS / "translationese.md", "T", 10)


class CaseFormatTest(unittest.TestCase):
    def all_cases(self):
        return case_dirs(FIXED_DIR) + [p for p in case_dirs(BANK_DIR) if p.name != "_common"]

    def test_prompt_frontmatter(self):
        for case in self.all_cases():
            fm = frontmatter((case / "prompt.md").read_text(encoding="utf-8"))
            with self.subTest(case=case.name):
                self.assertIsNotNone(fm)
                for key in ["description", "tags", "max_turns", "allowed_tools"]:
                    self.assertRegex(fm, rf"(?m)^{key}:")

    def test_graders(self):
        for case in self.all_cases():
            graders = sorted((case / "graders").glob("*.md"))
            with self.subTest(case=case.name):
                self.assertTrue(graders)
            for g in graders:
                fm = frontmatter(g.read_text(encoding="utf-8"))
                with self.subTest(grader=f"{case.name}/{g.name}"):
                    self.assertIsNotNone(fm)
                    self.assertRegex(fm, r"(?m)^type: (regex|llm|tool_used)$")
                    self.assertNotIn("(?m)", fm, "改用 flags: m")

    def test_trigger_cases_use_one_turn(self):
        for case in case_dirs(FIXED_DIR):
            text = (case / "prompt.md").read_text(encoding="utf-8")
            if "trigger" in runner.Case(case).tags:
                with self.subTest(case=case.name):
                    self.assertRegex(text, r"(?m)^max_turns: 1$")

    def test_bank_tags(self):
        sources = {"src-hand", "src-directed", "src-self", "src-synthetic"}
        for case in case_dirs(BANK_DIR):
            if case.name == "_common":
                continue
            tags = set(runner.Case(case).tags)
            with self.subTest(case=case.name):
                self.assertIn("bank", tags)
                self.assertEqual(len(tags & set(runner.CATEGORIES)), 1)
                self.assertEqual(len(tags & sources), 1)

    def test_bank_text_not_in_skill(self):
        """題庫的原文若已經出現在 skill 的範例裡，模型等於看過答案。"""
        skill_text = "".join(p.read_text(encoding="utf-8") for p in SKILL.rglob("*.md"))
        for case in case_dirs(BANK_DIR):
            if case.name == "_common":
                continue
            body = (case / "prompt.md").read_text(encoding="utf-8").split("---", 2)[2]
            for line in body.splitlines():
                line = line.strip()
                if line.startswith("|"):
                    continue
                if len(line) >= 20 and line in skill_text:
                    self.fail(f"{case.name} 的原文出現在 skill 裡：{line}")


class SamplingTest(unittest.TestCase):
    def test_sample_covers_every_category(self):
        bank = [runner.Case(p) for p in case_dirs(BANK_DIR) if p.name != "_common"]
        present = {c.category for c in bank}
        for seed in range(20):
            picked = runner.sample(bank, runner.SAMPLE_SIZE, runner.random.Random(seed))
            with self.subTest(seed=seed):
                self.assertEqual(len(picked), min(runner.SAMPLE_SIZE, len(bank)))
                self.assertEqual({c.category for c in picked} & present, present)

    def test_same_seed_same_sample(self):
        bank = [runner.Case(p) for p in case_dirs(BANK_DIR) if p.name != "_common"]
        a = runner.sample(bank, 8, runner.random.Random(7))
        b = runner.sample(bank, 8, runner.random.Random(7))
        self.assertEqual([c.name for c in a], [c.name for c in b])


if __name__ == "__main__":
    unittest.main()

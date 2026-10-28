# 貢獻指南

歡迎提出新的模式、用語對照、誤判回報與 eval 案例。

## 提 issue

開 issue 時選對應的範本：

- 「新的寫作模式」：附上原文例句、改寫後，以及什麼時候應該保留這個寫法。沒有保留條件的模式不會收錄，因為它會讓模型過度改寫。
- 「誤判或過度改寫」：附上原文、skill 或 check.py 的輸出，以及原文為什麼是對的。
- 「用語對照」：附上依據，例如教育部《重編國語辭典修訂本》、國家教育研究院雙語詞彙，或主要軟體的台灣在地化介面。

## 修改規則

1. 例句請自己寫，不貼他人文章或書籍的段落。
2. 新增或修改 `taiwan-usage.md` 的列時，確認「例外」欄列出所有包含該字串、但本身是正確用法的詞，避免誤判。
3. SKILL.md 維持 500 行以內。新內容優先放進 references。
4. 修改 check.py 時，在 `tests/test_check.py` 加上對應測試。

## 測試

```bash
python -m unittest discover -s tests
python skills/zh-tw-prose/scripts/check.py README.md
claude plugin validate --strict .
```

改動 SKILL.md 或 references 時，用 `scripts/eval.py` 跑 eval，並在 PR 說明附上結果摘要。eval 需要 Claude Code，會實際呼叫模型並產生費用，分層方式見 [evals/README.md](evals/README.md)。

```bash
# 只跑和改動有關的題目，例如改了保留條件
python scripts/eval.py L1 --tag false-positive
```

```bash
# 發 release 前：固定題、抽考 8 題與觸發題
python scripts/eval.py L2
```

新增 eval 題目時，真實改稿案例放進 `eval-bank/`，格式見 [evals/README.md](evals/README.md)。

## 分支

`main` 只接受 PR。請從 `main` 開分支，PR 合併方式為 merge commit。

## 授權

貢獻內容以 MIT 授權釋出。

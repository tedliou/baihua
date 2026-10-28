# 貢獻指南

歡迎提出新的模式、用語對照、誤判回報與 eval 案例。

## 提 issue

- 新模式：附上原文例句、改寫後，以及什麼時候應該保留這個寫法。沒有「保留」條件的模式不會收錄，因為它會讓模型過度改寫。
- 誤判：附上原文、skill 或 check.py 的輸出，以及原文為什麼是對的。
- 用語對照：附上依據，例如教育部辭典、樂詞網或主要軟體的台灣在地化介面。

## 修改規則

1. 例句自己寫，不貼他人文章或書籍的段落。
2. 新增或修改 `taiwan-usage.md` 的列時，確認「例外」欄涵蓋所有剛好包含該字串的正確詞，避免誤判。
3. SKILL.md 維持 500 行以內。新內容優先放進 references。
4. 修改 check.py 時，在 `tests/test_check.py` 加上對應測試。

## 測試

```bash
python -m unittest discover -s tests
python skills/zh-tw-prose/scripts/check.py README.md
claude plugin validate --strict .
```

改動 SKILL.md、references 或 description 時，請跑 eval，並在 PR 說明附上結果摘要。eval 會實際呼叫模型並產生費用，執行方式見 [evals/README.md](evals/README.md)。

```bash
claude plugin eval . --tag behavior --runs 2 --judge-model sonnet
claude plugin eval . --tag trigger --ablation none --runs 3
```

## 分支

`main` 只接受 PR。請從 `main` 開分支，PR 合併方式為 merge commit。

## 授權

貢獻內容以 MIT 授權釋出。

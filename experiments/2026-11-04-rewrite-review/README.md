# 改寫成效審閱

2026-11-04。題庫複審收錄的 33 題，交給 skill 改寫一遍，由作者逐題判斷改得好不好。

- 題目：`cases/`，每題開頭寫明「使用 zh-tw-prose skill。」。用 `claude plugin eval` 跑有 skill 的一組，每題 1 次，Sonnet，Claude Code 2.1.318，花費約 1.80 美元。
- 輸出：`outputs/`。`run-summary.json` 記錄每題有沒有呼叫 skill、讀了哪些 references：33 題都呼叫了 skill，讀過 `article.md` 的有 8 題、`ui.md` 1 題、`integrity.md` 1 題。
- 審閱頁：`review-page.html`，發佈成 claude.ai 上的 Artifact。作者選通過或不通過，寫意見或直接改字，判斷存在 Artifact 的資料庫。

# 改寫成效審閱：第三輪

2026-11-05。作者快速看過第二輪，認為大方向可以，只指出「判斷錯」過於口語，細部交給 Claude 評估。Claude 逐題讀完第二輪的輸出，修改 skill（commit `9b22964`）後，同樣的 33 題重跑一次，再由 Claude 逐題比對。

## 第二輪找到的問題與修法

- 詞被截短：「判斷錯」。核心規則 1 補上詞也要寫完整。
- 說教與評語被當成論點留下：「這個選項先不要當成……」「分清楚它們才能用好」。改稿原則 4 補上說教、評語與建議不算論點。
- 33 題只有 7 題讀了語域檔案，標題與未實測情境的規則因此沒有作用。改稿步驟 1 改成先讀全文與語域檔案。

## 第三輪的結果

- 33 題都呼叫了 skill，讀了語域檔案的從 7 題增加到 23 題。花費約 2.12 美元。
- 修好的題目：`lede-rules-not-enough-compressed` 改成「判斷錯誤」；`denial-before-doc-quote` 與 `lecture-lead-in` 刪掉了說教句；`untested-scenario-disclaimer` 不再寫 portable 版與「沒有實測」；`aphorism-closing` 不再先下評語、重列指令；`argumentative-section-flow` 不再用「最簡單的做法」鋪陳。
- 還沒解決的細節：
  - `closing-advice-after-measure` 仍有「適合先在筆電上試效果」。
  - `lede-starts-with-constraint` 的第一段仍有實測用的外掛與標記方塊。
  - `jar-swap-steps-and-worries` 仍寫「Paper 發現世界需要轉換」。
  - `untested-scenario-disclaimer` 仍寫「我的兩個專案各放一份」。
  - `cute-tilde-transition` 多了一個原文沒有的分號。
- 標題題目 `overpromising-title` 與 `title-dated-performance-claim` 沒有讀 `article.md`，標題仍是描述句或塞了產品名。語域表的技術文章要點改成「開頭先寫讀者的問題或動機，再給做法。標題寫成『主題：讀者得到的結果』」後，這兩題各重跑 2 次，結果在 `title-recheck/`：`overpromising-title` 改成「用 Dev Containers 隔離 AI Agent：……」的形式，`title-dated-performance-claim` 仍列出 LuckPerms，作者先前判斷這題不一定是 skill 的問題。

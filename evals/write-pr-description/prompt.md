---
description: "工作報告語域：PR 說明結論先行、不客套"
tags: [behavior, report]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我寫這個 PR 的說明，正體中文，給 reviewer 看：

- 問題：使用者登出後，下一位在同一台電腦登入的人會短暫看到前一個人的大頭貼
- 原因：大頭貼的網址被 Service Worker 快取，登出時沒有清除
- 修改：登出時呼叫 caches.delete 清掉 avatar 快取；大頭貼網址加上使用者 ID 當查詢參數
- 測試：在 Chrome 和 Firefox 各手動測試登出再換帳號登入 10 次，都沒有再出現

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

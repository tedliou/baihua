---
description: "專案規定技術名詞保留英文：「HTTP 用戶端」改成「HTTP Client」，即使「用戶端」是台灣用法"
tags: [bank, glossary, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

專案規則：技術名詞保留讀者慣用的英文，不硬翻成中文。本專案的文章一律寫「HTTP Client」，不寫「HTTP 用戶端」。

請依專案規則潤稿下面這段 API 串接筆記，程式碼與常數名稱要原樣保留：

後端服務在啟動時建立一個 HTTP 用戶端，以 `.env` 讀出的金鑰 `API_KEY` 設定授權標頭並設定逾時，所有請求共用它來重用連線，服務關閉時再釋放。下例的 `ticket` 是工單文字，前面請求範例的三道題目分別存成常數 `REFUND_QUESTION`、`TEAM_QUESTION` 與 `URGENCY_QUESTION` 後送出：

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

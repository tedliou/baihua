---
type: llm
weight: 1
---

原文：「後端服務在啟動時建立一個 HTTP 用戶端，以 `.env` 讀出的金鑰 `API_KEY` 設定授權標頭並設定逾時，所有請求共用它來重用連線，服務關閉時再釋放。下例的 `ticket` 是工單文字，前面請求範例的三道題目分別存成常數 `REFUND_QUESTION`、`TEAM_QUESTION` 與 `URGENCY_QUESTION` 後送出：」
專案規則要求寫「HTTP Client」，其餘文字沒有問題。
PASS if 「HTTP 用戶端」改成「HTTP Client」，並保留這些事實：服務啟動時建立一個 HTTP Client、用 `.env` 讀出的 `API_KEY` 設定授權標頭並設定逾時、所有請求共用它以重用連線、服務關閉時釋放、`ticket` 是工單文字、三道題目分別存成 `REFUND_QUESTION`、`TEAM_QUESTION`、`URGENCY_QUESTION` 三個常數後送出，句尾仍以冒號接後面的程式碼。程式碼與常數名稱原樣不動，改動範圍很小。
FAIL if 仍用「用戶端」「HTTP 客戶端」等中文譯名、改動常數或程式碼名稱、刪掉任一事實，或大幅重寫整段。

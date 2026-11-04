---
description: "ui-error-messages-missing-please"
tags: [rewrite-review]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

使用 zh-tw-prose skill。

幫我潤稿一款合作遊戲的介面字串：

這是首頁在房間操作失敗時顯示的四則錯誤訊息，每則一行。專案的介面文字規則（節錄）：
- 句子寫完整，保留主詞、助詞與「請」，不把訊息壓成電報式短句。
- 系統訊息平實直接，不加道歉或裝可愛，一則訊息只講一件事。
- 照原順序，每則仍然是一行。

原文：
這個世界封存了，先取消封存
找不到房間，檢查代碼
房間有密碼，先在上面輸入
沒有成功，再試一次

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

---
description: "使用者交代的概念句「重點是 AI 改壞的檔案都能還原」被原樣放進第一句，應該用筆記裡的機制展開，而且不補筆記沒有的功能"
tags: [bank, core-rule, src-synthetic]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我寫部落格文章介紹 snapback 的第一段。讀者是用 AI 寫程式的工程師，還沒聽過這個工具。

我想傳達的重點：snapback 的重點是 AI 改壞的檔案都能還原。

我的筆記：
- snapback 是命令列工具，掛在 AI Agent 的每一回合前面執行
- 每一回合開始前，把工作目錄的狀態存成一個 Git commit，放在 refs/snapback/ 底下，不會出現在 git log
- 執行 snapback undo 回到上一回合開始前的狀態，snapback undo 3 回到三回合前
- 不在 .gitignore 裡的檔案才會被存下來

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

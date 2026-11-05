---
description: "限制段的擋不到的寫法用逗號串成一句，因果沒寫出來；應寫出腳本為什麼擋不到"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我改寫技術文章的這一段。讀者剛看完一支擋下 Agent 推送 main 的 PreToolUse hook 腳本，這段說明腳本擋不到的情況。

這支腳本防的是 Agent 判斷錯誤，不是刻意繞過。`bash -c "git push origin main"` 這種把指令包在字串裡的寫法、用 `env git` 或完整路徑呼叫 git，以及 `$(...)` 裡的指令，它都不會拆開檢查。腳本本身也是 repo 裡的檔案，Agent 改掉腳本，下一次檢查就跟著失效。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

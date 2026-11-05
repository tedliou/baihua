---
description: "summary 與開頭用否定句開場、判斷句壓成片語；應先寫讀者讓 Agent 推送的情境與風險，再寫 hook 怎麼擋"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我改寫這篇技術文章的 summary 和開頭兩段。讀者是讓 Claude Code 的 Agent 自己 commit 與推送、想防止它直接推送 main 的工程師。標題是「Claude Code Hooks：私有 repo 沒有分支保護時，擋下 Agent 直接推送 main」。第三段是測試環境，之後是 hook 擋下指令的流程圖與設定步驟。補充事實：hook 只檢查 Claude Code 透過 Bash 與 PowerShell 工具執行的指令，人在終端機手動推送不受影響。

summary: "寫給 Agent 看的規則只是提醒，Agent 判斷錯時仍可能直接推送 main 或 force-push。Claude Code 的 PreToolUse hook 會在工具執行前先跑檢查腳本，只要腳本回答擋下，指令就不會執行，權限模式與子代理都一樣。"

想讓 Agent 只在開發分支工作、不直接推送 `main`，只把規則寫給 Agent 看並不夠，Agent 判斷錯時仍會照樣執行。Claude Code 的 PreToolUse hook 會在每次執行指令前先跑一支檢查腳本，腳本回答擋下，這次指令就不會執行，不受權限模式影響，子代理也一樣。

本站的原始碼放在 GitHub 的私有 repo，在 `draft` 分支開發，再開 PR 合併到 `main`。[私有 repo 的分支保護需要付費方案](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)，我當時用免費組織帳號開不了，只能把規則寫給 Agent 看，後來改用 hook 在指令執行前檢查。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

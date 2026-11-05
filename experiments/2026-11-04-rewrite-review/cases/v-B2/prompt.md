---
description: "telegraphic-article-sentences"
tags: [rewrite-review]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

使用 zh-tw-prose skill。

幫我潤稿這篇技術文章的一節，句子要寫完整。讀者是要設定 Claude Code PreToolUse hook 的工程師。這一節在開頭之後，說明 hook 怎麼依檢查腳本的結束碼擋下指令，流程圖在這題用〔流程圖〕代替，保留位置即可。下一節說明腳本怎麼判斷推送 main。

Hook 依檢查腳本的結束碼，決定這次指令要擋下還是交回原本的流程：

〔圖〕
腳本以結束碼 2 結束時，寫到標準錯誤輸出（stderr）的文字會回給 Agent，當作指令被擋下的原因。[官方的 hooks 指南](https://code.claude.com/docs/en/hooks-guide#hooks-and-permission-modes)寫明，PreToolUse hook 在任何權限模式的檢查之前執行，`bypassPermissions` 模式下一樣擋得下，[子代理呼叫工具](https://code.claude.com/docs/en/hooks.md)時也會經過同樣的 hook。結束碼 0 只代表 hook 不擋，指令仍要經過原本的權限設定。

權限設定的 deny 規則也能擋指令，但只能用萬用字元比對指令文字，`git push origin +main` 這類寫法會漏掉，原因見[權限規則怎麼比對 Bash 指令](/ai/claude-code-bash-deny-rules/)。Hook 的腳本可以自己寫判斷，例如查 Agent 目前在哪個分支。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

---
description: "技術文章語域：從筆記寫部落格開頭，應先給答案、沒有 AI 腔"
tags: [bank, ai-flavor, src-synthetic]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我寫部落格文章的開頭兩段。讀者是剛開始用 Docker 的工程師，從搜尋引擎進來。

我的筆記：
- 症狀：容器裡的程式寫入掛載的 volume 時出現 Permission denied
- 原因：容器內的程式用 uid 1000 執行，主機上的資料夾擁有者是 root
- 解法：docker run 加上 --user "$(id -u):$(id -g)"，或在 Dockerfile 建立相同 uid 的使用者
- 我自己在 Ubuntu 24.04 遇到

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

---
description: "標題的保證超過正文能證明的範圍：「放心」「不會搞爛電腦」"
tags: [bank, core-rule, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這篇教學文章的標題，只輸出標題一行。

文章內容：用 VS Code 的 Dev Containers 把 AI Agent 放進 Docker 容器執行，並在容器裡開啟 Full Access（完整權限）。文章裡有一段寫著：

Full Access 的隔離範圍也要看實際掛載內容。Agent 仍然能修改掛載進容器的專案、憑證、Socket 或其他目錄，因此只掛載必要的專案與資料，重要變更由 Git 保存。

目前的標題：把 Agent 關在開發容器，放心開完整權限也不會搞爛電腦

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

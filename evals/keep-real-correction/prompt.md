---
description: "不誤殺：讀者真的有誤解時，更正句型要保留"
tags: [behavior, rewrite, false-positive]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這段 Git 教學的段落：

很多人以為 `git pull` 只會下載遠端的變更。其實 `git pull` 不只是下載，而是先執行 `git fetch`，再把遠端分支合併進目前的分支，所以本機和遠端都改了同一段內容時，可能會產生合併衝突。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

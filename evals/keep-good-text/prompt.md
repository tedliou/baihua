---
description: "不誤殺：好的文字潤稿時應幾乎不動"
tags: [behavior, rewrite, false-positive]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這段技術文章的段落：

容器裡的程式寫不進掛載目錄時，八成是使用者 ID 沒對上。映像檔裡的程式用另一個帳號執行，主機上的資料夾卻屬於你自己的帳號，所以寫入會被拒絕。執行容器時加上 --user 參數，讓容器用和主機相同的 UID 執行，就能正常寫入。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

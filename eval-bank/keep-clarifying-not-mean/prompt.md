---
description: "作者保留的澄清句：「打開這個選項不代表整個遊戲都在背景照常跑」是讀者真的會誤會的地方，不要當成假對比刪掉"
tags: [bank, core-rule, src-hand, false-positive]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我看這兩段 Unity 技術文章的段落，有需要改的地方再改，沒有問題的句子保持原樣。

文章背景：Windows 遊戲用瀏覽器登入並導回本機的 localhost，切到瀏覽器時遊戲失去焦點就會被凍結，打開 Player Settings 的「Run In Background」可以讓遊戲在背景繼續執行。

只要遊戲切出去後還要等外部流程回來，我就會把「失焦後 Unity 是否仍要執行」列進 Build 前檢查。像瀏覽器登入、本機 Server、Socket、Launcher、展演控制，這些流程只要被失焦凍住，看起來就很像通訊壞掉。

我會先讓登入、Socket、展演控制這些必要流程活著。至於遊戲時間、輸入、音訊或會影響公平性的邏輯，那是另一個暫停策略要處理的問題。打開「Run In Background」不代表整個遊戲都該在背景照常跑。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

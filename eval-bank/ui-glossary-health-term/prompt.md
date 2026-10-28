---
description: "原文混用「生命值」「HP」「血量」，潤稿後同一個概念只用一種說法，用哪一種都可以"
tags: [bank, glossary, src-directed, no-spacing, keep-punct]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿一款合作遊戲的介面字串。這是四個效果的「名稱｜說明」，維持同樣的格式，一個效果一行：

治療｜命中隊友時，回復隊友生命值
HP 回復｜每 2 秒自然回復 HP +1（原本每 5 秒）
無法回血｜不會自然回復血量
過飽｜每 1 秒自然回復生命值 +1；移動速度 −25%、跳躍高度 −40%

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

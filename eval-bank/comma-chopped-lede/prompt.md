---
description: "逗號切碎又用冒號列舉的開頭句：合併成連貫的句子，逗號變少"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這篇 API 串接筆記的開頭段落。讀者是要把這個模型接進後端系統的工程師。

Jev 是 TypeSafe 的決策模型，後端系統串接只需要一個 HTTP POST 請求：送出要判斷的資料 `state` 與一或多個題目，回傳的是各個答案的機率，不會產生文字。模型只負責判斷，結果要自動執行還是交給人工，由程式依機率或 `confidence` 門檻決定。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

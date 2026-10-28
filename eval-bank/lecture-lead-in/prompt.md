---
description: "說教式的引導句：「分清楚它們才用得好」改成直接說明接下來是什麼"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這段工具教學的引導句與清單。引導句和清單中間原本有一張設定畫面的截圖，不用輸出圖片。

往下捲有兩組解析度，分清楚它們才用得好 Upscaler：

- Generation Resolution（生成解析度）是 sd-turbo 實際作畫的大小，決定每格處理時間和 VRAM 用量。TD 送來的畫面會先縮放到這個大小，比例不同時依 Fit Mode 處理：Fill 裁切填滿，Fit 加黑邊，Stretch 直接拉伸。sd-turbo 在 512×512 的效果最好。
- Output Resolution（輸出解析度）是送回 TD 的畫面大小，不影響 sd-turbo 怎麼畫，只決定最後放大到多大。輸出大於生成時，開著 Upscaler 就用 AI 模型放大並補細節，關掉就是一般縮放。介面上的說明建議設成生成解析度的 2 倍或 4 倍。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

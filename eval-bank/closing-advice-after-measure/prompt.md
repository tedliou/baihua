---
description: "實測數字後面附上評價與使用建議：只留測到的事實"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這段實測結果的說明。段落前面有一張測試結果表，內容是 RTX 3050 Laptop（4 GB VRAM）用 TensorRT 的數字：5.8 fps，每格處理時間 p50 為 163 ms、p95 為 168 ms。表格不用輸出，只輸出潤稿後的段落。

p95 表示 95% 的影格在這個時間內完成。同樣的 512×384 加 Upscaler，RTX 3070 在 60% 功率上限下 p50 是 26.6 ms，筆電約慢 6 倍。可以用，但明顯比較慢，比較適合先在筆電上試效果。那台筆電的 Engine 建置時間沒有量到，完整紀錄在 [GitHub issue #28](https://github.com/example/tool/issues/28)。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

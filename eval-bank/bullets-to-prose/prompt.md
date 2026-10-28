---
description: "彼此有對照關係的兩條條列，後面接一句結論：改成一段連貫的文字"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這段 API 實測結果的說明。段落前面有一張圖，內容是七張客服工單的 Noul 與 Score 對照，不用輸出圖片。

- B2「Safari 上傳會當機，Chrome 正常」的 Noul 只有 0.51，模型無法確定它是否緊急，但 Score 給出 2.08（This week）且 `confidence` 達 0.92。
- S3 與 S4 的 Score 幾乎相同（2.98 與 3.00），Noul 卻是 0.82 與 0.97。

Noul 回答的是「這件事成立的可能性多高」，工單要分級或排序時改用 Score。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

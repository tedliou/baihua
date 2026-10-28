---
description: "評價詞「大幅縮短」：後面的表格已有數字，改成具體的延遲前後值"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這段 CLI 工具升級說明的開頭段落。段落後面緊接著下面這張實測表，表格不用輸出，只輸出潤稿後的段落。

| 指令 | 0.11.0 | 1.0.0 |
| --- | --- | --- |
| `td --version` | 500 ms | 12 ms |
| `td --json instances list` | 1,447 ms | 17 ms |
| `td --json parameters get` | 1,954 ms | 33 ms |

1.0.0 把通訊協定換成 v4，`td` 也改成原生執行檔，指令延遲大幅縮短。我在同一台電腦用 TouchDesigner 2025.32050 的空專案比較 0.11.0 與 1.0.0，單一指令各執行 10 次取中位數：

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

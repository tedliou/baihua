---
type: llm
weight: 1
---

PASS if summary 與第一段先寫讀者的問題或目的，以及理解後文需要的概念（ComfyUI 是什麼、讓 Claude Code 透過官方的 comfy-mcp 啟動 ComfyUI、下載模型、執行 workflow，人也能打開同一份 workflow 手動調整），不列安裝指令與套件版本；測試環境放在後面。
FAIL if summary 或第一段仍出現 `comfy install`、`claude mcp add` 或套件版本號；仍以步驟數或「最短」開場；刪掉 Windows 11、RTX 3070 8 GB、只用 Prompt 產出 1024 × 1024 logo 這些事實；或加入原文沒有的功能。

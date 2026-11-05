---
description: "summary 與開頭用「最短的路徑是三步」切入，一次倒出指令與版本，沒有先鋪陳問題、目的與概念"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我改寫這篇技術文章的 summary 和開頭兩段。讀者是會用 Claude Code、想讓它在自己電腦上用 ComfyUI 產圖的人，不一定熟 ComfyUI。後面的「架構」一節說明 Claude Code、comfy-mcp 與 comfy-cli 的關係，「安裝」一節會列出完整的指令與版本。開頭那張 logo 圖在這題用〔logo 圖〕代替。

summary: "裝好官方的 comfy-mcp 並用 `comfy install` 建立 ComfyUI 後，以 `claude mcp add` 接上 Claude Code，就能用對話啟動 ComfyUI、下載模型與執行 workflow。本文在 Windows 11 與 RTX 3070 上從零實測，也說明怎麼用瀏覽器或 Comfy Desktop 打開 Claude Code 改過的 workflow。"

要讓 Claude Code 操作本機的 ComfyUI，最短的路徑是三步：用 uv 安裝 Comfy-Org 官方的 comfy-mcp，用 `comfy install` 建一個 ComfyUI 工作區，再用 `claude mcp add` 把 comfy-mcp 註冊給 Claude Code。之後啟動 ComfyUI、下載模型、套範本與執行 workflow 都能用對話完成，想看 workflow 或手動調整時，再用瀏覽器或 Comfy Desktop 打開。

本文在 Windows 11 與 RTX 3070 8 GB 上，用 uv 0.13.6、comfy-cli 1.24.0、comfy-mcp 0.10.0 與 ComfyUI 0.43.2 從零實測一次，不寫設定檔也不設環境變數，最後讓 Claude Code 只用 Prompt 產出這張 1024 × 1024 的 logo：

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

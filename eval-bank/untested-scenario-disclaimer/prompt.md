---
description: "教學文章照官方文件補上作者沒做過的安裝方式，總結再加「沒有實測」的範圍聲明，應整句刪掉，不改寫成推論"
tags: [bank, core-rule, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我改寫技術文章的這兩段，第一段在「設定檔」小節，第二段是「總結」。讀者是在同一台電腦裝了多個 ComfyUI、想讓它們共用模型的人。我實際測過的只有兩個用 comfy-cli 安裝的 ComfyUI 專案。

comfy-cli 安裝的 ComfyUI 在 `main.py` 旁放一份 `extra_model_paths.yaml`，裡面寫共用資料夾的路徑與各類模型的子資料夾。我的兩個專案各放一份，內容相同。portable 版則是放在 `ComfyUI_windows_portable\ComfyUI`，官方文件說明的設定檔位置也在這一層。之後新增模型類型時，兩份設定檔都要改。

兩個 ComfyUI 專案改讀共用資料夾後，MOSS-Image 與 Qwen-Image 在硬碟上各只存一份。portable 版的接法照官方文件整理，沒有實測。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

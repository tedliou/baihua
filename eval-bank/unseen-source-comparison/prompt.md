---
description: "拿「舊教學」「常見的教學」當對照，讀者不知道那些教學寫了什麼；應改成讀者做過的事或版本差異"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我改寫技術文章的這一段。讀者正要在新電腦上安裝 PyTorch，並想用 GPU 訓練。

照常見的教學執行 `pip install torch` 後，裝到的是只支援 CPU 的版本，`torch.cuda.is_available()` 會回傳 `False`。舊教學裡的 `--extra-index-url` 寫法在新版 pip 也行不通了。要用 GPU，需要到官方安裝頁面選好 CUDA 版本，再執行頁面給的指令，例如 `pip install torch --index-url https://download.pytorch.org/whl/cu124`。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

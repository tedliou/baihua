---
description: "技術文章的標題與開頭寫出設定檔名、資料夾與啟動參數，應改成讀者的問題與結果，檔名留給正文的步驟"
tags: [bank, core-rule, src-hand]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我改寫這篇技術文章的標題和開頭第一段。讀者是在同一台電腦裝了好幾個 ComfyUI、硬碟被重複的模型塞滿的人。正文的步驟已經完整寫了共用資料夾的位置、設定檔的內容與啟動參數，標題和開頭不用再交代做法細節。

標題：ComfyUI 共用模型資料夾：用 extra_model_paths.yaml 讓多套 ComfyUI 讀同一份模型

開頭：同一台電腦裝了好幾套 ComfyUI 時，每套都會在自己的 `models` 資料夾各下載一份模型。只要建一個共用資料夾，在裡面放一份 `extra_model_paths.yaml`，再讓每套 ComfyUI 啟動時用 `--extra-model-paths-config` 指向它，同一個模型就只要下載一次。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

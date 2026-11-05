---
description: "jar-swap-steps-and-worries"
tags: [rewrite-review]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

使用 zh-tw-prose skill。

幫我改寫教學文章「換成 Paper 並啟動」這一節。讀者剛照前一節備份好整個伺服器資料夾，並把地獄與終界搬回原版的位置。原文的伺服器 log 在這題用〔ALERT 警告〕代替，保留位置即可。下一節「確認轉換結果」會教讀者用 `version` 與 `plugins` 檢查；文章最後的「實測紀錄」已經寫了第一次約 39 秒、之後約 9 秒的啟動時間。

## 換成 Paper 並啟動

從 [Paper 下載頁](https://papermc.io/downloads/paper)下載和 Spigot 相同 Minecraft 版本的 Paper，放進伺服器資料夾，並照遷移文件的做法把檔名改成啟動指令裡的 jar 檔名。例如 `start.bat` 啟動的是 `spigot-26.3.jar`，就先刪掉原本的 Spigot jar，再把 Paper 的檔案改成這個名字，`start.bat` 不用改。`plugins` 資料夾留在原位。

照原本的方式啟動伺服器，Paper 發現世界要轉換，會先印出這段警告並等 30 秒：

〔ALERT 警告〕

已經備份就不用中斷，30 秒後 Paper 會轉換三個維度的資料夾，實測從開啟到 `Done` 約 39 秒。之後再啟動就不會出現這段警告，到 `Done` 約 9 秒。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

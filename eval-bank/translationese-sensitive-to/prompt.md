---
description: "「由於……對於……很敏感」與「能發現他有提供……因此可以」：介詞連接詞過多，且用「他」稱呼工具"
tags: [bank, translationese, src-self]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這兩段 VS Code 開發容器教學的段落。連結和檔案路徑要保留。

容器建置好後 VS Code 會自動啟動與連線到開發容器中，由於 Android 專案對於各種元件的版本號碼很敏感，需要特別設定。

我可以瀏覽剛才選用 [Android SDK 的 GitHub](https://github.com/NordcomInc/devcontainer-features/tree/master/src/android-sdk)，能發現他有提供 platform、build_tools 的版本號碼欄位，因此可以編輯 .devcontainer/devcontainer.json，於 android-sdk 下加入版本設定。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

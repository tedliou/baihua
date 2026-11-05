---
description: "技術文章的 summary 與第一段先丟限制與步驟，還混進驗證用的外掛與標記方塊；應先寫 Paper 是什麼、伺服主為什麼想換，再寫限制與結果"
tags: [bank, core-rule, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我改寫這篇技術文章的 summary 和第一段。讀者是經營 Minecraft Spigot 伺服器、考慮換成 Paper 的伺服主，最在意世界與外掛的資料能不能完整搬過去。第一段後面是測試環境那段（下面附上，不用改），接著是備份、把地獄與終界搬回原版位置、換上 Paper jar 的步驟。文章最後有「實測紀錄」一節，已經寫了測試用的 LuckPerms、EssentialsX、vip 群組與三個維度的標記方塊。補充事實：從 Minecraft 26.1 起，Spigot 把地獄與終界存在和原版不同的資料夾。

summary: "Paper 是 Spigot 的直接替代品，原本的外掛不用修改就能使用。從 Minecraft 26.1 起，Spigot 的世界要先轉回原版的資料夾結構，才能換成 Paper。"

Minecraft 26.1 起，Spigot 伺服器要換成 Paper，得先把世界轉回原版的資料夾結構，再換上 Paper 的 jar 檔，[Paper 的遷移文件](https://docs.papermc.io/paper/migration)寫明 Spigot 已經不能直接遷移。Paper 在[官方文件](https://docs.papermc.io/paper/getting-started/)裡是 Spigot 的直接替代品，外掛不用修改，[官方網站](https://papermc.io/software/paper)另外列出光照引擎、漏斗與實體的效能最佳化。我在一個裝了 LuckPerms 與 EssentialsX 的 Spigot 26.3 伺服器的三個維度各放一塊標記方塊，把地獄與終界搬回原版的位置再換成 Paper，三塊方塊、LuckPerms 建立的群組和兩個外掛都保留下來。

測試環境是 Windows 11 與 Java 25，Spigot 26.3 用 BuildTools 建置，Paper 是 26.3 的 build 240，外掛是 LuckPerms 5.5.71 與 EssentialsX 2.22.0。Paper 26.1 起需要 Java 25，和 26.1 起的原版伺服器相同，原本執行 Spigot 26.x 的電腦不用另外安裝。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

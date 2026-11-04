---
description: "comma-chained-summary"
tags: [rewrite-review]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

使用 zh-tw-prose skill。

幫我改寫這篇技術文章的 summary（front matter 的摘要，三句以內）。文章教讀者在 ComfyUI 用 MOSS-Image 的官方範本，先在畫布上框出文字與照片的位置再產圖，用繁體中文實測了咖啡店貼文、市集活動海報與 YouTube 縮圖。summary 的語氣與節奏要和作者寫的第一段一致，第一段如下：〔附上第一段〕

summary: "MOSS-Image 會把 Prompt 裡指定的文字直接畫進圖裡，做社群貼文或海報時不用再另外排字。ComfyUI 的官方範本可以先在畫布上框出標題、照片和價格的位置再產圖，用繁體中文實測，框好位置的貼文、海報和縮圖字都寫對，就算換一個隨機種子重產，版面也和原本一樣。"

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

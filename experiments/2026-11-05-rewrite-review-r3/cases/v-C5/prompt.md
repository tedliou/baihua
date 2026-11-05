---
description: "lede-absolute-claims"
tags: [rewrite-review]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

使用 zh-tw-prose skill。

幫我改寫這篇技術文章的第一段。讀者是想用 AI 生圖做社群貼文與海報的人。

在 ComfyUI 用 MOSS-Image 產圖時，要出現在圖上的字直接寫進 Prompt，模型就會把它畫在畫面上，做社群貼文或活動海報不用再另外開設計軟體排字。這類圖的標題、品名和價格通常有固定的位置，只靠 Prompt 描述的話，每次產出的版面都不一樣。ComfyUI 的 MOSS-Image 範本可以先在畫布上框出每段文字和照片的位置，再照這個版面產圖。我用繁體中文做了咖啡店的新品貼文、市集活動海報和教學影片縮圖，框好位置後每張的字都寫對，換一個隨機種子重產，文字的位置也和原本一樣。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

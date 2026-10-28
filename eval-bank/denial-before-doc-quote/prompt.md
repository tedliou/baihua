---
description: "先否定一個讀者沒有的誤解，再用評價詞引官方說明：直接寫設定的位置與官方行為"
tags: [bank, ai-flavor, src-hand]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這段 Unity 技術文章的段落。程式碼區塊、選單路徑與連結要原樣保留。

「Run In Background」的位置在這裡：

```text
Edit > Project Settings > Player > Resolution and Presentation > Run In Background
```

這裡先不要把它想成背景畫面設定。這次要確認的是，瀏覽器被打開之後，Unity 還會不會繼續處理 Callback。

對 Windows Player 來說，這個行為就是由「Run In Background」控制。Unity 的 [Windows Player settings](https://docs.unity3d.com/Manual/playersettings-windows.html) 對這個選項講得很直接：啟用後，App 失去焦點時仍會在背景執行。關閉時，App 失去焦點就會暫停。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

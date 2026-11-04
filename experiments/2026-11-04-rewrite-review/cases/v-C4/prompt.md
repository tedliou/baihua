---
description: "untranslated-ui-option-in-parens"
tags: [rewrite-review]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

使用 zh-tw-prose skill。

幫我潤稿教學文章的這一段。讀者正在 ComfyUI 的 MOSS-Image 版式控制範本填好框，下一步按「執行」。ComfyUI 有正體中文介面，但「Text to Image (MOSS-Image)」節點上的 enable_prompt_enhancer 這個開關沒有翻譯，介面上顯示的就是 enable_prompt_enhancer；開啟後，產圖前會先把 Prompt 擴寫成一段詳細的英文描述。

這個範本的提示詞擴寫（「enable_prompt_enhancer」）預設關閉，範本裡的說明提到開啟後會改寫框的內容，維持關閉就好。畫面右下另一則說明寫著「Prompt upsampler is on」，和實際的預設不同，不用理會。按「執行」，就會產出開頭那張貼文。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

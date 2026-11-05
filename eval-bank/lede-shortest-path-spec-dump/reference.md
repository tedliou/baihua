# 作者發佈的版本

給人對照用，不會送給模型，也不參與評分。圖片換成〔圖〕。

````markdown
summary: "Claude Code 本身不會生圖，但接上 ComfyUI 官方的 comfy-mcp 後，可以照文字描述調整 ComfyUI workflow 裡的節點，用自己電腦上的模型產出想要的圖。改好的 workflow 能直接在 ComfyUI 打開，人再接著手動調整。"

ComfyUI 產圖的流程是一份 workflow，載入模型、輸入 Prompt、取樣和存檔各是一個節點，每個節點上的參數都是可以改的值。Claude Code 本身不會生圖，但讀得懂也改得動 workflow，等於能用程式控制 ComfyUI 產圖。我接上 ComfyUI 官方的 comfy-mcp 後，只用文字描述想要的 logo，Claude Code 就從範本改出一份 workflow，連缺的模型也一起下載，再交給本機的 ComfyUI 跑出圖。圖不滿意可以再描述一次，也可以在 ComfyUI 打開同一份 workflow，自己調整節點。

本文的測試環境是 Windows 11 與 RTX 3070 8 GB 顯示卡，ComfyUI 從零開始安裝，模型用 MOSS-Image。生圖要求是只用文字 Prompt、不給參考圖，產出一張 1024 × 1024 的 logo：暗色底，中上方是貓咪形狀的 logo，下方是 VerveCode 字樣。
````

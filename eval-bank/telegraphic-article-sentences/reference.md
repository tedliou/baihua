# 作者發佈的版本

給人對照用，不會送給模型，也不參與評分。圖片換成〔圖〕。

````markdown
Hook 會依照檢查腳本回傳的結束碼，決定要擋下這次的指令，還是交回原本的流程繼續處理：

〔圖〕
腳本以結束碼 2 結束時，寫到標準錯誤輸出（stderr）的文字會傳回給 Agent，作為指令被擋下的原因。[官方的 hooks 指南](https://code.claude.com/docs/en/hooks-guide#hooks-and-permission-modes)寫明，PreToolUse hook 會在任何權限模式的檢查之前執行，因此即使在 `bypassPermissions` 模式下也一樣能擋下指令，而[子代理在呼叫工具](https://code.claude.com/docs/en/hooks.md)時，也會經過同樣的 hook。結束碼 0 只代表 hook 不擋下這次的指令，指令仍然要經過原本的權限設定，才會真正執行。

權限設定裡的 deny 規則雖然也能擋下指令，但它只能用萬用字元比對指令的文字，像 `git push origin +main` 這類寫法就會被漏掉，詳細原因可以參考[權限規則怎麼比對 Bash 指令](/ai/claude-code-bash-deny-rules/)。Hook 的腳本則可以自己撰寫判斷邏輯，例如先查出 Agent 目前所在的分支，再決定要不要擋下。
````

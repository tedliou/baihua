# 作者發佈的版本

給人對照用，不會送給模型，也不參與評分。圖片換成〔圖〕。

````markdown
summary: "當私有 repo 無法開啟分支保護時，Agent 一旦判斷錯誤，就可能直接把改動推送到 main 或執行 force-push，而寫給它看的規則只能作為一種提醒，模型不一定會完全遵從。透過 Claude Code 的 PreToolUse hook，Agent 每次執行指令前都會先經過一支檢查腳本，只要腳本判定指令違反規則，這個指令就不會被執行，而且不論使用哪種權限模式都一樣有效。"

讓 Agent 自己 commit 與推送，可以省下手動操作 git 的時間，但當它判斷錯誤時，可能會把改動直接推送到 `main`，或用 force-push 覆蓋掉遠端的提交歷史。即使把「不要推送 main」寫進專案規則，[Claude Code 也只會把這些規則當成參考的內容](https://code.claude.com/docs/en/memory.md)，模型不一定會完全遵從。若要在 Agent 判斷錯誤時也能擋下指令，就要使用 PreToolUse hook。設定 hook 之後，Agent 每次執行指令前，Claude Code 都會先把指令交給一支檢查腳本，只要腳本判定這個指令違反規則，指令就不會被執行。

本站的原始碼放在 GitHub 的私有 repo，平時在 `draft` 分支上開發，完成後再開 PR 合併到 `main`。GitHub 的[私有 repo 要開啟分支保護需要付費方案](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)，我當時使用的免費組織帳號無法開啟，於是改用 hook 來擋下 Agent 推送 `main` 的指令。Hook 只會檢查 Claude Code 透過 Bash 與 PowerShell 工具執行的指令，我們自己在終端機手動推送時不會受到影響。
````

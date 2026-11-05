---
type: llm
weight: 1
---

PASS if 每個判斷句都有主詞、動作與後果：結束碼 0 寫出 hook 不擋下這次的指令、指令仍要經過原本的權限設定；`bypassPermissions` 一句寫出這個模式下也擋得下指令；deny 規則一句寫出它只能用萬用字元比對指令文字，所以會漏掉 `git push origin +main`；連結前的「原因見」寫成完整句。連接詞與被動句不扣分。
FAIL if 大部分壓縮句仍原樣留著；改動或刪掉三個連結、`stderr`、`bypassPermissions`、`git push origin +main`、子代理也會經過同樣的 hook；或加入原文沒有的事實。

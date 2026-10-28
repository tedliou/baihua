---
description: "用分號串起來又以「不要繼續亂改」收尾的總結"
tags: [bank, ai-flavor, src-self]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這篇 Windows 更改 DNS 教學的總結段落。文章前面已經教過怎麼在網路設定裡改成公共 DNS，以及怎麼恢復成自動取得（DHCP）。

改用公共 DNS 適合處理解析品質、隱私偏好或已確認的 DNS 層問題。先用 `Resolve-DnsName` 驗證，再判斷網站能否開啟；若改動無效或影響整體連線，立即恢復 DHCP，不要繼續亂改 IP 與閘道設定。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

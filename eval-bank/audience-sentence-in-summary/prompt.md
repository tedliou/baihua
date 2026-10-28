---
description: "總結第一句替讀者對號入座，並把沒有驗證的「省下時間與額度」當成事實"
tags: [bank, ai-flavor, src-directed]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這篇文章「總結」小節的第一段。

背景：這組 Skill 是只為 Claude Code 與 GitHub Issues 改寫的版本。文章其他段落已經寫過：審查次數從每張工單一次，減少為 checkpoint 數量加一次。文末的「尚未驗證」清單寫著：實際省下多少 Token，以及延後審查是否漏掉逐張審查能抓到的問題，都還沒測過。

這組 Skill 適合用 Claude Code 與 GitHub Issues、想讓主流程一路接下去的人。它最大的取捨在審查：只有容易擴散錯誤的 checkpoint 工單先審，其餘集中在開 PR 前審一次，省下逐張審查的時間與額度。實作預設由主 Session 用同一個 Context 完成，只有長 spec 才把工單全部派給 Subagent。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

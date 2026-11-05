# vervecode.dev 2026-11-04 改稿紀錄：baihua 題庫候選

來源：`/home/user/vervecode.dev`（shallow clone，HEAD `626c95e`），只讀未改。commit 時間是台灣時間（`55c53f9`、`15dc5eb` 的時間記成 UTC 2026-11-03 18:09，等於台灣時間 11-04 02:09）。

## 0. 先看結論

- 範圍：先完整比對今天（2026-11-04）的文章，再往前挑了兩篇歷史文章，湊到 15 題就停（協調者轉達作者的要求：15～20 題、品質優先）。歷史只看了 2026-10 下旬到 11-03 有改稿紀錄的幾篇，沒有搜遍 934 個 commit。
- 今天有改稿紀錄的文章有四篇：Spigot 轉 Paper、Claude Code hooks、MOSS-Image 圖文排版（凌晨 00:45～02:09，不在原本的清單裡），以及 PyTorch CUDA。PyTorch 的草稿 `6353107` 到發佈 `5ce6881` 只改了 `publishDate` 與 `draft`，正文一字未動，所以沒有候選。`4e64152` 是在 ComfyUI MCP 文章加一條連結，屬於事實增補。
- 草稿與發佈版的位置：文章是 `content/posts/{category}/{slug}/index.md` 的 page bundle，草稿和發佈版是同一個檔案，靠 front matter 的 `draft: true／false` 與 `publishDate` 區分。
- 改稿流程：作者在對話裡退回、AI（Claude）照指示改寫後 commit。commit 都是作者帳號加 `Co-Authored-By: Claude`。作者親手改的文字只有兩處有紀錄：MOSS-Image 第一段（`c4e84bd`，writing-style 寫「作者自己改的開頭」）與 hooks 的 summary（`8a780fc`，writing-style 寫「作者改成……並要求全文都照這樣寫」）。其他改動是作者指示、AI 改寫、作者發佈，依 baihua 的標籤是 `src-directed`。
- 候選共 15 題：高 5 題、中高 5 題、中 4 題、中低 1 題。各篇題數：Spigot 轉 Paper 4、Claude Code hooks 4、MOSS-Image 5、ComfyUI 官方 MCP 1、Claude Code deny 規則 1。
- 作者已同意這些內容都能放進 baihua 的公開題庫。

## 1. 候選總表

| # | 建議名稱 | 文章 | 一句話問題 | 適合度 |
| --- | --- | --- | --- | --- |
| A1 | `lede-starts-with-constraint` | Spigot 轉 Paper | 開頭先寫限制與步驟，還把驗證用的外掛與標記方塊塞進第一段 | 高（但要先決定規則） |
| A2 | `title-dated-performance-claim` | Spigot 轉 Paper | 標題冒號後寫「效能最佳化的伺服器」這種日後會過時的評價 | 中 |
| A3 | `jar-swap-steps-and-worries` | Spigot 轉 Paper | 換 jar 的好幾個動作塞在一段，「哪些不用動」放在句尾，警告要不要理會沒交代 | 中高 |
| A4 | `closing-leads-with-paths-versions` | Spigot 轉 Paper | 總結第一句塞路徑與外掛版本號，沒有先用概念寫關鍵動作 | 中 |
| B1 | `lede-rules-not-enough-compressed` | Claude Code hooks | 開頭用「只寫規則並不夠」的否定句起頭，判斷句壓成片語 | 中高 |
| B2 | `telegraphic-article-sentences` | Claude Code hooks | 正文判斷句壓成片語（「hook 不擋」「原因見」），要補回動作與後果 | 高 |
| B3 | `limitation-scope-contrast` | Claude Code hooks | 限制段用「防的是……不是……」開場，後果句壓縮 | 中 |
| B4 | `title-mechanism-after-colon` | Claude Code hooks | 標題冒號後寫機制名稱 PreToolUse，不寫讀者的情境 | 中 |
| C1 | `wrong-result-before-steps` | MOSS-Image | 小節先講內部機制與錯誤產圖，才給拆線步驟 | 高 |
| C2 | `argumentative-section-flow` | MOSS-Image | 「先試最簡單的做法」「卻」「想要……就要改用」的論證式鋪陳 | 中高 |
| C3 | `comma-chained-summary` | MOSS-Image | summary 用一連串逗號接短分句，結果寫成口語的「字都寫對」 | 高 |
| C4 | `untranslated-ui-option-in-parens` | MOSS-Image | 沒翻譯的介面選項自創中文名「提示詞擴寫」，原名放進括號 | 中 |
| C5 | `lede-absolute-claims` | MOSS-Image | 開頭沒先說主角是什麼，結果寫成「都不一樣」「每張的字都寫對」這類絕對說法 | 中低 |
| E1 | `lede-shortest-path-spec-dump` | ComfyUI 官方 MCP（11-02） | summary 與開頭用「最短的路徑是三步」起頭，把指令、版本與環境一次倒出來 | 高 |
| E2 | `formal-dense-rule-explanation` | Claude Code deny 規則（10-26） | 開頭用「拿整段指令文字比對」「規則就不算符合」這類書面、密集的機制句解釋症狀 | 中高 |

不採用的改動（只是增刪事實、換圖、改結構或調整程式碼）列在第 6 節，包含原本列為候選的 B5（小節順序）與 D1（PyTorch 不該改的「不是……而是」）。

---

## 2. Spigot 轉 Paper

文章：`content/posts/games/spigot-to-paper/index.md`，公開網址 `/games/spigot-to-paper/`。

版本鏈：`35ccac6` 起稿（12:47）→ `bc1e255` 改從換伺服器的理由切入、外掛實驗移到實測紀錄 → `a1353ee` 第一段強調資料完整保留 → `9067d37` 標題改成強調資料完整保留 → `2219d6e` 拆清楚換 jar 的步驟、補示意圖與警告截圖 → `b739037` 用示意圖說明地獄與終界 → `5b4a7b9` 發佈（13:55，只改 `publishDate`、`draft` 與 `_redirects`）。全部在 PR #94（`c1815c4`，13:58）一次合併到 main，中間各版都是 `draft: true`。

作者意見的出處：`aeb94ea`（官方做法為主、最小實作）、`dca8dcd`（標題不寫會過時的評價、關鍵步驟配示意圖）、`c727145` 起稿格式對照表的 Paper 列。

### A1 `lede-starts-with-constraint`

- 文章與 commit：Spigot 轉 Paper，初稿 `35ccac6`，中間 `bc1e255`（重寫第一段）、`a1353ee`（句尾改成「都能被完整保留下來」），發佈 `5b4a7b9`。
- 初稿原文（summary、第一段、第二段）：

`paper-35ccac6` 第 3,17,19 行：

````markdown
summary: "Paper 是 Spigot 的直接替代品，原本的外掛不用修改就能使用。從 Minecraft 26.1 起，Spigot 的世界要先轉回原版的資料夾結構，才能換成 Paper。"

Minecraft 26.1 起，Spigot 伺服器要換成 Paper，得先把世界轉回原版的資料夾結構，再換上 Paper 的 jar 檔，[Paper 的遷移文件](https://docs.papermc.io/paper/migration)寫明 Spigot 已經不能直接遷移。Paper 在[官方文件](https://docs.papermc.io/paper/getting-started/)裡是 Spigot 的直接替代品，外掛不用修改，[官方網站](https://papermc.io/software/paper)另外列出光照引擎、漏斗與實體的效能最佳化。我在一個裝了 LuckPerms 與 EssentialsX 的 Spigot 26.3 伺服器的三個維度各放一塊標記方塊，把地獄與終界搬回原版的位置再換成 Paper，三塊方塊、LuckPerms 建立的群組和兩個外掛都保留下來。

測試環境是 Windows 11 與 Java 25，Spigot 26.3 用 BuildTools 建置，Paper 是 26.3 的 build 240，外掛是 LuckPerms 5.5.71 與 EssentialsX 2.22.0。Paper 26.1 起需要 Java 25，和 26.1 起的原版伺服器相同，原本執行 Spigot 26.x 的電腦不用另外安裝。
````

- 發佈版：

`paper-5b4a7b9` 第 3,17,19 行：

````markdown
summary: "Paper 是以 Spigot 為基礎、針對效能做最佳化的 Minecraft 伺服器，Spigot 的外掛不用修改就能繼續使用。新版的 Spigot 把地獄與終界存在和原版不同的位置，先把世界轉回原版的結構再換成 Paper，世界與外掛的資料都能完整保留。"

Paper 是以 Spigot 為基礎的 Minecraft 伺服器，[官方網站](https://papermc.io/software/paper)列出它對光照引擎、漏斗與實體做的效能最佳化，[官方文件](https://docs.papermc.io/paper/getting-started/)也把它定位成 Spigot 的直接替代品，原本的外掛不用修改就能繼續使用。從 Minecraft 26.1 起，Spigot 把地獄與終界存在和原版不同的資料夾，[Paper 的遷移文件](https://docs.papermc.io/paper/migration)因此要求先把世界轉回原版的結構，再換上 Paper 的 jar 檔。我照這個順序把一台 Spigot 伺服器換成 Paper，三個維度的世界與外掛的資料都能被完整保留下來。

測試環境是 Windows 11 與 Java 25，Spigot 26.3 用 BuildTools 建置，Paper 是 26.3 的 build 240。Paper 26.1 起需要 Java 25，和 26.1 起的原版伺服器相同，原本執行 Spigot 26.x 的電腦不用另外安裝。
````

- 作者改了什麼：開頭依序寫「主角是什麼、伺服主為什麼要換（外掛不用改、效能最佳化）→ 限制與原因（26.1 起 Spigot 把地獄與終界存在不同的資料夾，遷移文件要求先轉回原版）→ 照做後的結果（資料完整保留）」，驗證用的外掛、標記方塊與外掛版本移到「實測紀錄」。初稿第一句先丟限制與步驟，第一段後半是實驗設計。
- 對照 baihua：
  - 實驗設計移後：部分涵蓋。`registers/article.md`「內容取捨」寫了環境與版本依讀者需要分開寫，「結構」的保留條件提到實測紀錄是報告體，但沒有寫「驗證用的素材、案例數放到實測紀錄，開頭只寫讀者層級的結論」（vervecode 起稿格式第 9 條）。
  - 開頭順序：沒有涵蓋，而且和 SKILL.md 核心規則 2「先給答案」與 `article.md`「第一段直接回答讀者來找的問題」有張力。初稿的第一句其實就是答案（先轉回原版再換 jar），作者要的是先介紹主角與動機（起稿格式第 1 條）。這條要先決定 baihua 要不要收，才能當題目。
- 建議的任務說明：

  > 幫我改寫這篇技術文章的 summary 和第一段。讀者是經營 Minecraft Spigot 伺服器、考慮換成 Paper 的伺服主，最在意世界與外掛的資料能不能完整搬過去。第一段後面是測試環境那段（下面附上，不用改），接著是備份、把地獄與終界搬回原版位置、換上 Paper jar 的步驟。文章最後有「實測紀錄」一節，已經寫了測試用的 LuckPerms、EssentialsX、vip 群組與三個維度的標記方塊。補充事實：從 Minecraft 26.1 起，Spigot 把地獄與終界存在和原版不同的資料夾。
  >
  > （附上初稿的 summary、第一段、第二段）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if summary 與第一段先說 Paper 是什麼、伺服主為什麼會想換（官方定位為 Spigot 的直接替代品，外掛不用修改；官方網站列出的效能最佳化），再寫限制與原因（26.1 起地獄與終界的位置不同，遷移文件要求先轉回原版結構再換 jar），最後寫照做後世界與外掛的資料都保留下來；第一段不再出現 LuckPerms、EssentialsX、標記方塊這類驗證用的素材。
  - FAIL if 第一句仍以「26.1 起要先轉回原版」這類限制或步驟開場、第一段仍描述實驗設計、刪掉或改動三個官方連結與「光照引擎、漏斗與實體」，或加入原文沒有的效能數字與功能。
- 必須保留的事實（regex）：`26\.1`、`光照引擎`、`直接替代品`、`jar`、`docs\.papermc\.io/paper/migration`（contains）；`LuckPerms|EssentialsX|標記方塊` 不得出現在 summary 與第一段（not_contains，第二段若一起輸出，要把測試環境段排除在外，或只讓模型輸出 summary 與第一段）。
- 適合度：高。片段獨立、改法清楚，而且能測出 baihua 目前沒有的規則。風險是「主角先介紹」和「先給答案」衝突，規則沒定之前，有 skill 的組很可能保留初稿的句序。

### A2 `title-dated-performance-claim`

- 文章與 commit：Spigot 轉 Paper，初稿 `35ccac6`，AI 依作者「改從換伺服器的理由切入」重寫的 `bc1e255`（作者退回的就是這版），發佈 `9067d37`／`5b4a7b9`。
- 初稿原文：

`paper-35ccac6` 第 2 行：

````markdown
title: "Spigot 伺服器轉 Paper：保留世界與外掛的 Minecraft 26.x 遷移步驟"
````

`paper-bc1e255` 第 2 行：

````markdown
title: "Minecraft Spigot 伺服器轉 Paper：保留世界與外掛，換成效能最佳化的伺服器"
````

- 發佈版：

`paper-5b4a7b9` 第 2 行：

````markdown
title: "Minecraft Spigot 伺服器轉 Paper：世界與外掛資料完整保留的遷移步驟"
````

- 作者改了什麼：作者退回「直接寫效能最佳化的伺服器感覺不對，如果之後有更強的核心得改標題」（`dca8dcd` 的 writing-style 紀錄）。冒號後改寫伺服主在意的結果：資料完整保留。`35ccac6` 的「Minecraft 26.x」是版本號。
- 對照 baihua：版本號已涵蓋（`article.md`「標題、摘要與第一段……套件版本……都不放進來」、「標題冒號後面寫讀者的問題或得到的結果」）。「日後會過時的評價」沒有明寫，最接近的是 `patterns.md` P10 評價詞，但「效能最佳化」是官方網站列出的事實，不是空泛評價，P10 判不出來。
- 建議的任務說明（用 `bc1e255` 的標題當原文）：

  > 幫我潤稿這篇教學文章的標題，只輸出標題一行。文章教 Spigot 伺服主照 Paper 官方遷移文件，把伺服器換成 Paper：先備份、把地獄與終界搬回原版的位置，再換上 Paper 的 jar 檔。實測換完後，三個維度的世界、LuckPerms 的群組和兩個外掛都還在。
  >
  > 目前的標題：Minecraft Spigot 伺服器轉 Paper：保留世界與外掛，換成效能最佳化的伺服器
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 冒號前保留 Minecraft、Spigot 與 Paper，冒號後寫讀者在意的結果或任務，例如世界與外掛資料保留、遷移步驟，不再以效能當賣點。
  - FAIL if 冒號後仍有「效能最佳化」「更快」「更強」這類評價，或加入版本號、資料夾名稱。
- regex：`效能|最佳化|更快|26\.` not_contains。
- 適合度：中。題目短、好評分，但和現有的 `overpromising-title` 同類，而且「會過時」這個理由要靠任務說明以外的判斷，沒有 skill 的組也可能自然改對。

### A3 `jar-swap-steps-and-worries`

- 文章與 commit：Spigot 轉 Paper，初稿 `35ccac6`（`bc1e255`～`9067d37` 這段只刪了啟動秒數），改寫 `2219d6e`，發佈 `5b4a7b9`。
- 初稿原文（「換成 Paper 並啟動」一節）：

`paper-35ccac6` 第 41-55 行：

````markdown
## 換成 Paper 並啟動

從 [Paper 下載頁](https://papermc.io/downloads/paper)下載和 Spigot 相同 Minecraft 版本的 Paper，放進伺服器資料夾，並照遷移文件的做法把檔名改成啟動指令裡的 jar 檔名。例如 `start.bat` 啟動的是 `spigot-26.3.jar`，就先刪掉原本的 Spigot jar，再把 Paper 的檔案改成這個名字，`start.bat` 不用改。`plugins` 資料夾留在原位。

照原本的方式啟動伺服器，Paper 發現世界要轉換，會先印出這段警告並等 30 秒：

```text
[WorldFolderMigration] ===================== ! ALERT ! =====================
[WorldFolderMigration] World storage migration is required during startup.
[WorldFolderMigration] If you do not have a backup: interrupt the server now. Use Ctrl+C, your panel kill function, etc.
[WorldFolderMigration] =====================================================
[WorldFolderMigration] Continuing in 30 seconds...
```

已經備份就不用中斷，30 秒後 Paper 會轉換三個維度的資料夾，實測從開啟到 `Done` 約 39 秒。之後再啟動就不會出現這段警告，到 `Done` 約 9 秒。
````

- 發佈版：

`paper-5b4a7b9` 第 39-53 行：

````markdown
## 換成 Paper 並啟動

換成 Paper 只要換掉伺服器資料夾裡的 jar 檔，世界、`plugins` 資料夾與啟動指令都不用動。Paper 的遷移文件要求把 Paper 的 jar 改成啟動指令裡的檔名：

1. 從 [Paper 下載頁](https://papermc.io/downloads/paper)下載和 Spigot 相同 Minecraft 版本的 Paper，檔名類似 `paper-26.3-240.jar`。
2. 刪掉伺服器資料夾裡原本的 Spigot jar，例如 `spigot-26.3.jar`。
3. 把下載的 Paper 放進伺服器資料夾，改成剛才刪掉的檔名。

![左邊是換之前的伺服器資料夾，Spigot 的 spigot-26.3.jar 要刪掉，下載的 paper-26.3-240.jar 改名成 spigot-26.3.jar 放進右邊的資料夾，plugins、world 與 start.bat 都不動](jar-swap.svg)

接著照原本的方式啟動伺服器，例如雙擊 `start.bat`。Paper 第一次啟動時會發現世界要轉換，先印出 ALERT 警告並倒數 30 秒：

![伺服器視窗裡 WorldFolderMigration 印出的黃色 ALERT 警告，寫著沒有備份就現在中斷伺服器，最後一行是 Continuing in 30 seconds](migration-alert.png)

這段警告提醒沒有備份的人在倒數結束前中斷。前面已經備份，就等它倒數完，Paper 會轉換三個維度的資料夾並繼續啟動，看到 `Done` 就啟動完成。之後再啟動就不會出現這段警告。
````

- 作者改了什麼：先回答讀者照做時的擔心（只換 jar，世界、`plugins` 與啟動指令都不用動），下載、刪除、改名拆成編號步驟，警告說明它的用意與「已經備份就等倒數」，用 `Done` 當成功訊號；39 秒與 9 秒移到實測紀錄。log 改成截圖、加示意圖不算文字改動。
- 對照 baihua：部分涵蓋。SKILL.md 核心規則 9「步驟用條列」、`article.md`「每篇都要讓讀者能確認自己做對了」。沒有涵蓋的是 vervecode 起稿格式第 3 條「每個操作先回答讀者照做時會擔心的事：哪些東西不用動、畫面上的警告要不要理會」與第 7 條「一句有好幾個動作就拆成編號步驟」。
- 建議的任務說明：

  > 幫我改寫教學文章「換成 Paper 並啟動」這一節。讀者剛照前一節備份好整個伺服器資料夾，並把地獄與終界搬回原版的位置。原文的伺服器 log 在這題用〔ALERT 警告〕代替，保留位置即可。下一節「確認轉換結果」會教讀者用 `version` 與 `plugins` 檢查；文章最後的「實測紀錄」已經寫了第一次約 39 秒、之後約 9 秒的啟動時間。
  >
  > （附上初稿第 43～55 行，log 換成〔ALERT 警告〕）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 一節開頭就讓讀者知道換成 Paper 只要換掉 jar，世界、`plugins` 與啟動指令都不用動；下載相同 Minecraft 版本的 Paper、刪掉原本的 Spigot jar、把 Paper 改成啟動指令裡的檔名寫成依序的步驟；寫出 ALERT 警告是要沒有備份的人中斷，已經備份就等 30 秒的倒數結束；以看到 `Done` 當啟動完成的訊號。
  - FAIL if 下載、改名、刪除仍擠在同一段，「不用改」「留在原位」仍只放在句尾；沒交代警告要不要理會；改動「相同 Minecraft 版本」「30 秒」「三個維度」「之後不會再出現警告」任一事實；或加入原文沒有的指令、檔名與步驟。啟動秒數因為實測紀錄已有，刪掉不算錯。
- regex：`30 秒`、`plugins`、`Done`、`start\.bat|啟動指令`（contains）。
- 適合度：中高。改法清楚、能測出 baihua 缺的規則；但要把 log 換成佔位符，判斷「讀者的擔心」比較主觀。

### A4 `closing-leads-with-paths-versions`

- 文章與 commit：Spigot 轉 Paper，初稿 `35ccac6`，改寫 `bc1e255`，發佈 `5b4a7b9`。
- 初稿原文：

`paper-35ccac6` 第 65-67 行：

````markdown
## 總結

Spigot 26.3 的地獄與終界搬回 `world/dimensions/minecraft/` 後換成 Paper 26.3，三個維度的標記方塊、LuckPerms 建立的群組，以及 LuckPerms 5.5.71 與 EssentialsX 2.22.0 都保留下來。Paper 的遷移文件寫明不支援轉回 Spigot。
````

- 發佈版：

`paper-5b4a7b9` 第 77-79 行：

````markdown
## 總結

Spigot 換成 Paper 前，要先把地獄與終界搬回原版的位置，再換上 Paper 的 jar 檔。實測 Spigot 26.3 換成 Paper 26.3 後，三個維度的方塊、LuckPerms 的群組與兩個外掛都保留下來。Paper 的遷移文件寫明不支援轉回 Spigot。
````

- 作者改了什麼：第一句用概念寫讀者要做的關鍵動作與順序（先搬地獄與終界，再換 jar），不寫路徑；第二句才是實測結果，外掛版本號拿掉。`c727145` 把它寫成 vervecode 規則：「教學與技術紀錄的總結……第一句用概念寫出讀者要做的關鍵動作（不寫路徑與版本），第二句寫實測結果」。
- 對照 baihua：部分涵蓋。`article.md`「結尾用一到兩段具體結論，不重述正文」與 P17。「第一句用概念寫關鍵動作、不寫路徑與版本」沒有涵蓋，`article.md` 只規定標題、摘要與第一段不放路徑與版本。
- 建議的任務說明：

  > 幫我改寫這篇教學文章的總結。文章教 Spigot 伺服主把伺服器換成 Paper：備份、把地獄與終界搬回原版的位置、換上 Paper 的 jar 檔。正文的「實測紀錄」已經寫了：在 Spigot 26.3 裝 LuckPerms 5.5.71 與 EssentialsX 2.22.0、用 LuckPerms 建一個 vip 群組、在三個維度各放一塊標記方塊，換成 Paper 26.3 後都還在。
  >
  > （附上初稿的總結段）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 第一句寫讀者要做的關鍵動作與順序（先把地獄與終界搬回原版的位置，再換上 Paper），不寫資料夾路徑；接著寫實測結果（Spigot 26.3 換成 Paper 26.3 後，三個維度的方塊、群組與兩個外掛都保留）；保留遷移文件不支援轉回 Spigot。
  - FAIL if 第一句仍以路徑或版本號開頭、仍列出外掛的版本號、重述正文的步驟細節、加上優缺點或條列，或加入原文沒有的結果。
- regex：`world/dimensions|5\.5\.71|2\.22\.0` not_contains；`轉回 Spigot` contains。
- 適合度：中。短、好評分，但「實測結果要不要寫版本」有灰色地帶（發佈版保留了 26.3）。

---

## 3. Claude Code PreToolUse hook

文章：`content/posts/ai/claude-code-hooks-git-guard/index.md`，公開網址 `/ai/claude-code-hooks-git-guard/`。

版本鏈：`5f9c2fc` 草稿（14:24）→ `0e4cb77` 依作者「整篇很亂」從讀者操作順序重寫，加流程圖與指令拆解圖、腳本只留推送相關規則 → `8a780fc` 依作者改的 summary「全文改成完整句」→ `f69e352` 發佈（14:57，只改 `publishDate`、`draft`、加縮圖）。全部在 PR #95（`74316fe`，14:59）合併。

作者意見的出處：`2e7a677`（話要寫完整、把結果說出來）、`75b8314`（小節照讀者操作順序、腳本只放讀者需要的規則、完整句）、`c727145` 起稿格式對照表的 hooks 列。

### B1 `lede-rules-not-enough-compressed`

- 文章與 commit：hooks，初稿 `5f9c2fc`，中間 `0e4cb77`（重排）與 `8a780fc`（補完整句，summary 是作者改的），發佈 `f69e352`。
- 初稿原文（summary、第一段、第二段）：

`hooks-5f9c2fc` 第 3,16-18 行：

````markdown
summary: "寫給 Agent 看的規則只是提醒，Agent 判斷錯時仍可能直接推送 main 或 force-push。Claude Code 的 PreToolUse hook 會在工具執行前先跑檢查腳本，只要腳本回答擋下，指令就不會執行，權限模式與子代理都一樣。"

想讓 Agent 只在開發分支工作、不直接推送 `main`，只把規則寫給 Agent 看並不夠，Agent 判斷錯時仍會照樣執行。Claude Code 的 PreToolUse hook 會在每次執行指令前先跑一支檢查腳本，腳本回答擋下，這次指令就不會執行，不受權限模式影響，子代理也一樣。

本站的原始碼放在 GitHub 的私有 repo，在 `draft` 分支開發，再開 PR 合併到 `main`。[私有 repo 的分支保護需要付費方案](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)，我當時用免費組織帳號開不了，只能把規則寫給 Agent 看，後來改用 hook 在指令執行前檢查。
````

- 中間版 `0e4cb77`（結構已改，句子還是壓縮的）：

`hooks-0e4cb77` 第 3,16-18 行：

````markdown
summary: "私有 repo 開不了分支保護時，Agent 判斷錯就可能直接推送 main 或 force-push，寫給它看的規則只能提醒。透過 Claude Code 的 PreToolUse hook，Agent 每次執行指令前都會先經過一支檢查腳本，只要腳本判定違規，指令就不會執行，且不受權限模式影響。"

讓 Agent 自己 commit 與推送很省事，但它判斷錯時，可能把改動直接推上 `main`，或用 force-push 蓋掉遠端的歷史。把「不要推送 main」寫進專案規則，[Claude Code 只會把它當成參考的內容](https://code.claude.com/docs/en/memory.md)，要在 Agent 判斷錯時也擋得下來，就要用 PreToolUse hook。Agent 每次執行指令前，Claude Code 都會先把指令交給一支檢查腳本，腳本判定違規，這次指令就不會執行。

本站的原始碼放在 GitHub 的私有 repo，在 `draft` 分支開發，再開 PR 合併到 `main`。[私有 repo 的分支保護需要付費方案](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)，我當時用的免費組織帳號開不了，就改用 hook 擋下 Agent 推送 `main`。Hook 只檢查 Claude Code 透過 Bash 與 PowerShell 工具執行的指令，自己在終端機推送不受影響。
````

- 發佈版：

`hooks-f69e352` 第 3,17-19 行：

````markdown
summary: "當私有 repo 無法開啟分支保護時，Agent 一旦判斷錯誤，就可能直接把改動推送到 main 或執行 force-push，而寫給它看的規則只能作為一種提醒，模型不一定會完全遵從。透過 Claude Code 的 PreToolUse hook，Agent 每次執行指令前都會先經過一支檢查腳本，只要腳本判定指令違反規則，這個指令就不會被執行，而且不論使用哪種權限模式都一樣有效。"

讓 Agent 自己 commit 與推送，可以省下手動操作 git 的時間，但當它判斷錯誤時，可能會把改動直接推送到 `main`，或用 force-push 覆蓋掉遠端的提交歷史。即使把「不要推送 main」寫進專案規則，[Claude Code 也只會把這些規則當成參考的內容](https://code.claude.com/docs/en/memory.md)，模型不一定會完全遵從。若要在 Agent 判斷錯誤時也能擋下指令，就要使用 PreToolUse hook。設定 hook 之後，Agent 每次執行指令前，Claude Code 都會先把指令交給一支檢查腳本，只要腳本判定這個指令違反規則，指令就不會被執行。

本站的原始碼放在 GitHub 的私有 repo，平時在 `draft` 分支上開發，完成後再開 PR 合併到 `main`。GitHub 的[私有 repo 要開啟分支保護需要付費方案](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)，我當時使用的免費組織帳號無法開啟，於是改用 hook 來擋下 Agent 推送 `main` 的指令。Hook 只會檢查 Claude Code 透過 Bash 與 PowerShell 工具執行的指令，我們自己在終端機手動推送時不會受到影響。
````

- 作者改了什麼：
  - 開頭順序：從「讓 Agent 自己推送可以省時間，但判斷錯誤時可能推送 main」起頭，再寫規則只是參考、模型不一定遵從，最後才帶出 hook（起稿格式第 1 條，對照表引了這兩句）。
  - 句子補齊：「開不了」→「無法開啟」、「判斷錯時」→「判斷錯誤時」、「腳本回答擋下，這次指令就不會執行」→「只要腳本判定這個指令違反規則，指令就不會被執行」（起稿格式第 2 條）。
  - 補上讀者的擔心：「我們自己在終端機手動推送時不會受到影響」（起稿格式第 3 條，屬於事實增補，題目要在說明裡給）。
- 對照 baihua：句子補齊已涵蓋（SKILL.md 核心規則 1、P01）。用否定句起頭、先講「只寫規則並不夠」接近 P02 假對比，但不完全是。開頭順序與讀者擔心沒有涵蓋（同 A1、A3）。
- 建議的任務說明：

  > 幫我改寫這篇技術文章的 summary 和開頭兩段。讀者是讓 Claude Code 的 Agent 自己 commit 與推送、想防止它直接推送 main 的工程師。標題是「Claude Code Hooks：私有 repo 沒有分支保護時，擋下 Agent 直接推送 main」。第三段是測試環境，之後是 hook 擋下指令的流程圖與設定步驟。補充事實：hook 只檢查 Claude Code 透過 Bash 與 PowerShell 工具執行的指令，人在終端機手動推送不受影響。
  >
  > （附上初稿的 summary 與第一、二段）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 開頭從讀者讓 Agent 自己推送的情境與風險（直接推送 main、force-push）寫起，再寫只寫進規則的做法模型不一定遵從，接著寫 hook 在指令執行前檢查、判定違規就不執行；判斷句都有主詞、動作與後果；第二段保留私有 repo、付費方案、免費組織帳號、draft → PR → main 的流程，並寫出手動推送不受影響。
  - FAIL if 仍以「想讓……，只把規則寫給 Agent 看並不夠」這類否定句開場；仍有「開不了」「腳本回答擋下，這次指令就不會執行」這類壓成片語的句子；刪掉付費方案連結、權限模式等事實；或加入原文與說明都沒有的功能。不要因為加了「而、則、即使……也」等連接詞或「被執行」這類被動句判 FAIL（作者發佈版就是這樣寫）。
- regex：`付費方案`、`force-push`、`draft`、`docs\.github\.com`（contains）；`開不了` not_contains。
- 適合度：中高。真實初稿、改法完整，但一次混了三種改法（順序、完整句、讀者擔心），評分重點要收斂；和 B2 重疊時二選一。

### B2 `telegraphic-article-sentences`

- 文章與 commit：hooks，原文用 `0e4cb77`（AI 依「整篇很亂」重寫後的版本，作者看完要求全文改成完整句），改寫 `8a780fc`，發佈 `f69e352`。這是今天最乾淨的一組：`8a780fc` 只改句子，不動結構與事實。
- 原文（「PreToolUse hook 擋下指令的流程」一節的文字）：

`hooks-0e4cb77` 第 24-30 行：

````markdown
Hook 依檢查腳本的結束碼，決定這次指令要擋下還是交回原本的流程：

![Agent 要執行的指令先交給 PreToolUse hook 的檢查腳本。結束碼 2 擋下並把原因回給 Agent，結束碼 0 交回原本的權限設定後執行，腳本出錯、無法執行或逾時時預設照常執行，設定 onFailure: block 時改成擋下](hook-flow.svg)

腳本以結束碼 2 結束時，寫到標準錯誤輸出（stderr）的文字會回給 Agent，當作指令被擋下的原因。[官方的 hooks 指南](https://code.claude.com/docs/en/hooks-guide#hooks-and-permission-modes)寫明，PreToolUse hook 在任何權限模式的檢查之前執行，`bypassPermissions` 模式下一樣擋得下，[子代理呼叫工具](https://code.claude.com/docs/en/hooks.md)時也會經過同樣的 hook。結束碼 0 只代表 hook 不擋，指令仍要經過原本的權限設定。

權限設定的 deny 規則也能擋指令，但只能用萬用字元比對指令文字，`git push origin +main` 這類寫法會漏掉，原因見[權限規則怎麼比對 Bash 指令](/ai/claude-code-bash-deny-rules/)。Hook 的腳本可以自己寫判斷，例如查 Agent 目前在哪個分支。
````

- 發佈版：

`hooks-f69e352` 第 25-31 行：

````markdown
Hook 會依照檢查腳本回傳的結束碼，決定要擋下這次的指令，還是交回原本的流程繼續處理：

![Agent 要執行的指令先交給 PreToolUse hook 的檢查腳本。結束碼 2 擋下並把原因回給 Agent，結束碼 0 交回原本的權限設定後執行，腳本出錯、無法執行或逾時時預設照常執行，設定 onFailure: block 時改成擋下](hook-flow.svg)

腳本以結束碼 2 結束時，寫到標準錯誤輸出（stderr）的文字會傳回給 Agent，作為指令被擋下的原因。[官方的 hooks 指南](https://code.claude.com/docs/en/hooks-guide#hooks-and-permission-modes)寫明，PreToolUse hook 會在任何權限模式的檢查之前執行，因此即使在 `bypassPermissions` 模式下也一樣能擋下指令，而[子代理在呼叫工具](https://code.claude.com/docs/en/hooks.md)時，也會經過同樣的 hook。結束碼 0 只代表 hook 不擋下這次的指令，指令仍然要經過原本的權限設定，才會真正執行。

權限設定裡的 deny 規則雖然也能擋下指令，但它只能用萬用字元比對指令的文字，像 `git push origin +main` 這類寫法就會被漏掉，詳細原因可以參考[權限規則怎麼比對 Bash 指令](/ai/claude-code-bash-deny-rules/)。Hook 的腳本則可以自己撰寫判斷邏輯，例如先查出 Agent 目前所在的分支，再決定要不要擋下。
````

- 同一個 commit 裡其他可以換用的段落（原文 → 發佈版）：

`hooks-0e4cb77` 第 214 行：

````markdown
`$CLAUDE_PROJECT_DIR` 是專案根目錄，Agent 先 `cd` 到子資料夾也找得到腳本。`"onFailure": "block"` 讓腳本出錯、無法執行或逾時的時候也擋下指令，這個欄位需要 [Claude Code 2.1.295 以上](https://code.claude.com/docs/en/hooks.md)。設定生效後，腳本只要壞掉，Agent 的所有 Bash 與 PowerShell 指令都會被擋下，這時要自己在編輯器修好腳本，或先拿掉這段設定。
````

`hooks-f69e352` 第 215 行：

````markdown
設定裡的 `$CLAUDE_PROJECT_DIR` 代表專案的根目錄，即使 Agent 先 `cd` 到子資料夾，也一樣找得到腳本。`"onFailure": "block"` 則讓腳本在出錯、無法執行或逾時的時候，也會擋下指令，這個欄位需要 [Claude Code 2.1.295 以上的版本](https://code.claude.com/docs/en/hooks.md)才能使用。設定生效後，只要腳本出現錯誤，Agent 執行的所有 Bash 與 PowerShell 指令都會被擋下，這時就要自己用編輯器修好腳本，或是先把這段設定拿掉。
````

- 作者改了什麼：壓成片語的判斷句補回動作與後果：「hook 不擋」→「hook 不擋下這次的指令，……才會真正執行」、「`bypassPermissions` 模式下一樣擋得下」→「因此即使在 `bypassPermissions` 模式下也一樣能擋下指令」、「原因見」→「詳細原因可以參考」、「腳本只要壞掉」→「只要腳本出現錯誤」。writing-style 的例子：「腳本判定違規，這次指令就不會執行」改成「只要腳本判定這個指令違反規則，指令就不會被執行」。
- 對照 baihua：已涵蓋，SKILL.md 核心規則 1（句子寫完整，保留「能、會、可以、的、和、再、就」）與 P01 電報式短句。要注意的是發佈版也和 baihua 其他規則衝突：
  - 被動句增加（「指令就不會被執行」「就會被漏掉」），核心規則 6 與 `translationese.md` 要少用不必要的被動。
  - 連接詞增加（「而」「則」「因此」「不過」「此外」），「中文句子的組法」第 3 條要省掉「因此、而且、此外、另外」。
  - 「撰寫判斷邏輯」偏書面。
  作者接受這些寫法，grader 不能因此判 FAIL。這題可能也會測出 baihua 把連接詞刪得比作者想要的多。
- 建議的任務說明：

  > 幫我潤稿這篇技術文章的一節，句子要寫完整。讀者是要設定 Claude Code PreToolUse hook 的工程師。這一節在開頭之後，說明 hook 怎麼依檢查腳本的結束碼擋下指令，流程圖在這題用〔流程圖〕代替，保留位置即可。下一節說明腳本怎麼判斷推送 main。
  >
  > （附上原文第 24～30 行，圖換成〔流程圖〕）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 每個判斷句都有主詞、動作與後果：結束碼 0 寫成 hook 不擋下這次的指令、指令仍要經過原本的權限設定才會執行；`bypassPermissions` 一句寫出「即使在這個模式下也能擋下指令」的關係；deny 規則一句寫出它只能用萬用字元比對指令文字、所以會漏掉 `git push origin +main`；連結前的「原因見」寫成完整句。連接詞與被動句不扣分。
  - FAIL if 仍留著「hook 不擋」「也能擋指令，但只能用萬用字元比對指令文字」「Hook 的腳本可以自己寫判斷」這類壓縮句；改動或刪掉三個連結、`stderr`、`bypassPermissions`、`git push origin +main`、子代理會經過同樣的 hook；或加入原文沒有的事實。
- regex：`bypassPermissions`、`\+main`、`stderr`、`hooks-guide#hooks-and-permission-modes`（contains）；`hook 不擋[，。]` not_contains。
- 適合度：高。片段獨立、只有句子層級的改動，對應 baihua 最核心的一條規則，而且題庫目前沒有技術文章語域的電報句題（`ui-error-messages-missing-please`、`ui-status-chip-terse-comparison` 都是介面文字）。

### B3 `limitation-scope-contrast`

- 文章與 commit：hooks，初稿 `5f9c2fc`，中間 `0e4cb77`，發佈 `f69e352`。
- 初稿原文：

`hooks-5f9c2fc` 第 267 行：

````markdown
這支腳本防的是 Agent 判斷錯誤，不是刻意繞過。`bash -c "git push origin main"` 這種把指令包在字串裡的寫法、用 `env git` 或完整路徑呼叫 git，以及 `$(...)` 裡的指令，它都不會拆開檢查。腳本本身也是 repo 裡的檔案，Agent 改掉腳本，下一次檢查就跟著失效。
````

- 中間版：

`hooks-0e4cb77` 第 189 行：

````markdown
這支腳本只拆解直接寫出的 git 指令。`bash -c "git push origin main"` 這種包在字串裡的寫法、`$(...)` 裡的指令，以及用完整路徑或 git alias 執行的推送，它都不會擋。腳本本身也是 repo 裡的檔案，Agent 改掉它，下一次檢查就跟著失效。
````

- 發佈版：

`hooks-f69e352` 第 190 行：

````markdown
這支腳本只會拆解直接寫出來的 git 指令，像 `bash -c "git push origin main"` 這種把指令包在字串裡的寫法、`$(...)` 裡的指令，以及用完整路徑或 git alias 執行的推送，都不會被擋下。此外，腳本本身也是 repo 裡的檔案，如果 Agent 修改了這支腳本，之後的檢查也會跟著失效。
````

- 作者改了什麼：刪掉「防的是 Agent 判斷錯誤，不是刻意繞過」的對比開場，直接寫腳本擋不到哪些寫法；「Agent 改掉腳本，下一次檢查就跟著失效」補成條件句。事實也有變動：拿掉 `env git`、加上 git alias（`0e4cb77` 在隔離環境重測後改的），題目要以初稿的事實為準。
- 對照 baihua：P02 假對比與核心規則 1。不過「防的是判斷錯誤，不是刻意繞過」也可以讀成在界定範圍：讀者可能以為 hook 是安全邊界。這符合 P02 的保留條件「讀者確實有那個誤解」，作者是在 `0e4cb77` 整篇重寫時一起刪掉的，沒有針對這句的評語。
- 建議的任務說明：

  > 幫我改寫技術文章的這一段。讀者剛看完一支擋下 Agent 推送 main 的 PreToolUse hook 腳本，這段說明腳本擋不到的情況。
  >
  > （附上初稿第 267 行）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 直接寫腳本只拆解直接寫出的 git 指令，列出擋不到的寫法；Agent 修改腳本的那句寫成有條件與後果的完整句（例如如果 Agent 修改了這支腳本，之後的檢查也會失效）。
  - FAIL if 刪掉 `bash -c`、`env git`、完整路徑、`$(...)` 任一項，或加入原文沒有的繞過方式（例如 git alias）。對比句是否保留不在 FAIL 條件裡，見下面的說明。
- regex：`bash -c`、`env git`、`\$\(\.\.\.\)`（contains）；`alias` not_contains。
- 適合度：中。片段短而獨立，但對比句該不該刪有爭議。比較穩的做法是只評完整句，或在任務說明裡寫明讀者不會把它當成安全機制。

### B4 `title-mechanism-after-colon`

- 文章與 commit：hooks，初稿 `5f9c2fc`，改寫 `0e4cb77`，發佈 `f69e352`。
- 初稿原文：

`hooks-5f9c2fc` 第 2 行：

````markdown
title: "Claude Code Hooks：用 PreToolUse 擋下 Agent 直接推送 main"
````

- 發佈版：

`hooks-f69e352` 第 2 行：

````markdown
title: "Claude Code Hooks：私有 repo 沒有分支保護時，擋下 Agent 直接推送 main"
````

- 作者改了什麼：冒號後從機制名稱（用 PreToolUse）改成讀者的情境（私有 repo 沒有分支保護時）與結果。`c727145` 把它寫進 vervecode 規則：「標題冒號後寫讀者遇到的情境或在意的結果……不寫機制名稱、檔名與版本號」。
- 對照 baihua：大致涵蓋。`article.md` 寫了「標題冒號後面寫讀者的問題或得到的結果」「最多點名主角工具」，檔名、參數、版本都排除，但「機制名稱」沒有明寫，PreToolUse 也可以算主角工具的一部分。
- 建議的任務說明：

  > 幫我潤稿這篇技術文章的標題，只輸出標題一行。文章寫給在 GitHub 私有 repo 開發、用免費方案開不了分支保護，又讓 Claude Code 的 Agent 自己 commit 與推送的人：用 PreToolUse hook 在 Agent 執行指令前先跑一支檢查腳本，擋下直接推送 main 的指令。
  >
  > 目前的標題：Claude Code Hooks：用 PreToolUse 擋下 Agent 直接推送 main
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 冒號前保留 Claude Code（Hooks），冒號後寫讀者的情境或結果，例如私有 repo 沒有分支保護、擋下 Agent 直接推送 main。
  - FAIL if 冒號後仍以「用 PreToolUse」這類做法或機制名稱帶頭，或加入版本號、檔名。
- regex：`：用 PreToolUse|2\.1\.` not_contains。
- 適合度：中。好評分，但任務說明一寫出情境就等於給了答案；不寫情境，模型又不可能知道「私有 repo」。

---

## 4. MOSS-Image 繁體中文圖文排版

文章：`content/posts/ai/moss-image-layout/index.md`，公開網址 `/ai/moss-image-layout/`。

版本鏈：`8f4bb6f` 草稿（00:45，test log 寫明這已經是作者退回第一版後的重寫，第一版沒有 commit）→ `c4e84bd` 正確做法先寫、直述寫法，第一段由作者親手改 → `85421e2` 改用介面名稱 enable_prompt_enhancer → `ab37481` 補縮圖結果、刪便條測試 → `6e79593` 發佈（01:18，PR #92 於 01:29 合併）→ `55c53f9` 重寫 summary 並改用「生成正確的文字」（UTC 11-03 18:09 = 台灣 02:09，PR #93 於 10:18 合併）。

作者意見寫在 `c4e84bd`、`85421e2`、`ab37481`、`55c53f9` 自己的 commit 裡（前綴是 `docs(content)`，不是 `docs(articles)`），見第 5.2 節。

### C1 `wrong-result-before-steps`

- 文章與 commit：MOSS-Image，初稿 `8f4bb6f`，改寫 `c4e84bd`，小修 `ab37481`、`6e79593`，最終 `55c53f9`。
- 初稿原文（「調整畫布比例」一小節）：

`moss-8f4bb6f` 第 73-89 行：

````markdown
### 調整畫布比例

在「解析度選擇器」選了 3:4 之後，「建立邊界框」節點的畫布仍是正方形。畫布的比例看的是這個節點自己的「寬度」和「高度」，這兩個欄位接著解析度選擇器的連線時不會顯示，數值停在範本預設的 1024：

![解析度選擇器已選 3:4 並顯示 1088 × 1456，建立邊界框的寬度與高度仍由連線帶入，下方畫框的畫布是正方形](editor-linked.png)

畫布上的座標以 1024 × 1024 為準，產圖時卻直接套在 1088 × 1456 的畫面上。照正方形畫布的位置排好五個框再產圖，所有的框都擠在畫面上方約七成的範圍，左邊這張的下方被補上一組沒要求的飲品照片拼貼，右邊這張的品名和日期變成亂碼：

![兩張寬高仍連著解析度選擇器時產出的咖啡店貼文。左邊的品名與價格擠在畫面中段，下方多出一組沒有要求的飲品照片拼貼，右邊的品名與日期變成拆開又疊在一起的亂碼](ig-square.jpg)

要讓畫布變成 3:4，先拆掉這兩條連線，再手動輸入寬高：

1. 從「建立邊界框」節點「寬度」的輸入點拖出連線，在畫布空白處放開。畫面跳出搜尋節點的視窗後按 Esc 關掉，連線就拆掉了。
2. 「高度」照同樣的方式拆掉。
3. 在出現的「寬度」與「高度」欄位輸入解析度選擇器顯示的尺寸，本例是寬度 1088、高度 1456。

畫布變成 3:4 後，已經畫好的框會照比例縮放。之後改了長寬比，這兩個欄位也要跟著改。
````

- 發佈版：

`moss-55c53f9` 第 55-67 行：

````markdown
### 調整畫布比例

在解析度選擇器選好 3:4 後，把「建立邊界框」節點的「寬度」和「高度」也改成同樣的尺寸，畫布才會變成 3:4。這兩個欄位預設連著解析度選擇器，要先拆掉連線才能輸入：

1. 從「建立邊界框」節點「寬度」的輸入點拖出連線，在畫布空白處放開。畫面跳出搜尋節點的視窗後按 Esc 關掉，連線就拆掉了。
2. 「高度」照同樣的方式拆掉。
3. 在出現的「寬度」與「高度」欄位輸入解析度選擇器顯示的尺寸，本例是寬度 1088、高度 1456。

畫布變成 3:4 後，已經畫好的框會照比例縮放。之後改了長寬比，這兩個欄位也要跟著改。

沒有拆線的話，畫布會維持 1024 × 1024 的正方形，框的位置照正方形計算，產圖時套在 1088 × 1456 的畫面上，所有的框都擠在畫面上方約七成的範圍。我在正方形畫布上框好開頭那張貼文的五個位置再產圖，左邊這張的下方多出一組沒要求的飲品照片拼貼，右邊這張的品名和日期變成亂碼：

![兩張寬高仍連著解析度選擇器時產出的咖啡店貼文。左邊的品名與價格擠在畫面中段，下方多出一組沒有要求的飲品照片拼貼，右邊的品名與日期變成拆開又疊在一起的亂碼](ig-square.jpg)
````

- 作者改了什麼：作者要求「不要做錯誤示範，文章都只能先寫正確方法，若要附上錯誤的結果是在該主題段落後補充」。改成先寫「把寬度和高度也改成同樣的尺寸，畫布才會變成 3:4」與拆線步驟，沒拆線的結果接在步驟後面，錯誤狀態的介面截圖刪掉。開頭也從「畫布的比例看的是這個節點自己的欄位」這類內部機制，改成讀者要做的事與看得到的結果。
- 對照 baihua：
  - 從機制切入：已涵蓋，`article.md`「結構」與檢查清單「從工具怎麼運作寫起」。題庫已有 `mechanism-first-paragraph`。
  - 錯誤示範在前、正確做法在後：沒有涵蓋。baihua 沒有「操作教學先寫正確做法，錯誤結果只在後面補充」的規則（vervecode 起稿格式第 5 條）。
- 建議的任務說明：

  > 幫我改寫教學文章的「調整畫布比例」這一小節。讀者已經打開 ComfyUI 的「MOSS-Image：版式控制生圖」範本，在「解析度選擇器」選了 3:4，下一小節要在「建立邊界框」的畫布上畫框。原文的截圖在這題用〔截圖：……〕代替，保留圖說即可；錯誤狀態的介面截圖可以刪掉。
  >
  > （附上初稿第 73～89 行，圖換成〔截圖：圖說〕）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 小節先寫讀者要做的事：把「建立邊界框」的寬度與高度改成和解析度選擇器相同的尺寸，要先拆掉連線再輸入（拖出連線放到空白處、按 Esc、輸入 1088 與 1456）；沒有拆線時畫布維持正方形、框擠到上方約七成、出現多餘的拼貼與亂碼，這些結果放在步驟之後補充。
  - FAIL if 仍先描述錯誤狀態或錯誤的產圖，再推到拆線步驟；第一句仍從「畫布的比例看的是……」這類機制寫起；刪掉拆線的任一步驟、「已經畫好的框會照比例縮放」「之後改了長寬比也要跟著改」，或改動 1024、1088 × 1456、約七成；或加入原文沒有的操作。
- regex：`1088`、`1456`、`七成`、`Esc`（contains）。
- 適合度：高。片段獨立、問題明確，發佈版的改法清楚，又能測出 baihua 缺的規則。

### C2 `argumentative-section-flow`

- 文章與 commit：MOSS-Image，初稿 `8f4bb6f`，改寫 `c4e84bd`（整節移到框選做法之後）、`85421e2`（介面名稱），最終 `55c53f9`。
- 初稿原文（「用 Prompt 描述版面」一節，排在框選做法之前）：

`moss-8f4bb6f` 第 51-67 行：

````markdown
## 用 Prompt 描述版面

先試最簡單的做法：打開「MOSS-Image：文字生圖」範本，把要放進圖裡的字和它們的位置都寫進 Prompt。範本預設開啟「Text to Image (MOSS-Image)」節點上的「enable_prompt_enhancer」，也就是提示詞擴寫，產圖前會先把 Prompt 改寫成一段詳細的英文描述。擴寫後的描述裡，用「」標出來的字都照原文留著，Prompt 直接用中文寫就可以。咖啡店貼文的 Prompt 如下：

```text
咖啡店的 Instagram 新品貼文，3:4 直式。上方寫「秋季限定」，中間是一杯桂花烏龍拿鐵的照片，下方大字寫品名「桂花烏龍拿鐵」，品名下面寫「11/8 起每日限量 50 杯」，右下角寫價格「NT$ 150」。暖色、溫暖的秋天氛圍，版面乾淨。
```

用兩個隨機種子各產一張，兩張都照 Prompt 的上下順序排好字，版面卻差很多。左邊的照片滿版，文字壓在上下兩條色帶上，「拿鐵」還寫成日文字形的「拿鉄」。右邊的照片縮成圓角卡片，字體和價格的顏色也不一樣：

![兩張用 Prompt 描述版面的咖啡店貼文。左邊照片滿版，品名寫成「桂花烏龍拿鉄」，右邊照片是圓角卡片，品名「桂花烏龍拿鐵」正確，兩張的價格位置與字體都不同](ig-auto.jpg)

活動海報也一樣，兩張的標題、日期、地點和「免費入場」都寫對了，插畫和標題的顏色卻各不相同。Prompt 沒有要求攤位的招牌寫字，右邊的招牌卻出現簡體的「艺术」和其他亂碼：

![兩張用 Prompt 描述版面的手作市集海報，標題「秋日手作市集」、日期、地點與「免費入場」都正確，右邊插畫的攤位招牌上有簡體字與亂碼](poster-auto.jpg)

YouTube 縮圖的兩張字也都寫對。想讓品名固定在照片下方、價格固定在右下角，就要改用框選位置的範本。
````

- 發佈版（「只用 Prompt 描述版面」一節，排在框選做法之後）：

`moss-55c53f9` 第 107-125 行：

````markdown
## 只用 Prompt 描述版面

「MOSS-Image：文字生圖」範本不用畫框，把要放進圖裡的字和位置都寫進 Prompt 就能產圖。這個範本預設開啟「enable_prompt_enhancer」，擴寫後的英文描述會保留 Prompt 裡用「」括起來的字，Prompt 直接用中文寫就可以。咖啡店貼文的 Prompt 如下：

```text
咖啡店的 Instagram 新品貼文，3:4 直式。上方寫「秋季限定」，中間是一杯桂花烏龍拿鐵的照片，下方大字寫品名「桂花烏龍拿鐵」，品名下面寫「11/8 起每日限量 50 杯」，右下角寫價格「NT$ 150」。暖色、溫暖的秋天氛圍，版面乾淨。
```

用兩個隨機種子各產一張，兩張都照 Prompt 的上下順序排好字，照片、字體和價格的位置每張不同。左邊的照片滿版，文字壓在上下兩條色帶上，品名的「拿鐵」生成為日文字形的「拿鉄」。右邊的照片縮成圓角卡片，品名正確：

![兩張用 Prompt 描述版面的咖啡店貼文。左邊照片滿版，品名是日文字形的「桂花烏龍拿鉄」，右邊照片是圓角卡片，品名「桂花烏龍拿鐵」正確，兩張的價格位置與字體都不同](ig-auto.jpg)

兩張活動海報都有生成正確的標題、日期、地點和「免費入場」，插畫和標題的顏色各不相同。右邊插畫的攤位招牌多出 Prompt 沒要求的簡體「艺术」和其他亂碼：

![兩張用 Prompt 描述版面的手作市集海報，標題「秋日手作市集」、日期、地點與「免費入場」都正確，右邊插畫的攤位招牌上有簡體字與亂碼](poster-auto.jpg)

YouTube 縮圖的兩張也都有生成正確的文字，只是標題的排法不同。上面這張把「3」放大成跨兩行的數字，「分鐘看懂」和「ComfyUI」排在它的右邊，下面這張的「3 分鐘看懂」排成一行。兩張的筆電都有一部分被畫面右緣切掉：

![兩張用 Prompt 描述版面的 YouTube 縮圖，字都正確。上面這張的「3」是跨兩行的大數字，下面這張的「3 分鐘看懂」排成一行，兩張的筆電都被右緣切掉一部分](thumb-auto.jpg)
````

- 作者改了什麼：作者退回「文章是直述的，而不是像在寫論文的論述法」。初稿用「先試最簡單的做法：」開段、「版面卻差很多」帶出問題、「想讓品名固定……就要改用框選位置的範本」推到下一節。發佈版每段直接寫讀者打開哪個範本、寫什麼、產出什麼，整節移到正確做法之後。`ab37481` 另外補了 YouTube 縮圖的結果與截圖，屬於事實增補。
- 對照 baihua：沒有涵蓋。最接近的是 P15 自我導覽與編輯語言、P16 首先其次最後，但「演進式鋪陳」（先試、卻、想要……就要改用）不在目錄裡。vervecode 起稿格式第 5 條把「先試」「最簡」「補上」「改用」列為要重排的訊號。
- 建議的任務說明：

  > 幫我改寫教學文章的「用 Prompt 描述版面」這一節，改成直述的寫法。這一節會放在「框出文字與物件的位置」那一節之後，讀者已經看過框選位置的做法和產出的圖。Prompt 與截圖在這題用〔Prompt〕〔截圖：……〕代替，保留位置即可。
  >
  > （附上初稿第 51～67 行）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 每段用直述句寫讀者打開「MOSS-Image：文字生圖」範本、把字和位置寫進 Prompt、產出什麼結果；沒有「先試最簡單的做法」這類演進式開場、「卻」這類製造轉折的寫法，也沒有「想讓……就要改用框選位置的範本」推到下一節的句子。
  - FAIL if 保留上述演進式或論證式的句子；刪掉或改動兩個隨機種子、「拿鉄」、簡體「艺术」與亂碼、YouTube 縮圖的字都正確、enable_prompt_enhancer 預設開啟與「」裡的字照原文留著；或加入原文沒有的結果。
- regex：`先試|最簡單|就要改用` not_contains；`拿鉄`、`艺术`、`enable_prompt_enhancer`（contains）。
- 適合度：中高。改法清楚，但任務說明必須交代「這一節排在框選之後」，不然模型不知道要拿掉推到下一節的句子；交代了又等於提示了一半。

### C3 `comma-chained-summary`

- 文章與 commit：MOSS-Image，初稿 `8f4bb6f`，`c4e84bd` 只加「就算」，`6e79593` 照這個 summary 發佈，`55c53f9` 重寫。
- 初稿原文（`8f4bb6f` 與 `6e79593`；6e79593 那版曾經公開）：

`moss-8f4bb6f` 第 3 行：

````markdown
summary: "MOSS-Image 會把 Prompt 裡指定的文字直接畫進圖裡，做社群貼文或海報時不用再另外排字。ComfyUI 的官方範本可以先在畫布上框出標題、照片和價格的位置再產圖，用繁體中文實測，框好位置的貼文、海報和縮圖字都寫對，換一個隨機種子重產，版面也和原本一樣。"
````

`moss-6e79593` 第 3 行：

````markdown
summary: "MOSS-Image 會把 Prompt 裡指定的文字直接畫進圖裡，做社群貼文或海報時不用再另外排字。ComfyUI 的官方範本可以先在畫布上框出標題、照片和價格的位置再產圖，用繁體中文實測，框好位置的貼文、海報和縮圖字都寫對，就算換一個隨機種子重產，版面也和原本一樣。"
````

- 發佈版（`55c53f9`）：

`moss-55c53f9` 第 3 行：

````markdown
summary: "MOSS-Image 能依照 Prompt 把指定的文字直接畫進圖裡，製作社群貼文或活動海報時就不必再另外排字。透過 ComfyUI 的官方範本，我們還能先在畫布上框出標題、照片和價格的位置，讓模型照著這個版面產圖。我用繁體中文實測，框好位置的貼文、海報和縮圖都有生成正確的文字，就算換一個隨機種子重產，版面也和原本一致。"
````

- 作者寫的第一段（給模型參考語氣用，作者在 `c4e84bd` 親手改）：

`moss-55c53f9` 第 17 行：

````markdown
MOSS-Image 是一個專精排版的生圖模型，我們能透過 ComfyUI 來使用此模型產圖，只要把想寫在圖上的字直接輸入進 Prompt，模型就會把它繪製到畫面上，做社群貼文或活動海報時就不用再另外開設計軟體排字。通常這類圖的標題、品名和價格有固定的位置，只靠 Prompt 描述的話，每次產出的版面容易有差異。ComfyUI 的 MOSS-Image 範本可讓我們先在畫布上框出每段文字和照片的位置，再照這個版面產圖。我嘗試用繁體中文來實驗生成咖啡店的新品貼文、市集活動海報和教學影片縮圖，每張的中文字品質頗高，且換一個隨機種子重產後，文字的位置也不會隨機偏移。
````

- 同一個 commit 的口語結果句（`6e79593` → `55c53f9`）：

`moss-6e79593` 第 99,103,115,119,123 行：

````markdown
活動海報框了標題、日期、地點、插畫和「免費入場」標籤，兩張的字都寫對，位置也幾乎一樣：

YouTube 縮圖框了標題（分兩行）、黃色副標和筆電三個框，兩張的字都寫對，標題和副標的位置幾乎一致，筆電的大小和角度不同：

用兩個隨機種子各產一張，兩張都照 Prompt 的上下順序排好字，照片、字體和價格的位置每張不同。左邊的照片滿版，文字壓在上下兩條色帶上，品名的「拿鐵」寫成日文字形的「拿鉄」。右邊的照片縮成圓角卡片，品名正確：

活動海報的標題、日期、地點和「免費入場」兩張都寫對，插畫和標題的顏色各不相同。右邊插畫的攤位招牌多出 Prompt 沒要求的簡體「艺术」和其他亂碼：

YouTube 縮圖的兩張字也都寫對，標題的排法不同。上面這張把「3」放大成跨兩行的數字，「分鐘看懂」和「ComfyUI」排在它的右邊，下面這張的「3 分鐘看懂」排成一行。兩張的筆電都有一部分被畫面右緣切掉：
````

`moss-55c53f9` 第 99,103,115,119,123 行：

````markdown
活動海報框了標題、日期、地點、插畫和「免費入場」標籤，兩張都有生成正確的文字，位置也幾乎一樣：

YouTube 縮圖框了標題（分兩行）、黃色副標和筆電三個框，兩張都有生成正確的文字，標題和副標的位置幾乎一致，筆電的大小和角度不同：

用兩個隨機種子各產一張，兩張都照 Prompt 的上下順序排好字，照片、字體和價格的位置每張不同。左邊的照片滿版，文字壓在上下兩條色帶上，品名的「拿鐵」生成為日文字形的「拿鉄」。右邊的照片縮成圓角卡片，品名正確：

兩張活動海報都有生成正確的標題、日期、地點和「免費入場」，插畫和標題的顏色各不相同。右邊插畫的攤位招牌多出 Prompt 沒要求的簡體「艺术」和其他亂碼：

YouTube 縮圖的兩張也都有生成正確的文字，只是標題的排法不同。上面這張把「3」放大成跨兩行的數字，「分鐘看懂」和「ComfyUI」排在它的右邊，下面這張的「3 分鐘看懂」排成一行。兩張的筆電都有一部分被畫面右緣切掉：
````

- 作者改了什麼：作者指出 summary「讀起來很像 AI 產的文字，缺少連接詞」，要和作者自己寫的第一段一樣，用「只要……就」「透過」「且」把分句的關係接起來；「字都寫對」過於口語，改成「模型有生成正確的文字」。
- 對照 baihua：
  - 逗號串短分句：已涵蓋，P06 逗號切碎與句長太平均。題庫的 `comma-chopped-lede` 同類，但那題是開頭句加冒號列舉，這題是 summary。
  - 補連接詞：和 baihua 有張力。「中文句子的組法」第 3 條要「關係看得出來就不寫連接詞」，作者要的是明寫「透過」「讓」「就算……也」。
  - 「字都寫對」這種口語動補：沒有涵蓋。baihua 的常見失誤只提「刻意口語、加語助詞」，沒有「口語動補要展開成主詞與動作完整的說法」。
- 建議的任務說明：

  > 幫我改寫這篇技術文章的 summary（front matter 的摘要，三句以內）。文章教讀者在 ComfyUI 用 MOSS-Image 的官方範本，先在畫布上框出文字與照片的位置再產圖，用繁體中文實測了咖啡店貼文、市集活動海報與 YouTube 縮圖。summary 的語氣與節奏要和作者寫的第一段一致，第一段如下：〔附上第一段〕
  >
  > （附上 `6e79593` 的 summary）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 分句之間的關係用完整句或連接詞寫出（例如透過範本框出位置、讓模型照著版面產圖、就算換隨機種子版面也一致），不再是「用繁體中文實測，框好位置的……字都寫對，……」這種一連串逗號接起來的短分句；結果寫成主詞與動作完整的說法（例如都有生成正確的文字）；三句以內。
  - FAIL if 仍有「字都寫對」；仍是逗號堆疊的短分句；刪掉把指定文字畫進圖裡、不用另外排字、框出標題照片和價格的位置、繁體中文實測、貼文海報縮圖、換隨機種子版面不變任一事實；或加入數字與原文沒有的功能。
- regex：`寫對` not_contains；`隨機種子`、`繁體中文`（contains）。
- 適合度：高。作者對 summary 有明確的評語，片段獨立；但這是今天唯一公開過的初稿（見第 7 節），而且「補連接詞」和 baihua 現有規則衝突，grader 要先對齊。

### C4 `untranslated-ui-option-in-parens`

- 文章與 commit：MOSS-Image，原文用 `c4e84bd`（這段的初稿 `8f4bb6f` 在「畫框並填寫內容」的最後一段，`c4e84bd` 把它改成這樣），改寫 `85421e2`，最終 `55c53f9` 相同。
- 初稿原文（`8f4bb6f`）：

`moss-8f4bb6f` 第 113 行：

````markdown
畫面右下的範本說明寫著「Prompt upsampler is on」，實際上這個範本的「enable_prompt_enhancer」預設是關閉的，範本裡另一則說明也提到開啟後擴寫會整個改寫框的內容，維持關閉就好。按「執行」，就會產出開頭那張貼文。
````

- 中間版（`c4e84bd`，作者指出錯誤的就是這版）：

`moss-c4e84bd` 第 91 行：

````markdown
這個範本的提示詞擴寫（「enable_prompt_enhancer」）預設關閉，範本裡的說明提到開啟後會改寫框的內容，維持關閉就好。畫面右下另一則說明寫著「Prompt upsampler is on」，和實際的預設不同，不用理會。按「執行」，就會產出開頭那張貼文。
````

- 發佈版：

`moss-55c53f9` 第 91 行：

````markdown
「Text to Image (MOSS-Image)」節點上的「enable_prompt_enhancer」開啟後，產圖前會先把 Prompt 擴寫成一段詳細的英文描述。這個範本預設關閉，範本裡的說明提到開啟後會改寫框的內容，維持關閉就好。畫面右下另一則說明寫著「Prompt upsampler is on」，和實際的預設不同，不用理會。按「執行」，就會產出開頭那張貼文。
````

- 作者改了什麼：作者指出「提示詞擴寫（「enable_prompt_enhancer」）」是錯誤用法：介面上顯示的就是 enable_prompt_enhancer，全文改成直接寫原名，第一次出現時用一句話說明開啟後的效果。`8f4bb6f` 到發佈版也從「實際上……預設是關閉的」改成先講功能、再講預設，最後寫明誤導的說明「不用理會」（起稿格式第 3 條）。
- 對照 baihua：部分涵蓋。`article.md`「術語」寫了用介面上看得到的字並加「」、不憑印象翻；但它把「有正體中文介面」與「沒有」分兩種情況，這個選項是「有中文介面但這個欄位沒翻」，沒有明寫「不自創中文名稱，也不把介面名稱放進括號當補充」。
- 建議的任務說明：

  > 幫我潤稿教學文章的這一段。讀者正在 ComfyUI 的 MOSS-Image 版式控制範本填好框，下一步按「執行」。ComfyUI 有正體中文介面，但「Text to Image (MOSS-Image)」節點上的 enable_prompt_enhancer 這個開關沒有翻譯，介面上顯示的就是 enable_prompt_enhancer；開啟後，產圖前會先把 Prompt 擴寫成一段詳細的英文描述。
  >
  > （附上 `c4e84bd` 第 91 行）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 用介面上的原字「enable_prompt_enhancer」稱呼這個開關，不以「提示詞擴寫」當名稱，也不把原名放進括號；第一次出現時說明開啟後的效果；保留範本預設關閉、範本說明提到開啟後會改寫框的內容、維持關閉、「Prompt upsampler is on」和實際預設不同不用理會、按「執行」產出開頭那張貼文。
  - FAIL if 仍寫「提示詞擴寫（「enable_prompt_enhancer」）」或用其他自創的中文名稱為主；刪掉或改動上述事實；或加入原文沒有的設定。
- regex：`擴寫（|提示詞擴寫（` not_contains；`enable_prompt_enhancer`、`Prompt upsampler is on`（contains）。
- 適合度：中。改法清楚，但任務說明一定要寫出「介面顯示原名」，題目就變得容易；適合當 glossary 類的題目。

### C5 `lede-absolute-claims`

- 文章與 commit：MOSS-Image，初稿 `8f4bb6f`，作者親手改 `c4e84bd`（之後不變）。
- 初稿原文：

`moss-8f4bb6f` 第 17 行：

````markdown
在 ComfyUI 用 MOSS-Image 產圖時，要出現在圖上的字直接寫進 Prompt，模型就會把它畫在畫面上，做社群貼文或活動海報不用再另外開設計軟體排字。這類圖的標題、品名和價格通常有固定的位置，只靠 Prompt 描述的話，每次產出的版面都不一樣。ComfyUI 的 MOSS-Image 範本可以先在畫布上框出每段文字和照片的位置，再照這個版面產圖。我用繁體中文做了咖啡店的新品貼文、市集活動海報和教學影片縮圖，框好位置後每張的字都寫對，換一個隨機種子重產，文字的位置也和原本一樣。
````

- 發佈版（作者寫的）：

`moss-55c53f9` 第 17 行：

````markdown
MOSS-Image 是一個專精排版的生圖模型，我們能透過 ComfyUI 來使用此模型產圖，只要把想寫在圖上的字直接輸入進 Prompt，模型就會把它繪製到畫面上，做社群貼文或活動海報時就不用再另外開設計軟體排字。通常這類圖的標題、品名和價格有固定的位置，只靠 Prompt 描述的話，每次產出的版面容易有差異。ComfyUI 的 MOSS-Image 範本可讓我們先在畫布上框出每段文字和照片的位置，再照這個版面產圖。我嘗試用繁體中文來實驗生成咖啡店的新品貼文、市集活動海報和教學影片縮圖，每張的中文字品質頗高，且換一個隨機種子重產後，文字的位置也不會隨機偏移。
````

- 作者改了什麼：先寫主角是什麼（「MOSS-Image 是一個專精排版的生圖模型，我們能透過 ComfyUI 來使用此模型產圖」），讀者也會做的事用「我們」當主詞，結果從絕對說法（「都不一樣」「每張的字都寫對」）改成「容易有差異」「中文字品質頗高」。
- 對照 baihua：開頭順序沒有涵蓋（同 A1）；「我們」已涵蓋（`article.md`「人稱以『我們』帶讀者」）。作者的文字也有 baihua 會挑的地方：「此模型」是 P25 書面腔，「品質頗高」是 P10 沒有依據的評價，「我嘗試用繁體中文來實驗生成」偏冗。
- 建議的任務說明：同 `write-article-intro` 的形式，給第一段原文，說明讀者是想用 AI 生圖做社群貼文與海報的人。
- PASS／FAIL 草稿（llm）：
  - PASS if 第一句先說 MOSS-Image 是什麼、能在 ComfyUI 使用；不用「都不一樣」「每張的字都寫對」這類絕對說法描述結果。
  - FAIL if 刪掉三種圖、換隨機種子文字位置不變等事實，或加入數字。
- 適合度：中低。這是 `src-hand` 的真實案例，價值在於作者的語感；但發佈版本身會被 baihua 的 P25、P10 判錯，用它當標準答案會讓 grader 和 skill 互相矛盾。比較適合拿去討論 baihua 的規則要不要放寬，不適合直接進題庫。

---

## 5. 歷史文章

### E1 `lede-shortest-path-spec-dump`

- 文章與 commit：`content/posts/ai/comfyui-mcp/index.md`（公開網址 `/ai/comfyui-mcp/`）。草稿 `63d4d59`（2026-11-02 23:25）→ `5e3a4b8`、`f3b22ed`、`185ccda`、`3bc2401`、`3d17b0c`、`ace6794`、`6b1591f` 用七個 commit 反覆改摘要與開頭 → `5fc9e12` 全文順稿 → `f405179` 發佈（11-03 00:14）。
- 初稿原文（summary、第一段、第二段）：

`mcp-63d4d59` 第 3,17,19 行：

````markdown
summary: "裝好官方的 comfy-mcp 並用 `comfy install` 建立 ComfyUI 後，以 `claude mcp add` 接上 Claude Code，就能用對話啟動 ComfyUI、下載模型與執行 workflow。本文在 Windows 11 與 RTX 3070 上從零實測，也說明怎麼用瀏覽器或 Comfy Desktop 打開 Claude Code 改過的 workflow。"

要讓 Claude Code 操作本機的 ComfyUI，最短的路徑是三步：用 uv 安裝 Comfy-Org 官方的 comfy-mcp，用 `comfy install` 建一個 ComfyUI 工作區，再用 `claude mcp add` 把 comfy-mcp 註冊給 Claude Code。之後啟動 ComfyUI、下載模型、套範本與執行 workflow 都能用對話完成，想看 workflow 或手動調整時，再用瀏覽器或 Comfy Desktop 打開。

本文在 Windows 11 與 RTX 3070 8 GB 上，用 uv 0.13.6、comfy-cli 1.24.0、comfy-mcp 0.10.0 與 ComfyUI 0.43.2 從零實測一次，不寫設定檔也不設環境變數，最後讓 Claude Code 只用 Prompt 產出這張 1024 × 1024 的 logo：
````

- 發佈版：

`mcp-f405179` 第 3,17,19 行：

````markdown
summary: "Claude Code 本身不會生圖，但接上 ComfyUI 官方的 comfy-mcp 後，可以照文字描述調整 ComfyUI workflow 裡的節點，用自己電腦上的模型產出想要的圖。改好的 workflow 能直接在 ComfyUI 打開，人再接著手動調整。"

ComfyUI 產圖的流程是一份 workflow，載入模型、輸入 Prompt、取樣和存檔各是一個節點，每個節點上的參數都是可以改的值。Claude Code 本身不會生圖，但讀得懂也改得動 workflow，等於能用程式控制 ComfyUI 產圖。我接上 ComfyUI 官方的 comfy-mcp 後，只用文字描述想要的 logo，Claude Code 就從範本改出一份 workflow，連缺的模型也一起下載，再交給本機的 ComfyUI 跑出圖。圖不滿意可以再描述一次，也可以在 ComfyUI 打開同一份 workflow，自己調整節點。

本文的測試環境是 Windows 11 與 RTX 3070 8 GB 顯示卡，ComfyUI 從零開始安裝，模型用 MOSS-Image。生圖要求是只用文字 Prompt、不給參考圖，產出一張 1024 × 1024 的 logo：暗色底，中上方是貓咪形狀的 logo，下方是 VerveCode 字樣。
````

- 作者改了什麼：作者退回「現在是一坨拉庫的把資訊都倒給讀者，認知負荷會太高」（writing-style「摘要與開頭分層」）。初稿用「最短的路徑是三步」開場，summary 與前兩段塞了三個安裝指令、四個套件版本、作業系統與顯示卡。定稿的 summary 只寫核心概念（Claude Code 本身不會生圖，接上 comfy-mcp 後能改 workflow 的節點、用本機模型產圖，人可以接手），第一段先說 workflow 由節點組成、參數可以改，再接作者實際的做法，第二段才是測試環境，套件版本留到安裝步驟。
- 對照 baihua：大致涵蓋。`article.md`「標題、摘要與第一段寫整篇要傳達的概念……指令、檔名與路徑都不放進來」與「環境與版本依讀者什麼時候需要分開寫」；`patterns.md` P15 自我導覽（「本文在……從零實測」）。「最短的路徑是三步」這種步驟式開場沒有明寫（vervecode 起稿格式第 1 條「不用步驟、要求或『最短做法』開場」）。題庫的 `filename-in-title-summary` 是同一條規則，但那題是檔名，這題是指令、版本與環境的堆疊，AI 腔更明顯。
- 建議的任務說明：

  > 幫我改寫這篇技術文章的 summary 和開頭兩段。讀者是會用 Claude Code、想讓它在自己電腦上用 ComfyUI 產圖的人，不一定熟 ComfyUI。後面的「架構」一節說明 Claude Code、comfy-mcp 與 comfy-cli 的關係，「安裝」一節會列出完整的指令與版本。開頭那張 logo 圖在這題用〔logo 圖〕代替。
  >
  > （附上初稿第 3、17、19 行）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if summary 與第一段寫讀者能得到什麼（讓 Claude Code 透過官方的 comfy-mcp 啟動 ComfyUI、下載模型、執行 workflow 產圖，人也能打開同一份 workflow 手動調整），不列安裝指令與套件版本；測試環境放在第二段；不再用「最短的路徑是三步」「本文在……」開場。
  - FAIL if summary 或第一段仍出現 `comfy install`、`claude mcp add` 或套件版本號；仍以步驟數或「最短」開場；刪掉 Windows 11、RTX 3070 8 GB、只用 Prompt 產出 1024 × 1024 logo 這些事實；或加入原文沒有的功能（例如 Claude Code 能直接生圖）。
- regex：`comfy install|claude mcp add|0\.13\.6|1\.24\.0|0\.10\.0|最短` not_contains（只檢查 summary 與第一段的話，要請模型照段落輸出，或改成 llm 判斷）。
- 適合度：高。AI 腔一眼可見（步驟式開場、規格清單、自我導覽），片段獨立，作者評語明確。

### E2 `formal-dense-rule-explanation`

- 文章與 commit：`content/posts/ai/claude-code-bash-deny-rules/index.md`（公開網址 `/ai/claude-code-bash-deny-rules/`）。草稿 `e617d13`（2026-10-26 20:06）→ `fe1f439`「改寫成白話版並補實測」→ `3b48d21` 發佈（只把 summary 的規則加上反引號）。
- 初稿原文（summary 與第一段）：

`deny-e617d13` 第 3,17 行：

````markdown
summary: "Claude Code 的 Bash 權限規則拿整段指令文字比對，所以 Bash(git push --force *) 擋不住 git push origin main --force。本文整理常見 deny 寫法漏掉的情況與改寫後的規則，規則列不完時改用 ask 或 hook。實測版本為 Claude Code 2.1.309。"

在 `.claude/settings.json` 寫了 `Bash(git push --force *)`，Claude 執行 `git push origin main --force` 時卻照樣推上遠端。原因是 Claude Code 的 Bash 權限規則拿整段指令文字比對，`*` 可以代表任意文字，其餘文字都要逐字相同。這條規則要求指令以 `git push --force` 開頭，`--force` 換到分支名稱後面，規則就不算符合。
````

- 發佈版（summary 與第一、二段）：

`deny-3b48d21` 第 3,17,19 行：

````markdown
summary: "Claude Code 的 Bash 權限規則只做文字比對，所以 `Bash(git push --force *)` 擋不住 `git push origin main --force`。本文列出常見 deny 寫法的漏洞、測過能用的規則，以及規則擋不住時改用 ask 或 hook 的做法。實測版本為 Claude Code 2.1.309。"

我在 `~/.claude/settings.json` 寫了 `Bash(git push --force *)`，想擋掉 Claude 的 force-push。實際測試時，`git push --force origin main` 有被擋下，但換成 `git push origin main --force`，Claude 就直接推上去了。這條規則要改成 `Bash(git push *--force*)` 才擋得住，`-f` 則要另外寫三條。

問題出在 Claude Code 只做文字比對。`Bash(git push --force *)` 只認 `git push --force` 開頭的指令，`--force` 放到後面就比對不到了。
````

- 作者改了什麼：作者要求改成白話版。「拿整段指令文字比對」→「只做文字比對」，「規則就不算符合」→「就比對不到了」，「本文整理……漏掉的情況與改寫後的規則」→「本文列出……的漏洞、測過能用的規則」。開頭改成作者的經驗順序：想擋什麼、哪個指令有擋下、哪個沒擋下，再寫原因與改法。vervecode 的速讀卡也收了這兩個例子：「不算符合」改成「比對不到」，「以 A 為例」改成「拿 A 來看」（同一個 commit 把「以 `Bash(...)` 為例」改成「拿 `Bash(...)` 來看」）。發佈版另外補了 `~/.claude/settings.json` 的路徑與「`--force` 有被擋下」的實測，屬於事實增補。
- 對照 baihua：部分涵蓋。`patterns.md` P25 書面腔、`registers/article.md`「像對同事說明：平實、直接」。「不算符合」這種繞口的書面說法、`*` 的定義句塞在症狀與原因之間（P05 一句塞太多概念）都有對應，但 baihua 的改稿原則 3 寫「沒有錯的詞不換」，vervecode 也明說「這條比 baihua 嚴格」，所以有 skill 的組未必會改。
- 建議的任務說明：

  > 幫我改寫這篇技術文章的 summary 和第一段，改得白話一點，像對同事說明。讀者是用 Claude Code 寫了 deny 規則、卻發現 force-push 沒被擋下的人。第一段後面接一份測過能用的設定檔，再來是比對方式的示意圖。補充事實：作者把規則寫在 `~/.claude/settings.json`，實測 `git push --force origin main` 有被擋下；規則要改成 `Bash(git push *--force*)` 才擋得住，`-f` 要另外寫三條。
  >
  > （附上初稿第 3、17 行）
  >
  > 只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

- PASS／FAIL 草稿（llm）：
  - PASS if 第一段照讀者遇到的順序寫：寫了什麼規則、哪個指令擋下、哪個指令照樣推上遠端，再用一兩句白話說出原因（規則只做文字比對，`--force` 換到後面就比對不到）；沒有「不算符合」這類繞口的說法；summary 保留實測版本 2.1.309 與 ask、hook 兩種替代做法。
  - FAIL if 仍有「規則就不算符合」「拿整段指令文字比對」這類書面又密集的句子；改動規則與指令的寫法；或加入原文與說明都沒有的事實。為了白話而加入語助詞、網路用語或裝熟口吻也算 FAIL（baihua 常見失誤）。
- regex：`Bash\(git push --force \*\)`、`git push origin main --force`、`2\.1\.309`（contains）；`不算符合` not_contains。
- 適合度：中高。初稿是典型的 AI 書面腔，作者的白話版清楚；但「白話」的程度和 baihua「沒有錯的詞不換」有張力，grader 要寫清楚哪些說法算問題。

## 6. 不採用的改動

| 文章 | commit | 改動 | 不採用的原因 |
| --- | --- | --- | --- |
| Paper | `b739037` | 維度對照表換成 `dimension-move.svg`，步驟改成「在 `world_nether/dimensions/minecraft` 裡的 `the_nether` 資料夾」，加「搬完後打開……應該有三個資料夾」 | 主要是換圖；成功訊號那句是事實增補 |
| Paper | `2219d6e` | ALERT log 換成截圖、加 `jar-swap.svg` | 換圖（文字部分已收進 A3） |
| Paper | `bc1e255` | 「確認版本、外掛與世界」一節併入啟動後、外掛實驗與 EssentialsX 的 ERROR 移到「實測紀錄」 | 內容搬移，不是句子問題 |
| hooks | `0e4cb77` | 結束碼表格換成流程圖、指令誤判表加「目前分支」「正確結果」欄、腳本拿掉本站專用的規則（`gh pr merge`、刪除 `draft`、main 上 commit） | 換圖、表格與程式碼內容；腳本取捨是內容決定 |
| hooks | `0e4cb77` | 單元測試數字從 44 個案例改成 38 個指令 | 重測後的事實變動 |
| MOSS | `ab37481` | 刪掉手寫便條的繁簡字測試、補 Prompt 縮圖的結果與截圖、Instagram 裁切數字改成 1086 × 1448 | 刪旁支內容與事實變動 |
| MOSS | `c4e84bd` | 刪掉「開發過程」一節 | vervecode 專屬的章節規則 |
| MOSS | `c4e84bd` | 「版式控制範本畫框用的「建立邊界框」節點，要在 Nodes 2.0 介面才看得到編輯器」→「版式控制範本用「建立邊界框」節點畫框，這個節點的編輯器只在 Nodes 2.0 介面顯示」 | 符合 baihua「中文句子的組法」第 4 條（名詞前只放短的修飾），但只有一句，太小 |
| hooks | `5f9c2fc` → `0e4cb77` | 小標順序從「規則只是提醒，hook 才會擋下／設定 hook／先擋下寫明 main 的推送／補上沒寫出 main 的推送／完整版擋下的動作」改成「PreToolUse hook 擋下指令的流程／判斷推送 main 的方式／建立檢查腳本／設定 hook／確認設定生效」（原 B5） | 改結構；要整篇重排又牽涉大量程式碼。小標改成名詞片語的部分 baihua 已涵蓋（P22） |
| PyTorch | `6353107`＝`5ce6881` | 正文沒改。第二段「這不是顯示卡或驅動程式出了問題，而是 pip 預設從 PyPI 下載」更正讀者真的有的誤解（原 D1，false-positive 候選） | 沒有改稿；作者沒留下評語，題庫已有同類的 `keep-clarifying-not-mean` |
| PyTorch | `4e64152` | ComfyUI MCP 的事前準備加一條連到 PyTorch 文章的內鏈 | 事實增補 |

---

## 7. 文風偏好

### 7.1 今天 `docs(articles)` commit 新增的偏好

依 commit 列出新增的原文。「規則」是寫進 `.claude/rules/article-style.md`（速讀卡）的句子，「例子」是寫進 `.claude/skills/vervecode-article-forge/references/writing-style.md` 的紀錄。涵蓋欄：「涵蓋」是 baihua 已有同樣的規則，「部分」是 baihua 有相近的規則但沒寫到這一點，「未涵蓋」是沒有，「範圍外」是內容或版面的決定，依 SKILL.md「本 skill 只決定句子怎麼寫，內容、術語與版面由使用者、專案與領域 skill 決定」不屬於 baihua。

`4158afb`、`bef75e2` 只加實測紀錄，沒有文風偏好。

| # | commit | 類型 | 原文 | baihua | 對應或說明 |
| --- | --- | --- | --- | --- | --- |
| 1 | `aeb94ea` | 規則 | 主要做法照官方文件寫。實測發現、官方沒寫的特殊行為隨時可能被改掉，不當主線，也不為它另開段落。文章收斂成讀者完成任務的最小做法，和主線不相干的內容不提。 | 部分／範圍外 | `article.md`「內容取捨」有「旁支刪掉」「操作教學只交付標題承諾的任務」；「官方做法為主」是內容決定 |
| 2 | `aeb94ea` | 例子 | **官方做法為主，最小實作：** Paper 文章實測發現 Paper 26.3 會自動轉換 Spigot 的世界資料夾，和官方遷移頁「先轉回原版」的說法不同。作者決定「以官方的做法為主，自己發現的特殊用法都有可能隨時被改掉」，並要求「收斂成最小實作，避免提到與主線不相干的內容，減少認知負荷」。（Paper 2026-11-04） | 同 1 | |
| 3 | `dca8dcd` | 規則（後來由 `c727145` 改寫，見 #14） | 標題寫讀者在意的結果（例如資料完整保留），不寫「效能最佳化」這類日後可能被超越而要改標題的評價。 | 部分 | `article.md` 的標題規則；「會過時的評價」沒寫 |
| 4 | `dca8dcd` | 規則（後來併入 #20） | 操作教學裡最關鍵、最容易做錯的步驟（例如搬資料夾、換檔案）配示意圖，畫出操作前後的對照。 | 範圍外 | SKILL.md 核心規則 9「流程用圖」只到格式選擇 |
| 5 | `dca8dcd` | 例子 | **標題寫讀者在意的結果，不寫會過時的評價：** Paper 文章的標題原本是「保留世界與外掛，換成效能最佳化的伺服器」，作者退回「直接寫效能最佳化的伺服器感覺不對，如果之後有更強的核心得改標題」。依讀者分析（伺服主最在意能不能無痛遷移），改成「世界與外掛資料完整保留的遷移步驟」，正文同一句也改成「都能被完整保留下來」，凸顯資料可以完整遷移。（Paper 2026-11-04） | 同 3 | |
| 6 | `dca8dcd` | 例子 | **關鍵步驟配示意圖：** Paper 文章的換 jar 與搬地獄、終界兩步原本只有文字和路徑對照表，作者要求「這是重要的關鍵內容，需要讓使用者非常容易理解」。換 jar 畫成換之前、換之後的資料夾對照，搬資料夾畫成左右兩棵資料夾樹加箭頭，標出要搬的、要刪的與用不到的，示意圖取代原本的對照表。步驟裡會出現的畫面（例如伺服器的遷移警告）用實際截圖，不貼成文字 log。（Paper 2026-11-04） | 範圍外 | |
| 7 | `2e7a677` | 例子 | **話要寫完整，把結果說出來：** Hooks 文章的 summary 寫「寫給它看的規則只能提醒」，作者改成「寫給它看的規則只能作為一種提醒，模型不一定會完全遵從」，並要求全文都照這樣寫。壓成片語的判斷句要補回動作與後果，例如「腳本判定違規，這次指令就不會執行」改成「只要腳本判定這個指令違反規則，指令就不會被執行」，「`--dry-run` 只模擬推送」改成「`--dry-run` 只會模擬推送的過程」。（Claude Code Hooks 2026-11-04） | 涵蓋 | SKILL.md 核心規則 1、P01；例句裡的被動「不會被執行」和核心規則 6 有張力 |
| 8 | `75b8314` | 規則 | 小節順序照讀者實際操作的先後排：設定檔參照的檔案先建立再加設定，確認生效放在設定之後。說明原理用的精簡程式碼不寫成要存檔的步驟，讀者只存一次完整版。 | 未涵蓋 | `article.md`「結構」沒有小節順序；「組法」第 2 條只管句內順序 |
| 9 | `75b8314` | 規則 | 文章附的腳本或設定只放讀者任務需要的規則，作者站內專用的規則用一句話帶過，不讓讀者自己刪。 | 範圍外 | 內容決定；最接近的是「每一段都服務讀者的任務」 |
| 10 | `75b8314` | 規則 | 話要寫完整，判斷句寫出動作與後果，例如「規則只能提醒」寫成「規則只能作為一種提醒，模型不一定會完全遵從」。 | 涵蓋 | 同 7（`c727145` 併進起稿格式第 2 條） |
| 11 | `75b8314` | 例子 | **小節照讀者操作的先後排：** Hooks 文章第二版的順序是「設定 hook → 最小腳本 → 完整版」，作者退回「整篇很亂」。審稿指出讀者照做會先存好設定，設定裡的 `onFailure: block` 會讓腳本存好之前的所有指令都被擋下，最小腳本存檔後又要被完整版覆蓋。定稿改成「流程圖 → 判斷方式（精簡程式碼只說明原理）→ 建立腳本 → 設定 hook → 確認生效 → 實測紀錄」，並用流程圖與指令拆解圖取代結束碼表格與長段說明。（Claude Code Hooks 2026-11-04） | 同 8 | |
| 12 | `75b8314` | 例子 | **附給讀者的腳本只放讀者需要的規則：** 同一篇原本貼本站完整的 hook，混著刪除 `draft`、在 main 上 commit 與 `gh pr merge` 這些發佈流程專用的規則，讀者要自己刪掉才能用。定稿的文章腳本只留推送相關的判斷，另外在隔離環境重新實測，本站專用規則用一句話帶過。（Claude Code Hooks 2026-11-04） | 同 9 | |
| 13 | `c727145` | 規則（起稿格式說明） | 這幾條是作者定稿時最常動手改的地方（2026-11 的 Paper、hooks、MOSS-Image、ComfyUI 共用模型），起稿就照這個格式寫，不等作者改。對照例子在 writing-style 第 5 節「起稿格式對照」。 | — | 說明句 |
| 14 | `c727145` | 規則（起稿格式 1） | 開頭段與 `summary` 依序寫：主角是什麼、讀者為什麼要用它，讀者遇到的限制與原因，照做後的結果。不用步驟、要求或「最短做法」開場。 | 未涵蓋（有衝突） | 和核心規則 2「先給答案」、`article.md`「第一段直接回答讀者來找的問題」順序不同 |
| 15 | `c727145` | 規則（起稿格式 2） | 句子補齊主詞、受詞與「會、則、也、才」，分句用「如果……就」「即使……也」「雖然……但」「而」接起來，讀者也會做的事用「我們」當主詞。口語動補展開成完整動詞，例如「開不了」寫成「無法開啟」、「字都寫對」寫成「模型有生成正確的文字」，但不換成「採用」這類書面腔。 | 部分（有衝突） | 補齊助詞＝核心規則 1；「我們」＝`article.md` 人稱；口語動補沒寫；多用連接詞和「組法」第 3 條相反 |
| 16 | `c727145` | 規則（起稿格式 3） | 每個操作先回答讀者照做時會擔心的事：哪些東西不用動、哪些不受影響、畫面上的警告要不要理會、出錯時怎麼還原。 | 未涵蓋 | |
| 17 | `c727145` | 規則（起稿格式 4） | 寫「要怎麼做」時，同一句接上讀者看得到的效果，例如「名稱要一樣，模型才會出現在節點的選單」，不用工具內部怎麼判斷來解釋。 | 涵蓋 | `article.md`「結構」：理由寫讀者看得到的結果（Vite 例） |
| 18 | `c727145` | 規則（起稿格式 5） | 第一個出現的做法就是讀者要用的完整做法，較差做法的結果只在正確做法後面補充。小標或段首出現「先試」「最簡」「補上」「改用」時，代表寫成了演進式結構，要重排。 | 未涵蓋 | |
| 19 | `c727145` | 規則（起稿格式 6） | 每節起稿時就判斷要不要配圖：路徑對照、操作前後對照與分支流程畫成 SVG，程式或伺服器的輸出畫面用截圖，不先寫成表格或文字 log 等作者要求。 | 範圍外 | |
| 20 | `c727145` | 規則（起稿格式 7） | 每一步開頭承接上一步（「模型搬好後」「設定完成後」），一句有好幾個動作就拆成編號步驟，寫出讀者實際用的工具，結尾寫讀者看得到的成功訊號。 | 部分 | 成功訊號＝`article.md`「讓讀者能確認自己做對了」；段落推進有寫；「一句多動作拆成編號步驟」只有核心規則 9 的「步驟用條列」 |
| 21 | `c727145` | 規則（起稿格式 8） | 小標用名詞片語，例如「X 的流程」「確認 X」「產出的 X」，不寫主張句或比較動作。 | 涵蓋 | `article.md`「小標寫成名詞片語」、P22 |
| 22 | `c727145` | 規則（起稿格式 9） | 作者為了驗證布置的素材、版本與案例數放到「實測紀錄」，開頭與正文只寫讀者層級的結論，所有操作教學都適用。 | 部分 | `article.md` 環境與版本分開寫、實測紀錄是報告體 |
| 23 | `c727145` | 規則（改寫 #3） | 主標題對準核心查詢，內文小標專業、直接且同篇一致，每個小節承擔完整意思。標題冒號後寫讀者遇到的情境或在意的結果（例如「私有 repo 沒有分支保護時」「資料完整保留」），不寫機制名稱、檔名與版本號，也不寫「效能最佳化」這類日後可能被超越而要改標題的評價。 | 部分 | 檔名、版本已涵蓋；機制名稱與會過時的評價沒寫 |
| 24 | `c727145` | 規則（改寫總結） | 結尾固定用「總結」，最多三句。評測或作品介紹可以在後面接「優點」「缺點」「尚未驗證」三行條列。教學與技術紀錄的總結只用陳述句，第一句用概念寫出讀者要做的關鍵動作（不寫路徑與版本），第二句寫實測結果，不接條列、不寫優缺點，也不重述正文已交代的限制。 | 部分 | 不重述＝`article.md`、P17；「第一句概念、不寫路徑與版本」沒寫；固定「總結」與三句是 vervecode 專屬 |
| 25 | `c727145` | 例子 | 「起稿格式對照」表（17 列初稿 → 定稿），例如「Agent 改掉它，下一次檢查就跟著失效」→「如果 Agent 修改了這支腳本，之後的檢查也會跟著失效」、「先試最簡單的做法……」→「只用 Prompt 描述版面」。 | — | 例子，對應 #14～#24 |

`c727145` 同時刪掉三條舊規則，內容併進起稿格式：「操作教學照讀者操作的順序直接寫正確做法……」（併入 #18）、「描述結果寫成主詞、動作完整的書面說法……」（併入 #15）、「開頭的概念從讀者的操作與目標說……」（併入 #14 與 #17）。`915f0b7` 刪掉 writing-style 一列已退役 vault 草稿的參考，和文風無關。

去重後的偏好共 15 條：#1、#3＋#23、#4＋#19、#8、#9、#7＋#10＋#15 的句子補齊、#14、#15 的連接詞與口語動補、#16、#17、#18、#20、#21、#22、#24。

- 涵蓋：3 條（話要寫完整、同一句接上效果、小標用名詞片語）。
- 部分：6 條（標題、句子補齊之外的連接詞與口語動補、承接與編號步驟、驗證素材放實測紀錄、總結第一句、官方做法為主）。
- 未涵蓋：4 條（開頭順序、讀者的擔心、演進式結構與錯誤示範放後、小節照操作順序）。
- 範圍外：2 條（配圖、附給讀者的腳本內容）。

### 7.2 今天其他 commit 裡的偏好（`docs(content)` 前綴，MOSS-Image）

不在 `docs(articles)` 裡，但同樣是今天作者對 AI 稿的明確意見。

| commit | 原文（規則句） | baihua |
| --- | --- | --- |
| `c4e84bd` | 部落格文章用直述句寫讀者要做的事與看到的結果，不用論文的論證鋪陳，例如「先試最簡單的做法」、用「卻」帶出問題，再用「想要……就要改用」推到下一節。 | 未涵蓋（C2） |
| `c4e84bd` | 操作教學照讀者操作的順序直接寫正確做法。錯誤設定或較差做法的結果只在該主題的正確做法後面補充，不先做錯誤示範再推到正確做法。 | 未涵蓋（C1，後來併入起稿格式 5） |
| `c4e84bd` | 「開發過程」一節改成「讀者照著做的安裝或操作教學即使由 AI 實測，也不寫這一節」 | 範圍外 |
| `85421e2` | 介面沒有翻譯的選項照原文寫在「」裡稱呼，不自創中文名稱，也不把介面名稱放進括號當補充。 | 部分（C4） |
| `ab37481` | 「只寫範圍內的任務」例子補上 MOSS-Image 的手寫便條測試是冗餘資料。 | 涵蓋（`article.md`「內容取捨」旁支刪掉） |
| `55c53f9` | 描述結果寫成主詞、動作完整的書面說法，例如「字都寫對」改成「模型有生成正確的文字」，口語動詞片語不適合部落格正文。 | 未涵蓋（C3；後來併入起稿格式 2） |
| `55c53f9` | `summary`……語氣與節奏跟第一段一致，用「只要……就」「透過」「且」這類連接詞交代分句的關係，不用一連串逗號堆短分句。 | 部分（P06 涵蓋逗號；多用連接詞和「組法」第 3 條相反） |

---

## 8. 公開狀態（參考）

作者已同意這些內容都能放進公開題庫，這一節只留紀錄。正式站與 preview 都用 `npm run build`，`src/lib/pages.ts` 只在 dev 模式加 `VERVECODE_INCLUDE_DRAFTS=1` 時輸出草稿，所以 `draft: true` 的版本從未出現在公開網址；今天的候選裡，只有 C3 的原文（MOSS-Image `6e79593` 的 summary）在 PR #92（01:29）到 PR #93（10:18）之間公開過。E1、E2 的初稿也都是 `draft: true`，沒有公開過。

## 9. 判斷時的不確定之處

1. 歷史只挖到兩篇：看過 2026-10-26 之後有改稿紀錄的 deny 規則、雙投影機、Whetstone、StreamTurbo、Pi、CLIProxyAPI、ComfyUI MCP 與 ComfyUI 共用模型，再往前沒有看。Whetstone、Jev API、Unity、td-cli、ComfyUI 共用模型已經有題目進了 baihua 題庫（例如 `audience-sentence-in-summary`、`comma-chopped-lede`、`mechanism-first-paragraph`），所以沒有再挑；雙投影機的改動多半是刪掉模擬數據這類內容取捨；10-27 的「修正文風與 AI 寫作痕跡」三個 commit 每篇只改一兩句，題庫也已經收過幾題；10-03 那批「重寫……草稿」是 AI 重寫舊文，方向相反，所以都沒採用。
2. 誰改的字：commit 都由作者帳號送出並附 `Co-Authored-By: Claude`。只有 MOSS-Image 第一段與 hooks summary 有紀錄寫明是作者親手改（`src-hand`），其他是作者指示、AI 改寫（`src-directed`）。對話裡的退回與 git 外的修改輪次看不到；MOSS-Image 的第一版草稿沒有 commit，PyTorch 起稿前有沒有退回也不知道。
3. 發佈版和 baihua 規則衝突：作者接受的文字有被動句（「不會被執行」「就會被漏掉」）、較多連接詞（「而」「則」「因此」「此外」「不過」）、書面的「此模型」與評價「品質頗高」。grader 不能因為這些判 FAIL；baihua 是否要放寬「組法」第 3 條、核心規則 6 與 P25，要作者決定。
4. 起稿格式第 1 條（主角是什麼 → 為什麼用 → 限制 → 結果）和 baihua「先給答案」的順序不同。A1、B1、C5 都靠這條，規則沒定之前，這幾題的 PASS 條件會和 skill 互相矛盾。
5. 有些作者偏好是內容或版面的決定（配圖、腳本內容、官方做法為主），依 SKILL.md 的優先順序屬於專案文風檔，不一定該進 baihua。
6. 事實和文字一起改：hooks 限制段拿掉 `env git`、加上 git alias；開頭拿掉子代理；Paper 的啟動秒數移到實測紀錄；MOSS-Image 的裁切數字改了。PASS 條件以初稿的事實為準，要在 grader 寫明哪些刪除不算錯。
7. regex 的 `match: contains`：題庫現有的 regex grader 全部用 `not_contains`，`contains` 能不能用要先確認；不能用的話，必須保留的事實改寫進 llm grader（像 `mechanism-first-paragraph/graders/facts-kept.md`）。
8. B3 的「防的是判斷錯誤，不是刻意繞過」可能是合理的範圍說明（P02 的保留條件），作者是整篇重寫時一起刪的，沒有針對這句的評語。

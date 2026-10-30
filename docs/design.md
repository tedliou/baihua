# 設計說明

這份文件說明 zh-tw-prose 為什麼這樣設計，給想修改規則或貢獻的人讀。規則參考了哪些來源見 [sources.md](sources.md)，修改後怎麼驗證見文末。

## 範圍

skill 只決定句子怎麼寫：句法、語氣、用詞、標點與段落組織。要寫什麼內容、術語叫什麼、畫面怎麼排，交給使用者、專案文件與其他 skill。這個切分讓它可以和介面設計、遊戲文案、技術文件等領域 skill 同時使用，不會互相搶決定權。

## 三層結構

```
SKILL.md            核心規則、語域要點、檢查清單，觸發時載入
references/         依需要讀取
  registers/*.md    六種語域的寫法
  patterns.md       AI 腔模式 P01–P25
  translationese.md 翻譯腔 T01–T10
  taiwan-usage.md   台灣用語對照，check.py 也讀這張表
  punctuation.md    標點與空格
  integrity.md      內容誠實
  review.md         審稿交辦
  learning.md       把使用者的修改整理成偏好
scripts/check.py    機械檢查
```

上面是 `skills/zh-tw-prose/` 的內容，也就是上傳到 claude.ai 的部分。repo 根目錄另有審稿子代理 `agents/`、常駐片段 `snippets/` 與測試案例 `evals/`，它們不在 skill 資料夾裡。

SKILL.md 控制在 5,000 token 以內，因為 Claude Code 在對話壓縮後只保留每個 skill 的前 5,000 token（token 是模型計算文字長度的單位，見 [Claude Code skills 文件](https://code.claude.com/docs/en/skills)）。

哪些內容放 SKILL.md，依「作答當下會不會用到」決定。2026-10-28 的 eval 檢查了 20 次潤稿與改寫：每次都有載入 skill，但沒有一次讀過 references，模型載入 skill 後就直接作答。所以改稿時每一句都要對照的東西放在 SKILL.md：

- 檢查清單：每一類問題的常見寫法、處理方式與保留條件，各一行。
- 語域表：每種語域最重要的兩三條規則。

references 放完整說明、前後例與長文才需要的細節，例如文章的開頭與結構、介面文字的各種元件。SKILL.md 寫明寫整篇文章或整份文件時才讀這些檔案。

SKILL.md 直接連到每一個 references 檔，Claude 從 SKILL.md 一步就能找到需要的檔案。references 之間也有幾處互相指引，例如 patterns.md 指向 translationese.md，但被指到的檔案都能從 SKILL.md 直接找到，不依賴這些連結。

## 句子的組法

核心規則與檢查清單處理用詞與語氣，「中文句子的組法」處理句子的骨架：主詞何時省略、分句的順序、連接詞與名詞前修飾的長度。研究顯示模型的中文和英譯中的文字一樣，代名詞、連接詞與「名詞＋的」修飾都比母語中文多，這些是句法層次的偏差，換詞改不掉。這一節用正面的「怎麼寫」表述，不列禁止的說法，理由與文獻見 [theory.md](theory.md)，實驗見 `experiments/2026-10-30-syntax/`。

## 規則的寫法

每條規則都附理由。模型遇到規則沒想到的情況時，可以依理由判斷，而不是硬套字面。patterns.md 與 translationese.md 的每個模式由這幾部分組成：

1. 模式：一句話描述。
2. 理由：讀者為什麼會覺得不自然。
3. 改法：怎麼改。
4. 前後例：自己寫的例句，多數模式有。
5. 保留：什麼時候這個寫法是對的。

保留條件很重要。只列禁止事項的規則會讓模型過度改寫，把讀者真的有誤解時才用的「不是 A 而是 B」也改掉。所以每個模式都寫了保留條件，SKILL.md 的檢查清單也有「保留」欄。evals 裡標了 `false-positive` 的案例專門檢查這件事。

但漏改和過度改寫一樣常見。用真實改稿案例測試時，模型被要求「潤稿」，常常只修標點與用字，留下先下評語的開頭、沒有依據的評價與說教句。所以 SKILL.md 的改稿步驟是先逐句對照清單、找出要處理的句子，再用保留條件排除對的寫法，而不是先假設文字沒問題。清單的例句刻意不用 eval 題庫裡的原句，讓題庫能檢查規則有沒有類推到沒看過的寫法。

## 優先順序

```
使用者這次的指示
  > 專案文風檔與用詞表
    > 其他 skill 的領域規定
      > 本 skill 的語域
        > 本 skill 的核心規則
```

本 skill 排在最後，因為它的規則是通用預設。分號、破折號、空格這類偏好都可以由專案或使用者覆寫。check.py 的分號與空格檢查有開關（`--allow-semicolon`、`--no-spacing`），破折號只列為 warning，不影響結束碼。

## 機械檢查與審稿分工

字串能判斷的事交給 check.py：對岸用語、半形標點、引號、刪節號、中英文空格、分號。句型與語氣需要讀懂上下文，交給模型自己檢查，長文再交給沒看過寫作過程的審稿子代理。check.py 只用 Python 標準函式庫，因為 skill 可能在 claude.ai 的沙盒裡執行，無法安裝套件。

AI 腔片語在 check.py 裡只是 warning。同一個片語在不同語境可能是對的，硬性禁止會誤傷。

## 觸發範圍

description 列出會用到的文字類型，也列出不使用的情況：一般問答、簡體中文或給中國大陸讀者的文字、英文寫作與英譯、寫程式（含程式碼註解）、版面設計。排除一般問答是刻意的選擇，因為每次中文對話都載入 skill 會浪費 context。想讓對話回覆也套用原則的人，可以把 repo 根目錄的 `snippets/claude-md.md` 貼進 CLAUDE.md。

## 可攜性

frontmatter 是 SKILL.md 開頭的設定區塊。這裡只用 Agent Skills 規格的欄位（name、description、license、metadata），不用 Claude Code 專屬欄位，讓同一個資料夾能上傳到 claude.ai 與 Claude API。

description 控制在 200 字元以內。Agent Skills 規格的上限是 1,024 字元，但 claude.ai 說明中心寫的上限是 200 字元，取兩者中較嚴的一個。

## 修改與驗證

- 改 `taiwan-usage.md`：check.py 執行時直接讀這張表，不需要改程式。「檢查」欄為「是」的列才會被標出，「例外」欄列出包含該字串但正確的詞。改完跑 `python -m unittest discover -s tests`。
- 改 SKILL.md 或 references：跑行為 eval，比較修改前後的分數。
- 改 description：跑觸發 eval，確認該載入時載入、不該載入時不載入。

eval 是用 `claude plugin eval` 實際呼叫模型的測試，案例、跑法與最新結果見 [evals/README.md](../evals/README.md)。

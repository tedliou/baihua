# 設計說明

這份文件說明 zh-tw-prose 為什麼這樣設計，給想修改規則或貢獻的人讀。

## 範圍

skill 只決定句子怎麼寫：句法、語氣、用詞、標點與段落組織。要寫什麼內容、術語叫什麼、畫面怎麼排，交給使用者、專案文件與其他 skill。這個切分讓它可以和介面設計、遊戲文案、技術文件等領域 skill 同時使用，不會互相搶決定權。

## 三層結構

```
SKILL.md            核心規則，每次載入（約 2,800 字）
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

SKILL.md 保持精簡，因為 Claude Code 在對話壓縮後只保留每個 skill 的前 5,000 token。細節放在 references，只在需要時讀。references 只連一層，不從 references 再連到別的 references。

## 規則的寫法

每條規則都附理由。模型遇到規則沒想到的情況時，可以依理由判斷，而不是硬套字面。每個模式都寫成四部分：

1. 模式：一句話描述。
2. 理由：讀者為什麼會覺得不自然。
3. 前後例：自己寫的例句。
4. 保留：什麼時候這個寫法是對的。

第 4 部分最重要。只列禁止事項的規則會讓模型過度改寫，把正確的「不是 A 而是 B」也改掉。

## 優先順序

```
使用者這次的指示
  > 專案文風檔與用詞表
    > 其他 skill 的領域規定
      > 本 skill 的語域
        > 本 skill 的核心規則
```

本 skill 排在最後，因為它的規則是通用預設。分號、破折號、空格這類偏好都可以由專案或使用者覆寫，check.py 也提供對應的開關。

## 機械檢查與審稿分工

字串能判斷的事交給 check.py：對岸用語、半形標點、引號、刪節號、中英文空格、分號。句型與語氣需要讀懂上下文，交給模型自己檢查，長文再交給沒看過寫作過程的審稿子代理。check.py 只用 Python 標準函式庫，因為 skill 可能在 claude.ai 的沙盒裡執行，無法安裝套件。

AI 腔片語在 check.py 裡只是 warning。同一個片語在不同語境可能是對的，硬性禁止會誤傷。

## 觸發範圍

description 列出會用到的文字類型，也列出不使用的情況：一般問答、簡體中文、英文寫作、翻譯成英文、程式碼本身與版面設計。排除一般問答是刻意的選擇，因為每次中文對話都載入 skill 會浪費 context。想讓對話回覆也套用原則的人，可以把 `snippets/claude-md.md` 貼進 CLAUDE.md。

## 可攜性

frontmatter 只用 Agent Skills 規格的欄位（name、description、license、metadata），不用 Claude Code 專屬欄位，讓同一個資料夾能上傳到 claude.ai 與 Claude API。description 的前 200 字自成一段完整說明，因為 claude.ai 只顯示前 200 字。

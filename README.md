# 白話 baihua

[English](README.en.md)

讓 Claude 寫出台灣讀者讀得順的正體中文。`zh-tw-prose` 是一個 skill，也就是 Claude 在需要時才載入的一組指示。Claude 寫文章、文件、介面文案、公告與 PR 時會載入它，避開 AI 腔、翻譯腔與對岸用語，把句子寫完整、先給答案。

## 改寫前後

AI 腔，改寫前：

> 在當今快速發展的數位時代，持續整合扮演著至關重要的角色。我們導入了全新的建置快取機制，這不僅大幅提升了開發效率，更標誌著工程文化的全新里程碑。

改寫後：

> 我們在 CI 加上建置快取，建置時間從 90 秒降到 20 秒。

翻譯腔，改寫前：

> 在對設定檔進行修改之後，系統將會針對所有服務作出重新啟動的動作。

改寫後：

> 改完設定檔，系統會重新啟動所有服務。

電報式短句，改寫前：

> 設定完成。重啟生效。失敗查 log。

改寫後：

> 設定完成後要重新啟動才會生效。如果啟動失敗，先查看 log 裡的錯誤訊息。

## 功能

- 10 條核心規則，每條附理由，讓 Claude 在規則沒寫到的情況下也能判斷。
- 6 種語域：技術文章、參考文件、介面文字、工作報告、社群貼文、正式文件。
- 25 個 AI 腔模式與 10 個翻譯腔模式，每個都寫明理由、改法、前後例，以及什麼情況要保留，避免把好文字改壞。
- 台灣用語對照表，以及只用 Python 標準函式庫的檢查腳本 `check.py`。
- 審稿子代理 `zh-tw-reviewer`，以沒看過寫作過程的角度讀全文。

它只決定句子怎麼寫。寫什麼內容、術語叫什麼、畫面怎麼排，由你、你的專案文件與其他 skill 決定，所以可以和介面設計、遊戲文案、技術文件等 skill 一起用。

## 安裝

### Claude Code

```text
/plugin marketplace add tedliou/baihua
/plugin install baihua@baihua
```

安裝後 skill 與審稿子代理都會啟用。plugin 是 Claude Code 的擴充套件格式，可以同時裝好 skill 與子代理。

### claude.ai

從 [Releases](https://github.com/tedliou/baihua/releases) 下載 `zh-tw-prose.zip`，在 claude.ai 的設定頁上傳。claude.ai 要先開啟程式碼執行功能才能使用 skill。

### Claude API

把 `skills/zh-tw-prose` 資料夾以 Skills API 上傳，做法見 [Agent Skills 文件](https://platform.claude.com/docs/en/build-with-claude/skills-guide)。

### 直接連結（開發本專案時）

```bash
git clone https://github.com/tedliou/baihua.git
cd baihua
bash scripts/link.sh
```

Windows 用 `pwsh scripts/link.ps1`。腳本把 skill 連結到 `~/.claude/skills`，改 repo 裡的 skill 會立刻生效。審稿子代理在 macOS 與 Linux 是連結，在 Windows 是複製，所以 Windows 上改了 `agents/` 要重跑一次腳本。

## 使用

不需要特別指令。請 Claude 寫或改中文文章、README、錯誤訊息、公告時，skill 會自動載入。也可以用 `/zh-tw-prose` 直接呼叫。

一般問答、簡體中文、英文寫作與寫程式時不會載入。想讓平常的對話回覆也照同樣原則寫，把 [snippets/claude-md.md](snippets/claude-md.md) 的片段貼進 `CLAUDE.md`。這段不含空白約 380 字，每個 session 都會載入。

檢查腳本也可以單獨用，需要 Python 3.9 以上，不必安裝其他套件：

```bash
python skills/zh-tw-prose/scripts/check.py docs/*.md
python skills/zh-tw-prose/scripts/check.py README.md --glossary GLOSSARY.md
```

| 選項 | 作用 |
| --- | --- |
| `--glossary <檔案>` | 讀專案用詞表的「不要用」欄 |
| `--allow-semicolon` | 允許分號 |
| `--no-spacing` | 不檢查中英文之間的空格 |
| `--no-hints` | 不顯示 AI 腔片語提示 |
| `--strict` | 提示也視為錯誤 |
| `--markdown` | 從標準輸入讀取時，當成 Markdown 處理 |

## 專案設定

規則衝突時依這個順序：你這次的指示、專案的文風檔與用詞表、其他 skill 的領域規定、本 skill 的語域、本 skill 的核心規則。

所以分號、破折號、中英文空格這類偏好，都可以在專案的 `CLAUDE.md` 寫一句覆寫。專案有 `GLOSSARY.md` 時，Claude 會以它的術語為準。

## 測試

每次修改都用 `claude plugin eval` 跑 33 個案例：17 個行為案例比較有 skill 與沒有 skill 的分數，16 個觸發案例確認該載入時載入、不該載入時不載入。行為案例中有 5 個專門檢查過度改寫，例如讀者真的有誤解時的更正句、服務條款的法律用語、真正並列的清單。做法與最新結果見 [evals/README.md](evals/README.md)。

## 限制

- skill 降低 AI 腔，不保證文字看不出 AI 參與，也不是用來規避 AI 偵測。
- `check.py` 只查字串。句型與語氣仍靠模型判斷，長文建議再請人讀一次。
- 用語對照以資訊與日常用語為主，專業領域的用詞請以專案用詞表補充。

## 貢獻

新的模式、誤判回報與用語對照都歡迎，請先讀 [CONTRIBUTING.md](CONTRIBUTING.md)。設計理由見 [docs/design.md](docs/design.md)，參考來源見 [docs/sources.md](docs/sources.md)。

## 授權

MIT。用語對照部分參考 OpenCC（Apache-2.0），見 [NOTICE](NOTICE)。

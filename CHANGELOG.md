# 變更紀錄

格式參考 Keep a Changelog，版本號遵循語意化版本。

## [未發佈]

### 修改

- description 縮短到 200 字元以內，符合 claude.ai 說明中心寫的上限。
- 整理 README、貢獻指南、設計說明、參考來源、eval 說明、常駐片段與 issue 範本的文字，修正與實際檔案不符的描述。

## [0.1.0] - 2026-10-28

### 新增

- `zh-tw-prose` skill：10 條核心規則與 6 種語域。
- 參考檔：AI 腔模式 P01–P25、翻譯腔 T01–T10、台灣用語對照、標點、內容誠實、審稿與偏好學習。
- `scripts/check.py`：檢查對岸用語、標點、引號、刪節號、中英文空格與分號，可以讀專案用詞表。
- `zh-tw-reviewer` 審稿子代理與常駐片段 `snippets/claude-md.md`。
- 28 個 eval 案例，也就是用 `claude plugin eval` 實際呼叫模型的測試：12 個行為案例與 16 個觸發案例。

### 已知問題

- 改稿時偶爾會把沒有錯的口語詞換成正式說法，見 [evals/README.md](evals/README.md)。
- 25 個 AI 腔模式中只有 7 個寫了保留條件，翻譯腔模式還沒有。

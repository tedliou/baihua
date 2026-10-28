# 變更紀錄

格式參考 Keep a Changelog，版本號遵循語意化版本。

## [未發佈]

### 新增

- AI 腔模式 P01–P25 與翻譯腔 T01–T10 全部補上理由、前後例與保留條件。
- SKILL.md 的改稿規則加上「先對照保留條件」。
- 5 個 eval 案例：讀者真的有誤解時的更正句、服務條款的法律用語、安全警告與不幸的被動句、真正並列的清單，以及翻譯腔改寫。

- 抽考題庫 `eval-bank/`：35 題，其中 29 題取自真實改稿案例。發 release 前每次抽 8 題，每個類別至少 1 題。
- `scripts/eval.py`：依四層執行 eval、合併私有題庫，並和 `evals/baseline.json` 比較，找出退化的題目。
- `tests/test_structure.py`：不花額度的結構檢查，涵蓋模式欄位、description 長度與題目格式。

### 修改

- eval 只用 Sonnet 執行。固定題從 17 題減為 10 題，其餘移到題庫。觸發題只給 1 回合。沒有 skill 的對照組只在換模型版本時跑。
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

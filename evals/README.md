# Eval

這裡的案例用 `claude plugin eval` 執行，確認 skill 有幫助、會在該用的時候載入，而且修改後不退化。

## 案例

| 標籤 | 數量 | 檢查什麼 |
| --- | --- | --- |
| `behavior` | 17 | 寫出或改出的文字是否符合規則。每個案例同時跑有 skill 與沒有 skill 兩組，比較分數差（Δ）。 |
| `trigger` | 16 | 該用的請求會載入 skill（8 個），不該用的請求不會載入（8 個）。 |

行為案例的評分分兩種：

- regex：檢查 AI 腔片語、假對比、對岸用語、半形標點、中英文空格、emoji，以及必須保留的事實。
- llm：由評審模型依案例寫明的 PASS／FAIL 條件判斷，三票取多數。

標了 `false-positive` 的 5 個案例專門檢查過度改寫：`keep-good-text`（自然的段落）、`keep-real-correction`（讀者真的有誤解時的更正句）、`keep-formal-terms`（服務條款的法律用語）、`keep-warning-and-passive`（寫出後果的警告與不幸的被動句）、`keep-real-list`（真正並列的清單）。另外 `condense-keep-complete` 檢查精簡時不刪掉助詞。

## 執行

```bash
# 行為：有 skill 與沒有 skill 各跑兩次
claude plugin eval . --tag behavior --runs 2 --judge-model sonnet -j 4

# 觸發：只跑有 skill 的一組
claude plugin eval . --tag trigger --ablation none --runs 3 -j 4
```

結果寫到 `evals/results/<時間>/`，這個資料夾不進版本控制。eval 會實際呼叫模型並產生費用。2026-10-28 用上面的指令跑一次，行為測試約 4 美元，觸發測試約 3.8 美元。

## 修改 skill 時

1. 修改前先跑一次，記下各案例分數。
2. 修改後再跑一次。任何案例的 with 分數下降，或觸發案例出現誤觸發，都要先查原因再合併。
3. 新規則要附對應案例，至少一個「該改」與一個「不該改」。

## 最新結果

2026-10-28，Claude Code 2.1.309，預設模型，評審模型 Sonnet，每組跑 3 次。「修改前」是 v0.1.0 的 skill 跑同一套案例。

每次執行的分數是通過的評分項目占全部項目的比例，介於 0 與 1。表中是各次執行的平均，Δ 是有 skill 減沒有 skill。

| 案例 | 修改前（有 skill） | 有 skill | 沒有 skill |
| --- | --- | --- | --- |
| compose-with-glossary | 0.94 | 1.00 | 1.00 |
| condense-keep-complete | 1.00 | 0.96 | 0.93 |
| fix-translationese | 1.00 | 1.00 | 1.00 |
| keep-formal-terms | 1.00 | 1.00 | 1.00 |
| keep-good-text | 1.00 | 1.00 | 0.50 |
| keep-real-correction | 0.92 | 1.00 | 1.00 |
| keep-real-list | 1.00 | 1.00 | 0.93 |
| keep-warning-and-passive | 0.92 | 1.00 | 0.88 |
| localize-mainland-terms | 1.00 | 1.00 | 1.00 |
| no-fabrication | 1.00 | 1.00 | 0.96 |
| rewrite-ai-paragraph | 0.93 | 1.00 | 0.90 |
| write-article-intro | 0.93 | 1.00 | 0.63 |
| write-maintenance-notice | 1.00 | 1.00 | 0.67 |
| write-pr-description | 0.94 | 0.94 | 0.83 |
| write-readme-intro | 0.86 | 1.00 | 0.86 |
| write-social-post | 1.00 | 1.00 | 0.72 |
| write-ui-errors | 1.00 | 1.00 | 1.00 |

平均 Δ 從修改前的 +0.08 升到 +0.12。觸發案例在預設模型與 Sonnet 上 48 次全部正確。Haiku 每案跑 5 次，介面文案、公告與在地化各有 1 到 2 次沒有載入 skill。

已知問題：

- Sonnet 的行為測試這次沒有跑完整，結果待補。
- Haiku 對短文案的觸發不穩定。

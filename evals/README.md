# Eval

這裡的案例用 `claude plugin eval` 執行，確認 skill 有幫助、會在該用的時候載入，而且修改後不退化。

## 案例

| 標籤 | 數量 | 檢查什麼 |
| --- | --- | --- |
| `behavior` | 12 | 寫出或改出的文字是否符合規則。每個案例同時跑有 skill 與沒有 skill 兩組，比較分數差（Δ）。 |
| `trigger` | 16 | 該用的請求會載入 skill（8 個），不該用的請求不會載入（8 個）。 |

行為案例的評分分兩種：

- regex：檢查 AI 腔片語、假對比、對岸用語、半形標點、中英文空格、emoji，以及必須保留的事實。
- llm：由評審模型依案例寫明的 PASS／FAIL 條件判斷，三票取多數。

`keep-good-text` 與 `condense-keep-complete` 專門檢查過度改寫：好的文字不該被大改，精簡時不該刪掉助詞。

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

2026-10-28，Claude Code 2.1.309，評審模型 Sonnet。行為案例每組跑 2 次，觸發案例跑 3 次。

每次執行的分數是通過的評分項目占全部項目的比例，介於 0 與 1。表中是同一組各次執行的平均，Δ 是有 skill 減沒有 skill。

| 案例 | 有 skill | 沒有 skill | Δ |
| --- | --- | --- | --- |
| write-article-intro | 1.00 | 0.67 | +0.33 |
| write-maintenance-notice | 1.00 | 0.67 | +0.33 |
| keep-good-text | 0.83 | 0.50 | +0.33 |
| write-pr-description | 1.00 | 0.83 | +0.17 |
| write-social-post | 1.00 | 0.83 | +0.17 |
| no-fabrication | 1.00 | 1.00 | 0.00 |
| localize-mainland-terms | 1.00 | 1.00 | 0.00 |
| write-ui-errors | 1.00 | 1.00 | 0.00 |
| condense-keep-complete | 1.00 | 1.00 | 0.00 |
| write-readme-intro | 0.93 | 0.93 | 0.00 |
| rewrite-ai-paragraph | 0.90 | 0.90 | 0.00 |
| compose-with-glossary | 0.92 | 1.00 | -0.08 |

觸發案例 16 個全部通過：8 個該用的請求每次都載入 skill，8 個不該用的請求一次都沒有載入。

Δ 為 0 的案例，兩組分數相同，skill 在這些案例沒有造成差異，留著當回歸測試。

已知問題：

- `compose-with-glossary`：有 skill 的一次執行中，`ui-quality` 評分項目的三位評審 1 票通過、2 票不通過，這次得 0.83，平均成 0.92。下次修改後如果同一項目再次不通過，就要查原因。
- `keep-good-text`：有 skill 的兩次執行中，有一次把原文的「八成」改成「多半」，是目前已知的過度改寫。

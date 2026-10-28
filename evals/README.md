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

結果寫到 `evals/results/<時間>/`，這個資料夾不進版本控制。eval 會實際呼叫模型並產生費用，一次完整的行為測試約 4 美元。

## 修改 skill 時

1. 修改前先跑一次，記下各案例分數。
2. 修改後再跑一次。任何案例的 with 分數下降，或觸發案例出現誤觸發，都要先查原因再合併。
3. 新規則要附對應案例，至少一個「該改」與一個「不該改」。

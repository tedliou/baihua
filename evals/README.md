# Eval

eval 只測一件事：給 skill 一段明顯是 AI 寫的文字，它能不能改成像人寫的。每題用 `claude plugin eval` 實際呼叫模型，題目開頭寫明「使用 zh-tw-prose skill。」，照實際用法由使用者或其他 skill 指名呼叫。只跑有 skill 的一組。

## 題目

`eval-bank/` 有 33 題，2026-11-04 由作者逐題複審收錄（紀錄在 `experiments/2026-11-04-bank-review/`）：

- 21 題取自過去的改稿案例，涵蓋技術文章、wiki、技術文件與遊戲介面字串。
- 12 題取自作者部落格 vervecode.dev 的改稿紀錄：AI 寫的初稿，經作者要求大改後發佈。這 12 題的 `reference.md` 放作者發佈的版本，給人對照，不會送給模型，也不參與評分。

每題的標籤：

- 類別，三選一：`ai-flavor`（AI 腔）、`translationese`（翻譯腔）、`core-rule`（核心規則）。
- 來源，四選一：`src-hand` 是作者親手改的文字，`src-directed` 是作者指示後改寫、經作者認可的文字，`src-self` 是依規則自查修改的文字，`src-synthetic` 是自己寫的示範題。
- `no-spacing`：介面字串，中英文之間本來不加空格，不套用空格檢查。
- `keep-punct`：題目要求保留原文的標點，不套用標點檢查。

## 評分

- 共用評分表 `eval-bank/_common/graders/author-rubric.md`：整理自作者審閱改寫結果時的判斷，例如不指導讀者、不過於口語、詞寫完整、標題寫成「主題：結果」、開頭先交代問題。由評審模型三票取多數，權重 3。
- 各題的 regex：檢查必須保留的事實與不得出現的寫法。
- 共用的機械檢查：emoji、對岸用語、半形標點與中英文空格。

共用評分表用作者的判斷校準過，見 `experiments/2026-11-05-grader-calibration/`。原本各題自己的 llm 評分條件和作者的 33 個判斷只有 15 題一致，改用共用評分表後一致 30 題。加上第二輪的判斷，66 筆一致 58 筆。評審模型仍不能代替作者，分數用來找出退化，改寫得好不好最後由作者審閱。

## 跑法

```bash
python scripts/eval.py L1 --case <題目…>    # 改 skill 時，只跑相關的題目
python scripts/eval.py L2                   # 發 release 前，跑全部題目
python scripts/eval.py L2 --update-baseline # 重建基準
python scripts/eval.py L2 --dry-run         # 只列出會跑哪些題目，不花額度
```

結果寫到 `eval-run/<時間>/`，這個資料夾不進版本控制：

- `outputs/<題目>.txt`：每題改寫後的文字，給人審閱。
- `outputs/_reads.json`：每題讀了哪些 references，以及讀了語域檔案的題目比例。
- `summary.json`：各題分數與費用。

所有分數都用 Sonnet 產生與評審。Haiku 評審會數錯中文字數，不採用。

## 退化的判斷

每題跑 1 次，分數和 `evals/baseline.json` 比較。有基準的題目平均下降 0.03 以上算退化，`eval.py` 會以非零狀態結束。單題分數在兩次執行之間可能差到 0.3，所以單題下降 0.17 以上只會列出來提醒。要確認某一題，用 `--case` 指定、加上 `--runs 3` 重跑。不要為了拉高單題分數去改 skill，規則要對沒看過的文字也成立。

## 人工審閱

分數只能抓明顯的退化，文字好不好由作者判斷。做法是單份審閱：每題只看一份輸出，選「通過」或「不通過」，不通過時寫意見或直接改字，再依意見找出根因修改 skill。審閱頁做成 claude.ai 上的 Artifact，判斷存在頁面的資料庫。歷次紀錄在 `experiments/` 下以日期開頭的資料夾。

原本的配對盲測（同一題有、無 skill 的兩份輸出排成 A、B 選一份）已經停用：兩份常常差不多、分不出好壞，也沒有「原文比較好」這個選項。

## 私有題庫

不能公開的真實案例放在 repo 之外，格式和 `eval-bank/` 相同，用 `--private <資料夾>` 合併進來。私有題的名稱前面會加上 `p-`，基準分數寫進該資料夾的 `baseline.json`。

資料夾裡可以放 `forbidden.txt`，一行一個字串。執行時如果公開題目出現這些字串，`eval.py` 會停下來，提醒先把題目移到私有題庫。

## 新增題目

1. 在 `eval-bank/<題目名稱>/` 建立 `prompt.md`。名稱描述問題，不寫專案名稱。原文要是明顯的 AI 文體。
2. `prompt.md` 放任務說明、判斷需要的上下文與原文，最後一行寫「只輸出成品本身，不要加任何說明、前言或改了什麼的清單。」不用寫「使用 zh-tw-prose skill」，`eval.py` 會加。
3. 必須保留的事實與不得出現的寫法，在 `graders/` 加 regex grader。regex 一律用 YAML 單引號，多行模式用 `flags: m`。改得好不好交給共用評分表。
4. 跑 `python -m unittest discover -s tests` 確認格式，再用 `python scripts/eval.py L1 --case <題目名稱> --update-baseline` 跑一次並寫入基準。

## 基準分數

BASELINE_TABLE

# 實驗：單份審閱

2026-11-03 開始。配對盲測常常出現兩份差不多、分不出好壞的情況，所以改成一次只看一份輸出：作者選「通過」或「不通過」，不通過時寫意見或直接改字。Claude 再依意見歸納問題、查證來源、找出根因，對症修改 skill。各版本的輸出隨機混在一起、不標來源，最後用通過率比較版本。

## 第一輪（r1）

- 題目：10 題，取自 `experiments/2026-10-30-syntax/tasks-set2.json`、`experiments/2026-10-30-human/` 的題目檔與 `eval-bank/`，清單在 `tasks-r1.json`，由 `scripts/build_tasks.py` 產生。
- 條件：cur 是 v0.3.2，用 `claude -p --model sonnet` 載入已安裝的 baihua plugin，允許 Read、Glob、Grep、Skill、Bash，和實際使用時一樣由模型自己決定要不要呼叫 skill。none 停用所有 skill、不給工具。每題每個條件各跑 1 次，Claude Code 2.1.317。
- 輸出：`outputs-r1/`。cur 另外存了 stream-json 的完整紀錄（`.jsonl`），可以查模型呼叫了哪些工具、讀了哪些檔案。
- 出題：12 張卡片。cur 5 張、none 5 張，第 11、12 張重複前面一張 cur 與一張 none 的輸出，當作檢查判斷一致性的錨點。卡片內容在 `rounds/r1-items.json`，審閱頁是 `review-page.html`，發佈成 claude.ai 上的 Artifact，判斷存在 Artifact 的資料庫。
- 對照表：`rounds/r1-key.json` 記錄每張卡片的條件。作者審完之前不要打開。

cur 的 10 次執行有 3 次沒有呼叫 skill：`h-rewrite-review`、`h-translate-guide`、`wiki-claim-left-to-discover`。這 3 題的 cur 輸出等於沒有 skill，所以出題時 cur 只從其他 7 題抽 5 題。

## 重跑

在 repo 根目錄執行：

```bash
python3 experiments/2026-11-03-review/scripts/build_tasks.py experiments/2026-11-03-review/tasks-r1.json
python3 experiments/2026-11-03-review/scripts/gen.py experiments/2026-11-03-review/tasks-r1.json experiments/2026-11-03-review/outputs-r1
```

已經存在的輸出會略過。`gen.py` 在輸出資料夾旁建立空的 `work/` 當執行目錄，這個資料夾不進版本控制。

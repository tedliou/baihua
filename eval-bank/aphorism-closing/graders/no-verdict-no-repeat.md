---
type: llm
weight: 1
---

原文：「VS Code + uv 的分工很清楚：uv 管 Python 版本、`.venv` 與套件，VS Code 只需要指向專案內的 `.venv`。建立專案用 `uv init --python 版本號`，加套件用 `uv add`，執行用 `uv run`，換電腦用 `uv sync`。只要 `pyproject.toml`、`uv.lock` 與 `.python-version` 跟著專案走，環境就能在任何一台電腦重建。」
開頭先下「分工很清楚」的評語再解釋；第二句把前文已經教過的四個指令又列了一遍，同一個資訊重複。
PASS if 「分工很清楚」這種先下評語的開頭已刪除，直接說明 uv 管什麼、VS Code 做什麼；沒有把 `uv init`、`uv add`、`uv run`、`uv sync` 四個指令再完整列一遍（只提 `uv sync` 作為換電腦的做法可以）；並保留這些事實：uv 管 Python 版本、`.venv` 與套件，VS Code 只需要指向專案內的 `.venv`，`pyproject.toml`、`uv.lock`、`.python-version` 跟著專案走時，環境可以在其他電腦重建。
FAIL if 仍以「分工很清楚」「各司其職」之類的評語開頭、仍把四個指令全部重列、刪掉上述任一事實，或加入原文沒有的事實。

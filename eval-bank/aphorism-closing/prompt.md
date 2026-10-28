---
description: "總結先下評語（「分工很清楚」），又把前文教過的四個指令再列一遍"
tags: [bank, ai-flavor, src-self]
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
---

幫我潤稿這篇 Python 環境教學的最後一段。文章前面已經分段教過建立專案用 `uv init`、加套件用 `uv add`、執行用 `uv run`、換電腦用 `uv sync`。

VS Code + uv 的分工很清楚：uv 管 Python 版本、`.venv` 與套件，VS Code 只需要指向專案內的 `.venv`。建立專案用 `uv init --python 版本號`，加套件用 `uv add`，執行用 `uv run`，換電腦用 `uv sync`。只要 `pyproject.toml`、`uv.lock` 與 `.python-version` 跟著專案走，環境就能在任何一台電腦重建。

只輸出成品本身，不要加任何說明、前言或改了什麼的清單。

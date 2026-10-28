# baihua

[正體中文](README.md)

baihua (白話, "plain speech") helps Claude write Traditional Chinese that reads naturally to Taiwanese readers. The `zh-tw-prose` skill loads when Claude writes or edits articles, docs, UI copy, announcements and PR descriptions in zh-TW. It removes AI-flavoured phrasing, translationese and Mainland Chinese terms, keeps sentences complete, and puts the answer first.

The skill itself is written in Chinese, because it is read by Claude while writing Chinese. This page is a short English summary.

## What is inside

- 10 core rules, each with its reason, so Claude can handle cases the rules do not cover.
- 6 registers: technical articles, reference docs, UI text, work reports, social posts, formal notices.
- 25 AI-writing patterns and 10 translationese patterns. Each has a before/after example and a "keep it when" boundary, so good text is not over-edited.
- A Taiwan usage table and `check.py`, a standard-library Python linter for terms, punctuation and CJK–Latin spacing.
- `zh-tw-reviewer`, a read-only reviewer subagent with a clean context.

The skill only decides how sentences are written. Content, terminology and layout belong to you, your project files and other skills, so it composes with UI, game-writing or documentation skills.

## Install

Claude Code:

```text
/plugin marketplace add tedliou/baihua
/plugin install baihua@baihua
```

claude.ai: download `zh-tw-prose.zip` from [Releases](https://github.com/tedliou/baihua/releases) and upload it under Settings → Capabilities → Skills.

Claude API: upload the `skills/zh-tw-prose` folder through the Skills API.

## Evals

33 cases run with `claude plugin eval`: 17 behaviour cases (5 of them check that good text is left alone) compare with-skill and without-skill scores, and 16 trigger cases check that the skill loads when it should and stays out otherwise. See [evals/README.md](evals/README.md).

## Limits

The skill reduces AI-flavoured writing. It does not promise that text is undetectable as AI-assisted, and it is not meant for evading AI detection.

## License

MIT. Part of the usage table draws on OpenCC (Apache-2.0); see [NOTICE](NOTICE).

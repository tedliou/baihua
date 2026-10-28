# 參考來源

規則參考了下列來源，分類對應 skill 裡的檔案。本專案沒有轉載這些來源的文字，所有例句都是為本專案寫的。

## 標點與排版（punctuation.md、check.py）

- 教育部《重訂標點符號手冊》修訂版：https://language.moe.gov.tw/001/Upload/FILES/SITE_CONTENT/M0001/HAU/shiou.pdf
- W3C《中文排版需求》（clreq）：https://www.w3.org/TR/clreq/
- 中文文案排版指北：https://github.com/sparanoid/chinese-copywriting-guidelines
- zhlint：https://github.com/Jinjiang/zhlint
- AutoCorrect：https://github.com/huacnlee/autocorrect

## 在地化與用語（taiwan-usage.md、registers/）

- Microsoft 正體中文風格指南：https://aka.ms/chinese-traditional-styleguide
- Mozilla 正體中文風格指南：https://mozilla-l10n.github.io/styleguides/zh-TW/
- Google 翻譯風格指南：https://developers.google.com/style/translation
- 台灣在地化社群翻譯風格指南：https://hackmd.io/@l10n-tw/translation_style_guide
- 國家教育研究院樂詞網：https://terms.naer.edu.tw/
- 教育部《重編國語辭典修訂本》：https://dict.revised.moe.edu.tw/
- OpenCC 台灣詞組表（TWPhrases，Apache-2.0）：https://github.com/BYVoid/OpenCC

## AI 腔與翻譯腔（patterns.md、translationese.md）

- Wikipedia: Signs of AI writing：https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- 維基百科：AI 生成文的特徵：https://zh.wikipedia.org/wiki/Wikipedia:AI%E7%94%9F%E6%88%90%E6%96%87%E7%9A%84%E7%89%B9%E5%BE%81
- 過度使用詞彙研究（llm-excess-vocab）：https://github.com/berenslab/llm-excess-vocab
- 余光中〈怎樣改進英式中文？——論中文的常態與變態〉，原載《明報月刊》1987 年，收入《中和西》。
- 思果《翻譯研究》。
- 中文 AI 腔整理：https://sspai.com/post/98169 、https://yage.ai/share/ai-chinese-translationese-20260418.html

## Skill 設計

- Agent Skills 規格：https://agentskills.io/specification
- Agent Skills 最佳實踐：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Claude Code skills：https://code.claude.com/docs/en/skills
- Plugin eval：https://code.claude.com/docs/en/plugin-evals
- Plugin marketplace：https://code.claude.com/docs/en/plugin-marketplaces

## 同類專案

下列專案以「改稿去 AI 味」為主，本專案參考了它們的模式清單，沒有直接採用。本專案的差異是在寫作當下套用、可以和領域 skill 組合，以及用 eval 檢查有沒有過度改寫好文字（見 [evals/README.md](../evals/README.md) 的 `keep-good-text` 案例）。

- https://github.com/blader/humanizer
- https://github.com/hardikpandya/stop-slop
- https://github.com/op7418/Humanizer-zh
- https://github.com/kevintsai1202/Humanizer-zh-TW
- https://github.com/acchuang/zh-tw-humanizer
- https://github.com/cashwu/humanizer-tw
- https://github.com/Raymondhou0917/speak-human-tw
- https://github.com/nagameTW/formosa-humanizer

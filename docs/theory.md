# 理論依據

這份文件說明 SKILL.md「中文句子的組法」五條規則與 check.py `--profile` 的學術依據。原本的規則多半來自風格指南與實務經驗，整理的是「看到什麼要改」。這五條補上的是另一半：中文句子本來怎麼組，模型的中文又在哪裡偏離。

## 問題：模型的中文偏離在哪裡

三組研究指向同一個方向。

- 翻譯中文。Xiao（2010）比較 100 萬字的英譯中語料（ZCTC）與 100 萬字的母語中文（LCMC），翻譯中文的連接詞每萬字 306 次，母語中文 243 次，多了約四分之一。「被」字句也明顯較多，詞彙密度較低（61.6% 對 66.9%），高頻詞重複得更多。研究者把連接詞增加歸為「明示化」（explicitation），把被動句增加歸為原文語言的影響。
- 翻譯中文的句法。Hu、Li 與 Kübler（2018）只用句法樹訓練分類器，分辨翻譯與原創中文的 F 值超過 90%。翻譯中文較常出現主語位置的代名詞、限定詞，以及「名詞＋的」當修飾語。
- 模型的中文。Guo 等人（2023）的 HC3 語料比較 ChatGPT 與人類的中文回答：ChatGPT 的回答比較長、用詞較少、詞彙密度較低，連接詞與代名詞較多，副詞較少，語氣也比較正式、四平八穩。Reinhart 等人（2025）用 Biber 的語域特徵分析英文，發現經過指令微調的模型使用名詞化約為人類的 1.5 到 2 倍，分詞子句 2 到 5 倍，基礎模型則接近人類。也就是說，這些偏差主要來自指令微調，不是訓練語料本身。

模型的中文同時帶有翻譯中文與模型文字兩種特徵：代名詞多、連接詞多、名詞前修飾長、名詞化多、句長平均。這些都是句法層次的問題，換掉幾個詞不會消失。

## 五條規則與對應的理論

| 規則 | 理論 | 對應的偏差 |
| --- | --- | --- |
| 1. 話題說一次，後面接著說 | 漢語是話題優先的語言（Li & Thompson 1976），話題鏈裡的後續分句以零形式回指話題（Tsao 1979） | 主語位置的代名詞增加（Hu et al. 2018、HC3） |
| 2. 照事情發生的順序寫 | 時間順序原則：兩個句法單位的相對次序，由它們所表達的狀態在概念世界的時間順序決定（Tai 1985） | 英文語序的「在……之前」後置條件、結果在前的句子 |
| 3. 關係看得出來就不寫連接詞 | 漢語以意合為主、英語以形合為主的對比（連淑能 1993），以及翻譯共性中的明示化（Baker 1993） | 連接詞多四分之一（Xiao 2010、HC3） |
| 4. 名詞前面只放短的修飾 | 依存距離最小化：各語言都傾向讓有依存關係的詞靠近，降低記憶負擔（Futrell, Mahowald & Gibson 2015）。中文的關係子句在名詞前，越長負擔越重 | 「名詞＋的」修飾語增加（Hu et al. 2018）。王力（1944）列出的歐化現象之一是句子延長 |
| 5. 句子長短跟著內容走 | 人類文字的句子層次困惑度有長尾，模型文字比較平均（Guo et al. 2023） | 句長平均、節奏單調 |

規則 3 和核心規則 1（保留助詞與連接詞）不衝突。核心規則 1 保留的是「就、再、才、也、能、會」這類把分句接起來的詞，規則 3 省掉的是「因此、而且、此外」這類在每句前面交代邏輯的詞。中文的流水句正是靠前者連接。

## 為什麼寫成正面的組法

原本的檢查清單以「看到什麼」為主，大量列出不該出現的說法。Rana（2026）分析模型違反「不要用某詞」指令的情況，87.5% 的失敗來自提示本身點名了那個詞，反而讓模型更容易寫出來。這不代表要刪掉檢查清單：改稿時需要辨認問題，清單仍然有用。但寫作當下，正面描述「中文怎麼組」比列出禁止事項更容易照做，所以五條規則都用「怎麼寫」表述，例句也只示範組法。

## 機械指標

`check.py --profile` 計算每千字的連接詞、代名詞、限定詞、被字句與虛動詞次數，以及每百字的「的」與句長的變異係數。這些項目直接取自上面研究裡翻譯中文或模型中文偏高的特徵。

這些數字沒有對錯門檻。用途是比較同一份文字改稿前後，或和同一語域的人寫文字比較。2026-10-30 用 reactjs101（2016 年的台灣 React 教學，17 個 800 字以上的檔案）與 Mozilla 正體中文風格指南試算，中位數約為：連接詞 7.9、代名詞 15.4、限定詞 6.5、被字句 0、「的」每百字 3.9、句長變異係數 0.85。這只是一位作者、一種語域的參考值，不能當成標準。

模型輸出的句長變異係數約 0.2 到 0.26，比參考語料的 0.85 低很多，但兩者長度差很多（模型輸出多在 100 字左右），這個比較只能當成方向。

`check.py` 另外加了一個 warning：一個分句裡出現三個以上的「的」。這是規則 4 唯一能用字串判斷的部分。

## 參考文獻

- Baker, M. (1993). Corpus linguistics and translation studies: Implications and applications. In *Text and Technology*. John Benjamins.
- Futrell, R., Mahowald, K., & Gibson, E. (2015). Large-scale evidence of dependency length minimization in 37 languages. *PNAS*, 112(33). https://pmc.ncbi.nlm.nih.gov/articles/PMC4547262
- Guo, B. et al. (2023). How close is ChatGPT to human experts? Comparison corpus, evaluation, and detection. arXiv:2301.07597. https://arxiv.org/abs/2301.07597
- Hu, H., Li, W., & Kübler, S. (2018). Detecting syntactic features of translated Chinese. arXiv:1804.08756. https://arxiv.org/abs/1804.08756
- Li, C. N., & Thompson, S. A. (1976). Subject and topic: A new typology of language. In *Subject and Topic*. Academic Press.
- Rana, S. (2026). Semantic gravity wells: Why negative constraints backfire. arXiv:2601.08070. https://arxiv.org/abs/2601.08070
- Reinhart, A. et al. (2025). Do LLMs write like humans? Variation in grammatical and rhetorical styles. arXiv:2410.16107. https://arxiv.org/abs/2410.16107
- Tai, J. H.-Y. (1985). Temporal sequence and Chinese word order. In *Iconicity in Syntax*. John Benjamins.
- Tsao, F.-F.（曹逢甫）(1979). *A Functional Study of Topic in Chinese*. Student Book.
- Xiao, R. (2010). How different is translated Chinese from native Chinese? A corpus-based study of translation universals. *International Journal of Corpus Linguistics*, 15(1). https://www.lancaster.ac.uk/fass/projects/corpus/ZJU/xpapers/Xiao_IJCL_TransChinese.pdf
- 王力（1944）。《中國現代語法》第六章〈歐化的語法〉。
- 連淑能（1993）。《英漢對比研究》。高等教育出版社。
- ISO 24495-1:2023 Plain language, Part 1: Governing principles and guidelines. 本專案的「先給答案」「依資訊性質選格式」與標準的四個原則（relevant、findable、understandable、usable）一致。

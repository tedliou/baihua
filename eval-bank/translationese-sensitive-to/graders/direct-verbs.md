---
type: llm
weight: 1
---

原文：「容器建置好後 VS Code 會自動啟動與連線到開發容器中，由於 Android 專案對於各種元件的版本號碼很敏感，需要特別設定。」「我可以瀏覽剛才選用 [Android SDK 的 GitHub](https://github.com/NordcomInc/devcontainer-features/tree/master/src/android-sdk)，能發現他有提供 platform、build_tools 的版本號碼欄位，因此可以編輯 .devcontainer/devcontainer.json，於 android-sdk 下加入版本設定。」
前版有「由於……對於……」疊用的介詞與連接詞，「能發現他有提供……因此可以編輯」把工具叫成「他」，句子拖長而且主詞不清楚。
PASS if 這兩處改成直接的動詞句（例如「Android 專案要求各元件的版本號碼和專案設定一致，所以要另外指定版本」「這個 Feature 提供 platform 與 build_tools 兩個版本欄位，編輯……加入版本設定」），不再有「由於……對於……」，「他」不再指稱工具；並保留這些事實：容器建置後 VS Code 自動連進開發容器、Android 專案需要設定元件版本、選用的 Android SDK Feature 提供 platform 與 build_tools 版本欄位、在 .devcontainer/devcontainer.json 的 android-sdk 底下加入版本設定、連結網址不變。
FAIL if 仍有「由於……對於……」或「能發現他有提供……因此」這類句型、刪掉連結或任一事實，或加入原文沒有的事實（例如具體版本號）。

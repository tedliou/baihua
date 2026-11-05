# 作者發佈的版本

給人對照用，不會送給模型，也不參與評分。圖片換成〔圖〕。

````markdown
## 換成 Paper 並啟動

換成 Paper 只要換掉伺服器資料夾裡的 jar 檔，世界、`plugins` 資料夾與啟動指令都不用動。Paper 的遷移文件要求把 Paper 的 jar 改成啟動指令裡的檔名：

1. 從 [Paper 下載頁](https://papermc.io/downloads/paper)下載和 Spigot 相同 Minecraft 版本的 Paper，檔名類似 `paper-26.3-240.jar`。
2. 刪掉伺服器資料夾裡原本的 Spigot jar，例如 `spigot-26.3.jar`。
3. 把下載的 Paper 放進伺服器資料夾，改成剛才刪掉的檔名。

〔圖〕
接著照原本的方式啟動伺服器，例如雙擊 `start.bat`。Paper 第一次啟動時會發現世界要轉換，先印出 ALERT 警告並倒數 30 秒：

〔圖〕
這段警告提醒沒有備份的人在倒數結束前中斷。前面已經備份，就等它倒數完，Paper 會轉換三個維度的資料夾並繼續啟動，看到 `Done` 就啟動完成。之後再啟動就不會出現這段警告。
````

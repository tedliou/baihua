---
type: llm
weight: 1
---

PASS if 保留這些事實：comfy-cli 安裝的 ComfyUI 在 `main.py` 旁放 `extra_model_paths.yaml`、設定檔寫共用資料夾的路徑與各類模型的子資料夾、兩個專案各放一份且內容相同、新增模型類型時兩份都要改、改用共用資料夾後 MOSS-Image 與 Qwen-Image 在硬碟上各只存一份。
FAIL if 刪掉或改動上述任一事實，或加入原文沒有的數字、步驟、功能或使用經驗。

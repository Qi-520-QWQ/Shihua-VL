# Contributing（Shihua-VL 公开评测包）

欢迎两种贡献：**提交模型结果**（PR）与**真值勘误**（Issue）。请先读 `README.md` 与 `DATA_CARD.md`。

## 提交模型结果（PR）

1. 在 T4（或同等环境）按 `notebooks/reproduce_2b_baseline.ipynb` 的协议跑完 60 题，或用自己的环境按 `scripts/run_audit_t4.py` 的同款参数（prompt、max_num=12、max_new_tokens=768、温度与采样设置见脚本）跑完。
2. PR 里新增两个文件：
   - `predictions/<模型名>.jsonl`：每行一个 JSON，至少含 `id`（与 `data/questions.jsonl` 的题目 ID 一一对应）、`model`（仓库名＋版本／量化，如 `OpenGVLab/InternVL2_5-8B int8-8bit`）、`answer`（非空）；建议同时含 `seconds`、`peak_mem_gb`、`n_tiles`、`max_num`。
   - `predictions/<模型名>_manifest.json`：运行清单（模型、量化、环境、日期、60 行计数、去重规则）。
3. 结果必须来自**未在 60 题上训练过**的模型——用评测集训练会使分数失效，投稿时请声明未训练。
4. 评分由维护者用 `scripts/` 的双评协议复核；自评分数可附在 PR 描述里，但不作为官方分数。
5. 代码类改动走 MIT 许可、数据类改动走 CC-BY-4.0（署名 Shihua-VL / Qi-520-QWQ）；提交即表示同意按此许可发布。

## 真值勘误（Issue）

用 `.github/ISSUE_TEMPLATE/truth_correction.md` 模板发 Issue，写明：

- 题目 ID（如 `audit_v0_met_39936_mingwu`）；
- 哪一条参考答案／必需事实有误；
- 证据：馆藏页 URL 原文，或画上可见文字的位置描述（须可复核，**不接受无出处的主张**）；
- 建议改法。

维护者核实后会修正答案、记入 `CHANGELOG.md`，**题目 ID 不变**。

## 题目 ID 稳定承诺

- 题目 ID（`audit_v0_<作品>_<维度>`）在 v0.x 系列内稳定不变，不改义、不复用。
- 参考答案勘误只改答案文本并在 CHANGELOG 记一行；题目本身有错到必须撤题时，该 ID 标记为撤回、不再分配给别的题目。
- v1.0（360 题主评测集）启用新 ID 段，与 v0.1 的 60 题 ID 不重叠；两层分层报告、不混平均。

## 行为准则

- 只讨论公开的馆藏材料与模型输出；不要贴密钥、账号、个人联系方式。
- 图像本身不随包分发，按 `data/items.jsonl` 的 URL＋SHA256 自行获取（CC0）。

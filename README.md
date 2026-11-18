# Shihua-VL 审计 v0 —— 公开评测包

中国古画细节理解评测包：20 件馆藏中国画 × 3 个维度（名物考据 / 笔墨技法 / 诗画意象）= 60 题，
每题带锁定参考答案、必需事实、禁止断言与证据出处。配套十条审计线的模型原始答案
（十条均已完成互盲双评与分歧裁决），以及 60 件失败案例。

> **状态：v0.1-preview，未发布。** 本包为 20 件馆藏中国画 × 3 个维度的评测集（60 题，参考答案全部可追溯到馆藏元数据或画上可见文字），配套十条审计线的模型原始答案（十条均已完成互盲双评与分歧裁决）与 60 件失败案例。结论见 `docs/decision.md`。

## 目录

| 路径 | 内容 |
| --- | --- |
| `data/questions.jsonl` | 60 题：题干、锁定参考答案、必需事实、可接受别名、禁止断言、证据出处、answerability（60 行） |
| `data/items.jsonl` | 20 件作品：馆藏出处、授权证据、原图 URL＋SHA256（20 行） |
| `data/museum_descriptions.md` | 20 馆方页实取描述 |
| `data/visual_notes.md` | 20 图原图目检笔记 |
| `data/SCREENING_RULES.md` | 选图八条硬规矩 |
| `predictions/reference_gemini4carbon.jsonl` | 旗舰参照 Gemini 4 Carbon 60 题原始答案（60 行） |
| `predictions/reference_gemini4argon.jsonl` | 首选参照 Gemini 4 Argon · High gemini-4-argon-high，**60/60 全齐** |
| `predictions/internvl2_5_2b.jsonl` | InternVL2.5-2B（T4，bf16，max_num=12）原始答案，见下方去重规则 |
| `predictions/internvl2_5_8b.jsonl` | InternVL2.5-8B（T4，int8-8bit，max_num=12）原始答案（60 行） |
| `predictions/internvl2_5_4b.jsonl` | InternVL2.5-4B（T4，bf16，max_num=12）原始答案（60 行） |
| `predictions/qwen2_5_vl_7b.jsonl` | Qwen2.5-VL-7B（T4，4bit，smart resize 256–1280）原始答案（60 行） |
| `predictions/qwen2_5_vl_3b.jsonl` | Qwen2.5-VL-3B（T4，bf16，smart resize 256–1280）原始答案（60 行） |
| `predictions/minicpm_v26_int4.jsonl` | MiniCPM-V-2_6-int4（T4，int4，max_slice_nums=9）原始答案（60 行） |
| `predictions/reference_gemini38flash.jsonl` | Gemini 3.8 Flash 无元数据基线 60 题原始答案（60 行） |
| `predictions/reference_gemini38flash_metadata.jsonl` | Gemini 3.8 Flash 有元数据条件 60 题原始答案（60 行） |
| `predictions/*_manifest.json` | 各预测文件的运行清单 |
| `ratings/ratings_reference_gemini4carbon.jsonl` | Carbon 双评原始评分记录（含重试记录，见下方说明） |
| `ratings/ratings_internvl2_5_2b.jsonl` | 2B 双评原始评分记录（含重试记录） |
| `ratings/ratings_internvl2_5_8b.jsonl` | 8B 双评原始评分记录（120 行，零失败重试） |
| `ratings/ratings_internvl2_5_4b.jsonl` | 4B 双评原始评分记录（143 行，含 23 行容量窗失败重试记录） |
| `ratings/ratings_qwen2_5_vl_7b.jsonl` | Qwen2.5-VL-7B 双评原始评分记录（120 行，零失败重试） |
| `ratings/ratings_qwen2_5_vl_3b.jsonl` | Qwen2.5-VL-3B 双评原始评分记录（120 行，零失败重试） |
| `ratings/ratings_minicpm_v26.jsonl` | MiniCPM-V-2_6-int4 双评原始评分记录（120 行，零失败重试） |
| `ratings/ratings_reference_38flash.jsonl` | 3.8 Flash 无元数据基线双评原始评分记录（122 行，含 2 行容量窗失败重试记录） |
| `ratings/ratings_reference_38flash_metadata.jsonl` | 3.8 Flash 有元数据条件双评原始评分记录（124 行，含 4 行容量窗失败重试记录） |
| `ratings/adjudication_carbon.jsonl` | Carbon 裁决后终判，**60 行，为准** |
| `ratings/adjudication_2b.jsonl` | 2B 裁决后终判，**60 行，为准** |
| `ratings/adjudication_8b.jsonl` | 8B 裁决后终判，**60 行，为准** |
| `ratings/adjudication_4b.jsonl` | 4B 裁决后终判，**60 行，为准** |
| `ratings/adjudication_qwen2_5_vl_7b.jsonl` | Qwen2.5-VL-7B 裁决后终判，**60 行，为准** |
| `ratings/adjudication_qwen2_5_vl_3b.jsonl` | Qwen2.5-VL-3B 裁决后终判，**60 行，为准** |
| `ratings/adjudication_minicpm_v26.jsonl` | MiniCPM-V-2_6-int4 裁决后终判，**60 行，为准** |
| `ratings/adjudication_38flash.jsonl` | 3.8 Flash 无元数据基线裁决后终判，**60 行，为准** |
| `ratings/adjudication_38flash_metadata.jsonl` | 3.8 Flash 有元数据条件裁决后终判，**60 行，为准** |
| `ratings/ratings_summary_*.md` | 十线评分汇总 |
| `failures/cases/` | 60 件失败案例（每件含缩略图、题干、参考答案、模型预测、双评、裁决书） |
| `docs/decision.md` | 验证期结论（定稿 v1：继续） |
| `docs/scoring_tiers_analysis.md` | strict 口径分层计分分析（2026-11-16） |
| `docs/a04-2b-spotcheck-2026-11-15.md` | 2B 单评抽查 15 题 |
| `docs/a04-reference-channel.md` | 参照通道核查与定案 |
| `docs/reference_rerate_results.md` | Gemini 4 Argon · High 第三方复核结果（Claude Sonnet 5.5 High 盲评 10 题） |
| `docs/landscape.md` | 查重报告（未发现等价项目） |
| `docs/README_A04_T4.md` | T4 审计运行协议 |
| `docs/reference_batches3-4_prompts.md` | Gemini 4 Argon · High 参照答案转录说明 |
| `scripts/` | 可运行脚本：参照跑、双评、T4 审计、词表补丁、Gemini 4 Argon · High 转录 |
| `notebooks/reproduce_2b_baseline.ipynb` | 可选便利：2B 基线一键复现（2B-only） |
| `ENVIRONMENT.md` | 复现环境配置说明（版本钉死清单，复现以此为准） |
| `CHANGELOG.md` | 版本变更记录 |
| `CONTRIBUTING.md` | 提交模型结果（PR）与真值勘误（Issue）通道、题目 ID 稳定承诺 |
| `.github/ISSUE_TEMPLATE/` | Issue 模板：真值勘误、提交模型结果 |
| `MANIFEST.json` | 全部 2062 个文件的 SHA256 清单 |

## 结果（裁决后，60 题）

| 线 | strict_hit | hallucination | partial 均值（0–2） | 完全干净 |
| --- | --- | --- | --- | --- |
| Gemini 4 Carbon（旗舰参照） | 4/60（6.7%） | 41/60（68.3%） | 1.34 | 3/60 |
| Gemini 4 Argon · High（首选参照） | 2/60（3.3%） | 45/60（75.0%） | 1.18 | 2/60 |
| InternVL2.5-2B（T4 本地） | 0/60（0%） | 36/60（60.0%） | 0.58 | 0/60 |
| InternVL2.5-8B（T4 本地，int8-8bit） | 0/60（0%） | 35/60（58.3%） | 0.79 | 0/60 |
| InternVL2.5-4B（T4 本地） | 0/60（0%） | 36/60（60.0%） | 0.82 | 0/60 |
| Qwen2.5-VL-7B（T4 本地，4bit） | 0/60（0%） | 37/60（61.7%） | 0.78 | 0/60 |
| Qwen2.5-VL-3B（T4 本地，bf16） | 0/60（0%） | 41/60（68.3%） | 0.77 | 0/60 |
| MiniCPM-V-2_6-int4（T4 本地，int4） | 0/60（0%） | 36/60（60.0%） | 0.80 | 0/60 |
| Gemini 3.8 Flash（无元数据，对照基线） | 4/60（6.7%） | 53/60（88.3%） | 1.25 | 1/60 |
| Gemini 3.8 Flash（有元数据，对照） | 14/60（23.3%） | 55/60（91.7%） | 1.65 | 4/60 |

元数据对照为同模型配对实验（非基线矩阵线）：有元数据使 strict 4→14、partial 均值 1.25→1.65，但幻觉率 53→55 未降——元数据使答案更全更准，不治幻觉。

分维 strict：Carbon 名物 1/20、笔墨 2/20、意象 1/20；2B 三维全 0/20；8B 三维全 0/20；4B 三维全 0/20；Qwen 三维全 0/20；Qwen-3B 三维全 0/20；MiniCPM 三维全 0/20；3.8 Flash 无元数据 名物 2/20、笔墨 1/20、意象 1/20，有元数据 名物 4/20、笔墨 2/20、意象 8/20。
8B 幻觉分维 名物 16/20、笔墨 15/20、意象 4/20（意象为四线最低）；8B 宽松命中（partial 均值 ≥1）39/60（65.0%），高于 2B 的 28/60——8B 增益在「答多答全」不在「答对考据事实」。4B 幻觉分维 名物 18/20、笔墨 13/20、意象 5/20；4B 宽松命中 41/60（68.3%），略高于 8B 的 39/60——同样是答案更全而非考据更准。Qwen 幻觉分维 名物 13/20、笔墨 14/20、意象 10/20；Qwen 宽松命中 39/60（65.0%），与 8B 持平——不同厂商、不同架构的 7B 级模型落在同一分数带，缺口是任务本身的考据难度、非某一模型家族的短板。Qwen-3B 幻觉分维 名物 18/20、笔墨 13/20、意象 10/20；Qwen-3B 宽松命中 38/60（63.3%）——3B 的答案完整度与 7B 同档，但幻觉为小模型线最高（41/60，与 Carbon 旗舰线持平），且更易编造具体的画面细节（见 `docs/decision.md` 方法学事项 2 与 7）。MiniCPM 幻觉分维 名物 16/20、笔墨 15/20、意象 5/20；MiniCPM 宽松命中 37/60（61.7%）——首个非 InternVL/Qwen 架构的小模型基线（中文厂商 VLM 一款），与同级模型落在同一分数带（见 `docs/decision.md` 方法学事项 2 与 8）。3.8 Flash 幻觉分维：无元数据 名物 20/20、笔墨 18/20、意象 15/20，有元数据 名物 20/20、笔墨 19/20、意象 16/20；宽松命中无元数据 53/60、有元数据 59/60——元数据对照结论见 `docs/decision.md` 方法学事项 5。
详见 `docs/decision.md` 与 `docs/scoring_tiers_analysis.md`（strict 口径严苛性分析：
Carbon 宽松命中 partial ≥ 1 达 55/60，strict 只计全中；幻觉率在任何口径下都远超 5% 门槛，
「缺口确认」结论不依赖 strict 口径）。

## 去重与读取规则（重要）

- `predictions/internvl2_5_2b.jsonl` 共 64 行、60 个唯一 id：4 个重复 id
  （met_39936 三题、met_40062 mingwu）各有一条早期失败记录（空答案＋error 字段，
  tokenizer 故障期）与一条后期成功记录（带 `tokenizer_source` 字段）。
  **读取时以后来的成功记录为准**，失败记录留档仅供追溯。
- `ratings/ratings_*.jsonl` 行数多于 120（Carbon 155 行、2B 129 行；8B 恰 120 行，零失败重试）：
  含网关 503 等失败重试记录。**逐题终判以 `ratings/adjudication_*.jsonl`（各 60 行）为准**，
  原始 ratings 文件仅供审计追溯。
- 3 条参考答案标注 `verified_evidence_insufficient`
  （met_51705 bimo/yixiang、cma_141693 mingwu）：答案中已明写无法确认之项，不编造。

## 图像获取

原图不随包分发（54 MB）。`data/items.jsonl` 每件含 `source.image_url` 与 `source.sha256`，
按 URL 下载后核对 SHA256 即可复现。图像权利：Met / Cleveland 馆藏页均标注 CC0，
逐件授权证据见 `source.rights_statement` 与 `rights_evidence`。
缩略图见 `failures/cases/<条目>/` 内。

## 复现

复现以 `ENVIRONMENT.md` 的独立配置说明为准（版本钉死清单见该文件）；`notebooks/reproduce_2b_baseline.ipynb` 只是按该配置写好的可选便利、不得作为复现的唯一路径。

- 2B 基线复现：见 `ENVIRONMENT.md`（硬件 T4 16GB、transformers==4.49.0、词表补丁、按 `data/items.jsonl` 的 URL＋SHA256 取图、跑满 60 题；输出为 `predictions/internvl2_5_2b_reproduced.jsonl`，不覆盖包内已带的结果文件）。
- 参照跑：`scripts/run_reference_carbon.py`（Gemini 4 Carbon，reasoning none，stream＋逐题落盘；注意单次 completion 硬顶 16,384 token）。服务地址与密钥文件由环境变量 `SHIHUA_API_BASE_URL` / `SHIHUA_API_KEY_FILE` 配置。
- 双评：`scripts/rate_reference_carbon.py`、`scripts/rate_internvl2b.py`（DeepSeek V4.1 Flash＋Gemini 3.8 Flash 互盲，模型身份隐藏）。
- T4 审计：`scripts/run_audit_t4.py`＋`docs/README_A04_T4.md`（transformers==4.49.0 钉版＋词表补丁 `scripts/patch_tokenizer_null.py`，见 README 内故障史）。
- 8B 线：int8-8bit 于 2026-11-18 01:00 CST 跑完 60/60（早期 NF4 路径因加载错误退役，改用 int8）；双评 120/120 对＋8 题裁决已完成（终判 strict 0/60、hallu 35/60，见 `ratings/ratings_summary_8b.md`）。

## 许可

见 `LICENSES.md`：代码 MIT；标注与评测数据 CC-BY-4.0；图像依各馆 CC0 声明。

## 版本

- v0.1-preview（未发布）：见 `CHANGELOG.md`。题目 ID（`audit_v0_<作品>_<维度>`）在 v0.x 内稳定不变，承诺全文见 `CONTRIBUTING.md`。

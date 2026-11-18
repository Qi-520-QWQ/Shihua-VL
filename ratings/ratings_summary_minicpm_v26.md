# MiniCPM-V-2_6-int4 双评终结报告（2026-11-18 20:31 CST）

考生模型：MiniCPM-V-2_6-int4（T4，int4，官方 `model.chat()`、max_slice_nums=9、贪心 sampling=False/num_beams=1/repetition_penalty=1.0/max_new_tokens=768，transformers 4.49.0；`minicpm_v26_int4.jsonl`，60/60 题有答案）

评者：rater_a = DeepSeek V4.1 Flash，rater_b = Gemini 3.8 Flash，互盲

评分文件：`ratings_minicpm_v26.jsonl`（120 对有效评分；零失败）

裁决文件：`adjudication_minicpm_v26.jsonl`（60 题终判）

失败案例：`failures/cases/<question_id>/<dimension>/`（60 件全量，各含 prediction_minicpm_v26.json / ratings_minicpm_v26.json / judgment_minicpm_v26.md）

## 终判分数（裁决后）

| 维度 | strict_hit | hallucination |
| --- | --- | --- |
| 名物 mingwu | 0/20 | 16/20 |
| 笔墨 bimo | 0/20 | 15/20 |
| 意象 yixiang | 0/20 | 5/20 |
| 合计 | 0/60（0%） | 36/60（60.0%） |

- 完全干净（strict=1 且 hallu=0）：0/60
- partial 均值 0.80/2（名物 0.68、笔墨 0.72、意象 1.00）
- 宽松命中（partial 均值 ≥1）：37/60（61.7%）

## 双评者一致率

- strict_hit 一致 60/60（100%），hallucination 一致 38/60（63.3%，低于 85% 目标线；为小模型六线最低）
- 分歧 22 题已全部裁决（`adjudication_minicpm_v26.jsonl`，逐题有据）：rater_a 正确 5 题、rater_b 正确 17 题
- 系统性差异：rater_a 全程严于 rater_b（hallucination 53/60 vs 31/60），裁决后终值 36/60 贴近 rater_b——与 Qwen/Qwen-3B 两线同构：本线 rater_a 大量把含糊风格形容词与泛泛抒情措辞判为幻觉，裁决按统一口径（仅矛盾/无据的具体事实断言计幻觉）逐题推翻
- 裁决口径（与 Carbon/2B/8B/Gemini 4 Argon · High/4B/Qwen/Qwen-3B 线统一）：hallucination=1 仅当断言了与参考答案矛盾的具体事实，或无据断言了具体归属/题跋/题款/器物/形状/数量等可核查事实；通用笔法术语、通用文化常识性说法、不确定性段内的 hedges 不计幻觉；遗漏事实只扣 strict、不计幻觉；参考答案未言明的画面细节以目检记录（data/visual_notes.md）为准

## 方法学注记

1. **MiniCPM 与其他小模型线对照**：strict 同为 0/60；hallu 36/60 与 2B（36/60）、4B（36/60）持平，低于 3B（41/60）、7B（37/60），高于 8B（35/60）；partial 均值 0.80 与 8B/4B/7B 同档（0.79/0.82/0.78）、明显高于 2B（0.58）；宽松命中 37/60 vs 39/39/41/28。结论与既往线一致：小模型间的差异在答案完整度，不在考据准确度；MiniCPM 是首个非 InternVL/Qwen 架构的小模型基线（中文厂商 VLM 一款），与同级模型落在同一分数带。
2. **MiniCPM 的幻觉形态更具体**：22 道分歧中 5 道判 rater_a 正确，均为对具体画面事实的编造或直接矛盾（141693_bimo 把云气留白错安为山石高光留白、35989_mingwu 无据断言「盘腿而坐」并把文人居士说成僧侣/修行者、39936_mingwu 「树枝」与参考答案「竹枝」直接矛盾、49047_bimo 把蝴蝶定性为工笔/湖石花朵定性为写意、与参考答案明示的「无法确认严格画法归属」直接矛盾、62002_yixiang 把从者甲胄错安到绿袍主角身上）；其余 17 道仍为 rater_a 把含糊措辞判为幻觉（与 Qwen/Qwen-3B 线同构）。
3. **目检记录救回两题**：142579_mingwu「崖顶有树木」「画面上方有书法题字」与目检记录（崖顶有小树、上部布满石涛题跋数列＋朱印）相合，非编造；142579_yixiang「树木光秃」为崖顶小树＋右下枯梅的含糊视觉印象，未断言与目检记录矛盾的具体物象——参考答案未言明的画面细节须以目检记录为准，不能只凭参考答案判编造（裁决口径补充，见 3B 线）。
4. **分维差异**：名物 hallu 16/20、笔墨 15/20、意象 5/20——意象 hallu 与 4B 并列八线最低，意象 partial 均值 1.00 为三维最高；名物仍是重灾区，一碰具体器物/题款/形制即错。三维难度分层再次得到验证。
5. **推理实况**：T4：smoke 2/2＋全量 58/58 合并 60/60，零失败；平均 21.6 秒/题（最慢 cma_141693_bimo 42.4 秒）、平均峰值显存 7.00GB（最高 7.12GB）。n_tiles 为 null：官方 `model.chat()` 在内部处理预处理，不暴露逐图切块数，不推断。首轮 smoke 失败的根因已修复（图像预处理参数类型不匹配）。
6. **双评实况**：双评 120/120 对有效评分，全程零失败。
7. **成本**：服务方未返回 usage 字段，成本按费率估算约 $0.008/次；双评 120 次约 $1。

## 基线矩阵计数

- 可复现基线现为 6 个：InternVL2.5-2B（bf16）、InternVL2.5-8B（int8-8bit）、InternVL2.5-4B（bf16）、Qwen2.5-VL-7B（4bit）、Qwen2.5-VL-3B（bf16）与 MiniCPM-V-2_6-int4（int4）；Carbon/Argon 只算参考线。MiniCPM-V-2_6-int4 线至此全部完成（推理＋双评＋裁决＋失败案例归档），并入 `docs/decision.md` 基线表。**≥6 个可复现基线的要求已达成。**

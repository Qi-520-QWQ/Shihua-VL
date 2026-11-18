# Qwen2.5-VL-3B 双评终结报告（2026-11-18 15:40 CST）

考生模型：Qwen2.5-VL-3B-Instruct（T4，bf16，官方 quick-start smart resize 256–1280、贪心、max_new_tokens=768，transformers 4.49.0；`qwen2_5_vl_3b.jsonl`，60/60 题有答案）

评者：rater_a = DeepSeek V4.1 Flash，rater_b = Gemini 3.8 Flash，互盲

评分文件：`ratings_qwen2_5_vl_3b.jsonl`（120 对有效评分；零失败）

裁决文件：`adjudication_qwen2_5_vl_3b.jsonl`（60 题终判）

失败案例：`failures/cases/<question_id>/<dimension>/`（60 件全量，各含 prediction_qwen2_5_vl_3b.json / ratings_qwen2_5_vl_3b.json / judgment_qwen2_5_vl_3b.md）

## 终判分数（裁决后）

| 维度 | strict_hit | hallucination |
| --- | --- | --- |
| 名物 mingwu | 0/20 | 18/20 |
| 笔墨 bimo | 0/20 | 13/20 |
| 意象 yixiang | 0/20 | 10/20 |
| 合计 | 0/60（0%） | 41/60（68.3%） |

- 完全干净（strict=1 且 hallu=0）：0/60
- partial 均值 0.77/2（名物 0.68、笔墨 0.80、意象 0.82）
- 宽松命中（partial 均值 ≥1）：38/60（63.3%）

## 双评者一致率

- strict_hit 一致 60/60（100%），hallucination 一致 40/60（66.7%，低于 85% 目标线）
- 分歧 20 题已全部裁决（`adjudication_qwen2_5_vl_3b.jsonl`，逐题有据）：rater_a 正确 5 题、rater_b 正确 15 题
- 系统性差异：rater_a 全程严于 rater_b（hallucination 56/60 vs 36/60），裁决后终值 41/60 贴近 rater_b——与 7B 线（rater_a 55 vs rater_b 38，终值 37）方向相同：本线 rater_a 大量把含糊风格形容词与泛泛抒情措辞判为幻觉，裁决按统一口径（仅矛盾/无据的具体事实断言计幻觉）逐题推翻
- 裁决口径（与 Carbon/2B/8B/Gemini 4 Argon · High/4B/7B 线统一）：hallucination=1 仅当断言了与参考答案矛盾的具体事实，或无据断言了具体归属/题跋/题款/器物/形状/数量等可核查事实；通用笔法术语、通用文化常识性说法、不确定性段内的 hedges 不计幻觉；遗漏事实只扣 strict、不计幻觉；参考答案未言明的画面细节以目检记录（data/visual_notes.md）为准

## 方法学注记

1. **Qwen2.5-VL-3B 与 7B 及 InternVL 三线对照**：strict 同为 0/60；hallu 41/60 vs 7B 37/60、8B 35/60、4B 36/60、2B 36/60——3B 是小模型线中幻觉最高者，与 Carbon 旗舰线（41/60）持平；partial 均值 0.77 vs 7B 0.78、8B 0.79、4B 0.82、2B 0.58、宽松命中 38/60 vs 39/60、39/60、41/60、28/60——3B 的答案完整度与 7B/8B/4B 同档、明显高于 2B。结论与既往线一致：小模型间的差异在答案完整度，不在考据准确度；馆方特异事实仍基本答不出，缺口不在参数量一端（与 Carbon 旗舰 strict 4/60 对照一致）。
2. **3B 的幻觉形态更具体**：20 道分歧中 5 道判 rater_a 正确，均为对具体画面事实的编造或直接矛盾（142579_yixiang 编造蜿蜒河流与两岸山石、62002_yixiang 编造"龙"并把青龙偃月刀说成宝剑、739501_mingwu "仅一朵莲花"与"数朵"直接矛盾、813350_mingwu "姿态各异"与"朝向高度一致"直接矛盾、40062_mingwu "方形"与茅顶小屋形制不符），远多于 7B 线的 1 道（813350_yixiang）。小模型不仅答不出考据事实，还更易编造具体的画面细节；其余 15 道仍为 rater_a 把含糊措辞判为幻觉（与 7B 线同构）。
3. **目检记录救回两题**：160135_yixiang "两位渔夫"与目检记录（左缘小舟人影＋中左篷船红袍渔人，渔人 2 名）相合，非编造；135836_yixiang "寺庙坐落在山脚下"与目检记录"山脚溪畔有小型寺宇建筑群"相合。参考答案未言明的画面细节须以目检记录为准，不能只凭参考答案判编造——此为裁决口径的补充，已写入裁决脚本头注。
4. **分维差异**：名物 hallu 18/20（与 4B 并列小模型线最高，与 2B 的 15/20、8B 的 16/20、7B 的 13/20 对照），一碰具体器物/题款/形制即错；意象 10/20 与 7B 持平，四线意象均低——意象题可用通用文化常识蒙对方向而不触具体事实。三维难度分层再次得到验证。
5. **推理实况**：T4：smoke 2/2＋全量 58/58 合并 60/60，零失败；平均 48.1 秒/题（最慢 cma_139824_mingwu 124.4 秒，一次成功）、平均峰值显存 10.11GB（最高 11.00GB）。n_tiles 口径与 InternVL 不同：此处为 smart resize 后 28×28 patch 网格数（约 4872–5100），非 InternVL 的 dynamic tiling 切块数，见 runner 文件头注记。
6. **双评实况**：双评 120/120 对有效评分，全程零失败。
7. **成本**：服务方未返回 usage 字段，成本按费率估算约 $0.008/次；双评 120 次约 $1。

## 基线矩阵计数

- 可复现基线现为 5 个：InternVL2.5-2B（bf16）、InternVL2.5-8B（int8-8bit）、InternVL2.5-4B（bf16）、Qwen2.5-VL-7B（4bit）与 Qwen2.5-VL-3B（bf16）；Carbon/Argon 只算参考线。Qwen2.5-VL-3B 线至此全部完成（推理＋双评＋裁决＋失败案例归档），并入 `docs/decision.md` 基线表。下一基线 MiniCPM-V-2_6-int4 已完成，见 ratings_summary_minicpm_v26.md。

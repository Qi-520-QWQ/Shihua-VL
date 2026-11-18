# Qwen2.5-VL-7B 双评终结报告（2026-11-18 12:00 CST）

考生模型：Qwen2.5-VL-7B-Instruct（T4，4bit，官方 quick-start smart resize 256–1280、贪心、max_new_tokens=768，transformers 4.49.0；`qwen2_5_vl_7b.jsonl`，60/60 题有答案）

评者：rater_a = DeepSeek V4.1 Flash，rater_b = Gemini 3.8 Flash，互盲

评分文件：`ratings_qwen2_5_vl_7b.jsonl`（120 对有效评分；零失败）

裁决文件：`adjudication_qwen2_5_vl_7b.jsonl`（60 题终判）

失败案例：`failures/cases/<question_id>/<dimension>/`（60 件全量，各含 prediction_qwen2_5_vl_7b.json / ratings_qwen2_5_vl_7b.json / judgment_qwen2_5_vl_7b.md）

## 终判分数（裁决后）

| 维度 | strict_hit | hallucination |
| --- | --- | --- |
| 名物 mingwu | 0/20 | 13/20 |
| 笔墨 bimo | 0/20 | 14/20 |
| 意象 yixiang | 0/20 | 10/20 |
| 合计 | 0/60（0%） | 37/60（61.7%） |

- 完全干净（strict=1 且 hallu=0）：0/60
- partial 均值 0.78/2（名物 0.68、笔墨 0.80、意象 0.88）
- 宽松命中（partial 均值 ≥1）：39/60（65.0%）

## 双评者一致率

- strict_hit 一致 60/60（100%），hallucination 一致 41/60（68.3%，低于 85% 目标线）
- 分歧 19 题已全部裁决（`adjudication_qwen2_5_vl_7b.jsonl`，逐题有据）：rater_a 正确 1 题、rater_b 正确 18 题
- 系统性差异：rater_a 全程严于 rater_b（hallucination 55/60 vs 38/60），裁决后终值 37/60 贴近 rater_b——与 4B 线（rater_a 45 vs rater_b 34，终值 36）方向相反：本线 rater_a 大量把含糊风格形容词与泛泛抒情措辞判为幻觉，裁决按统一口径（仅矛盾/无据的具体事实断言计幻觉）逐题推翻
- 裁决口径（与 Carbon/2B/8B/Gemini 4 Argon · High/4B 线统一）：hallucination=1 仅当断言了与参考答案矛盾的具体事实，或无据断言了具体归属/题跋/题款/器物等可核查事实；通用笔法术语、通用文化常识性说法、不确定性段内的 hedges 不计幻觉；遗漏事实只扣 strict、不计幻觉

## 方法学注记

1. **Qwen2.5-VL-7B 与 InternVL 三线对照**：strict 同为 0/60；hallu 37/60 vs 8B 35/60、4B 36/60、2B 36/60，四线几乎持平；partial 均值 0.78 vs 8B 0.79、4B 0.82、2B 0.58、宽松命中 39/60 vs 39/60、41/60、28/60——Qwen 7B 的答案完整度与 8B/4B 同档、明显高于 2B。结论与 8B/4B 线一致：小模型间的差异在答案完整度，不在考据准确度；馆方特异事实仍基本答不出，缺口不在参数量一端（与 Carbon 旗舰 strict 4/60 对照一致）。不同厂商、不同架构的 7B 级模型落在同一分数带，进一步证实缺口是任务本身的考据难度、非某一模型家族的短板。
2. **分维差异**：意象 hallu 10/20（2B 6/20、8B 4/20、4B 5/20），四线意象均低——意象题可用通用文化常识蒙对方向而不触具体事实；名物 13/20 与笔墨 14/20 仍高，一碰具体器物/题款/皴法命名即错。三维难度分层再次得到验证。
3. **裁决细节**：19 道分歧中 18 道判 rater_b 正确，均为「遗漏≠幻觉」与「泛泛抒情/风格形容词不计幻觉」（135836_bimo/yixiang、141693_yixiang、142579_yixiang、160135_yixiang、35989_bimo、36178_yixiang、39936_bimo/mingwu、40062_bimo、41462_yixiang、41468_mingwu/yixiang、62002_bimo、739501_mingwu、78125_yixiang、813350_bimo/mingwu）；唯一判 rater_a 正确的是 813350_yixiang（“枝叶繁茂”为泛泛视觉形容，未断言具体可核查事实）。边界判例两则：① 40062_bimo——rater_a 称“由浅入深”方向不符，实测答案“左侧清淡、右侧浓郁”与参考答案“浓墨集中于右侧松崖、左侧水面清淡”方向一致，rater_a 的方向指控不成立；② 41462_yixiang——“枝干扭曲、根部盘绕”是对画中孤松形态的泛泛视觉描述，未触禁止断言（未称富贵荣华/松梅合绘/忠君报国），不计幻觉。另：141693_yixiang 与 41468_yixiang 沿用 4B 线同题判例（泛泛抒情措辞不计幻觉）。
4. **推理实况**：T4：smoke 2/2（48.3 秒）＋全量 58/58（1638.7 秒）合并 60/60，零失败；平均 28.1 秒/题（最慢 met_49047_mingwu 103.2 秒，一次成功）、平均峰值显存 9.67GB（最高 9.89GB）。n_tiles 口径与 InternVL 不同：此处为 smart resize 后 28×28 patch 网格数（约 4872–5100），非 InternVL 的 dynamic tiling 切块数，见 runner 文件头注记。
5. **双评实况**：双评 120/120 对有效评分，全程零失败。
6. **成本**：服务方未返回 usage 字段，成本按费率估算约 $0.008/次；双评 120 次约 $1。

## 基线矩阵计数

- 可复现基线现为 4 个：InternVL2.5-2B（bf16）、InternVL2.5-8B（int8-8bit）、InternVL2.5-4B（bf16）与 Qwen2.5-VL-7B（4bit）；Carbon/Argon 只算参考线。Qwen2.5-VL-7B 线至此全部完成（推理＋双评＋裁决＋失败案例归档），并入 `docs/decision.md` 基线表。

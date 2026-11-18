# InternVL2.5-4B 双评终结报告（2026-11-18 08:20 CST）

考生模型：InternVL2.5-4B（T4，bf16，dynamic tiling max_num=12，贪心，max_new_tokens=768，词表直取仓库 Qwen2Tokenizer、无补丁；`internvl2_5_4b.jsonl`，60/60 题有答案）

评者：rater_a = DeepSeek V4.1 Flash，rater_b = Gemini 3.8 Flash，互盲

评分文件：`ratings_internvl2_5_4b.jsonl`（120 对有效评分；另有 23 行历史失败记录，皆为服务容量波动，重试后全部成功）

裁决文件：`adjudication_4b.jsonl`（60 题终判）

失败案例：`failures/cases/<question_id>/<dimension>/`（60 件全量，各含 prediction_internvl2_5_4b.json / ratings_4b.json / judgment_4b.md）

## 终判分数（裁决后）

| 维度 | strict_hit | hallucination |
| --- | --- | --- |
| 名物 mingwu | 0/20 | 18/20 |
| 笔墨 bimo | 0/20 | 13/20 |
| 意象 yixiang | 0/20 | 5/20 |
| 合计 | 0/60（0%） | 36/60（60.0%） |

- 完全干净（strict=1 且 hallu=0）：0/60
- partial 均值 0.82/2（名物 0.65、笔墨 0.78、意象 1.03）
- 宽松命中（partial 均值 ≥1）：41/60（68.3%）

## 双评者一致率

- strict_hit 一致 60/60（100%），hallucination 一致 47/60（78.3%，低于 85% 目标线）
- 分歧 13 题已全部裁决（`adjudication_4b.jsonl`，逐题有据）：rater_a 正确 2 题、rater_b 正确 11 题
- 系统性差异：rater_a 全程严于 rater_b（hallucination 45/60 vs 34/60），裁决后终值 36/60 介于两者之间
- 裁决口径（与 Carbon/2B/8B/Gemini 4 Argon · High 线统一）：hallucination=1 仅当断言了与参考答案矛盾的具体事实，或无据断言了具体归属/题跋/题款/器物等可核查事实；通用笔法术语、通用文化常识性说法、不确定性段内的 hedges 不计幻觉；遗漏事实只扣 strict、不计幻觉

## 方法学注记

1. **4B 与 8B/2B 对照**：strict 同为 0/60；hallu 36/60 vs 8B 35/60、2B 36/60，三线几乎持平；partial 均值 0.82 vs 8B 0.79、2B 0.58、宽松命中 41/60 vs 39/60、28/60——4B 的答案完整度略高于 8B、明显高于 2B。结论与 8B 线一致：小模型间的差异在答案完整度，不在考据准确度；馆方特异事实仍基本答不出，缺口不在参数量一端（与 Carbon 旗舰 strict 4/60 对照一致）。
2. **分维差异**：意象 hallu 仅 5/20（2B 6/20、8B 4/20），三线意象均低——意象题可用通用文化常识蒙对方向而不触具体事实；名物 18/20 仍高（Carbon 19/20、Gemini 4 Argon · High 18/20、2B 15/20、8B 16/20），一碰具体器物/题款/归属即错。三维难度分层再次得到验证。
3. **裁决细节**：13 道分歧中 11 道判 rater_b 正确，均为「遗漏≠幻觉」（141693_yixiang、35989_mingwu/yixiang、41185_yixiang、41468_yixiang、739501_mingwu、78125_bimo/yixiang、813350_bimo/yixiang）与「泛泛抒情/风格形容词不计幻觉」；2 道判 rater_a 正确，均为具体事实矛盾（41462_mingwu“老干生枝”画论断言、78125_mingwu 文字“装饰和补充”作用）。边界判例：39936_yixiang“宁静致远”判幻觉（直接作答画论通识含义，与参考答案所定通识不符），而 78125_yixiang 同词仅作泛泛意境措辞不判幻觉——同一措辞是否构成幻觉取决于它是否被当作通识断言提出。
4. **容量波动**：双评曾遇服务容量波动（2026-11-18 约 05:00–08:00），恢复后一次跑完余下 24 对，零失败。
5. **一处记账异常**：`audit_v0_met_739501_yixiang` rater_a 行 score 已完整解析（与 rater_b 逐项一致：strict 0、partial 2、hallu 0、proper_refusal 1），但完成标记为 false（流在收尾处中断）。按既有口径（有 score 即计完成）计入 120 对，不单独重跑；该行 error 字段保留原值备查。
6. **成本**：服务方未返回 usage 字段，成本按费率估算约 $0.008/次；双评 120 次约 $1。

## 基线矩阵计数

- 可复现基线现为 3 个：InternVL2.5-2B（bf16）、InternVL2.5-8B（int8-8bit）与 InternVL2.5-4B（bf16）；Carbon/Argon 只算参考线。4B 线至此全部完成（推理＋双评＋裁决＋失败案例归档），并入 `docs/decision.md` 基线表。

# InternVL2.5-8B 双评终结报告（2026-11-18 02:03 CST）

考生模型：InternVL2.5-8B（T4，int8-8bit，dynamic tiling max_num=12，贪心，max_new_tokens=768，词表补丁 tokenizer；`internvl2_5_8b.jsonl`，60/60 题有答案）

评者：rater_a = DeepSeek V4.1 Flash，rater_b = Gemini 3.8 Flash，互盲

评分文件：`ratings_internvl2_5_8b.jsonl`（120 对有效评分；零失败）

裁决文件：`adjudication_8b.jsonl`（60 题终判）

失败案例：`failures/cases/<question_id>/<dimension>/`（60 件全量，各含 prediction_internvl2_5_8b.json / ratings_8b.json / judgment_8b.md）

## 终判分数（裁决后）

| 维度 | strict_hit | hallucination |
| --- | --- | --- |
| 名物 mingwu | 0/20 | 16/20 |
| 笔墨 bimo | 0/20 | 15/20 |
| 意象 yixiang | 0/20 | 4/20 |
| 合计 | 0/60（0%） | 35/60（58.3%） |

- 完全干净（strict=1 且 hallu=0）：0/60
- partial 均值 0.79/2（名物 0.70、笔墨 0.75、意象 0.93）
- 宽松命中（partial 均值 ≥1）：39/60（65.0%）

## 双评者一致率

- strict_hit 一致 60/60（100%），hallucination 一致 52/60（86.7%，高于 85% 目标线）
- 分歧 8 题已全部裁决（`adjudication_8b.jsonl`，逐题有据）：rater_a 正确 3 题、rater_b 正确 5 题
- 系统性差异：rater_a 全程严于 rater_b（hallucination 38/60 vs 32/60），裁决后终值 35/60 介于两者之间
- 裁决口径（与 Carbon/2B/Gemini 4 Argon · High 线统一）：hallucination=1 仅当断言了与参考答案矛盾的具体事实，或无据断言了具体归属/题跋/题款/器物等可核查事实；通用笔法术语、不确定性段内的 hedges 不计幻觉；遗漏事实只扣 strict、不计幻觉

## 方法学注记

1. **8B 与 2B 对照**：strict 同为 0/60；hallu 35/60 vs 36/60，几乎持平；但 partial 均值 0.79 vs 0.58、宽松命中 39/60 vs 28/60——8B int8 的答案明显更完整、更少空泛。结论：8B 相对 2B 的增益在「答多答全」不在「答对考据事实」；馆方特异事实仍基本答不出，缺口不在参数量一端（与 Carbon 旗舰 strict 4/60 对照一致）。
2. **分维差异**：意象 hallu 仅 4/20，为四线意象最低（Carbon 9/20、Gemini 4 Argon · High 14/20、2B 6/20）——意象题可用通用文化常识蒙对方向而不触具体事实；名物 16/20 仍高（Carbon 19/20、Gemini 4 Argon · High 18/20、2B 15/20），一碰具体器物/题款/归属即错。三维难度分层再次得到验证。
3. **裁决细节**：8 道分歧中 5 道判 rater_b 正确，均为「遗漏≠幻觉」（139824_yixiang、35989_mingwu、39547_yixiang、41468_yixiang）与「套模板编造建筑特征」（142579_bimo）；3 道判 rater_a 正确，均为具体事实矛盾（39936_bimo 鸟羽粗重刚劲、40062_bimo 披麻/斧劈皴、78125_mingwu 文字解释作用）。分歧模式与既往线一致：rater_a 对具体事实断言更敏感。
4. **成本**：服务方未返回 usage 字段，成本按费率估算约 $0.008/次；双评 120 次约 $1。评分全程零失败（个别调用约 60 秒，疑为重试后成功）。

## 基线矩阵计数

- 可复现基线现为 2 个：InternVL2.5-2B（bf16）与 InternVL2.5-8B（int8-8bit）；Carbon/Argon 只算参考线。8B 线至此全部完成（推理＋双评＋裁决＋失败案例归档），并入 `docs/decision.md` 基线表。

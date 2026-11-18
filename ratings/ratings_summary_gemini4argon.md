# Gemini 4 Argon · High 参照双评终结报告（2026-11-17 20:36 CST）

参照模型：Gemini 4 Argon（首选参照，`reference_gemini4argon.jsonl`，60/60 题，2026-11-17 20:00 CST 跑完）
评者：rater_a = DeepSeek V4.1 Flash，rater_b = Gemini 3.8 Flash，互盲
评分文件：`ratings_reference_gemini4argon.jsonl`（120 对有效评分；另有 15 行失败重试记录，成功记录为准）
裁决文件：`adjudication_gemini4argon.jsonl`（60 题终判）
失败案例：`failures/cases/<question_id>/<dimension>/`（58 件，各含 prediction_gemini4argon.json 与双评、裁决文件；另 2 题干净，仅有预测与双评文件）

## 终判分数（裁决后）

| 维度 | strict_hit | hallucination |
| --- | --- | --- |
| 名物 mingwu | 0/20 | 18/20 |
| 笔墨 bimo | 1/20 | 13/20 |
| 意象 yixiang | 1/20 | 14/20 |
| **合计** | **2/60（3.3%）** | **45/60（75.0%）** |

- 完全干净（strict=1 且 hallu=0）：仅 2/60（cma_135836_bimo、met_739501_yixiang）
- partial 均值 1.18/2（分布：2.0 分 7 题、1.5 分 15 题、1.0 分 33 题、0.5 分 3 题、0 分 2 题）——答案大体部分正确，strict 全中率低主因与 Carbon 线相同：每题总有一两项馆方特异事实未命中

## 双评者一致率

- strict_hit 一致 56/60（93.3%），hallucination 一致 42/60（70.0%）
- 分歧 20 题已全部裁决（adjudication_gemini4argon.jsonl，逐题有据）：rater_a 正确 11 题、rater_b 正确 9 题，无分判
- 系统性差异：rater_a 全程严于 rater_b（hallucination 51/60 vs 37/60），裁决后终值 45/60 介于两者之间、偏向 rater_a；与 Carbon 线（rater_a 45/60、rater_b 29/60、终值 41/60）、2B 线（rater_a 严于 rater_b）同一模式
- 裁决口径（与 Carbon/2B 线统一）：hallucination=1 仅当断言了与参考答案矛盾的具体事实，或无据断言了具体归属/题跋/题款/器物等可核查事实；通用笔法术语、不确定性段内的 hedges 不计幻觉；遗漏事实只扣 strict、不计幻觉

## 三线对照

| 线 | 模型 | strict_hit | hallucination | 完全干净 | partial 均值 |
| --- | --- | --- | --- | --- | --- |
| 旗舰参照 | Gemini 4 Carbon | 4/60（6.7%） | 41/60（68.3%） | 3/60 | 1.34/2 |
| 首选参照 | Gemini 4 Argon（Gemini 4 Argon · High） | 2/60（3.3%） | 45/60（75.0%） | 2/60 | 1.18/2 |
| 小模型 | InternVL2.5-2B（T4，bf16，max_num=12） | 0/60（0%） | 36/60（60.0%） | 0/60 | 0.58/2 |

三线均远低于预设的退出门槛（strict ≥85%、hallu ≤5%），停止条件不触发。Gemini 4 Argon · High 线幻觉率最高（75.0%），但三线 strict 均在 0–6.7% 区间、幻觉率均在 60–75% 区间，量级一致，缺口结论对模型与通道选择稳健。分维：三线意象 hallu 均低于名物/笔墨（Gemini 4 Argon · High 意象 14/20 vs 名物 18/20），三维难度确有分层。

## 幻觉主因有模式（Gemini 4 Argon · High 线）

- 无据的题跋/题款/印章断言（5 题）：135836_yixiang（留白处藏家印章）、41185_yixiang（引述两首题跋诗）、41462_mingwu（题款“元统三年冬”）、41468_mingwu（题诗“挂起渔竿不钓鱼”）、813350_yixiang（题款纪年/上款）
- 无据的具体建筑/器物断言（3 题）：40062_mingwu（溪桥竹篱柴门代茅屋）、62002_bimo（金线龙纹云纹、金饰冠靴，漏右上金字题识）、41468_mingwu（网格竹编船篷、短棹划行）
- 与参考答案矛盾的画面细节断言（3 题）：36178_mingwu（鹰回首向右 vs 面朝左）、78125_bimo（墨色“基本一致” vs 并不一致）、41462_mingwu（“倒挂松” vs 单株巨松盘曲而上）
- 其余为象征置换与馆方特异事实遗漏（36178_yixiang 超然物外、813350_yixiang 漏遗民拒仕清等）——与 Carbon 线同一失败模式：以模型内部知识补足画面信息

## 方法学注记

1. **缺口确认**：Gemini 4 Argon · High 终判 strict 2/60、hallu 45/60，旗舰参照亦未达标，继续推进的理由成立；三线一致，结论不依赖单一模型或通道。
2. **strict 门槛的严苛性**：与 Carbon 线相同，strict=1 要求命中全部必须事实（含馆方特异事实）；partial 均值 1.18/2 说明能力并非全无。结论见 docs/decision.md 方法学事项 1：四指标并报（strict、partial 均值、宽松命中、幻觉率），退出/达标门槛改为幻觉率 ≤5% ＋逐事实命中率 ≥85%。
3. **成本**：服务方未返回 usage 字段，成本按费率估算约 $0.008/次；双评 120 次约 $1。另有 15 次失败重试记录（均为 rater_a 流式截断/未回 [DONE]，重试后成功）。

## 状态

- Gemini 4 Argon · High 参照线全部完成（60/60 答案＋120/120 对双评＋20 题裁决＋58 件失败案例归档）。
- 8B 线后改用 int8-8bit 路径跑通 60/60（见 ratings_summary_8b.md），终判 strict 0/60、hallu 35/60。

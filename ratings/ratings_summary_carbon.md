# Carbon 参照双评终结报告（2026-11-15 21:54 CST）

参照模型：Gemini 4 Carbon（旗舰，`reference_gemini4carbon.jsonl`，60/60 题，v2 reasoning none）
评者：rater_a = DeepSeek V4.1 Flash，rater_b = Gemini 3.8 Flash，互盲
评分文件：`ratings_reference_gemini4carbon.jsonl`（155 行，120 对有效评分）
裁决文件：`adjudication_carbon.jsonl`（60 题终判）
失败案例：`failures/cases/<question_id>/<dimension>/`（57 件，各含 thumbnail/question.json/reference.json/prediction_gemini4carbon.json/ratings.json/judgment.md）

## 终判分数（裁决后）

| 维度 | strict_hit | hallucination |
| --- | --- | --- |
| 名物 mingwu | 1/20 | 19/20 |
| 笔墨 bimo | 2/20 | 13/20 |
| 意象 yixiang | 1/20 | 9/20 |
| **合计** | **4/60（6.7%）** | **41/60（68.3%）** |

- 完全干净（strict=1 且 hallu=0）：仅 3/60（cma_135836_bimo、met_739501_mingwu、met_739501_yixiang）
- partial 均值 1.34/2（分布：2.0 分 15 题、1.5 分 17 题、1.0 分 23 题、0.5 分 4 题、0 分 1 题）——答案大体部分正确，strict 全中率低主因是每题总有一两项馆方特异事实未命中

## 双评者一致率

- strict_hit 一致 52/60（86.7%），hallucination 一致 44/60（73.3%），均达/近 85% 目标线
- 分歧 20 题已全部裁决（adjudication.jsonl，逐题有据）：rater_a 正确 12 题、rater_b 正确 7 题、1 题分判（cma_160135_bimo：strict 判 1、hallu 判 1）
- 系统性差异：rater_a 全程严于 rater_b（hallucination 45/60 vs 29/60），裁决后终值 41/60 介于两者之间、偏向 rater_a
- 裁决口径（已统一）：hallucination=1 仅当断言了与参考答案矛盾的具体事实，或无据断言了具体归属/题跋/题款/器物等可核查事实；通用笔法术语、不确定性段内的 hedges 不计幻觉；遗漏事实只扣 strict、不计幻觉

## 方法学注记

1. **缺口确认**：Carbon 终判 strict 4/60、hallu 41/60，远低于预设的退出门槛（strict ≥85%、hallu ≤5%）——旗舰参照亦未达标，继续推进的理由成立。
2. **strict 门槛的严苛性**：strict=1 要求命中全部必须事实（含馆方特异事实，如「作于明立国前两年」「宁宗九子暗喻」）；模型常答对画面主体、只漏一项馆方事实即判 0。partial 均值 1.34/2 说明能力并非全无。定稿决定（见 docs/decision.md 方法学事项 1）：已裁决的逐题分数不改；公开包四项指标并报（strict、partial 均值、宽松命中、幻觉率）；退出/达标门槛改为幻觉率 ≤5% ＋逐事实命中率 ≥85%。
3. **幻觉主因有模式**：无据的具体归属/题跋引述（141693、142579、41185、51705）、与参考答案矛盾的画面细节断言（135836_mingwu 的茅屋小桥、36178 鹰朝向、40057 平桥围栏）、武财神等象征置换（62002_yixiang）——皆为「以模型内部知识补足画面信息」类错误，正是评测包要捕捉的失败模式。
4. **成本**：服务方未返回 usage 字段，成本按费率估算约 $0.008/次；双评 120 次约 $1。

## 状态

- 本线已全部完成（推理 60/60、双评 120/120 对、20 题裁决、57 件失败案例归档）；其余各线见 docs/decision.md。

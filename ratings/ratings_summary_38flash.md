# Gemini 3.8 Flash（无元数据基线）双评终结报告（2026-11-18 09:40 CST）

考生模型：Gemini 3.8 Flash（gemini-3-8-flash），无元数据条件——题干只给问题与图像，不给馆藏元数据（`reference_gemini38flash.jsonl`，60/60 题有答案）

评者：rater_a = DeepSeek V4.1 Flash，rater_b = Gemini 3.8 Flash，互盲

评分文件：`ratings_reference_38flash.jsonl`（120 对有效评分；另有 2 行历史失败记录，皆为服务容量波动，重试后全部成功）

裁决文件：`adjudication_38flash.jsonl`（60 题终判）

失败案例：`failures/cases/<question_id>/<dimension>/`（60 件全量，各含 prediction_gemini38flash.json / ratings_38flash.json / judgment_38flash.md）

## 终判分数（裁决后）

| 维度 | strict_hit | hallucination |
| --- | --- | --- |
| 名物 mingwu | 2/20 | 20/20 |
| 笔墨 bimo | 1/20 | 18/20 |
| 意象 yixiang | 1/20 | 15/20 |
| 合计 | 4/60（6.7%） | 53/60（88.3%） |

- 完全干净（strict=1 且 hallu=0）：1/60
- partial 均值 1.25/2（名物 1.12、笔墨 1.32、意象 1.30）
- 宽松命中（partial 均值 ≥1）：53/60（88.3%）

## 双评者一致率

- strict_hit 一致 54/60（90.0%），hallucination 一致 31/60（51.7%，为各线最低）
- 分歧 30 题已全部裁决（`adjudication_38flash.jsonl`，逐题有据）：rater_a 正确 23 题、rater_b 正确 4 题、split 3 题
- 系统性差异：rater_a 远严于 rater_b（hallucination 57/60 vs 28/60），裁决后终值 53/60 贴近 rater_a——rater_b 在本线系统性漏判幻觉（无据的具体笔墨名称、皴法确指、画面细节编造多未计幻觉）；终值偏向 rater_a 与五线既有规律一致
- 裁决口径（与 Carbon/2B/8B/4B/Gemini 4 Argon · High 线统一）：hallucination=1 仅当断言了与参考答案矛盾的具体事实，或无据断言了具体归属/题跋/题款/器物等可核查事实；通用笔法术语、通用文化常识性说法、不确定性段内的 hedges 不计幻觉；遗漏事实只扣 strict、不计幻觉

## 方法学注记

1. **与 Carbon 旗舰对照**：同为 60 题、strict 同为 4/60，但幻觉率 53/60（88.3%）高于 Carbon 的 41/60（68.3%）——Gemini 3.8 Flash 无元数据时比 Gemini 4 Carbon 更爱编造具体事实；partial 均值 1.25 vs Carbon 1.34，宽松命中 53/60 vs 55/60，答案完整度接近，差距在「编造」不在「答多」。
2. **幻觉率各线最高**：53/60 高于 Gemini 4 Argon · High 45/60、Carbon 41/60 与三条小模型线（35–36/60）。名物 hallu 20/20 全满——一碰具体器物/题款/归属即错；意象 15/20 仍为三维最低，意象题可用通用文化常识蒙对方向而不触具体事实，三维难度分层再次得到验证。
3. **裁决细节**：30 道分歧中 23 道判 rater_a 正确，均为 rater_b 漏判的无据断言——具体皴法确指（141693_bimo“折带/披麻化用”、40062 同类判例）、具体笔墨名称编造（135836_bimo“蟹爪/解索皴/破颜点”）、画面细节编造（142579_mingwu“独木舟、白衣文士”）、题款/印章事实断言（135836_yixiang“右上可见红印”）；4 道判 rater_b 正确，均为「遗漏≠幻觉」；split 3 题为 strict 与 hallu 各判一方。
4. **容量波动**：双评曾遇服务容量波动（2026-11-18 约 05:00–08:00）；本线 2 行失败记录皆为该窗口期，重试后全部成功；09:02 CST 终验 120/120 对。
5. **成本**：服务方未返回 usage 字段，成本按费率估算约 $0.008/次；双评 120 次约 $1。

## 元数据对照（与有元数据线配对解读）

- 同模型有元数据条件见 `ratings_summary_38flash_metadata.md`：strict 14/60、hallu 55/60、partial 均值 1.65/2。元数据使 strict 提升 4→14（名物 2→4、笔墨 1→2、意象 1→8）、partial 均值提升 1.25→1.65、宽松命中 53→59——题目可作答、可评分（元数据对照判据成立）；但幻觉率 53→55 未降——幻觉是模型内生编造问题、非信息缺失所致，给元数据也压不住。结论见 `docs/decision.md` 方法学事项 5。

# InternVL2.5-2B 双评终结报告（2026-11-15 23:12 CST）

考生模型：InternVL2.5-2B（T4，bf16，dynamic tiling max_num=12，贪心，max_new_tokens=768，词表补丁 tokenizer；`internvl2_5_2b.jsonl`，60/60 题有答案）
评者：rater_a = DeepSeek V4.1 Flash，rater_b = Gemini 3.8 Flash，互盲
评分文件：`ratings_internvl2_5_2b.jsonl`（120 对有效评分；另有 8 行 503 失败记录，已由重跑补齐）
裁决文件：`adjudication_2b.jsonl`（60 题终判）
失败案例：`failures/cases/<question_id>/<dimension>/`（60 件全量，各含 prediction_internvl2_5_2b.json / ratings_2b.json / judgment_2b.md；其中 3 件为 Carbon 线干净题，新建目录并补 thumbnail/question/reference）

## 终判分数（裁决后）

| 维度 | strict_hit | hallucination |
| --- | --- | --- |
| 名物 mingwu | 0/20 | 15/20 |
| 笔墨 bimo | 0/20 | 15/20 |
| 意象 yixiang | 0/20 | 6/20 |
| **合计** | **0/60（0%）** | **36/60（60.0%）** |

- 完全干净（strict=1 且 hallu=0）：0/60
- partial 均值 0.58/2（名物 0.40、笔墨 0.62、意象 0.72）——意象靠常识套话能沾边，名物几乎全军覆没
- 单评抽查（15 题，见 `docs/a04-2b-spotcheck-2026-11-15.md`）先行结论一致：strict 0/15，名物全硬伤

## 双评者一致率

- strict_hit 一致 60/60（100%），hallucination 一致 49/60（81.7%，低于 85% 目标线）
- 分歧 11 题已全部裁决（adjudication_2b.jsonl，逐题有据）：rater_a 正确 5 题、rater_b 正确 6 题
- 系统性差异：rater_a 全程严于 rater_b（hallucination 42/60 vs 31/60），裁决后终值 36/60 介于两者之间、偏向 rater_b
- 裁决口径（与 Carbon 线统一）：hallucination=1 仅当断言了与参考答案矛盾的具体事实，或无据断言了具体归属/题跋/题款/器物等可核查事实；通用笔法术语、不确定性段内的 hedges 不计幻觉；遗漏事实只扣 strict、不计幻觉

## 方法学注记

1. **缺口确认**：2B 终判 strict 0/60、hallu 36/60——小模型在三维上均远低于预设的退出门槛，失败模式普查的目的达到。结合 Carbon 旗舰参照 strict 4/60、hallu 41/60，缺口不在模型大小一端，而在考据类事实本身（馆方特异事实＋画面细节）。
2. **分维差异真实**：意象 hallu 仅 6/20，显著低于名物/笔墨的 15/20——意象题可用通用文化常识蒙对方向而不触具体事实；名物题一碰具体器物/题款/归属即错。这是评测包设计有效的证据：三维难度确有分层。
3. **8B 线说明**：8B 后改用 int8-8bit 路径跑通 60/60（见 ratings_summary_8b.md），终判 strict 0/60、hallu 35/60，与 2B 同档。
4. **成本**：服务方未返回 usage 字段，成本按费率估算约 $0.008/次；双评 120 次约 $1。评分中 rater_a 遇 8 次 503（均重试后补齐），属容量波动。

## 状态

- 本线已全部完成（推理 60/60、双评 120/120 对、11 题裁决、60 件失败案例归档）；其余各线见 docs/decision.md。

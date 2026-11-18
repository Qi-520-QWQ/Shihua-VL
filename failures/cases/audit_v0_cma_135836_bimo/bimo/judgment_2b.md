# 失败案例 audit_v0_cma_135836_bimo（bimo）——InternVL2.5-2B

- 作品：cma_135836（Buddhist Retreat by Stream and Mountains，Buddhist Retreat by Stream and Mountains (溪山蘭若圖), 960–85，960–85）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

远山用了何种墨法表现云雾缭绕？近景树木与远山的用笔有何不同？

## 参考答案（锁定 v0）

远山以淡墨晕染表现，山间云雾主要靠留白与墨色渐淡衬托，视觉笔记所见即淡墨渲染加云气留白，馆方未就远山墨法另作专门说明。用笔上，馆方描述山体以长披麻皴（长麻纤维状线条）皴出质感，并辅以湿点与山顶圆石；近景树木墨色较浓、用笔肯定，远山则墨色清淡、以渲染为主，浓淡与虚实对比拉开前后空间。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

远山用了“泼墨法”表现云雾缭绕，而近景树木则用了“点景法”。

## 评者 notes

- rater_a：回答称远山用泼墨法、近景树木用点景法，均无参考答案支持，且未命中任何必须事实，属于编造事实。
- rater_b：完全未命中任何必须事实，且凭空编造了“泼墨法”与“点景法”。

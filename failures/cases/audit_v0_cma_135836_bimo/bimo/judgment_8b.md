# 失败案例 audit_v0_cma_135836_bimo（bimo）——InternVL2.5-8B

- 作品：cma_135836（Buddhist Retreat by Stream and Mountains，Buddhist Retreat by Stream and Mountains (溪山蘭若圖), 960–85，960–85）
- 考生模型：InternVL2.5-8B (int8)（T4，int8-8bit，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.5
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

远山用了何种墨法表现云雾缭绕？近景树木与远山的用笔有何不同？

## 参考答案（锁定 v0）

远山以淡墨晕染表现，山间云雾主要靠留白与墨色渐淡衬托，视觉笔记所见即淡墨渲染加云气留白，馆方未就远山墨法另作专门说明。用笔上，馆方描述山体以长披麻皴（长麻纤维状线条）皴出质感，并辅以湿点与山顶圆石；近景树木墨色较浓、用笔肯定，远山则墨色清淡、以渲染为主，浓淡与虚实对比拉开前后空间。

## 8B 回答（全文见 prediction_internvl2_5_8b.json）

这幅中国古画运用了“披麻皴”技法来表现远山的云雾缭绕。近景树木的用笔较为细腻，线条较为清晰，而远山的用笔则较为简略，线条较为模糊，以表现远近的空间感。

## 评者 notes

- rater_a：把披麻皴用于远山云雾表现，既未命中淡墨晕染与云雾留白等必须事实，也无近景浓远山淡的对比，属对技法对象的错误断言。
- rater_b：错误将披麻皴当作表现云雾的墨法，遗漏了淡墨晕染、留白衬托及墨色浓淡对比等核心事实。

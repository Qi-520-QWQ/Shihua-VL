# 失败案例 audit_v0_met_39547_mingwu（mingwu）——MiniCPM-V-2_6-int4

- 作品：met_39547（Bamboo, old tree, and rock，Wu Zhen，dated 1338）
- 考生模型：MiniCPM-V-2_6-int4 (int4)（T4，int4，max_slice_nums=9，transformers 4.49.0）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.5
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面中竹、石、兰各占何处？三者的组合在中国画中被称为什么题材？

## 参考答案（锁定 v0）

题干预设「竹、石、兰」三者有误：本幅并无兰花，实为枯木竹石题材。据画面，左侧中部为一丛竹叶，右上方是虬曲枯干、枝叶下垂的老树，下部中央为大石块，下部两角仅有些细叶小草，不构成兰花主体。此类组合在画史上称「枯木竹石」，由十一世纪文人画家确立典范，吴镇此图即其创造性变体。

## MiniCPM-V-2_6-int4 回答（全文见 prediction_minicpm_v26.json）

这幅画中的竹子位于画面的左侧和中间部分，石头位于画面的底部，兰花则在石头的右侧。在中国画中，竹、石、兰的组合被称为“岁寒三友”，象征着坚韧和高洁的品格。

## 评者 notes

- rater_a：虽提到竹在左侧、石在底部，但错误断言有兰花并将题材称为“岁寒三友”，未命中枯木竹石及树木位置等关键事实。
- rater_b：顺从了题干的错误预设，编造兰花在石头右侧并误称为岁寒三友，触发了禁止断言，关键事实几乎全未命中。

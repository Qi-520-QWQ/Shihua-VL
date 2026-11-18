# 失败案例 audit_v0_met_40062_yixiang（yixiang）——InternVL2.5-2B

- 作品：met_40062（Hermitage by a pine-covered bluff，Yan Ciyu，second half 12th century）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=0，partial 均值=1.0
- 双评者：rater_a strict=0/hallu=0；rater_b strict=0/hallu=0
- 裁决：双评者一致，无分歧

## 题干

隐居于松石之间的画面传达了怎样的士人理想？

## 参考答案（锁定 v0）

画面以松崖、茅屋、溪流与空阔水面构成幽僻之境：松树覆崖、崖顶松枝俯垂，小茅屋隐于石树之间，前临溪流，左侧一片空明水景与远岸礁石。这种「松壑隐栖」的图式寄托士人避世高蹈、以山林为归的理想，松象征岁寒坚贞与高士品格，茅舍点出栖隐生活，传达出远离尘嚣、寄情山水的心境。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

这幅画描绘了隐士与自然和谐共处的场景，传达了隐士理想中与自然和谐共处的生活。

## 评者 notes

- rater_a：仅笼统提到隐士与自然和谐，命中避世隐逸意境，但未明确茅屋栖隐、松象征坚贞及寄情山水等关键事实，未达全对。
- rater_b：仅泛泛提及隐士理想，遗漏了松象征坚贞品格、茅屋点出栖隐生活及幽僻山林之境等关键事实。

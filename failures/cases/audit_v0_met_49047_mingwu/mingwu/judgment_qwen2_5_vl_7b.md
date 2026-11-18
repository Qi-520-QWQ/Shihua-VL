# 失败案例 audit_v0_met_49047_mingwu（mingwu）——Qwen2.5-VL-7B

- 作品：met_49047（Rock, Tiger Lily and Orchid，Unidentified，dated 1627）
- 考生模型：Qwen2.5-VL-7B (4bit)（T4，4bit，max_num=1280，transformers 4.49.0）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.5
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面左上方有一段题款，写明了作者与作画时间。请读出题款的大意，并据此判断这幅画的作者身份与年代。

## 参考答案（锁定 v0）

题款大意是「丁卯夏日天水赵氏文淑写」，即自称赵文淑（文俶）在丁卯年（1627）夏日作画。但馆方著录此轴为「仿赵文俶 萱石图」，作者为佚名（Unidentified artist / After Zhao Wenchu），并指出画面笔法欠精，很可能是后世众多仿赵氏风格者之一所作。因此题款只能说明画上标称的作者与纪年，不能据此判定它是文俶真迹；年代上限依款为1627年，实际绘制时间可能更晚。

## Qwen2.5-VL-7B 回答（全文见 prediction_qwen2_5_vl_7b.json）

大意：丁卯夏日天水赵氏文仲画。
作者身份：赵氏文仲。
年代：丁卯年，即公元17
 addCriterion

 addCriterion

 addCriterion

 addCriterion

 addCriterion

 addCriterion

 addCriterion

 addCriterion

 addCriterion

 addCriterion

 addCriterion

## 评者 notes

- rater_a：将题款中的文淑误读为文仲，且未说明馆方著录为佚名仿赵文俶及疑为后人仿作；年代回答也不完整。
- rater_b：释读错误（误作文仲），未提及馆方著录为仿作及佚名等关键事实，且回答截断并伴有乱码异常。

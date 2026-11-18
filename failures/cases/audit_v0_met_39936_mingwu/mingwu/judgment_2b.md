# 失败案例 audit_v0_met_39936_mingwu（mingwu）——InternVL2.5-2B

- 作品：met_39936（Finches and bamboo，Emperor Huizong，early 12th century）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面中的禽鸟有几只、分别栖于何处？画面中竹子的画法与鸟的种类指向哪一类花鸟画传统？

## 参考答案（锁定 v0）

画面中有两只禽鸟，左上的一只栖于竹枝上向右，中下偏右的一只栖于竹枝上向左，两鸟相向而立。竹子从右侧石壁生出，枝叶向左伸展，右侧有湖石。禽鸟为小型雀类，属花鸟画中的翎毛一路，配合竹石构成宋代院体花鸟画常见题材；馆方描述指出此作体现徽宗画院写实风格的花鸟画传统。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

画面中有三只禽鸟，分别栖于左上、中下和右上的树枝。竹子的画法与鸟的栖枝指向了“写意花鸟”的传统。

## 评者 notes

- rater_a：回答称三只禽鸟且栖于右上树枝，属禁止断言与编造；又误判为写意花鸟传统，未命中任何必须事实。
- rater_b：触发禁止断言（称有三只禽鸟），禽鸟数量、位置及所属花鸟传统（误作写意花鸟）均答错。

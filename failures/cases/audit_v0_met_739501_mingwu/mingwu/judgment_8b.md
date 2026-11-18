# 失败案例 audit_v0_met_739501_mingwu（mingwu）——InternVL2.5-8B

- 作品：met_739501（Zhou Dunyi Admiring Lotuses，Lu Peng，dated 1896）
- 考生模型：InternVL2.5-8B (int8)（T4，int8-8bit，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=1.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面中人物的身份与动作是什么？莲花在画面中占何位置？

## 参考答案（锁定 v0）

画中人为北宋学者周敦颐（1017—1073），他安坐于园石之上，手持团扇，面向右侧莲池，凝神观赏盛开的莲花。莲花集中在画面右下，莲叶成丛，间有淡粉、白色花朵数朵，生于右缘虬曲树干脚下，并非满幅铺开。

## 8B 回答（全文见 prediction_internvl2_5_8b.json）

这幅画描绘了一位古代文人，他坐在岩石上，手持镜子，似乎在整理仪容。这种姿态常见于文人雅士，象征着对自我形象的关注和修养。

莲花位于画面的右下角，作为点缀，增加了画面的自然美感。

## 评者 notes

- rater_a：仅命中莲花位于右下角；人物身份、持团扇、观莲、莲花生于树干脚下均未命中，且将团扇误作镜子属编造事实。
- rater_b：命中坐石及莲花在右下角，但未识别出周敦颐，且将手持团扇观莲误判为手持镜子整理仪容。

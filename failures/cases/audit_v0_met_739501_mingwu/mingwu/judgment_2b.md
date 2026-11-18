# 失败案例 audit_v0_met_739501_mingwu（mingwu）——InternVL2.5-2B

- 作品：met_739501（Zhou Dunyi Admiring Lotuses，Lu Peng，dated 1896）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面中人物的身份与动作是什么？莲花在画面中占何位置？

## 参考答案（锁定 v0）

画中人为北宋学者周敦颐（1017—1073），他安坐于园石之上，手持团扇，面向右侧莲池，凝神观赏盛开的莲花。莲花集中在画面右下，莲叶成丛，间有淡粉、白色花朵数朵，生于右缘虬曲树干脚下，并非满幅铺开。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

画面中的人物是画家，正在磨墨。莲花位于画面左侧。

## 评者 notes

- rater_a：人物身份与动作错误（称画家磨墨，非周敦颐观莲），莲花位置错误（称左侧，非右下），含编造事实与禁止断言。
- rater_b：人物身份、动作及莲花位置全部答错，且存在严重的事实编造。

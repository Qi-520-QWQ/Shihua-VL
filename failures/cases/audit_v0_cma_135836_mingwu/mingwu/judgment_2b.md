# 失败案例 audit_v0_cma_135836_mingwu（mingwu）——InternVL2.5-2B

- 作品：cma_135836（Buddhist Retreat by Stream and Mountains，Buddhist Retreat by Stream and Mountains (溪山蘭若圖), 960–85，960–85）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面下方的溪流边有哪些建筑？结合题名，这些建筑最可能是什么性质的处所？

## 参考答案（锁定 v0）

画面下方溪流边的树丛间只有极小的建筑数间，几不可辨，具体间数与形制无法精确确认，也未见馆方文字对这些建筑作直接描述。结合题名「溪山蘭若圖」，「蘭若」为佛寺、僧舍的通称，且馆方说明本幅作者巨然为僧、承续江南山水传统，故这些建筑最可能是溪畔佛寺（兰若）一类的宗教处所，而非普通民居或亭榭。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

画面中溪流边有亭子。根据题名，这些建筑可能是茶馆。

## 评者 notes

- rater_a：回答将建筑说成亭子、茶馆，未命中「极小不可辨」「蘭若即佛寺」等事实，且编造茶馆性质，属禁止断言。
- rater_b：未命中任何必须事实，且无端猜测建筑为亭子和茶馆，完全未涉及“兰若”的佛寺性质。

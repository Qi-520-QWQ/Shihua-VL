# 失败案例 audit_v0_cma_135836_mingwu（mingwu）——InternVL2.5-8B

- 作品：cma_135836（Buddhist Retreat by Stream and Mountains，Buddhist Retreat by Stream and Mountains (溪山蘭若圖), 960–85，960–85）
- 考生模型：InternVL2.5-8B (int8)（T4，int8-8bit，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面下方的溪流边有哪些建筑？结合题名，这些建筑最可能是什么性质的处所？

## 参考答案（锁定 v0）

画面下方溪流边的树丛间只有极小的建筑数间，几不可辨，具体间数与形制无法精确确认，也未见馆方文字对这些建筑作直接描述。结合题名「溪山蘭若圖」，「蘭若」为佛寺、僧舍的通称，且馆方说明本幅作者巨然为僧、承续江南山水传统，故这些建筑最可能是溪畔佛寺（兰若）一类的宗教处所，而非普通民居或亭榭。

## 8B 回答（全文见 prediction_internvl2_5_8b.json）

画面下方的溪流边有一些亭子或房屋。结合题名“溪山行旅图”，这些建筑最可能是供旅行者休息或观赏风景的处所。

## 评者 notes

- rater_a：将题名误作「溪山行旅图」并断言建筑为旅行者休息处所，未命中任何必须事实，且含禁止断言（编造性质/题名）。
- rater_b：题名误作《溪山行旅图》，未指出建筑极小几不可辨，且完全未命中“兰若”为佛寺僧舍及建筑属宗教处所的事实。

# 失败案例 audit_v0_cma_135836_mingwu（mingwu）——InternVL2.5-4B

- 作品：cma_135836（Buddhist Retreat by Stream and Mountains，Buddhist Retreat by Stream and Mountains (溪山蘭若圖), 960–85，960–85）
- 考生模型：InternVL2.5-4B (bf16)（T4，bf16，max_num=12，词表直取仓库 Qwen2Tokenizer，无补丁）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.5
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面下方的溪流边有哪些建筑？结合题名，这些建筑最可能是什么性质的处所？

## 参考答案（锁定 v0）

画面下方溪流边的树丛间只有极小的建筑数间，几不可辨，具体间数与形制无法精确确认，也未见馆方文字对这些建筑作直接描述。结合题名「溪山蘭若圖」，「蘭若」为佛寺、僧舍的通称，且馆方说明本幅作者巨然为僧、承续江南山水传统，故这些建筑最可能是溪畔佛寺（兰若）一类的宗教处所，而非普通民居或亭榭。

## 8B 回答（全文见 prediction_internvl2_5_4b.json）

这幅画的下方溪流边有几座小屋和桥梁。结合题名来看，这些建筑可能是一个隐士的居所或道观。画中的山水和建筑风格也符合隐逸或道家修行的意境。

## 评者 notes

- rater_a：回答将建筑臆断为隐士居所或道观，未提'蘭若'即佛寺，且含'桥梁'等不支持的编造事实，故不得分。
- rater_b：完全未命中必须事实，未能结合题名指出「兰若」为佛寺僧舍，且臆测为隐士居所或道观，并编造了桥梁。

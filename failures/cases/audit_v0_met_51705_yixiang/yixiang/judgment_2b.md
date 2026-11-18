# 失败案例 audit_v0_met_51705_yixiang（yixiang）——InternVL2.5-2B

- 作品：met_51705（Horse and groom，Unidentified artist，16th century）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

牵马人物与马的组合在古代绘画中常有何种寓意？

## 参考答案（锁定 v0）

馆方未就牵马人物与马的组合给出寓意说明，仅称其母本为八世纪唐画、风格属十六世纪，且题款与印章真伪杂糅。画史通识中，圉人与骏马常象征相马识才、贤才待遇，或用于表现贡马与异域人物来朝。本题只能作通识性说明，不能视为本件馆方定论。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

这幅画描绘了牵马的人物与马的组合，这在古代绘画中通常象征着权势、威严或贵族身份。

## 评者 notes

- rater_a：回答未提及馆方未给出寓意说明，也未命中圉人骏马喻相马识才或贡马来朝的通识；'象征权势、威严或贵族身份'缺乏参考答案支持，属编造事实。
- rater_b：未提及馆方未提供寓意说明，且编造了权势、威严等参考答案未支持的寓意，必须事实均未命中。

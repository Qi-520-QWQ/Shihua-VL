# 失败案例 audit_v0_met_51705_yixiang（yixiang）——InternVL2.5-4B

- 作品：met_51705（Horse and groom，Unidentified artist，16th century）
- 考生模型：InternVL2.5-4B (bf16)（T4，bf16，max_num=12，词表直取仓库 Qwen2Tokenizer，无补丁）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

牵马人物与马的组合在古代绘画中常有何种寓意？

## 参考答案（锁定 v0）

馆方未就牵马人物与马的组合给出寓意说明，仅称其母本为八世纪唐画、风格属十六世纪，且题款与印章真伪杂糅。画史通识中，圉人与骏马常象征相马识才、贤才待遇，或用于表现贡马与异域人物来朝。本题只能作通识性说明，不能视为本件馆方定论。

## 8B 回答（全文见 prediction_internvl2_5_4b.json）

这幅画中牵马人物与马的组合常寓意“马上”或“马上权”，象征权力、威严和军事力量。古代绘画中，马常被用来象征帝王的权威和军事力量，而人物牵马则进一步强化了这种象征意义。

## 评者 notes

- rater_a：回答未命中参考答案要求的馆方未提供寓意及圉人骏马通识寓意，反而编造“马上权”等无据说法，属幻觉。
- rater_b：完全未提及馆方未提供说明，亦未命中相马识才或贡马来朝等通识，且编造了“马上权”、军事力量等未经参考答案支持的寓意。

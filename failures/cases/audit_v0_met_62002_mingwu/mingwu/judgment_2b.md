# 失败案例 audit_v0_met_62002_mingwu（mingwu）——InternVL2.5-2B

- 作品：met_62002（Guan Yu，Unidentified artist，ca. 1700）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面中人物的服饰、兵器与面容特征指向哪位历史人物？有哪些可辨认的标志？

## 参考答案（锁定 v0）

画中人物是关羽（卒于公元219年），即后世尊称的关帝、关圣帝君。可辨认的标志有：绿袍、长髯、蓝色头巾、偏红面色，手持青龙偃月刀（长柄、青色大刀、红缨），头后有光晕；身侧有两名从者，一为红袍文官样人物拱手侍立，一为戴红缨盔着甲的武将。画面右上有金字题识“監門關聖帝君”，即馆方所述“Overseer of the Gate, Sage-Emperor Lord Guan”，据此可确认身份。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

这幅画描绘的是文成公主的形象。服饰和剑具有典型的唐朝风格，面容特征包括胡须和头饰。标志包括服饰上的纹饰和头饰上的红色装饰。

## 评者 notes

- rater_a：回答误认人物为文成公主，未命中任何必须事实，且编造唐朝风格等画面不支持内容。
- rater_b：回答完全错误，将关羽误识为文成公主，且服饰兵器等特征描述纯属捏造，未命中任何必须事实。

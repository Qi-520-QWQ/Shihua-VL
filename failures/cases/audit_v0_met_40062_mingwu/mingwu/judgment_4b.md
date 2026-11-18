# 失败案例 audit_v0_met_40062_mingwu（mingwu）——InternVL2.5-4B

- 作品：met_40062（Hermitage by a pine-covered bluff，Yan Ciyu，second half 12th century）
- 考生模型：InternVL2.5-4B (bf16)（T4，bf16，max_num=12，词表直取仓库 Qwen2Tokenizer，无补丁）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面中松树下的建筑是什么形制？画面中山石与树木的组合指向哪个时代的山水样式？

## 参考答案（锁定 v0）

松树覆盖的陡崖崖脚、中下偏右处有一座小茅屋，隐于石树之间，屋前有溪流，即所谓隐栖之所，形制为简朴茅舍而非楼阁寺观。画面右侧为松崖，左侧为开阔水面与远岸礁石，属南宋院体山水常见的边角式构图与松石组合样式；馆方据风格将作者定为阎次于（阎次平之弟），其父阎仲及兄弟于1160年代供职孝宗画院。

## 8B 回答（全文见 prediction_internvl2_5_4b.json）

这幅画中松树下的建筑是亭子的形制。画面中山石与树木的组合指向了宋代的山水样式。

## 评者 notes

- rater_a：回答将建筑误判为亭子，未命中茅屋、崖脚位置、溪流、边角式南宋院体及阎次于等关键事实，且‘宋代山水样式’过于笼统，构成错误断言。
- rater_b：建筑形制误答为亭子（实为小茅屋），时代仅泛指宋代而未命中南宋院体边角式样式，遗漏几乎所有必须事实。

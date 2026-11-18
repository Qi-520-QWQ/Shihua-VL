# 失败案例 audit_v0_met_40062_mingwu（mingwu）——Qwen2.5-VL-7B

- 作品：met_40062（Hermitage by a pine-covered bluff，Yan Ciyu，second half 12th century）
- 考生模型：Qwen2.5-VL-7B (4bit)（T4，4bit，max_num=1280，transformers 4.49.0）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面中松树下的建筑是什么形制？画面中山石与树木的组合指向哪个时代的山水样式？

## 参考答案（锁定 v0）

松树覆盖的陡崖崖脚、中下偏右处有一座小茅屋，隐于石树之间，屋前有溪流，即所谓隐栖之所，形制为简朴茅舍而非楼阁寺观。画面右侧为松崖，左侧为开阔水面与远岸礁石，属南宋院体山水常见的边角式构图与松石组合样式；馆方据风格将作者定为阎次于（阎次平之弟），其父阎仲及兄弟于1160年代供职孝宗画院。

## Qwen2.5-VL-7B 回答（全文见 prediction_qwen2_5_vl_7b.json）

画面中松树下的建筑是亭子形制。画面中山石与树木的组合指向宋元时期的山水样式。

## 评者 notes

- rater_a：将建筑说成亭子，与参考答案的小茅屋不符；“宋元时期”未命中南宋院体边角式样，且作者信息缺失。
- rater_b：建筑形制误答为亭子，未指出茅舍；时代样式泛称宋元，未命中南宋院体边角式构图等核心事实。

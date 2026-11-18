# 失败案例 audit_v0_met_739501_yixiang（yixiang）——Qwen2.5-VL-3B

- 作品：met_739501（Zhou Dunyi Admiring Lotuses，Lu Peng，dated 1896）
- 考生模型：Qwen2.5-VL-3B (bf16)（T4，bf16，max_num=1280，transformers 4.49.0）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

赏莲人物在中国画中常与哪位历史人物及何种品格相联系？

## 参考答案（锁定 v0）

赏莲人物对应北宋周敦颐，他作《爱莲说》，以莲自况。莲花出淤泥而不染、濯清涟而不妖，故在中国画中与君子洁身自好、不慕荣利、特立独行的品格相联系；周敦颐赏莲图即以此寄寓高洁自守之志，晚清上海画家亦常取此题材。

## Qwen2.5-VL-3B 回答（全文见 prediction_qwen2_5_vl_3b.json）

赏莲人物在中国画中常与陶渊明及隐逸品格相联系。

## 评者 notes

- rater_a：将赏莲人物误说为陶渊明，触犯禁止断言，且未命中周敦颐及莲喻君子的关键事实。
- rater_b：回答将赏莲人物错误断言为陶渊明（触碰禁止断言），未命中任何必须事实。

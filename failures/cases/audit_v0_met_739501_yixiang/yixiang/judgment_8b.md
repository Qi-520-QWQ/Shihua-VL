# 失败案例 audit_v0_met_739501_yixiang（yixiang）——InternVL2.5-8B

- 作品：met_739501（Zhou Dunyi Admiring Lotuses，Lu Peng，dated 1896）
- 考生模型：InternVL2.5-8B (int8)（T4，int8-8bit，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=0，partial 均值=2.0
- 双评者：rater_a strict=0/hallu=0；rater_b strict=0/hallu=0
- 裁决：双评者一致，无分歧

## 题干

赏莲人物在中国画中常与哪位历史人物及何种品格相联系？

## 参考答案（锁定 v0）

赏莲人物对应北宋周敦颐，他作《爱莲说》，以莲自况。莲花出淤泥而不染、濯清涟而不妖，故在中国画中与君子洁身自好、不慕荣利、特立独行的品格相联系；周敦颐赏莲图即以此寄寓高洁自守之志，晚清上海画家亦常取此题材。

## 8B 回答（全文见 prediction_internvl2_5_8b.json）

这幅画中的赏莲人物常与周敦颐相联系，他因《爱莲说》而闻名，象征着高洁、清雅的品格。

## 评者 notes

- rater_a：命中周敦颐、《爱莲说》及高洁品格，但未明确写出淤泥而不染与洁身自好、不慕荣利等核心表述，未达全部必须事实。
- rater_b：命中了周敦颐、《爱莲说》及高洁品格，但遗漏了莲花“出淤泥而不染”这一必须事实。

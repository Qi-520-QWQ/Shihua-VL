# 失败案例 audit_v0_met_739501_yixiang（yixiang）——InternVL2.5-2B

- 作品：met_739501（Zhou Dunyi Admiring Lotuses，Lu Peng，dated 1896）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=0，partial 均值=0.0
- 双评者：rater_a strict=0/hallu=0；rater_b strict=0/hallu=0
- 裁决：双评者一致，无分歧

## 题干

赏莲人物在中国画中常与哪位历史人物及何种品格相联系？

## 参考答案（锁定 v0）

赏莲人物对应北宋周敦颐，他作《爱莲说》，以莲自况。莲花出淤泥而不染、濯清涟而不妖，故在中国画中与君子洁身自好、不慕荣利、特立独行的品格相联系；周敦颐赏莲图即以此寄寓高洁自守之志，晚清上海画家亦常取此题材。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

赏莲人物在中国画中常与隐士相关，特别是文人隐士。这类人物通常被描绘在宁静的自然环境中，与自然和谐共处，体现了中国文人对隐逸生活的向往。

## 评者 notes

- rater_a：回答只泛泛谈隐士与隐逸，未命中周敦颐、《爱莲说》、出淤泥而不染及君子洁身自好等任一必须事实，也未出现禁止断言。
- rater_b：未提及周敦颐、《爱莲说》、出淤泥而不染及君子洁身自好等任何必须命中的事实，泛泛而谈隐逸生活。

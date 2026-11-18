# 失败案例 audit_v0_cma_160135_mingwu（mingwu）——InternVL2.5-2B

- 作品：cma_160135（Fishermen-Hermits in Stream and Mountain，Fishermen-Hermits in Stream and Mountain (溪山漁隱圖), 1300s，1300s）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=1，partial 均值=0.5
- 双评者：rater_a strict=0/hallu=1；rater_b strict=0/hallu=1
- 裁决：双评者一致，无分歧

## 题干

画面中渔隐人物的舟船、钓具与居所有何特征？山水环境指向何种地域？

## 参考答案（锁定 v0）

画面中部为大面积留白的江面，两岸分江。可见篷船：中左近岸一篷船上坐着一位红袍渔人，持短竿垂钓；左缘中部另有一叶小舟，人影不甚清晰。馆方描述称渔人各坐船尾、持装线轴的短竿在水中垂钓，但视觉上钓钩与线轴细节难以辨认。近岸有高树数株与石块，篷船带篷盖。山水为两岸夹江、远山淡墨的江南景致，馆方指出此类图景即赵氏等文人心中江南家乡，故地域指向江南。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

画面中渔隐人物的舟船、钓具与居所有竹制简篷，钓具包括钓竿与鱼网，居所有茅草屋。山水环境指向江南地区，表现宁静的湖泊与山丘。

## 评者 notes

- rater_a：未命中红袍渔人、短竿、左缘小舟、馆方线轴说明等必须事实，且编造竹制简篷、鱼网、茅草屋等参考答案不支持的内容。
- rater_b：仅命中山水指向江南，遗漏了绝大部分核心事实，且臆造了鱼网与茅草屋等参考答案中没有的要素。

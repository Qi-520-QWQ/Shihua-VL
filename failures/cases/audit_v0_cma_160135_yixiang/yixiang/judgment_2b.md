# 失败案例 audit_v0_cma_160135_yixiang（yixiang）——InternVL2.5-2B

- 作品：cma_160135（Fishermen-Hermits in Stream and Mountain，Fishermen-Hermits in Stream and Mountain (溪山漁隱圖), 1300s，1300s）
- 考生模型：InternVL2.5-2B（T4，bf16，max_num=12，词表补丁 tokenizer）
- 终判：strict_hit=0，hallucination=0，partial 均值=1.0
- 双评者：rater_a strict=0/hallu=0；rater_b strict=0/hallu=0
- 裁决：双评者一致，无分歧

## 题干

渔隐于山水之间的画面寄托了怎样的出世理想？

## 参考答案（锁定 v0）

此图将文人置于江南山水间垂钓，寄托避世隐居、以渔为隐的出世理想：两岸夹江、江面空阔，远山淡墨、留白浩渺，营造远离尘嚣的清远之境；篷船短竿、红袍点景，写渔人悠然自适的江湖生涯。馆方指出赵雍之父赵孟頫等文人喜绘自身作渔人徜徉江南，他们视江南为家园，故渔隐既是归乡之思，也是不慕荣利、寄情山水的人格自许。

## 2B 回答（全文见 prediction_internvl2_5_2b.json）

这幅画描绘渔隐在山水之间的生活，寄托了出世理想，即远离尘世喧嚣，追求宁静与隐逸。画中的渔舟和渔夫暗示了这种生活方式，与自然和谐共处，远离世俗的烦扰。

## 评者 notes

- rater_a：仅命中避世隐居、渔隐出世的理想，未提及江南为文人家园及馆方关于赵氏文人自绘渔人的说法，故未达全对。
- rater_b：命中了避世隐居的出世理想，但遗漏了江南作为家园的归乡之思及馆方关于赵氏文人画渔考据的核心事实。

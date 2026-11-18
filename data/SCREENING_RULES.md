# 选图硬规矩

候选池实测很脏：通用查询首批混入日本江户绘本、琉球漆盒、中国陶瓷茶壶、无主图条目。以下规矩是硬过滤，任何一条不过即剔除，不许「差不多」放行。

## 硬过滤（逐件全过才可入选）
1. **国别**：culture 字段为 China 或 Chinese；Japan、Korea、Ryūkyū、Tibet 等一律剔除（「Chinese-Style」的日韩器物也剔除）。
2. **类别**：classification 必须严格等于 Paintings；Illustrated Books、Lacquer、Ceramics、Textiles、Metalwork 等一律剔除。成对器物（title 含 "pair with"）剔除。
3. **主图**：primaryImage 非空；下载原图后实测像素，长边 ≥2000px 才算高清达标，不达标剔除（不得用 primaryImageSmall 充数）。
4. **授权**：isPublicDomain/CC0 标记为真，且在 items.jsonl 记录证据字段；标记缺失或不明的剔除。
5. **朝代归属**：dynasty 字段为空是常态，必须用 period＋objectDate＋objectBeginDate/objectEndDate 交叉定代——以年代区间中点落入的朝代为准入桶；仅靠搜索词命中不算数。明清仿古、托款、「in the style of / after / follower of」前代的作品，按其实际创作年代入桶，并在条目中如实记录 attribution 原文，不得按题材风格归入被仿朝代。
6. **去重**：按 objectID 唯一；同一作品在多个朝代查询里重复出现的只留一条。
7. **分层配额**：宋元明清各 5 件；题材山水 8／人物 6／花鸟 6。题材判定依据 title＋tags＋画面目检三者一致，单一字段猜测不算数；判定不了题材的剔除，不硬凑配额。
8. **可出题性**：每件入选作品须在画面或元数据中有可核查的出题点（题跋/钤印/款识文字、作者、年代、材质形制登记信息）；只有泛泛「好看」的剔除。

## 复核关（逐件验收，不过不锁定）
- items.jsonl 写完后先标 draft，不得直接标完成；逐件对照本规矩复核（国别/类别/朝代/授权/图清晰度）并抽查原图，复核记录落盘后才算锁定。
- 参考答案只能来自该件的馆藏元数据字段与可核文献，逐条注出处；元数据没有的信息不许补写。

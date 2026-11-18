# Shihua-VL 查重记录（2026-11-15，正式版 v1，查重已完成）

方法：网页搜索（中/英）＋ HuggingFace Hub API 直接查询（models / datasets，关键词 chinese painting）。
注意：这是初步扫查，不算穷尽；正式查重还需补 ModelScope、GitHub、论文库（arXiv/Semantic Scholar）与更多关键词（古画/书画/国画/皴法/painting connoisseurship 等）。

## 直接结论（初步）
未发现与 Shihua-VL 等价的开源成果：没有「基于大参数 VLM 微调、专做中国古画名物考据＋笔墨技法＋诗画意象」的开源权重，也没有专家考据级问答数据集。发现的是邻近工作，逐项如下。

## 邻近工作清单
1. **kaupane/chinese-painting-collection（HF 数据集，重点核查对象）**
   - 91,093 张中国绘画图像，带 VLM 生成的图注（中英、长短各一至三条）、书法 OCR 转写、视角分类、外来物检测与裁剪框；来源含台北故宫（npm_tw）等。
   - 与 Shihua 的差别：图注是 VLM 自动生成、未经专家考据校验；任务是 caption/OCR/分类，不是皴法辨识、名物断代、诗画意象的问答与评测；且未见配套的微调 VLM 权重。
   - **许可核对（2026-11-15 已完成，数据集卡 Licensing 节逐字核对）**：图像保留各来源许可——台北故宫 NPM 部分 86,321 张为 Taiwan Open Government Data License v1（须署名國立故宮博物院）；Met 1,186 张 CC0；Freer/Smithsonian 1,782 张 CC0；Art Institute of Chicago 173 张 CC0；Princeton 1,631 张「Check source terms; intended for research use」（条款未明示、不宜直接再分发）。标注层（图注、OCR、分类、裁剪框）为 **CC-BY-4.0**。图注由 gemini-3.5-flash-lite 与 DeepSeek V4.1 Flash 多轮生成，卡片明言有错漏（尤以草书 OCR 为甚）、65 行无图注、detail 视图可能与同物件 full 视图重复。HF 页面「Models trained or fine-tuned on」一栏为空——无任何模型以此集微调。
   - 对项目的影响：可作数据底料候选（省去部分图像收集），但替代不了专家考据标注层；**图像并非统一 CC0**——95% 的图是 NPM 的 OGDL v1（可再分发但须署名，非 CC0），选图若要纯 CC0 集只能取 Met/FSG/AIC 三家约 3,141 张，或接受 NPM 署名条款；标注文本 CC-BY-4.0 可用（须署名）。
2. **CulTi（arXiv 2505.10921）**：5,726 图文对，古代丝绸＋敦煌壁画，任务是跨模态检索（微调 Chinese-CLIP + LACLIP），非生成式 VLM、非绘画考据。
3. **HCSU（HF 数据集 YAN-LIU05/HCSU，ECCV 2026）**：39,307 张高清汉字图像，细粒度**书法**风格理解数据集＋基准；对象是单字书法，不是整幅古画的器物/技法/意象。
4. **AC-EVAL（HF 数据集 yuting-wei/aceval）**：古汉语理解纯文本评测（含艺术文化遗产选择题），无图像。
5. **ZuantuSet（CHI 2025，arXiv 2502.19093）**：71K 历史可视化＋108K 插图，数字人文分析用，非 VLM 训练集。
6. **HF 上 chinese painting 名下模型**：均为文生图生成向（SD textual inversion / dreambooth / ink painting 生成），与「理解/考据」方向无关。

## 待补（正式查重）
- [x] 打开 kaupane 数据集卡：许可全文、来源清单、图注生成所用模型、是否有专家校验（2026-11-15 完成：图像分来源许可，NPM OGDL v1 须署名、Met/FSG/AIC CC0、Princeton 条款未明；标注 CC-BY-4.0；图注由 gemini-3.5-flash-lite＋DeepSeek V4.1 Flash 生成、无专家校验）
- [x] ModelScope 同关键词扫查（2026-11-15 完成：官方 API 五关键词直查仅 2 命中，均为近乎空白的占位数据集；模型侧站内检索 0 命中）
- [x] GitHub 搜索：ancient chinese painting vlm / guhua / shihua 等（2026-11-15 完成：无等价仓库；CArtBench 仓为空占位；新增邻近项 Paint4Poem、Chinese_Landscape_Painting、MaskCLP、Moyun/Mobao）
- [x] 论文库补查（2026-11-15 13:45 CST 完成，见下节）——新增 CArtBench、HanMoVLM、VULCA-Bench 三项
- [x] HanMoVLM 开源状态核查（2026-11-15 完成：全文检索无 github 链接，论文称 HanMo-Bench "will be available"，定为未开源）
- [ ] 台北故宫 Open Data 与 Met/CMA API 的可用性与许可逐项确认（移入选图阶段做，不阻塞查重完成）

## 论文库补查（2026-11-15，arXiv 检索）
方法：arXiv 站内检索（关键词 chinese painting VLM benchmark / connoisseurship / brushwork）＋逐篇打开 arXiv 摘要页核对。检索日期 2026-11-15。

7. **CArtBench（arXiv:2604.11632，2026-04-13 提交，2026-05-25 修订 v2）**
   - 链接：https://arxiv.org/abs/2604.11632
   - 内容：中国艺术 VLM 评测基准（博物馆 grounded）；四子任务：CURATORQA（证据型识别与推理，14,421 题／1,589 件）、CATALOGCAPTION（四段式专家鉴赏）、REINTERPRET（专家评分的可辩护再解读，25 件）、CONNOISSEURPAIRS（真伪鉴别，10 对）；覆盖笔触、印章、材质、形制与时代推断；九个代表性 VLM 在证据链接与风格断代子集上显著下滑，真伪鉴别接近随机。
   - 与 Shihua 的差别：**纯评测基准，不提供微调权重**；任务是馆藏编目式问答与鉴赏，不覆盖 Shihua 三维中的名物断代问答＋诗画意象＋皴法形态依据的完整协议；代码仓已建但**截至 2026-11-15 仍为空占位**：https://github.com/Big-Sid/CARTBENCH-Chinese-Artwork-Benchmark（建于 2026-04-13，仅 2 次提交、2 星，根目录只有 README.md 一句 "Cooming Soon！"，无代码、无数据、无许可文件）。题库由 GPT-5.2 生成＋专家抽检（1,000 条抽查错误率 0.47%，据 papernotes.org 的 ACL 2026 笔记）。
   - 待核：数据集是否开源、许可、图像再分发条款；CURATORQA 题型与 Shihua 审计题的 overlap 程度（选图时须避开直接复用其题库，防泄漏）。
   - 对项目的影响：目前最接近的评测参照；不触发「等价成熟开源模型」退出门槛（无权重），但 Shihua 审计集设计须与之区分（题型/评分协议不同），并在 landscape 正式版中引用为对比基线候选。
8. **HanMoVLM（arXiv:2603.10814，2026-03-11 提交）**
   - 链接：https://arxiv.org/abs/2603.10814
   - 内容：面向中国画专业评价的 VLM；HanMo-Bench 数据集（真实拍卖级名作＋AI 生成画，以市场估值为锚）；专家验证的 CoT（内容识别→RoI 定位→主题评价＋三级评价法）＋GRPO 奖励微调；定位是「绘画评价/鉴赏打分」与生成模型的 test-time scaling 验证器。
   - 与 Shihua 的差别：任务是**审美评价**（画作好坏打分），不是名物考据／断代／诗画意象的事实型问答；**开源状态已核查（2026-11-15）：未开源**——arXiv 全文 v1（https://arxiv.org/html/2603.10814v1）全文检索 "github" 零命中，无代码仓、无权重、无数据集链接；全网检索 "HanMoVLM github" 亦只返回论文本身；论文措辞为 "The HanMo-Bench will be available"（将来时，未发布）。基底为 Qwen3-VL-Instruct 4B/8B，训练用 8× NVIDIA H20 96GB。
   - 对项目的影响：若其权重开源且可商用许可，将是「中国画方向已微调 VLM」的首个实例，须在正式版中单独评估是否构成部分等价；现阶段不改变「未发现等价项目」结论。
9. **VULCA-Bench（arXiv:2601.07986）**
   - 链接：https://arxiv.org/abs/2601.07986
   - 内容：多文化艺术批评基准，7,410 图—评对、八种文化传统、中英双语；五层框架 L1–L5（视觉感知→技术分析→文化象征→历史语境→哲学美学），225 个文化维度；数据集、评测脚本与标注工具随补充材料以 CC BY 4.0 发布。
   - 与 Shihua 的差别：多文化通吃、非中国古画专属；任务是艺术批评文本对齐，不是专家考据问答；L3–L5 层与 Shihua「诗画意象」维有概念重叠，但无名物断代与皴法形态协议。
   - 对项目的影响：可作「意象」维评分思路的参考；不构成等价项目。

### 本轮结论（2026-11-15）
- 仍未发现与 Shihua-VL 等价的开源成果（大参数 VLM 微调权重＋中国古画三维专家考据问答数据集）；CArtBench 是迄今最接近的评测基准（评测向、无权重、代码仓为空占位），HanMoVLM 是迄今最接近的微调 VLM（评价向、**未开源**）。
- 正式查重剩余缺口：~~ModelScope 平台检索、GitHub 检索、kaupane 数据集卡许可核对、HanMoVLM 开源状态核查~~——**已全部补完，见下节「补查（2026-11-15 14:39 CST）」**。查重至此完成，结论：未发现等价项目，查重通过，进入存储与计费文档核查。

## 补查（2026-11-15 14:39 CST，查重收尾）

### ModelScope 平台检索（官方 API 直查＋站内索引检索＋浏览器实开页面核对）
方法：ModelScope 开放 API `https://modelscope.cn/api/v1/datasets?Query=…` 直查五组关键词（chinese painting / 古画 / 书画 / 国画 / chinese art，2026-11-15 实测通，Code 200）；模型侧 API 端点 `/api/v1/models` 回 404（该路径不存在），改以 `site:modelscope.cn` 中英文检索补查；两命中数据集页由浏览器实开核对（只读、未登录）。
- 数据集 API 结果：`chinese painting` 0 条、`国画` 0 条、`chinese art` 0 条；`古画` 1 条、`书画` 1 条，合计仅 2 条。
- **talkart/shuhuaData**（书画数据集，Apache 2.0，2023-12-21 更新，18 次下载）：页面近乎空白——仅 README.md（406B）与 shuhuaData.json（14B），无图片、无条目、无预览（"No preview data available"），总大小 420B；README 为默认模板，无任务/来源/字段说明。**无法证实任何用途，与考据问答无关。**
- **GlowBond/SR_SSP**（古画复原，Apache 2.0，2026-07-14 更新，0 次下载）：页面近乎空白——仅 .gitattributes 与 README.md（406B），无图片、无数据、无预览，总大小 4.22KB；README 为默认模板，未解释 SR_SSP 含义。**仅名称与「古画复原」相关，非理解/考据/问答。**
- 模型侧：`site:modelscope.cn` 检索（中/英）未返回任何中国画相关模型页；结合数据集 API 结果，ModelScope 上无等价模型或数据集。
- 链接：https://modelscope.cn/datasets/talkart/shuhuaData ；https://modelscope.cn/datasets/GlowBond/SR_SSP

### GitHub 检索（网页检索＋仓库页实开）
方法：中英文网页检索（ancient chinese painting vlm / guhua / shihua / "chinese painting" vision language model）＋逐个打开仓库页核对。未发现古画理解/考据微调 VLM 仓库。相关仓库均已入邻近清单：第 7 项 CArtBench 仓（空占位）、第 10–12 项。

10. **Paint4Poem（arXiv:2109.11632，2021，https://github.com/paint4poem/paint4poem）**
    - 内容：古典诗词→绘画生成的文生图数据集（301 首冯子恺诗画对＋3,648 图注对＋89,204 自动配对的传统中国画诗画对），基准为 AttnGAN/MirrorGAN 生成模型。
    - 与 Shihua 的差别：**生成向**（诗→画），不是理解/考据问答；无 VLM 微调权重。
11. **AmazarashiEndure/Chinese_Landscape_Painting（HF 数据集）**
    - 内容：1,017 张局部＋79 张全景，采自中国山水画十大名画，带结构化标注；用途写明为 Flux 模型 LoRA 微调训练（课程项目，南京大学）。
    - 与 Shihua 的差别：**生成向**（文生图 LoRA 训练集），规模小、无考据问答、无 VLM 权重。
12. **MaskCLP（https://github.com/Makbaka1/MaskCLP，npj Heritage Science 2024，SGRGAN 论文配套）**
    - 内容：古画修复数据集（带特殊掩码的古代山水画修复）＋草图引导修复 GAN；任务是缺损修复/补全。
    - 与 Shihua 的差别：**修复向**，不是理解/考据问答；无 VLM 微调权重。
13. **Moyun / Mobao（arXiv:2410.07618，书法生成）**
    - 内容：1,929,393 张书法图像数据集 Mobao（2,681 书家、4,660 字、六体）＋扩散生成模型 Moyun；任务是书法风格生成。
    - 与 Shihua 的差别：对象是**单字书法生成**，不是整幅古画的理解/考据；无 VLM 问答权重。仅作邻近项备查。

### 最终结论（2026-11-15）
- **未发现等价项目**：HF（API＋网页）、ModelScope（官方 API 五关键词＋站内检索＋两页实开）、GitHub（检索＋仓库实开）、论文库（arXiv 三轮）四路均未发现「大参数 VLM 微调权重＋中国古画三维专家考据问答数据集」的等价开源成果。
- 最接近的三项：CArtBench（评测基准、无权重、代码仓空占位）、HanMoVLM（审美评价微调 VLM、未开源）、kaupane 数据集（91K 图 VLM 图注、非专家考据、无配套权重；许可已核：图像分来源许可，NPM 部分 OGDL v1 须署名、Met/FSG/AIC 为 CC0、Princeton 条款未明；标注 CC-BY-4.0）。
- 查重通过。下一步为存储与计费文档核查。

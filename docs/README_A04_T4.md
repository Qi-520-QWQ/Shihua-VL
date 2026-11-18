# T4 本地小模型审计 — 运行协议（Tesla T4）

## 审计协议（与 Carbon 参照跑同一口径）
- 题目：`questions.jsonl` 锁定 v0，60 题（名物/笔墨/意象各 20），题干不泄题。
- 提示词：`请看这幅中国古画，回答问题（用中文，简明扼要；给出结论、画面依据和不确定性说明）：` + 题干。
- 图像：原图直供，官方 dynamic tiling，max_num=12（config 默认上限），thumbnail 开；不做 1024px 缩放（与 API 参照跑不同，记入结果）。
- 解码：贪心（do_sample=False），max_new_tokens=768。
- 模型：2B = OpenGVLab/InternVL2_5-2B（bf16）；8B = OpenGVLab/InternVL2_5-8B
  （NF4 4-bit，bf16 计算——T4 16GB 装不下 8B bf16 权重约 16GB，量化如实记录，
  不得把量化造成的失败读成模型能力失败）。若 8B-4bit 加载失败，改跑 4B
  （OpenGVLab/InternVL2_5-4B，bf16，脚本已支持 --model 4b），并在运行清单中注明。
- **transformers 必须钉在 4.49.0**：环境默认装到的
  5.22.1 与 InternVL2_5 自定义建模代码不兼容——SDPA 被拒（`does not support
  ... scaled_dot_product_attention`），且 eager/默认加载均报
  `all_tied_weights_keys` 缺失。4.50+ 又把 generate
  从 PreTrainedModel 移走，InternLM2ForCausalLM 未继承 GenerationMixin，
  model.chat 会报 `no attribute 'generate'`。
  4.49.0 是 4.50 之前最后一版，两边都避开；`>=4.48` 的写法会装到 5.x，
  已废止。降级后须重启运行时再跑，工作目录与权重缓存
  不受影响。
- **sentencepiece 0.1.99 路已放弃**：0.1.99 在 Python 3.13 上从源码构建失败（exit 1、无输出；cmake 已装、非缺 cmake）。
  改走词表补丁（见下）。
- **词表补丁（patch_tokenizer_null.py，ID 不变、审计中立）**：InternLM2
  tokenizer.model 含空字符 piece，sentencepiece 0.2.x 在 sp_model.Load 处
  拒载；from_pretrained 吞掉异常返回 bool 是表象。补丁规则：把每个含 NUL
  的 piece 里的 NUL 字节换成 U+E000（私用区、真实文本永不出现），piece
  数量/顺序/分数/类型全不动——全部 token ID 不变，真实输入的分词结果与
  原词表逐字节一致；原文件永不改动，补丁写新文件；安全门：空字符 piece
  须全为 NORMAL 型且 ≤5 个，否则停下。补丁脚本自带校验：sentencepiece
  直载、AutoTokenizer 加载、60 题编码不断言被补 id 出现。补丁清单存
  tokenizer_patch_manifest.json；每条审计回答记 tokenizer_source。
- 断点续跑：每题落盘一条 JSONL（本地工作目录 audit_v0＋可选镜像目录），已完成题自动跳过；中途断线重跑同一命令即可。
- 每题记录：答案、耗时、峰值显存、tile 数、错误。

## 官方实现来源
图像预处理与 model.chat 调用参照 OpenGVLab/InternVL README
（https://raw.githubusercontent.com/OpenGVLab/InternVL/main/README.md，
"using InternVL 2.5 for multimodal chat" 一节，2026-11-15 取回）。

## 产出（包内 `predictions/`）
- predictions/internvl2_5_2b.jsonl / predictions/internvl2_5_2b_manifest.json
- predictions/internvl2_5_8b.jsonl / predictions/internvl2_5_8b_manifest.json（或 4b）
- 随后用 `scripts/rate_reference_carbon.py` 同款双评脚本评分。

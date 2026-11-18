# 复现环境配置（独立说明）

复现 2B 基线以本文件为准；`notebooks/reproduce_2b_baseline.ipynb` 只是按本配置写好的可选便利，不作复现的唯一路径。

## 硬件

- GPU：T4（16GB 显存）或同等及以上显存的 GPU；2B bf16 推理峰值显存约 5–7GB（切块数 12 时约 7GB）。
- 磁盘：仓库约 60MB＋模型权重约 4GB＋20 张原图约 54MB。

## 软件（版本钉死）

- Python 3.13（参考运行环境；Python 3 均可，须与所装 torch 轮子匹配）
- transformers == 4.49.0（必须：5.x 与 InternVL2.5 自定义建模代码不兼容；4.50+ 移走了 InternLM2 所需的 generate）
- torch：环境自带的 GPU 版（参考运行：2.14.1+cu130）
- sentencepiece 0.2.x（参考运行：0.2.2；0.1.99 在 Python 3.13 上无法从源码构建，勿用）
- accelerate 1.15.0、bitsandbytes 0.50.2（参考运行实测版本；不钉版亦可）
- protobuf、timm、einops、pillow（随 notebook 安装）

权重来源：HuggingFace OpenGVLab 官方仓库 `OpenGVLab/InternVL2_5-2B`（bf16），遵循其原始许可。

## 复现步骤

1. 克隆公开仓库（https://github.com/Qi-520-QWQ/Shihua-VL），或上传仓库 zip 解压。
2. 按 notebook 的环境安装 cell 安装依赖并核对版本（transformers 必须为 4.49.0）。
3. 运行词表补丁 `scripts/patch_tokenizer_null.py --models 2b`，必须打印 VALIDATED（tokenizer.model 含空字符 piece，须经补丁才能加载；补丁不改动原文件、不改变任何 token ID）。
4. 按 `data/items.jsonl` 的 URL＋SHA256 下载 20 张原图并逐一校验。
5. Smoke 2 题 → 全量 60 题：`scripts/run_audit_t4.py --model 2b`（贪心解码、max_new_tokens=768、dynamic tiling max_num=12；逐题落盘、可断点续跑）。
6. 输出 `predictions/internvl2_5_2b_reproduced.jsonl`，与包内 `predictions/internvl2_5_2b.jsonl` 的 60 条成功记录逐题比对（答案为贪心解码，应逐字一致；耗时与显存数值可不同）。

## 可配置项（环境变量）

- `SHIHUA_WORK_ROOT`：工作根目录（默认当前工作目录）
- `SHIHUA_BUNDLE_DIR`：审计包目录（默认 `bundle`）
- `SHIHUA_OUT_DIR`：输出目录（默认 `audit_v0`）
- `SHIHUA_MIRROR_DIR`：可选镜像目录（默认不启用）
- `SHIHUA_API_KEY_FILE` / `SHIHUA_API_BASE_URL`：参照跑与双评脚本所用的兼容 OpenAI 接口服务地址与密钥文件（默认占位，须自行填入）

#!/usr/bin/env python3
"""T4 audit: InternVL2.5 small models answer the 60 locked audit questions.

Protocol (docs/a04-reference-channel.md):
- Same prompt as the Gemini 4 Carbon reference run:
  '请看这幅中国古画，回答问题（用中文，简明扼要；给出结论、画面依据和不确定性说明）：' + question
- Images: original audit images, dynamic tiling max_num=12 (model default,
  matches config max_dynamic_patch=12),
  thumbnail on. No downscaling to 1024 (unlike the API reference run).
- Greedy decoding, max_new_tokens=768.
- Models: 2b = OpenGVLab/InternVL2_5-2B bf16;
          8b = OpenGVLab/InternVL2_5-8B int8 8-bit (bf16 compute) -- a T4 16GB
          cannot hold the 8B bf16 weights (~16GB); quantization is recorded
          per answer and must NOT be read as a capability failure.
          2026-11-17: NF4 4-bit smoke failed ('NoneType' has no attribute
          'chat', 2/2 failed) -- NF4 path retired, 8B retried once with
          load_in_8bit.
          4b = OpenGVLab/InternVL2_5-4B bf16 (fallback if 8b fails to load).
- Checkpointing: resume-aware, one JSONL record per question, flushed to
  disk after every question (local out dir + optional mirror dir if present).
- Also records per-question peak GPU memory.

Runs on a Tesla T4 GPU.
Usage:
  %run run_audit_t4.py --model 2b --limit 2        # smoke test
  %run run_audit_t4.py --model 2b                  # full 60
  %run run_audit_t4.py --model 8b
Outputs:
  <out>/internvl2_5_<model>.jsonl   (one record per question)
  <out>/internvl2_5_<model>_manifest.json

Official quick-start reference: OpenGVLab/InternVL README
(https://raw.githubusercontent.com/OpenGVLab/InternVL/main/README.md,
"using InternVL 2.5 for multimodal chat"), fetched 2026-11-15.
"""
import argparse
import json
import os
import sys
import time
import traceback

import torch

MODELS = {
    '2b': {'repo': 'OpenGVLab/InternVL2_5-2B', 'quant': 'bf16'},
    '8b': {'repo': 'OpenGVLab/InternVL2_5-8B', 'quant': 'int8-8bit'},
    '4b': {'repo': 'OpenGVLab/InternVL2_5-4B', 'quant': 'bf16'},
}

PROMPT_PREFIX = ('请看这幅中国古画，回答问题（用中文，简明扼要；'
                 '给出结论、画面依据和不确定性说明）：')
MAX_NUM = 12
MAX_NEW_TOKENS = 768

# --- Image preprocessing: verbatim from the official OpenGVLab/InternVL
# README quick start ("using InternVL 2.5 for multimodal chat") ---
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def build_transform(input_size):
    import torchvision.transforms as T
    from torchvision.transforms.functional import InterpolationMode
    return T.Compose([
        T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
        T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
        T.ToTensor(),
        T.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float('inf')
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio


def dynamic_preprocess(image, min_num=1, max_num=12, image_size=448, use_thumbnail=False):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height
    target_ratios = set(
        (i, j) for n in range(min_num, max_num + 1) for i in range(1, n + 1)
        for j in range(1, n + 1) if i * j <= max_num and i * j >= min_num)
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size)
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size,
        )
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images


def load_image(image_file, input_size=448, max_num=12):
    from PIL import Image
    image = Image.open(image_file).convert('RGB')
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(image, image_size=input_size,
                                use_thumbnail=True, max_num=max_num)
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values


def cst_now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() + 8 * 3600))


def load_questions(bundle_dir):
    qs = []
    with open(os.path.join(bundle_dir, 'questions.jsonl'), encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                qs.append(json.loads(line))
    return qs


def load_model(spec, tokenizer_dir=None):
    """Load one InternVL2.5 model per the official README pattern.

    Tries sdpa attention first (no flash-attn build needed on T4);
    falls back to eager, then to the model default. The sdpa->eager step is
    required: transformers 5.x raises ValueError for InternVLChatModel with
    sdpa ("does not support ... scaled_dot_product_attention yet", and the
    error itself suggests attn_implementation="eager" meanwhile).
    2026-11-15 T4 probe: sdpa failed exactly this way on transformers
    5.22.1; weights (2B, 4.41GB) were already cached in the session.

    tokenizer_dir: directory holding a (possibly patched) tokenizer
    (tokenizer.model + tokenizer_config.json + tokenization_internlm2.py).
    Used when the repo's own tokenizer.model cannot load under the
    installed sentencepiece (InternLM2 vocab contains a NUL piece that
    sentencepiece 0.2.x rejects); see patch_tokenizer_null.py. When None,
    the tokenizer is loaded from the model repo as usual.
    """
    from transformers import AutoModel, AutoTokenizer, BitsAndBytesConfig

    repo = spec['repo']
    print(f'loading {repo} quant={spec["quant"]}', flush=True)
    kwargs = dict(trust_remote_code=True, low_cpu_mem_usage=True)
    if spec['quant'] == 'int8-8bit':
        kwargs['quantization_config'] = BitsAndBytesConfig(
            load_in_8bit=True,
            bnb_8bit_compute_dtype=torch.bfloat16,
        )
        kwargs['torch_dtype'] = torch.bfloat16
    else:
        kwargs['torch_dtype'] = torch.bfloat16
    last_err = None
    model = None
    for impl in ('sdpa', 'eager', None):
        try:
            if impl is None:
                model = AutoModel.from_pretrained(repo, **kwargs)
            else:
                model = AutoModel.from_pretrained(
                    repo, attn_implementation=impl, **kwargs)
            print(f'loaded with attn_implementation={impl}', flush=True)
            break
        except Exception as e:
            last_err = e
            print(f'attn_implementation={impl} failed: '
                  f'{type(e).__name__}: {e}', flush=True)
    if model is None:
        raise RuntimeError(f'all attention implementations failed: {last_err}')
    model = model.eval()
    # 2026-11-17 int8 traceback (transformers 4.49.0): .cuda() rejects quantized models.
    # BitsAndBytes already places int8 models on CUDA; use them as-is.
    try:
        model = model.cuda()
    except ValueError as e:
        if 'quantized' not in str(e):
            raise
    tok_src = tokenizer_dir or repo
    tokenizer = AutoTokenizer.from_pretrained(tok_src, trust_remote_code=True,
                                              use_fast=False)
    if isinstance(tokenizer, bool):
        raise RuntimeError(
            f'tokenizer loaded as bool from {tok_src}; see '
            'patch_tokenizer_null.py (InternLM2 tokenizer.model contains a '
            'NUL piece rejected by sentencepiece 0.2.x)')
    print(f'loaded {repo} on {torch.cuda.get_device_name(0)}; '
          f'mem_allocated={torch.cuda.memory_allocated() / 2**30:.2f} GB; '
          f'tokenizer from {tok_src}', flush=True)
    return model, tokenizer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', choices=['2b', '8b', '4b'], required=True)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--only', nargs='*', default=None)
    ap.add_argument('--bundle-dir',
                    default=os.environ.get('SHIHUA_BUNDLE_DIR', 'bundle'))
    ap.add_argument('--out-dir',
                    default=os.environ.get('SHIHUA_OUT_DIR', 'audit_v0'))
    ap.add_argument('--mirror-dir',
                    default=os.environ.get('SHIHUA_MIRROR_DIR', ''))
    ap.add_argument('--max-num', type=int, default=MAX_NUM)
    ap.add_argument('--max-new-tokens', type=int, default=MAX_NEW_TOKENS)
    ap.add_argument('--tokenizer-dir', default=None,
                    help='directory with a (patched) tokenizer; '
                         'default loads the tokenizer from the model repo')
    args = ap.parse_args()

    spec = MODELS[args.model]
    out_name = f"internvl2_5_{args.model}.jsonl"
    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, out_name)
    mirror_path = None
    if args.mirror_dir and os.path.isdir(args.mirror_dir):
        os.makedirs(args.mirror_dir, exist_ok=True)
        mirror_path = os.path.join(args.mirror_dir, out_name)
        print(f'Mirror active: {mirror_path}', flush=True)
    else:
        print('Mirror dir not set or not present; local-only output.', flush=True)

    done_ids = set()
    if os.path.exists(out_path):
        with open(out_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        r = json.loads(line)
                        # only successful answers count as done; failed
                        # records stay in the file as history and the
                        # question is retried (a later record supersedes
                        # earlier failures for the same id)
                        if r.get('answer') and not r.get('error'):
                            done_ids.add(r['id'])
                    except Exception:
                        pass
    qs = load_questions(args.bundle_dir)
    if args.only:
        qs = [q for q in qs if q['id'] in set(args.only)]
    if args.limit:
        qs = [q for q in qs if q['id'] not in done_ids][:args.limit]
    else:
        qs = [q for q in qs if q['id'] not in done_ids]
    print(f'model={spec["repo"]} quant={spec["quant"]} max_num={args.max_num} '
          f'planned={len(qs)} already_done={len(done_ids)}', flush=True)
    if not qs:
        print('nothing to do', flush=True)
        return

    model, tokenizer = load_model(spec, args.tokenizer_dir)
    print(type(model), hasattr(model, 'chat'), type(tokenizer), flush=True)
    gen_config = dict(max_new_tokens=args.max_new_tokens, do_sample=False)

    n_ok = n_fail = 0
    t_start = time.time()
    out_f = open(out_path, 'a', encoding='utf-8')
    mirror_f = (open(mirror_path, 'a', encoding='utf-8')
               if mirror_path else None)
    try:
        for i, q in enumerate(qs, 1):
            img_path = os.path.join(args.bundle_dir, 'images',
                                    q['artwork_id'] + '.jpg')
            answer, err = '', ''
            n_tiles = None
            peak_gb = None
            pixel_values = None
            t0 = time.time()
            try:
                torch.cuda.reset_peak_memory_stats()
                pixel_values = load_image(
                    img_path, input_size=448,
                    max_num=args.max_num).to(torch.bfloat16).cuda()
                n_tiles = int(pixel_values.size(0))
                question = PROMPT_PREFIX + q['question']
                answer = model.chat(tokenizer, pixel_values, question,
                                    gen_config)
                answer = (answer or '').strip()
                if not answer:
                    err = 'empty answer'
            except Exception as e:
                err = f'{type(e).__name__}: {e}'
                print(f'ERROR {q["id"]}: {err}', flush=True)
                traceback.print_exc(file=sys.stdout)
            secs = round(time.time() - t0, 1)
            peak_gb = round(torch.cuda.max_memory_allocated() / 2**30, 2)
            rec = {'id': q['id'], 'artwork_id': q['artwork_id'],
                   'dimension': q['dimension'],
                   'model': spec['repo'], 'quantization': spec['quant'],
                   'tokenizer_source': args.tokenizer_dir or spec['repo'],
                   'max_num': args.max_num, 'n_tiles': n_tiles,
                   'max_new_tokens': args.max_new_tokens,
                   'seconds': secs, 'peak_mem_gb': peak_gb,
                   'answer': answer, 'error': err, 'ts_cst': cst_now()}
            line = json.dumps(rec, ensure_ascii=False) + '\n'
            out_f.write(line)
            out_f.flush()
            if mirror_f:
                mirror_f.write(line)
                mirror_f.flush()
            ok = bool(answer) and not err
            n_ok += int(ok)
            n_fail += int(not ok)
            print(f'[{i}/{len(qs)}] {q["id"]} ok={ok} tiles={n_tiles} '
                  f'{secs}s peak={peak_gb}GB ans_chars={len(answer)}',
                  flush=True)
            if pixel_values is not None:
                del pixel_values
            torch.cuda.empty_cache()
    finally:
        out_f.close()
        if mirror_f:
            mirror_f.close()

    manifest = {'model': spec['repo'], 'quantization': spec['quant'],
                'tokenizer_source': args.tokenizer_dir or spec['repo'],
                'max_num': args.max_num,
                'max_new_tokens': args.max_new_tokens,
                'planned': len(qs), 'ok': n_ok, 'failed': n_fail,
                'seconds': round(time.time() - t_start, 1),
                'ts_cst': cst_now(), 'out': out_path}
    mpath = os.path.join(args.out_dir, f"internvl2_5_{args.model}_manifest.json")
    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    if mirror_path:
        with open(os.path.join(args.mirror_dir,
                               f"internvl2_5_{args.model}_manifest.json"),
                  'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
    print('MANIFEST ' + json.dumps(manifest, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()

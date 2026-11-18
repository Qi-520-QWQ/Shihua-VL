#!/usr/bin/env python3
"""Qwen2.5-VL audit: mechanical adaptation of run_audit_t4.py.

Protocol:
- Same 60 locked questions, original local images, and verbatim prompt:
  '请看这幅中国古画，回答问题（用中文，简明扼要；给出结论、画面依据和不确定性说明）：' + question
- Greedy decoding, max_new_tokens=768; decode only newly generated tokens.
- Models: 7b = Qwen/Qwen2.5-VL-7B-Instruct, 4bit, bf16 compute;
          3b = Qwen/Qwen2.5-VL-3B-Instruct, bf16, no quantization (fallback).
- Smart resize uses the Qwen2.5-VL official quick-start's 256-1280 budget:
  min_pixels=256*28*28, max_pixels=1280*28*28. Both the processor and the
  image message receive these bounds so process_vision_info uses them too.
- n_tiles = grid_h * grid_w from image_grid_thw after smart resize (t=1
  for one image). This is the pre-spatial-merge visual patch-grid count,
  an information field, NOT the same unit as InternVL's tile count. Qwen's
  merge_size=2 produces one language-model visual token per four patches.
- max_num is fixed at 1280: max_pixels/(28*28), the quick-start's 28-pixel
  spatial-scale budget. Qwen has no dynamic-tiling max_num; this is neither
  InternVL's tile limit of 12 nor an image-side length limit in pixels.
- tokenizer_source is the model repo; the processor needs no vocab patch.
- Resume, JSONL/manifest field names, CST timestamps, per-question flush,
  Mirror output, timing, and peak GPU memory follow run_audit_t4.py.
  Failed records remain as history; later successes supersede them.

Dependencies: transformers==4.49.0, qwen-vl-utils, bitsandbytes (4bit),
torch, accelerate (device_map="auto"). No flash-attn build is needed;
eager attention is used. Device placement belongs to device_map="auto";
the model is never moved manually. Imports are lazy so --help needs only
the Python standard library and does not load a model.

Runs on a GPU. Usage:
  %run run_audit_qwen2_5_vl.py --model 7b --limit 2
  %run run_audit_qwen2_5_vl.py --model 7b
  %run run_audit_qwen2_5_vl.py --model 3b --limit 2
Outputs:
  <out>/qwen2_5_vl_<model>.jsonl
  <out>/qwen2_5_vl_<model>_manifest.json

Official quick-start reference: Qwen/Qwen2.5-VL-7B-Instruct model card
(https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct#quickstart).
"""
import argparse
import json
import os
import sys
import time
import traceback

MODELS = {
    '7b': {'repo': 'Qwen/Qwen2.5-VL-7B-Instruct', 'quant': '4bit'},
    '3b': {'repo': 'Qwen/Qwen2.5-VL-3B-Instruct', 'quant': 'bf16'},
}

PROMPT_PREFIX = ('请看这幅中国古画，回答问题（用中文，简明扼要；'
                 '给出结论、画面依据和不确定性说明）：')
MIN_PIXELS = 256 * 28 * 28
MAX_NUM = 1280
MAX_PIXELS = MAX_NUM * 28 * 28
MAX_NEW_TOKENS = 768
NOTE = ('Qwen official quick-start smart resize: min_pixels=256*28*28, '
        'max_pixels=1280*28*28; max_num=1280 is max_pixels/(28*28); '
        'n_tiles=grid_h*grid_w for t=1 (pre-merge patch grid), not InternVL '
        'tiles. planned/ok/failed count this invocation only; successful '
        'earlier answers are skipped.')


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


def load_model(spec):
    """Load Qwen2.5-VL and its unmodified repo processor on auto devices."""
    import torch
    from transformers import (AutoProcessor, BitsAndBytesConfig,
                              Qwen2_5_VLForConditionalGeneration)

    repo = spec['repo']
    print(f'loading {repo} quant={spec["quant"]}', flush=True)
    kwargs = dict(torch_dtype=torch.bfloat16, device_map='auto',
                  low_cpu_mem_usage=True, attn_implementation='eager')
    if spec['quant'] == '4bit':
        kwargs['quantization_config'] = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
    model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
        repo, **kwargs).eval()
    processor = AutoProcessor.from_pretrained(
        repo, min_pixels=MIN_PIXELS, max_pixels=MAX_PIXELS)
    print(f'loaded {repo} on {torch.cuda.get_device_name(0)}; '
          f'mem_allocated={torch.cuda.memory_allocated() / 2**30:.2f} GB; '
          f'tokenizer from {repo}', flush=True)
    return model, processor


def prepare_inputs(processor, image_file, question):
    from qwen_vl_utils import process_vision_info

    messages = [{
        'role': 'user',
        'content': [
            {'type': 'image', 'image': image_file,
             'min_pixels': MIN_PIXELS, 'max_pixels': MAX_PIXELS},
            {'type': 'text', 'text': question},
        ],
    }]
    text = processor.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True)
    image_inputs, video_inputs = process_vision_info(messages)
    inputs = processor(text=[text], images=image_inputs, videos=video_inputs,
                       padding=True, return_tensors='pt')
    grid_t, grid_h, grid_w = inputs['image_grid_thw'][0].tolist()
    if grid_t != 1:
        raise ValueError(f'expected t=1 for one audit image, got t={grid_t}')
    return inputs, int(grid_h * grid_w)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model', choices=['7b', '3b'], required=True)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--only', nargs='*', default=None)
    ap.add_argument('--bundle-dir',
                    default=os.environ.get('SHIHUA_BUNDLE_DIR', 'bundle'))
    ap.add_argument('--out-dir',
                    default=os.environ.get('SHIHUA_OUT_DIR', 'audit_v0'))
    ap.add_argument('--mirror-dir',
                    default=os.environ.get('SHIHUA_MIRROR_DIR', ''))
    ap.add_argument('--max-new-tokens', type=int, default=MAX_NEW_TOKENS)
    args = ap.parse_args()

    spec = MODELS[args.model]
    out_name = f"qwen2_5_vl_{args.model}.jsonl"
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
                        # Only successful answers count as done; failed
                        # records remain as history and are retried.
                        # A later success supersedes earlier failures.
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
    print(f'model={spec["repo"]} quant={spec["quant"]} max_num={MAX_NUM} '
          f'planned={len(qs)} already_done={len(done_ids)}', flush=True)
    if not qs:
        print('nothing to do', flush=True)
        return

    import torch
    if not torch.cuda.is_available():
        raise RuntimeError('a GPU runtime is required for the audit')
    model, processor = load_model(spec)
    print(type(model), hasattr(model, 'generate'), type(processor), flush=True)
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
            inputs = generated_ids = generated_ids_trimmed = None
            t0 = time.time()
            try:
                torch.cuda.reset_peak_memory_stats()
                question = PROMPT_PREFIX + q['question']
                inputs, n_tiles = prepare_inputs(processor, img_path, question)
                inputs = inputs.to(model.device)
                with torch.inference_mode():
                    generated_ids = model.generate(**inputs, **gen_config)
                generated_ids_trimmed = [
                    out_ids[len(in_ids):]
                    for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                ]
                answer = processor.batch_decode(
                    generated_ids_trimmed, skip_special_tokens=True,
                    clean_up_tokenization_spaces=False)[0]
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
                   'tokenizer_source': spec['repo'],
                   'max_num': MAX_NUM, 'n_tiles': n_tiles,
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
            if inputs is not None:
                del inputs
            if generated_ids is not None:
                del generated_ids
            if generated_ids_trimmed is not None:
                del generated_ids_trimmed
            torch.cuda.empty_cache()
    finally:
        out_f.close()
        if mirror_f:
            mirror_f.close()

    manifest = {'model': spec['repo'], 'quantization': spec['quant'],
                'tokenizer_source': spec['repo'],
                'max_num': MAX_NUM,
                'max_new_tokens': args.max_new_tokens,
                'planned': len(qs), 'ok': n_ok, 'failed': n_fail,
                'seconds': round(time.time() - t_start, 1),
                'ts_cst': cst_now(), 'out': out_path, 'note': NOTE}
    mpath = os.path.join(args.out_dir, f"qwen2_5_vl_{args.model}_manifest.json")
    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    if mirror_path:
        with open(os.path.join(args.mirror_dir,
                               f"qwen2_5_vl_{args.model}_manifest.json"),
                  'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
    print('MANIFEST ' + json.dumps(manifest, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Reference run: Gemini 4 Carbon (flagship, upper-bound reference)
answers all 60 locked audit questions with the artwork image.

Backup path per docs/a04-reference-channel.md §3 (preferred
首选渠道 Qwen2.5-VL-72B still awaits user's nod to register; this run does
not block it -- it yields the upper-bound reference either way).

Hardening (per EMPLOYEES.md API discipline):
- stream=true, incremental flush to disk (sandbox proxy cuts ~5 min connections)
- sequential calls only (concurrency <= 2)
- resume-aware: skips question ids already in the output jsonl
- retry up to 3 attempts on 5xx / URLError / IncompleteRead, 60 s backoff
- cost guard: estimated cost at $2/$10 per M tokens; stop if cumulative
  estimate exceeds $3.00 (60 calls should be ~$0.4)

Usage: run_reference_carbon.py [--limit N] [--only ID ...]
Outputs:
  eval/results/audit_v0/reference_gemini4carbon.jsonl  (one record per question)
  eval/results/audit_v0/logs_carbon/<question_id>.log  (raw SSE lines)
  eval/results/audit_v0/reference_gemini4carbon_manifest.json (run summary)
"""
import argparse, base64, io, json, os, sys, time, urllib.request, urllib.error
from PIL import Image

import os
# Project root: set SHIHUA_PROJECT_DIR, or run from the project root.
BASE = os.environ.get("SHIHUA_PROJECT_DIR", ".")
KEY_FILE = os.environ.get('SHIHUA_API_KEY_FILE', '<API_KEY_FILE>')
KEY = open(KEY_FILE).read().strip()
API_BASE_URL = os.environ.get('SHIHUA_API_BASE_URL', '<API_BASE_URL>')
URL = API_BASE_URL.rstrip('/') + '/chat/completions'
MODEL = 'gemini-4-carbon'
OUT_DIR = f'{BASE}/eval/results/audit_v0'
OUT_JSONL = f'{OUT_DIR}/reference_gemini4carbon.jsonl'
LOG_DIR = f'{OUT_DIR}/logs_carbon'
MANIFEST = f'{OUT_DIR}/reference_gemini4carbon_manifest.json'
COST_CAP_USD = 3.00
PRICE_IN_PER_M = 2.0
PRICE_OUT_PER_M = 10.0

os.makedirs(LOG_DIR, exist_ok=True)

def cst_now():
    # sandbox clock is UTC; CST = UTC+8
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time() + 8 * 3600))

def load_questions():
    qs = []
    with open(f'{BASE}/data/audit_v0/questions.jsonl', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                qs.append(json.loads(line))
    return qs

def img_b64(artwork_id):
    path = f'{BASE}/data/audit_v0/images/{artwork_id}.jpg'
    img = Image.open(path).convert('RGB')
    img.thumbnail((1024, 1024))
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=85)
    return base64.b64encode(buf.getvalue()).decode(), img.size

def one_call(q, b64):
    payload = {'model': MODEL,
               'messages': [{'role': 'user', 'content': [
                   {'type': 'text', 'text': '请看这幅中国古画，回答问题（用中文，简明扼要；给出结论、画面依据和不确定性说明）：' + q['question']},
                   {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + b64}}]}],
               # reasoning_effort none is REQUIRED for Gemini: its default
               # reasoning burns the completion cap and finish_reason=length
               # leaves 0-char (or truncated) answers (2026-11-15 v1 lesson)
               'reasoning_effort': 'none',
               'max_tokens': 2500, 'stream': True}
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
        headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    parts, chunks, usage, done = [], 0, None, False
    finish_reason = None
    log_path = f'{LOG_DIR}/{q["id"]}.log'
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r, \
         open(log_path, 'w', encoding='utf-8') as log:
        for raw in r:
            line = raw.decode('utf-8', 'replace').strip()
            log.write(line + '\n')
            if chunks % 20 == 0:
                log.flush()
            if not line.startswith('data:'):
                continue
            data = line[5:].strip()
            if data == '[DONE]':
                done = True
                break
            try:
                obj = json.loads(data)
            except Exception:
                continue
            if obj.get('usage'):
                usage = obj['usage']
            for ch in obj.get('choices', []):
                if ch.get('finish_reason'):
                    finish_reason = ch['finish_reason']
                delta = ch.get('delta', {}).get('content')
                if delta:
                    parts.append(delta)
                    chunks += 1
    return ''.join(parts), usage, done, time.time() - t0, finish_reason

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--only', nargs='*', default=None)
    args = ap.parse_args()

    done_ids = set()
    if os.path.exists(OUT_JSONL):
        with open(OUT_JSONL, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        done_ids.add(json.loads(line)['id'])
                    except Exception:
                        pass
    qs = load_questions()
    if args.only:
        qs = [q for q in qs if q['id'] in set(args.only)]
    if args.limit:
        qs = [q for q in qs if q['id'] not in done_ids][:args.limit]
    else:
        qs = [q for q in qs if q['id'] not in done_ids]

    print(f'total planned={len(qs)} already_done={len(done_ids)} model={MODEL}', flush=True)
    b64_cache = {}
    n_ok = n_fail = 0
    tot_in = tot_out = 0
    t_start = time.time()
    with open(OUT_JSONL, 'a', encoding='utf-8') as out:
        for i, q in enumerate(qs, 1):
            aid = q['artwork_id']
            if aid not in b64_cache:
                b64_cache[aid] = img_b64(aid)
            b64, size = b64_cache[aid]
            answer, usage, done, secs = None, None, False, 0.0
            finish_reason = None
            attempts = 0
            last_err = ''
            while attempts < 3 and not done:
                attempts += 1
                try:
                    answer, usage, done, secs, finish_reason = one_call(q, b64)
                    if not done:
                        last_err = 'stream ended without [DONE]'
                    elif finish_reason == 'length':
                        last_err = 'finish_reason=length (truncated)'
                except Exception as e:  # HTTPError 5xx / URLError / IncompleteRead
                    last_err = f'{type(e).__name__}: {e}'
                    code = getattr(e, 'code', None)
                    if code is not None and code < 500 and code != 429:
                        break
                    if attempts < 3:
                        time.sleep(60)
            rec = {'id': q['id'], 'artwork_id': aid, 'dimension': q['dimension'],
                   'model': MODEL, 'attempts': attempts, 'done': bool(done),
                   'finish_reason': finish_reason,
                   'seconds': round(secs, 1), 'usage': usage,
                   'answer': (answer or '').strip(), 'error': last_err if not done else '',
                   'ts_cst': cst_now()}
            out.write(json.dumps(rec, ensure_ascii=False) + '\n')
            out.flush()
            if usage:
                tot_in += usage.get('prompt_tokens', 0) or 0
                tot_out += usage.get('completion_tokens', 0) or 0
            if done and answer and finish_reason != 'length':
                n_ok += 1
            else:
                n_fail += 1
            est = (tot_in * PRICE_IN_PER_M + tot_out * PRICE_OUT_PER_M) / 1e6
            print(f'[{i}/{len(qs)}] {q["id"]} ok={done} attempts={attempts} '
                  f'usage={usage} cum_cost=${est:.4f} {secs:.0f}s', flush=True)
            if est > COST_CAP_USD:
                print(f'COST CAP ${COST_CAP_USD} exceeded, stopping.', flush=True)
                break
    manifest = {'model': MODEL, 'planned': len(qs), 'ok': n_ok, 'failed': n_fail,
                'total_prompt_tokens': tot_in, 'total_completion_tokens': tot_out,
                'est_cost_usd': round((tot_in * PRICE_IN_PER_M + tot_out * PRICE_OUT_PER_M) / 1e6, 4),
                'seconds': round(time.time() - t_start, 1),
                'ts_cst': cst_now(),
                'out': OUT_JSONL}
    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print('MANIFEST ' + json.dumps(manifest, ensure_ascii=False), flush=True)

if __name__ == '__main__':
    main()

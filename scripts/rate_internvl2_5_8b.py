#!/usr/bin/env python3
"""Dual rating: score the InternVL2.5-8B (int8) T4 answers against the
locked reference answers (required_facts / forbidden_claims).

Two raters, blind to each other and to the answerer's identity:
  rater_a = deepseek-v4-1-flash-1017  ($0.24/$0.48 per M)
  rater_b = gemini-3-8-flash         (flagship tier $2/$10 per M; text-only,
                                       ~1300 in / ~300 out tokens per call)
Scoring per PLAN: strict_hit 0/1, partial 0/1/2, hallucination 0/1,
proper_refusal 0/1. Agreement target >= 85% (strict_hit + hallucination).

Resumable: skips (id, rater) pairs already in the output jsonl.
Run only after reference_gemini4carbon.jsonl is complete (or it rates what
exists and can be re-run to pick up the rest).

Usage: rate_internvl2_5_8b.py [--limit N]
Outputs:
  eval/results/audit_v0/ratings_internvl2_5_8b.jsonl
  eval/results/audit_v0/ratings_internvl2_5_8b_manifest.json
"""
import argparse
import json
import os
import re
import time
import urllib.request
from datetime import datetime, timedelta

# Project root: set SHIHUA_PROJECT_DIR, or run from the project root.
BASE = os.environ.get("SHIHUA_PROJECT_DIR", ".")
KEY_FILE = os.environ.get('SHIHUA_API_KEY_FILE', '<API_KEY_FILE>')
KEY = open(KEY_FILE).read().strip()
API_BASE_URL = os.environ.get('SHIHUA_API_BASE_URL', '<API_BASE_URL>')
URL = API_BASE_URL.rstrip('/') + '/chat/completions'
OUT_DIR = f'{BASE}/eval/results/audit_v0'
OUT_JSONL = f'{OUT_DIR}/ratings_internvl2_5_8b.jsonl'
MANIFEST = f'{OUT_DIR}/ratings_internvl2_5_8b_manifest.json'
RATERS = {'rater_a': ('deepseek-v4-1-flash-1017', 0.24, 0.48),
          'rater_b': ('gemini-3-8-flash', 2.0, 10.0)}
COST_CAP_USD = 3.00


def cst_now():
    return (datetime.utcnow() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')


def call_rater(model, prompt):
    payload = {'model': model,
               'messages': [{'role': 'user', 'content': prompt}],
               'max_tokens': 1500, 'stream': True}
    if model.startswith('deepseek'):
        payload['reasoning_effort'] = 'none'
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(),
                                 headers={'Authorization': f'Bearer {KEY}',
                                          'Content-Type': 'application/json'})
    parts, usage, done = [], None, False
    with urllib.request.urlopen(req, timeout=300) as r:
        for raw in r:
            line = raw.decode('utf-8', 'replace').strip()
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
                delta = ch.get('delta', {}).get('content')
                if delta:
                    parts.append(delta)
    return ''.join(parts), usage, done


def parse_score(raw):
    m = re.search(r'\{.*\}', raw, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except Exception:
        return None
    try:
        return {'strict_hit': int(d['strict_hit']),
                'partial': int(d['partial']),
                'hallucination': int(d['hallucination']),
                'proper_refusal': int(d['proper_refusal']),
                'notes': str(d.get('notes', ''))[:500]}
    except Exception:
        return None


PROMPT_TMPL = """你是古画考据问答的评分员。只按给定的参考答案与事实清单打分，不要用你自己的知识补分。

【问题】{question}

【参考答案】{answer}

【必须命中的事实】{required_facts}

【可接受别名/说法】{accepted_variants}

【禁止断言（出现即错）】{forbidden_claims}

【待评回答】
{model_answer}

评分规则（只输出 JSON，不要其他文字）：
- strict_hit：待评回答是否命中全部必须事实且无禁止断言，0 或 1。
- partial：部分正确程度，0=基本不对，1=命中部分事实，2=接近全对但有小缺失或小错误。
- hallucination：是否含有参考答案不支持的编造事实或禁止断言，0 或 1（1=有幻觉）。
- proper_refusal：若问题确实无法从画面判断，待评回答是否恰当承认不确定而非编造，0 或 1（能确定回答的问题答对了也记 1；无端拒答记 0）。
- notes：一句话说明扣分/给分理由。

输出 JSON：{{"strict_hit": 0, "partial": 0, "hallucination": 0, "proper_refusal": 0, "notes": "..."}}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    qs = {}
    with open(f'{BASE}/data/audit_v0/questions.jsonl', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                qs[r['id']] = r
    answers = {}
    with open(f'{OUT_DIR}/internvl2_5_8b.jsonl', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                r = json.loads(line)
                # 2B file keeps stale failed rows; later successful rows win
                if r.get('answer'):
                    answers[r['id']] = r['answer']
    done_pairs = set()
    if os.path.exists(OUT_JSONL):
        with open(OUT_JSONL, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        r = json.loads(line)
                        # only scored pairs count as done; failed (score None)
                        # pairs are retried on the next run
                        if r.get('score'):
                            done_pairs.add((r['id'], r['rater']))
                    except Exception:
                        pass
    jobs = []
    for qid in sorted(answers):
        for rater in ('rater_a', 'rater_b'):
            if (qid, rater) not in done_pairs:
                jobs.append((qid, rater))
    if args.limit:
        jobs = jobs[:args.limit]
    print(f'rateable={len(answers)} pending_jobs={len(jobs)}', flush=True)

    tot_in = tot_out = 0.0
    n_ok = n_fail = 0
    with open(OUT_JSONL, 'a', encoding='utf-8') as out:
        for i, (qid, rater) in enumerate(jobs, 1):
            model, p_in, p_out = RATERS[rater]
            q = qs[qid]
            prompt = PROMPT_TMPL.format(
                question=q['question'], answer=q['answer'],
                required_facts='；'.join(q.get('required_facts', [])),
                accepted_variants='；'.join(q.get('accepted_variants', [])),
                forbidden_claims='；'.join(q.get('forbidden_claims', [])),
                model_answer=answers[qid])
            raw, usage, done = None, None, False
            last_err = ''
            for attempt in range(3):
                try:
                    raw, usage, done = call_rater(model, prompt)
                    if done:
                        break
                    last_err = 'stream ended without [DONE]'
                except Exception as e:
                    last_err = f'{type(e).__name__}: {e}'
                    code = getattr(e, 'code', None)
                    if code is not None and code < 500 and code != 429:
                        break
                    if attempt < 2:
                        time.sleep(60)
            score = parse_score(raw or '')
            if usage:
                tot_in += (usage.get('prompt_tokens', 0) or 0) * p_in / 1e6
                tot_out += (usage.get('completion_tokens', 0) or 0) * p_out / 1e6
            rec = {'id': qid, 'dimension': q['dimension'], 'rater': rater,
                   'model': model, 'done': bool(done), 'score': score,
                   'raw': (raw or '')[:2000], 'usage': usage,
                   'error': last_err if not (done and score) else '',
                   'ts_cst': cst_now()}
            out.write(json.dumps(rec, ensure_ascii=False) + '\n')
            out.flush()
            if done and score:
                n_ok += 1
            else:
                n_fail += 1
            print(f'[{i}/{len(jobs)}] {qid} {rater} ok={bool(done and score)} '
                  f'score={score} cum_cost=${tot_in + tot_out:.4f}', flush=True)
            if tot_in + tot_out > COST_CAP_USD:
                print('COST CAP exceeded, stopping.', flush=True)
                break
    scored = {}
    if os.path.exists(OUT_JSONL):
        with open(OUT_JSONL, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    r = json.loads(line)
                    if r.get('score'):
                        scored.setdefault(r['id'], {})[r['rater']] = r['score']
    both = [v for v in scored.values() if 'rater_a' in v and 'rater_b' in v]
    agree_s = sum(1 for v in both
                  if v['rater_a']['strict_hit'] == v['rater_b']['strict_hit'])
    agree_h = sum(1 for v in both
                  if v['rater_a']['hallucination'] == v['rater_b']['hallucination'])
    manifest = {'rated_questions': len(scored), 'both_raters': len(both),
                'agree_strict_hit': f'{agree_s}/{len(both)}' if both else 'n/a',
                'agree_hallucination': f'{agree_h}/{len(both)}' if both else 'n/a',
                'ok': n_ok, 'failed': n_fail,
                'est_cost_usd': round(tot_in + tot_out, 4), 'ts_cst': cst_now()}
    with open(MANIFEST, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print('MANIFEST ' + json.dumps(manifest, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()

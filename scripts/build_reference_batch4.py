#!/usr/bin/env python3
"""Gemini 4 Argon · High batch 4 skeleton (gemini-4-argon-high); answers pending.
骨架：第 4 批＋第 3 批余件 met_41468，答案待填，绝不编造答案文本。
执行包见 docs/reference_batches3-4_prompts.md。
"""
import json

import os
# Project root: set SHIHUA_PROJECT_DIR, or run from the project root.
BASE = os.environ.get("SHIHUA_PROJECT_DIR", ".")
OUT = f'{BASE}/eval/results/audit_v0/reference_gemini4argon.jsonl'

# TODO：填入记录的逐字原文，每项键为 (artwork, dim)，共 21 项。
ANS = {}

# TODO：填每幅的会话标识，键为 artwork（公开包中略去链接）。
SESSIONS = {}

ORDER = ['met_41468', 'met_49047', 'met_51705', 'met_62002', 'met_739501', 'met_78125', 'met_813350']
DIMS = ['mingwu', 'bimo', 'yixiang']

if not ANS:
    print('no answers yet — nothing appended')
    raise SystemExit(0)

assert len(ANS) == 21, len(ANS)
existing = set()
try:
    with open(OUT, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                existing.add(json.loads(line)['id'])
except FileNotFoundError:
    pass
recs = []
for art in ORDER:
    for dim in DIMS:
        qid = f'audit_v0_{art}_{dim}'
        if qid in existing:
            continue
        recs.append({
            'id': qid, 'artwork_id': art, 'dimension': dim,
            'model': 'gemini-4-argon-high', 'attempts': 1, 'done': True,
            'finish_reason': 'stop', 'seconds': None, 'usage': None,
            'answer': ANS[(art, dim)], 'error': '',
            'ts_cst': '',  # TODO：填入答案时改为实际时间。
            'session_url': SESSIONS[art],
        })
with open(OUT, 'a', encoding='utf-8') as f:
    for r in recs:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
with open(OUT, encoding='utf-8') as f:
    ok = sum(1 for line in f)
manifest = {
    'model': 'gemini-4-argon-high',
    'planned': 60, 'ok': ok, 'failed': 0,
    # TODO：填入时补充本批实际账号，保留 batch3 的历史文字。
    'account_note': 'Batch 3 dual-source: met_40057/met_40062/met_41185 from the first transcription; met_41462 from this script. Batches 1-2 ran earlier.',
    # TODO：填入时更新实际额度情况，保留 batch3 的历史文字；旧时间注记过期作废。
    'quota_block': 'met_41468 (3 questions) NOT run by either run: daily limit reached by 2026-11-16 23:47-23:49 CST. Batch 4 (6 artworks, 18 questions) also waits for the reset.',
    'sessions_batch4': SESSIONS,
    'batch': '4 of 4 (batch 4 + met_41468 remainder)',
    'ts_cst': '',  # TODO：填入答案时改为实际时间。
    'out': OUT,
}
with open(f'{BASE}/eval/results/audit_v0/reference_gemini4argon_manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print('appended', len(recs), 'records to', OUT)

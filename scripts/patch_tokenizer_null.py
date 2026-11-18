#!/usr/bin/env python3
"""Patch null-character pieces out of an InternLM2 tokenizer.model.

Root cause (2026-11-15, T4 diagnostics, 4 rounds): the
InternVL2_5-2B/8B tokenizer.model contains piece(s) with an embedded NUL
byte; sentencepiece 0.2.x refuses to Load it
(RuntimeError: INTERNAL: piece must not include null character), and
transformers' from_pretrained swallows the failure and returns a bool
instead of a tokenizer. sentencepiece 0.1.99 (which tolerates the file)
cannot be built from source on Python 3.13 (wheel build fails with
no output), so the file itself is patched.

Patch rule (ID-preserving, tokenization-neutral for all real inputs):
- parse tokenizer.model as ModelProto via sentencepiece_model_pb2
- for every piece whose text contains U+0000, replace each NUL with U+E000
  (private use, never occurs in real text)
- piece COUNT, ORDER, scores and types are unchanged, so every token ID
  stays identical, and no real input can ever produce a patched piece
- the original file is never modified; the patched model is written to a
  NEW file in a per-model output dir together with the tokenizer config
  and remote code copied from the repo snapshot
- validate: reload the patched file with sentencepiece directly; load it
  via AutoTokenizer; encode all 60 audit questions and assert the patched
  piece id(s) never appear

Safety gate: patch ONLY if every NUL piece is type NORMAL (1) and there
are at most 5 of them; otherwise stop and report (exit non-zero).

Usage:
  python3 patch_tokenizer_null.py --out-dir <bundle-dir>
Outputs (per model):
  <out-dir>/tokenizer_patched_<model>/tokenizer.model   (patched)
  <out-dir>/tokenizer_patched_<model>/tokenizer_config.json
  <out-dir>/tokenizer_patched_<model>/tokenization_internlm2.py
  <out-dir>/tokenizer_patched_<model>/special_tokens_map.json (if present)
  <out-dir>/tokenizer_patch_manifest.json
"""
import argparse
import glob
import hashlib
import json
import os
import shutil
import sys

MODELS = {
    '2b': 'OpenGVLab/InternVL2_5-2B',
    '8b': 'OpenGVLab/InternVL2_5-8B',
}
REPLACEMENT = '\ue000'  # private use, never occurs in real text
MAX_NULL_PIECES = 5


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def find_snapshot_dir(repo):
    base = os.path.expanduser(
        '~/.cache/huggingface/hub/models--' + repo.replace('/', '--'))
    snaps = sorted(glob.glob(os.path.join(base, 'snapshots', '*')))
    if not snaps:
        return None
    return snaps[-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir',
                    default=os.environ.get('SHIHUA_BUNDLE_DIR', 'bundle'))
    ap.add_argument('--models', nargs='*', default=['2b', '8b'])
    ap.add_argument('--questions',
                    default=os.path.join(os.environ.get('SHIHUA_BUNDLE_DIR', 'bundle'),
                       'questions.jsonl'))
    args = ap.parse_args()

    try:
        from sentencepiece import sentencepiece_model_pb2 as pb2
    except Exception:
        try:
            import sentencepiece_model_pb2 as pb2
        except Exception as e:
            print(f'FATAL: cannot import sentencepiece_model_pb2: {e}',
                  flush=True)
            return 2
    from huggingface_hub import hf_hub_download
    import sentencepiece as spm

    manifest = {'models': {}, 'ts_cst': __import__('time').strftime(
        '%Y-%m-%d %H:%M:%S',
        __import__('time').gmtime(__import__('time').time() + 8 * 3600))}
    for key in args.models:
        repo = MODELS[key]
        print(f'=== {key}: {repo}', flush=True)
        snap = find_snapshot_dir(repo)
        if snap and os.path.exists(os.path.join(snap, 'tokenizer.model')):
            model_path = os.path.join(snap, 'tokenizer.model')
            print(f'using cached tokenizer.model: {model_path}', flush=True)
        else:
            model_path = hf_hub_download(repo, 'tokenizer.model')
            print(f'downloaded tokenizer.model: {model_path}', flush=True)
            snap = os.path.dirname(model_path)
        orig_sha = sha256(model_path)

        proto = pb2.ModelProto()
        with open(model_path, 'rb') as f:
            proto.ParseFromString(f.read())
        n_pieces = len(proto.pieces)
        nulls = []
        for i, piece in enumerate(proto.pieces):
            if '\x00' in piece.piece:
                nulls.append({
                    'index': i,
                    'piece_hex': piece.piece.encode('utf-8').hex(),
                    'type': int(piece.type),
                    'score': float(piece.score),
                })
        print(f'pieces={n_pieces} null_pieces={len(nulls)}', flush=True)
        for n in nulls:
            print(f"  null piece idx={n['index']} type={n['type']} "
                  f"score={n['score']} hex={n['piece_hex']}", flush=True)
        if not nulls:
            print(f'{key}: no NUL pieces; nothing to patch', flush=True)
            manifest['models'][key] = {
                'repo': repo, 'orig_sha256': orig_sha,
                'null_pieces': [], 'patched': False,
            }
            continue
        if len(nulls) > MAX_NULL_PIECES or any(
                n['type'] != 1 for n in nulls):
            print(f'FATAL {key}: unsafe to patch '
                  f'(count={len(nulls)}, types={[n["type"] for n in nulls]})',
                  flush=True)
            return 3
        patched = []
        for i, piece in enumerate(proto.pieces):
            if '\x00' in piece.piece:
                new = piece.piece.replace('\x00', REPLACEMENT)
                patched.append({
                    'index': i,
                    'piece_hex_orig': piece.piece.encode('utf-8').hex(),
                    'piece_hex_new': new.encode('utf-8').hex(),
                    'type': int(piece.type),
                    'score': float(piece.score),
                })
                piece.piece = new
        out_dir = os.path.join(args.out_dir, f'tokenizer_patched_{key}')
        os.makedirs(out_dir, exist_ok=True)
        patched_path = os.path.join(out_dir, 'tokenizer.model')
        with open(patched_path, 'wb') as f:
            f.write(proto.SerializeToString())
        # copy tokenizer config + remote code (+ special tokens map if any)
        for name in ('tokenizer_config.json', 'special_tokens_map.json',
                     'generation_config.json'):
            src = os.path.join(snap, name)
            if not os.path.exists(src):
                try:
                    src = hf_hub_download(repo, name)
                except Exception:
                    continue
            shutil.copy(src, os.path.join(out_dir, name))
        code_src = glob.glob(
            os.path.expanduser(
                '~/.cache/huggingface/modules/transformers_modules/'
                + repo + '/*/tokenization_internlm2.py'))
        if code_src:
            shutil.copy(code_src[0], os.path.join(
                out_dir, 'tokenization_internlm2.py'))
        else:
            # model not loaded yet in this session: fetch the file itself
            code_path = hf_hub_download(repo, 'tokenization_internlm2.py')
            shutil.copy(code_path, os.path.join(
                out_dir, 'tokenization_internlm2.py'))

        # --- validation ---
        sp = spm.SentencePieceProcessor(model_file=patched_path)
        assert sp.get_piece_size() == n_pieces, (
            f'piece count changed: {sp.get_piece_size()} vs {n_pieces}')
        from transformers import AutoTokenizer
        tok = AutoTokenizer.from_pretrained(
            out_dir, trust_remote_code=True, use_fast=False)
        assert not isinstance(tok, bool), 'tokenizer still bool!'
        img_id = tok.convert_tokens_to_ids('<IMG_CONTEXT>')
        assert isinstance(img_id, int), f'IMG_CONTEXT id not int: {img_id}'
        patched_ids = {p['index'] for p in patched}
        qs = [json.loads(line) for line in open(
            args.questions, encoding='utf-8') if line.strip()]
        bad = []
        for q in qs:
            ids = tok(q['question'])['input_ids']
            hit = patched_ids.intersection(ids)
            if hit:
                bad.append((q['id'], sorted(hit)))
        assert not bad, f'patched piece id produced by questions: {bad}'
        sample = tok('你好，世界', return_tensors='pt')['input_ids'].tolist()
        print(f'{key}: VALIDATED pieces={n_pieces} patched={len(patched)} '
              f'img_context_id={img_id} sample_ids={sample}', flush=True)
        manifest['models'][key] = {
            'repo': repo, 'orig_sha256': orig_sha,
            'patched_sha256': sha256(patched_path),
            'null_pieces': patched, 'patched': True,
            'out_dir': out_dir, 'img_context_id': img_id,
            'validated_questions': len(qs),
        }
    mpath = os.path.join(args.out_dir, 'tokenizer_patch_manifest.json')
    with open(mpath, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print('MANIFEST ' + json.dumps(manifest, ensure_ascii=False), flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

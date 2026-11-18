#!/usr/bin/env python3
"""Build adjudication_qwen2_5_vl_3b.jsonl + Qwen2.5-VL-3B failure cases (60).

Mirrors the 4B pipeline (adjudication_4b.jsonl, eval/failures/<qid>/<dim>/).
Adjudication rule (same as Carbon/2B/Gemini 4 Argon · High/8B/4B lines): hallucination=1 only
when the answer asserts a specific fact contradicting the reference, or
asserts without evidence a specific verifiable fact (attribution/title/
inscription/object). Generic brushwork terms and hedges inside uncertainty
notes do not count; omissions only hurt strict, not hallucination.
"""
import json
import os

# Project root: set SHIHUA_PROJECT_DIR, or run from the project root.
BASE = os.environ.get("SHIHUA_PROJECT_DIR", ".")
OUT_DIR = f'{BASE}/eval/results/audit_v0'
FAIL_DIR = f'{BASE}/eval/failures'
MODEL_LABEL = 'Qwen2.5-VL-3B (bf16)'
MODEL_SHORT = 'Qwen2.5-VL-3B'

# qid -> (final_hallucination, correct_rater, basis)
# Chair adjudication 2026-11-18, unified rule (same as Carbon/2B/Gemini 4 Argon · High/8B/4B/Qwen-7B):
# hallucination=1 only when the answer asserts a specific fact contradicting the
# reference, or asserts without evidence a specific verifiable fact
# (attribution/title/inscription/object/shape/count). Generic brushwork terms,
# generic cultural common sense, hedges and vague location/shape impressions do
# not count; omissions only hurt strict, not hallucination. Visual facts checked
# against data/visual_notes.md (verified) where the reference is silent.
ADJUDICATIONS = {
    'audit_v0_cma_135836_yixiang': (0, 'rater_b',
        'rater_b 正确："寺庙坐落在山脚下"与目检记录"山脚溪畔有小型寺宇建筑群"相合；"没有人物出现"未被参考答案或目检记录反驳（寺宇极小、未记录人物），属未触具体可核查事实的泛泛描述；遗漏留白表现云雾天空/使山体高远空灵/引导视线自下而上只扣分。'),
    'audit_v0_cma_139824_bimo': (0, 'rater_b',
        'rater_b 正确："担架用笔粗犷"为含糊笔法形容词，未点名具体皴法/器物/题款，未断言与参考答案矛盾的具体事实；"简括"与"粗犷"分属结构与笔触两个层面，不构成矛盾；遗漏货郎与孩童线条有别/器物繁密/墨线为主只扣分。'),
    'audit_v0_cma_142579_yixiang': (1, 'rater_a',
        'rater_a 正确：答案编造了"河流蜿蜒曲折，两岸的山石高耸入云，树木稀疏"等具体画面细节——目检记录为一座危崖占满画面 4/5、下部中央一叶小舟、右下水边一枝枯梅，无蜿蜒河流与两岸山石；"船上的人似乎在前行"亦与"微小人物仰望危崖"不符，属无据断言具体可核查事实。'),
    'audit_v0_cma_160135_yixiang': (0, 'rater_b',
        'rater_b 正确："两位渔夫"与目检记录相合（左缘小舟 1–2 人影＋中左篷船红袍渔人，渔人 2 名），非编造；遗漏江南家园/归乡之意/赵氏文人传统只扣分。'),
    'audit_v0_met_35989_yixiang': (0, 'rater_b',
        'rater_b 正确："人物坐在屋内"为茅亭的含糊转述，未断言与参考答案矛盾的具体事实；"沉思/敬畏反思"为泛泛抒情解读，未点名具体可核查事实；遗漏松象征君子德操/人小山大/茅亭栖居只扣分。'),
    'audit_v0_met_36178_yixiang': (0, 'rater_b',
        'rater_b 正确："高洁/适应环境/独立自主"为通用文化常识性说法，未断言与参考答案矛盾的具体事实（同 7B 36178_yixiang 判例）；"寓意因人而异"为 hedge，未断言具体事实；遗漏清末猛禽流行/振作自强迎春复新只扣分。'),
    'audit_v0_met_39936_bimo': (0, 'rater_b',
        'rater_b 正确："竹叶粗犷/羽毛光泽"为含糊笔法形容词，未断言具体可核查事实（同 7B 39936_bimo 判例）；遗漏绢本设色/鸟身褐色/鸟眼点漆/院体写实只扣分。'),
    'audit_v0_met_39936_yixiang': (0, 'rater_b',
        'rater_b 正确："吉祥/和平与安宁/淡泊"为通用文化常识性说法，未断言与参考答案矛盾的具体事实；遗漏褐色雀鸟与湖石构成的清雅小景/禽鸟添自然天趣只扣分。'),
    'audit_v0_met_40062_mingwu': (1, 'rater_a',
        'rater_a 正确："建筑是方形的"是对茅屋形制的具体断言——参考答案与目检记录均为茅顶小屋（屋顶、围栏可辨，依崖而建），"方形"无据且与茅顶小屋的形制不符，属无据断言具体可核查事实。'),
    'audit_v0_met_41185_bimo': (0, 'rater_b',
        'rater_b 正确："松针分笔"为含糊笔法术语，结论"松针画法工细"与参考答案一致（相对工致、成簇点写），未断言与参考答案矛盾的具体事实；遗漏淡墨晕染/边界柔和/工放对照只扣分。'),
    'audit_v0_met_41185_mingwu': (0, 'rater_b',
        'rater_b 正确："山脚下的平地上"为含糊位置描述，未点名与参考答案矛盾的具体位置事实（"低矮"与"体量很小"相合）；"文人山水传统"方向正确；遗漏溪边小茅屋具体位置/米点启发只扣分。'),
    'audit_v0_met_41185_yixiang': (0, 'rater_b',
        'rater_b 正确："松树象征高洁坚韧/构图简洁"为通用文化常识性说法与泛泛抒情，未断言具体可核查事实；不确定性说明为 hedge，未断言具体事实；遗漏明立国前两年/溪畔草堂象征只扣分。'),
    'audit_v0_met_41462_mingwu': (0, 'rater_b',
        'rater_b 正确："弯曲/苍劲"为对虬曲树干的泛泛视觉描述，未断言与参考答案矛盾的具体事实；"画家对自然力量的表现"为泛泛解读；"无法提供确切细节"为回避措辞，非对画面的事实断言；遗漏单株占满画面/盘曲结疤/针叶留白/大石/吴镇题跋只扣分。'),
    'audit_v0_met_41462_yixiang': (0, 'rater_b',
        'rater_b 正确：与 7B 线同题同判例——"坚韧不拔/高洁自守/长寿"为通用文化常识性说法，"松树独自矗立"为泛泛视觉描述，未断言与参考答案矛盾的具体事实，也未触禁止断言；遗漏冬日常青/元代政治隐喻/吴镇隐居自号只扣分。'),
    'audit_v0_met_41468_yixiang': (0, 'rater_b',
        'rater_b 正确：与 7B 线同题同判例——只泛谈隐逸生活/远离尘嚣，未断言功成名就/积极入世等禁止内容；遗漏元末失意文人象征/思归/放下钓竿只扣分。'),
    'audit_v0_met_62002_yixiang': (1, 'rater_a',
        'rater_a 正确：答案无据断言了具体可核查的画面细节——"背景是云彩和龙"中"龙"为编造（目检记录背景为祥云、深蓝天与金色光线，无龙）；"手持宝剑"亦与目检记录的青龙偃月刀（长柄大刀）不符；且问题可据参考答案作答（关羽），拒答不恰当。'),
    'audit_v0_met_739501_mingwu': (1, 'rater_a',
        'rater_a 正确："仅一朵莲花"与参考答案"淡粉、白色花朵数朵"直接矛盾；"右手拿扇子、左手放在膝盖上"亦为无据的具体姿态断言（参考答案只称手持团扇）；遗漏周敦颐身份/面向右侧莲池观莲/莲花生于树干脚下只扣分。'),
    'audit_v0_met_78125_bimo': (0, 'rater_b',
        'rater_b 正确："竹叶粗犷/书法细腻"为含糊笔法形容词，未触禁止断言（未称纤弱迟缓/设色重彩，同 7B 813350_bimo 判例）；结论"墨色画浓字淡不一致"与参考答案一致；遗漏竹叶尖利如剑/草书流利盘绕只扣分。'),
    'audit_v0_met_78125_yixiang': (0, 'rater_b',
        'rater_b 正确：与 7B 线同题同判例——"竹象征高洁坚韧/与千字文含义相呼应"为通用文化常识性说法，未断言具体可核查事实；遗漏千字文无重复字/詹景凤晚明书画兼擅只扣分。'),
    'audit_v0_met_813350_mingwu': (1, 'rater_a',
        'rater_a 正确："竹叶姿态各异"与参考答案"竹竿竹叶整体向同一方向倾倒、竹叶朝向高度一致、叶尖一律顺风向"直接矛盾（目检记录亦称皆向同一方向倾倒）；遗漏瀑布与悬崖只扣分。'),
}




def load_jsonl(path):
    rows = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main():
    qs = {r['id']: r for r in load_jsonl(f'{BASE}/data/audit_v0/questions.jsonl')}
    items = {r['artwork_id']: r for r in load_jsonl(f'{BASE}/data/audit_v0/items.jsonl')}
    answers = {r['id']: r['answer'] for r in load_jsonl(f'{OUT_DIR}/qwen2_5_vl_3b.jsonl')}
    ratings = {}
    for r in load_jsonl(f'{OUT_DIR}/ratings_qwen2_5_vl_3b.jsonl'):
        if r.get('score'):
            ratings.setdefault(r['id'], {})[r['rater']] = r['score']
    assert len(qs) == 60 and len(answers) == 60, (len(qs), len(answers))
    assert len(ratings) == 60 and all(
        'rater_a' in v and 'rater_b' in v for v in ratings.values())

    n_adj = n_a_correct = n_b_correct = 0
    adj_rows = []
    for qid in sorted(qs):
        q = qs[qid]
        a, b = ratings[qid]['rater_a'], ratings[qid]['rater_b']
        if qid in ADJUDICATIONS:
            final_h, correct, basis = ADJUDICATIONS[qid]
            adjudicated = True
            n_adj += 1
            if correct == 'rater_a':
                n_a_correct += 1
            else:
                n_b_correct += 1
        else:
            assert a['hallucination'] == b['hallucination'], qid
            final_h = a['hallucination']
            correct = None
            basis = '双评者一致，无分歧'
            adjudicated = False
        assert a['strict_hit'] == b['strict_hit'], qid
        final_s = a['strict_hit']
        partial_mean = (a['partial'] + b['partial']) / 2
        adj_rows.append({
            'id': qid, 'dimension': q['dimension'],
            'strict_hit': final_s, 'hallucination': final_h,
            'adjudicated': adjudicated, 'adjudication_basis': basis,
            'correct_rater': correct,
            'rater_a': a, 'rater_b': b,
            'partial_mean': partial_mean,
            'proper_refusal_agree': a['proper_refusal'] == b['proper_refusal'],
        })

    out_path = f'{OUT_DIR}/adjudication_qwen2_5_vl_3b.jsonl'
    with open(out_path, 'w', encoding='utf-8') as f:
        for row in adj_rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')

    # Failure cases: all 60 (0 fully clean: strict=1 & hallu=0 nowhere).
    n_cases = 0
    for row in adj_rows:
        qid = row['id']
        q = qs[qid]
        dim = q['dimension']
        d = os.path.join(FAIL_DIR, qid, dim)
        assert os.path.isdir(d), f'missing failure dir {d}'
        pred = {'id': qid,
                'model': f'{MODEL_LABEL} (T4, bf16, max_num=1280, transformers 4.49.0)',
                'answer': answers[qid]}
        with open(os.path.join(d, 'prediction_qwen2_5_vl_3b.json'),
                  'w', encoding='utf-8') as f:
            json.dump(pred, f, ensure_ascii=False, indent=1)
        ratings_rec = {'rater_a': row['rater_a'], 'rater_b': row['rater_b'],
                       'adjudicated': row['adjudicated'],
                       'basis': row['adjudication_basis']}
        with open(os.path.join(d, 'ratings_qwen2_5_vl_3b.json'), 'w', encoding='utf-8') as f:
            json.dump(ratings_rec, f, ensure_ascii=False, indent=1)
        cat = items[q['artwork_id']]['catalogue']
        work_line = (f"{q['artwork_id']}（{cat['title']}，"
                     f"{cat['attribution_verbatim']}，{cat['date_verbatim']}）")
        adj_line = ('裁决：' + row['adjudication_basis']) if row['adjudicated'] \
            else '裁决：双评者一致，无分歧'
        md = (f"# 失败案例 {qid}（{dim}）——{MODEL_SHORT}\n\n"
              f"- 作品：{work_line}\n"
              f"- 考生模型：{MODEL_LABEL}（T4，bf16，max_num=1280，transformers 4.49.0）\n"
              f"- 终判：strict_hit={row['strict_hit']}，hallucination={row['hallucination']}，"
              f"partial 均值={row['partial_mean']}\n"
              f"- 双评者：rater_a strict={row['rater_a']['strict_hit']}/hallu={row['rater_a']['hallucination']}；"
              f"rater_b strict={row['rater_b']['strict_hit']}/hallu={row['rater_b']['hallucination']}\n"
              f"- {adj_line}\n\n"
              f"## 题干\n\n{q['question']}\n\n"
              f"## 参考答案（锁定 v0）\n\n{q['answer']}\n\n"
              f"## Qwen2.5-VL-3B 回答（全文见 prediction_qwen2_5_vl_3b.json）\n\n{answers[qid]}\n\n"
              f"## 评者 notes\n\n"
              f"- rater_a：{row['rater_a']['notes']}\n"
              f"- rater_b：{row['rater_b']['notes']}\n")
        with open(os.path.join(d, 'judgment_qwen2_5_vl_3b.md'), 'w', encoding='utf-8') as f:
            f.write(md)
        n_cases += 1

    tot_h = sum(r['hallucination'] for r in adj_rows)
    tot_s = sum(r['strict_hit'] for r in adj_rows)
    tot_p = sum(r['partial_mean'] for r in adj_rows) / 60
    print(f'adjudication rows: {len(adj_rows)}')
    print(f'disagreements adjudicated: {n_adj} (rater_a correct {n_a_correct}, rater_b correct {n_b_correct})')
    print(f'final strict {tot_s}/60 hallu {tot_h}/60 partial_mean {tot_p:.3f}')
    print(f'failure cases written: {n_cases}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build adjudication_minicpm_v26.jsonl + MiniCPM-V-2_6-int4 failure cases (60).

Mirrors the Qwen2.5-VL-3B pipeline (adjudication_qwen2_5_vl_3b.jsonl,
eval/failures/<qid>/<dim>/).
Adjudication rule (same as Carbon/2B/Gemini 4 Argon · High/8B/4B/Qwen/Qwen-3B lines):
hallucination=1 only when the answer asserts a specific fact contradicting
the reference, or asserts without evidence a specific verifiable fact
(attribution/title/inscription/object/shape/count). Generic brushwork terms,
generic cultural common sense, hedges and vague location/shape impressions do
not count; omissions only hurt strict, not hallucination. Visual facts checked
against data/visual_notes.md (verified) where the reference is silent.
"""
import json
import os

# Project root: set SHIHUA_PROJECT_DIR, or run from the project root.
BASE = os.environ.get("SHIHUA_PROJECT_DIR", ".")
OUT_DIR = f'{BASE}/eval/results/audit_v0'
FAIL_DIR = f'{BASE}/eval/failures'
MODEL_LABEL = 'MiniCPM-V-2_6-int4 (int4)'
MODEL_SHORT = 'MiniCPM-V-2_6-int4'

# qid -> (final_hallucination, correct_rater, basis)
# Chair adjudication 2026-11-18, unified rule (same as Carbon/2B/Gemini 4 Argon · High/8B/4B/
# Qwen/Qwen-3B): hallucination=1 only when the answer asserts a specific fact
# contradicting the reference, or asserts without evidence a specific verifiable
# fact (attribution/title/inscription/object/shape/count). Generic brushwork
# terms, generic cultural common sense, hedges and vague location/shape
# impressions do not count; omissions only hurt strict, not hallucination.
# Visual facts checked against data/visual_notes.md (verified)
# where the reference is silent.
ADJUDICATIONS = {
    'audit_v0_cma_135836_bimo': (0, 'rater_b',
        'rater_b 正确：「细致密集」为含糊笔法形容词，未点名具体皴法/器物/题款，未断言与参考答案矛盾的具体事实（同 3B 线 139824_bimo 判例）；「淡浓渐变」与参考答案「墨色渐淡」「浓淡与虚实对比」方向相合；遗漏长披麻皴/湿点/山顶圆石只扣分。'),
    'audit_v0_cma_139824_mingwu': (0, 'rater_b',
        'rater_b 正确：「食品」出现在「可能是玩具、食品或其他日常用品」的猜测清单中，未作肯定断言；「年代久远故不确定」为不确定性说明的 hedge，未断言具体事实；其余皆为泛泛空话与无端回避；遗漏罐壶盒/工具/旗幡/骷髅与人物服饰动作只扣分。'),
    'audit_v0_cma_141693_bimo': (1, 'rater_a',
        'rater_a 正确：「山石高光留白、阴影深墨」为无据的具体技法断言——参考答案明言晨光由山间大片白色旋涡状云气的留白与淡设色烘托、未见日轮，山石只以细劲线条勾勒并施皴加淡设色；答案把云气留白错安为山石高光处理；遗漏无日轮/深红点染/淡设色只扣分。'),
    'audit_v0_cma_141693_yixiang': (0, 'rater_b',
        'rater_b 正确：「象征希望和新生」「世外桃源」「宁静致远」为通用文化常识性说法与泛泛抒情，未断言具体可核查事实（同 3B 线 41462_yixiang 判例）；遗漏黄帝求仙传说/朱砂仙药/生日贺礼/早期黄山图只扣分。'),
    'audit_v0_cma_142579_mingwu': (0, 'rater_b',
        'rater_b 正确：「崖顶有树木」与目检记录「崖顶有小树」相合，「画面上方有书法题字」与目检记录「上部布满石涛题跋数列＋朱印」相合，均非编造；「宁静与悠远」为泛泛意境描述；遗漏戴笠仰望/比例悬殊/枯梅/六朝历史追忆只扣分。'),
    'audit_v0_cma_142579_yixiang': (0, 'rater_b',
        'rater_b 正确：「树木光秃」是对崖顶小树＋右下枯梅的含糊视觉印象，未断言与目检记录矛盾的具体物象（3B 线同题判 rater_a 正确的「蜿蜒河流与两岸山石」在画面中全无，此题无此种编造）；「与繁华秦淮形成鲜明对比」为泛泛修辞，未断言具体事实；遗漏危崖/微小人物仰视巨崖/枯梅只扣分。'),
    'audit_v0_met_35989_bimo': (0, 'rater_b',
        'rater_b 正确：「细致的笔触」「宁静空灵」均为含糊笔法/意境形容词，未断言具体可核查事实；遗漏绳状层叠笔触/王蒙/金笺设色/金地留白分隔景物只扣分。'),
    'audit_v0_met_35989_mingwu': (1, 'rater_a',
        'rater_a 正确：「盘腿而坐」为无据的具体姿态断言——目检记录只记亭内坐一红袍士人（极小），未记坐姿（同 3B 线 739501_mingwu「右手拿扇子、左手放在膝盖上」判例）；「僧侣/修行者」与参考答案「文人居士一类，而非仆役或仙佛」方向相悖；遗漏茅亭/巨松/山石松树巨大只扣分。'),
    'audit_v0_met_35989_yixiang': (0, 'rater_b',
        'rater_b 正确：全篇只泛谈人与自然和谐/平衡/相互依存/崇敬与谦卑，未断言具体可核查事实；遗漏松象征君子德操/人小山大/士人坐于茅亭栖居山林只扣分。'),
    'audit_v0_met_36178_yixiang': (0, 'rater_b',
        'rater_b 正确：与 3B 线同题同判例——「高洁/坚韧/不屈」「鹰象征力量和自由」为通用文化常识性说法，未断言与参考答案矛盾的具体事实；遗漏清末猛禽流行/振作自强迎春复新只扣分。'),
    'audit_v0_met_39936_mingwu': (1, 'rater_a',
        'rater_a 正确：「树枝」与参考答案「竹枝」直接矛盾（两鸟均栖于竹枝上、向左/向右相向而立）；「竹子以淡雅的青绿色描绘」亦为无据的具体设色断言；遗漏朝向/相向关系/竹子生长方向/宋代院体写实传统只扣分。'),
    'audit_v0_met_40062_yixiang': (0, 'rater_b',
        'rater_b 正确：与 3B 线 41462_yixiang 判例同——「长寿」为松的通用文化常识性象征，未断言具体可核查事实；遗漏茅屋点出栖隐生活/松象征高士品格只扣分。'),
    'audit_v0_met_41185_yixiang': (0, 'rater_b',
        'rater_b 正确：与 3B 线同题同判例——「松象征坚韧长寿」「崇敬自然、向往隐居」为通用文化常识性说法与泛泛抒情，未断言具体可核查事实；遗漏明立国前两年/元末溪畔草堂象征只扣分。'),
    'audit_v0_met_41462_bimo': (0, 'rater_b',
        'rater_b 正确：「线条细长」「空洞和空灵」为含糊笔法/意境形容词，未点名具体可核查事实（同 3B 线 39936_bimo「竹叶粗犷」判例）；「细小的点画」与参考答案「成簇点写」方向相合；遗漏纯水墨不施色/松皮粗犷皴笔/松针成簇生于枝端/枝间留白只扣分。'),
    'audit_v0_met_41462_yixiang': (0, 'rater_b',
        'rater_b 正确：与 3B 线同题同判例——「坚韧不拔/高风亮节/长寿」为通用文化常识性说法，「岩石上生存」为泛泛环境描述，未断言具体可核查事实；遗漏元代政治隐喻/吴镇隐居自号梅花道人只扣分。'),
    'audit_v0_met_41468_yixiang': (0, 'rater_b',
        'rater_b 正确：与 3B 线同题同判例——只泛谈闲适宁静/自由淡泊/远离喧嚣，未断言功成名就/积极入世等禁止内容；遗漏元末失意文人象征/思归/放下钓竿只扣分。'),
    'audit_v0_met_49047_bimo': (1, 'rater_a',
        'rater_a 正确：答案把蝴蝶确定为「工笔」、把湖石与花朵定为「写意」并作对比——参考答案明言「仅凭图像无法确认其严格画法归属」，且馆方称全画笔法欠精；肯定的画法归属断言与参考答案明示的不确定性直接矛盾；遗漏笔法欠精只扣分。'),
    'audit_v0_met_62002_bimo': (0, 'rater_b',
        'rater_b 正确：「衣纹线条流畅富有动感」「面部线条柔和」为含糊笔法形容词，未断言具体可核查事实；「金色可能象征高贵神圣」有「可能」修饰且为通用象征说法；遗漏贴金/矿物颜料/金色用于右上题识/衬托光晕只扣分。'),
    'audit_v0_met_62002_yixiang': (1, 'rater_a',
        'rater_a 正确：「身着华丽的盔甲」将从者（左后须髯武将戴红缨盔、着甲）的甲胄错安到主角身上——目检记录主角关羽为绿袍、长髯、蓝头巾、持青龙偃月刀、头后光晕，未着甲；属无据的具体服饰断言（「手持武器」「在云端」本身与青龙偃月刀/祥云背景相合，不另计）。'),
    'audit_v0_met_739501_mingwu': (0, 'rater_b',
        'rater_b 正确：「莲花位于右下角」与目检记录相合；「与周围的岩石和植物融为一体」为含糊环境印象，未点名具体位置/数量/形制；「可能暗示人物品格」为 hedge；遗漏周敦颐身份/倚石坐/面向莲池观莲/生于树干脚下只扣分。'),
    'audit_v0_met_739501_yixiang': (0, 'rater_b',
        'rater_b 正确：「服饰和举止……可能代表周敦颐」有「可能」修饰，未作肯定断言；周敦颐与《爱莲说》本身命中；遗漏「出淤泥而不染」/洁身自好/高洁自守只扣分。'),
    'audit_v0_met_78125_bimo': (0, 'rater_b',
        'rater_b 正确：「粗细均匀/墨色均匀」为含糊笔法形容词，未点名具体可核查事实（同 3B 线同题判例：书法细腻为含糊笔法形容词）；「竹叶浓、书法淡、不一致」与参考答案相合；遗漏竹叶尖利如剑出锋/草书流利盘绕只扣分。'),
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
    answers = {r['id']: r['answer'] for r in load_jsonl(f'{OUT_DIR}/minicpm_v26_int4.jsonl')}
    ratings = {}
    for r in load_jsonl(f'{OUT_DIR}/ratings_minicpm_v26.jsonl'):
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

    out_path = f'{OUT_DIR}/adjudication_minicpm_v26.jsonl'
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
                'model': f'{MODEL_LABEL} (T4, int4, max_slice_nums=9, transformers 4.49.0)',
                'answer': answers[qid]}
        with open(os.path.join(d, 'prediction_minicpm_v26.json'),
                  'w', encoding='utf-8') as f:
            json.dump(pred, f, ensure_ascii=False, indent=1)
        ratings_rec = {'rater_a': row['rater_a'], 'rater_b': row['rater_b'],
                       'adjudicated': row['adjudicated'],
                       'basis': row['adjudication_basis']}
        with open(os.path.join(d, 'ratings_minicpm_v26.json'), 'w', encoding='utf-8') as f:
            json.dump(ratings_rec, f, ensure_ascii=False, indent=1)
        cat = items[q['artwork_id']]['catalogue']
        work_line = (f"{q['artwork_id']}（{cat['title']}，"
                     f"{cat['attribution_verbatim']}，{cat['date_verbatim']}）")
        adj_line = ('裁决：' + row['adjudication_basis']) if row['adjudicated'] \
            else '裁决：双评者一致，无分歧'
        md = (f"# 失败案例 {qid}（{dim}）——{MODEL_SHORT}\n\n"
              f"- 作品：{work_line}\n"
              f"- 考生模型：{MODEL_LABEL}（T4，int4，max_slice_nums=9，transformers 4.49.0）\n"
              f"- 终判：strict_hit={row['strict_hit']}，hallucination={row['hallucination']}，"
              f"partial 均值={row['partial_mean']}\n"
              f"- 双评者：rater_a strict={row['rater_a']['strict_hit']}/hallu={row['rater_a']['hallucination']}；"
              f"rater_b strict={row['rater_b']['strict_hit']}/hallu={row['rater_b']['hallucination']}\n"
              f"- {adj_line}\n\n"
              f"## 题干\n\n{q['question']}\n\n"
              f"## 参考答案（锁定 v0）\n\n{q['answer']}\n\n"
              f"## {MODEL_SHORT} 回答（全文见 prediction_minicpm_v26.json）\n\n{answers[qid]}\n\n"
              f"## 评者 notes\n\n"
              f"- rater_a：{row['rater_a']['notes']}\n"
              f"- rater_b：{row['rater_b']['notes']}\n")
        with open(os.path.join(d, 'judgment_minicpm_v26.md'), 'w', encoding='utf-8') as f:
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

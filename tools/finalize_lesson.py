#!/usr/bin/env python3
"""
finalize_lesson.py — deterministic post-fixes + validation + merge for one authored lesson.

The lesson-authoring Workflow (see docs/AUTHORING.md) produces a raw lesson object
(title, next, blocks[], review[]). This script cleans it, validates it against the house
rules, and merges it into lessons/<course>/chapter-N.json. It NEVER invents math; it only
normalizes escaping/formatting and reports structural or style problems for a human to fix.

Usage:
    python3 tools/finalize_lesson.py <lesson.json> \
        --course algebra1 --chapter 1 --key 1.3 \
        --title "When Order Matters" --next 1.4 [--write]

Without --write it prints the issue report only. With --write it merges the lesson into the
chapter file (creating it if needed) and re-sorts lessons by key. After writing, ALWAYS run
`python3 tools/build_lessons.py` to regenerate data/lessons.js.
"""
import json, re, os, sys, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

KATEX_TOKENS = ('(', ')', '[', ']', 'boxed', 'frac', 'dfrac', 'sqrt', 'pi', 'times', 'cdot',
                'div', 'dots', 'ldots', 'text', 'quad', 'qquad', 'neq', 'le', 'ge', 'left',
                'right', 'overline', 'cdots')

# Register words that betray the "poetic" voice the user banned (see memory: no-em-dashes).
# Not exhaustive; a nudge, not a gate. Review anything flagged.
REGISTER_WORDS = ['honest reader', 'one string', 'the agreement', 'speaks first', 'the chant',
                  'rung of the ladder', 'outdoor clothing', 'in one breath', 'grabs', 'grip',
                  'seals', 'balloon', 'crowning', 'wears', 'costume', 'in disguise']


def fix_str(s):
    # collapse doubled backslashes that precede KaTeX tokens (a JSON-transport artifact)
    while any('\\\\' + t in s for t in KATEX_TOKENS):
        s = s.replace('\\\\', '\\')
    s = s.replace('\\n', ' ').replace('\n', ' ')
    return re.sub(r'  +', ' ', s).strip()


def walk_strings(obj, fn):
    if isinstance(obj, dict):
        return {k: walk_strings(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk_strings(v, fn) for v in obj]
    if isinstance(obj, str):
        return fn(obj)
    return obj


def norm(a):
    return str(a).lower().replace(' ', '').replace(',', '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lesson_json')
    ap.add_argument('--course', required=True)
    ap.add_argument('--chapter', type=int, required=True)
    ap.add_argument('--key', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--next', dest='nxt', default='')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()

    lesson = json.load(open(args.lesson_json, encoding='utf-8'))
    lesson = walk_strings(lesson, fix_str)
    lesson['title'] = args.title
    if args.nxt:
        lesson['next'] = args.nxt

    # review items are prob-shaped but carry NO t and NO xp
    for r in lesson.get('review', []):
        r.pop('t', None)
        r.pop('xp', None)

    problems = []

    def ensure_ans_in_accept(p):
        ans = str(p.get('ans', '')).strip()
        acc = [str(a).strip() for a in (p.get('accept') or [])]
        if ans and norm(ans) not in [norm(a) for a in acc]:
            acc.insert(0, ans)
        seen, out = set(), []
        for a in acc:
            if norm(a) not in seen:
                seen.add(norm(a)); out.append(a)
        p['ans'], p['accept'] = ans, out

    probs = [(f'block[{i}]', b) for i, b in enumerate(lesson.get('blocks', [])) if b.get('t') == 'prob']
    probs += [(f'review[{i}]', r) for i, r in enumerate(lesson.get('review', []))]
    for where, p in probs:
        ensure_ans_in_accept(p)
        if '\\boxed' not in p.get('sol', ''):
            problems.append((where, 'sol missing \\boxed'))
        if not p.get('hints'):
            problems.append((where, 'no hints'))

    for i, b in enumerate(lesson.get('blocks', [])):
        if b.get('t') != 'prob':
            for f in ('xp', 'ans', 'accept', 'hints', 'sol'):
                if f in b and not b[f]:
                    del b[f]
                elif f in b and b[f]:
                    problems.append((f'block[{i}]', f'non-prob block has non-empty {f}'))
        else:
            if not isinstance(b.get('xp'), (int, float)) or not (5 <= b['xp'] <= 8):
                problems.append((f'block[{i}]', f"xp={b.get('xp')!r} out of 5-8"))
        for f in ('label', 'cap'):
            if f in b and not b[f]:
                del b[f]
        if b.get('t') == 'fig' and 'Inter' in b.get('x', ''):
            problems.append((f'block[{i}]', 'figure uses Inter; must be Space Grotesk, sans-serif'))
        if b.get('t') == 'fig' and 'font-weight="800"' in b.get('x', ''):
            problems.append((f'block[{i}]', 'figure uses font-weight 800 (fake-bolds to a generic sans); cap at 700'))

    def check_text(where, s):
        if '—' in s:
            problems.append((where, 'EM-DASH present'))
        if s.count('\\(') != s.count('\\)'):
            problems.append((where, 'unbalanced \\( \\)'))
        if s.count('$$') % 2:
            problems.append((where, 'unbalanced $$'))
        for m in re.finditer(r'\\boxed', s):
            pre = s[:m.start()]
            if not (pre.count('\\(') > pre.count('\\)') or pre.count('$$') % 2 == 1):
                problems.append((where, 'unwrapped \\boxed (not inside \\( \\) or $$)'))

    def walk_check(obj, where):
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk_check(v, f'{where}.{k}')
        elif isinstance(obj, list):
            for j, v in enumerate(obj):
                walk_check(v, f'{where}[{j}]')
        elif isinstance(obj, str):
            check_text(where, obj)

    walk_check(lesson, 'lesson')

    # prose scans (skip inside math and inside svg)
    def prose(x):
        p = re.sub(r'\\\(.*?\\\)', '', x)
        p = re.sub(r'\$\$.*?\$\$', '', p)
        return p

    for i, b in enumerate(lesson.get('blocks', [])):
        if b.get('t') == 'fig':
            continue
        for f in ('x', 'sol'):
            if not b.get(f):
                continue
            pr = prose(b[f])
            if ':' in pr:
                idx = pr.index(':')
                problems.append((f'block[{i}].{f}', f'colon in prose: ...{pr[max(0,idx-30):idx+20]}...'))
            for w in REGISTER_WORDS:
                if w in pr.lower():
                    problems.append((f'block[{i}].{f}', f'register word: "{w}"'))
    for i, r in enumerate(lesson.get('review', [])):
        for f in ('x', 'sol'):
            pr = prose(r.get(f, ''))
            if ':' in pr:
                problems.append((f'review[{i}].{f}', 'colon in prose'))
            for w in REGISTER_WORDS:
                if w in pr.lower():
                    problems.append((f'review[{i}].{f}', f'register word: "{w}"'))

    print('=== issues ===')
    for w, m in problems:
        print(f'{w}: {m}')
    nprob = sum(1 for b in lesson['blocks'] if b.get('t') == 'prob')
    print(f'{len(problems)} issues | blocks={len(lesson["blocks"])} probs={nprob} '
          f'review={len(lesson.get("review", []))}')

    if args.write:
        if problems:
            print('\nWARNING: writing despite issues above. Re-run without --write after fixing, '
                  'or fix them in the chapter file.')
        path = os.path.join(ROOT, 'lessons', args.course, f'chapter-{args.chapter}.json')
        ch = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else {}
        ch[args.key] = lesson
        ch = {k: ch[k] for k in sorted(ch, key=lambda s: [int(p) for p in s.split('.')])}
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(ch, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print(f'wrote {path} with lessons {list(ch.keys())}')
        print('NEXT: python3 tools/build_lessons.py')


if __name__ == '__main__':
    main()

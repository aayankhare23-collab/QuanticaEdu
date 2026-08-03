#!/usr/bin/env python3
"""Swap a rendered figure SVG into a lesson's fig block.

    python3 tools/lesson-figs/apply_fig.py 7.1 --course algebra1 [--cap "..."] [--write]

Finds the single fig block in lessons/<course>/chapter-<N>.json for that key and
replaces its `x` with tools/lesson-figs/fig_<key>.svg. Without --write it only
reports what it would do. Run tools/build_lessons.py afterwards.
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('key')
    ap.add_argument('--course', default='algebra1')
    ap.add_argument('--cap')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()

    svg_path = ROOT / 'tools/lesson-figs' / f"fig_{a.key.replace('.', '_')}.svg"
    if not svg_path.exists():
        sys.exit(f'no rendered figure at {svg_path}')
    svg = svg_path.read_text(encoding='utf-8').strip()

    ch = a.key.split('.')[0]
    lesson_path = ROOT / 'lessons' / a.course / f'chapter-{ch}.json'
    if not lesson_path.exists():
        sys.exit(f'no {lesson_path}; the lesson has to exist first')
    raw = lesson_path.read_text(encoding='utf-8')
    data = json.loads(raw)
    if a.key not in data:
        sys.exit(f'{a.key} not in {lesson_path.name}')

    figs = [i for i, b in enumerate(data[a.key]['blocks']) if b.get('t') == 'fig']
    if len(figs) != 1:
        sys.exit(f'{a.key} has {len(figs)} fig blocks, expected exactly 1')
    i = figs[0]
    old = data[a.key]['blocks'][i]
    print(f'{a.key} blocks[{i}]: {len(old.get("x", ""))} bytes -> {len(svg)} bytes')
    print(f'  cap kept: {(a.cap or old.get("cap", ""))[:90]}')

    # the numbers a figure prints must not pre-solve a nearby problem
    fignums = {int(m.replace('−', '-')) for m in re.findall(r'>\s*([+−-]?\d+)', svg)}
    fignums = {n for n in fignums if abs(n) >= 12}
    probs = [b for b in data[a.key]['blocks'] if b.get('t') == 'prob'] + data[a.key].get('review', [])
    for p in probs:
        shared = fignums & {int(m) for m in re.findall(r'\d+', p.get('x', '')) if int(m) >= 12}
        if len(shared) >= 2:
            print(f'  WARNING shares {sorted(shared)} with a problem: {p["x"][:70]}')

    if not a.write:
        print('  (dry run, pass --write to apply)')
        return
    old['x'] = svg
    if a.cap:
        old['cap'] = a.cap
    indent = 1 if raw.startswith('{\n ') and not raw.startswith('{\n  ') else 2
    ensure_ascii = '\\u' in raw[:4000]
    lesson_path.write_text(
        json.dumps(data, indent=indent, ensure_ascii=ensure_ascii) + '\n', encoding='utf-8')
    print(f'  written to {lesson_path.name} (indent {indent}); now run tools/build_lessons.py')


if __name__ == '__main__':
    main()

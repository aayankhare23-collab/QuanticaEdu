#!/usr/bin/env python3
"""
Build step for QuanticaEdu.

Lesson content is authored in the external files lessons/prealgebra/chapter-*.json
(the single source of truth). The running app loads all lessons from data/lessons.js,
which sets the global `window.__CHDATA`; landing.html pulls it in with a <script> tag
placed just before the app script (this keeps landing.html small, ~381KB, and lets the
browser cache the content blob separately).

This script bakes the external JSON into data/lessons.js by regenerating the
`window.__CHDATA={...};` assignment. Workflow: edit the JSON, run this script,
commit both. Never hand-edit data/lessons.js; it is generated.

(History: before the 2026-07-01 split this wrote a `var chData={...}` block INSIDE
landing.html. It now targets data/lessons.js. Do not point it back at landing.html or
it will re-inline 2.24MB and undo the split.)
"""
import json, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'lessons.js')
LESSON_GLOB = os.path.join(ROOT, 'lessons', 'prealgebra', 'chapter-*.json')
PREFIX = 'window.__CHDATA='

def chapter_num(path):
    base = os.path.basename(path)
    return int(base.replace('chapter-', '').replace('.json', ''))

def main():
    merged = {}
    for f in sorted(glob.glob(LESSON_GLOB), key=chapter_num):
        merged.update(json.load(open(f, encoding='utf-8')))
    if not merged:
        sys.exit('no lesson JSON found')

    # one lesson per line, compact within each (generated asset, not hand-edited).
    # Byte-for-byte the same literal format the split extracted, so an unchanged
    # source set regenerates data/lessons.js identically (diff shows only real edits).
    lines = [json.dumps(k) + ':' + json.dumps(v, ensure_ascii=False, separators=(',', ':'))
             for k, v in merged.items()]
    literal = '{\n' + ',\n'.join(lines) + '\n}'
    out = PREFIX + literal + ';\n'

    # guard against breaking the surrounding <script> tag
    if '</script' in out.lower():
        sys.exit('lesson content contains </script>; refusing to embed')

    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    open(DATA, 'w', encoding='utf-8').write(out)

    # verify round-trip: re-parse and compare semantically
    got = json.loads(open(DATA, encoding='utf-8').read()[len(PREFIX):].rstrip().rstrip(';'))
    assert got == merged, 'round-trip mismatch'
    print(f'built {len(merged)} lessons into data/lessons.js ({len(out)} bytes)')

if __name__ == '__main__':
    main()

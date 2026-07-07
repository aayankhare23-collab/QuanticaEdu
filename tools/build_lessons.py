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
COURSES = ['prealgebra', 'algebra1']   # course dirs under lessons/; first is the default course
PREFIX = 'window.__COURSEDATA='

def chapter_num(path):
    base = os.path.basename(path)
    return int(base.replace('chapter-', '').replace('.json', ''))

def main():
    courses = {}
    for course in COURSES:
        merged = {}
        for f in sorted(glob.glob(os.path.join(ROOT, 'lessons', course, 'chapter-*.json')), key=chapter_num):
            merged.update(json.load(open(f, encoding='utf-8')))
        courses[course] = merged
    if not courses.get('prealgebra'):
        sys.exit('no prealgebra lesson JSON found')

    # one lesson per line, compact within each (generated asset, not hand-edited).
    # Courses nest one level deep; window.__CHDATA stays aliased to prealgebra for
    # back-compat with every existing consumer.
    course_blocks = []
    for course in COURSES:
        lines = [json.dumps(k) + ':' + json.dumps(v, ensure_ascii=False, separators=(',', ':'))
                 for k, v in courses[course].items()]
        course_blocks.append(json.dumps(course) + ':{\n' + ',\n'.join(lines) + '\n}')
    literal = '{\n' + ',\n'.join(course_blocks) + '\n}'
    out = PREFIX + literal + ';\nwindow.__CHDATA=window.__COURSEDATA["prealgebra"];\n'

    # guard against breaking the surrounding <script> tag
    if '</script' in out.lower():
        sys.exit('lesson content contains </script>; refusing to embed')

    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    open(DATA, 'w', encoding='utf-8').write(out)

    # verify round-trip: re-parse and compare semantically
    raw = open(DATA, encoding='utf-8').read()
    got = json.loads(raw[len(PREFIX):raw.index(';\nwindow.__CHDATA')])
    assert got == courses, 'round-trip mismatch'
    counts = ', '.join(f"{c}: {len(courses[c])}" for c in COURSES)
    print(f'built lessons into data/lessons.js ({counts}; {len(out)} bytes)')

if __name__ == '__main__':
    main()

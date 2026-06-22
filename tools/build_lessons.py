#!/usr/bin/env python3
"""
Build step for QuanticaEdu.

Lesson content is authored in the external files lessons/prealgebra/chapter-*.json
(the single source of truth). The deployed site is one self-contained landing.html
so the browser makes no per-lesson fetch (lowest lag, works even opened directly).

This script bakes the external JSON into landing.html by regenerating the
`var chData={...};` block in place. Workflow: edit the JSON, run this script,
commit both. Never hand-edit the chData block; it is generated.
"""
import json, glob, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANDING = os.path.join(ROOT, 'landing.html')
LESSON_GLOB = os.path.join(ROOT, 'lessons', 'prealgebra', 'chapter-*.json')

def chapter_num(path):
    base = os.path.basename(path)
    return int(base.replace('chapter-', '').replace('.json', ''))

def find_chdata_span(html):
    """Return (start, end) char offsets covering `var chData=...;` (incl. trailing ;)."""
    i = html.index('var chData=')
    j = html.index('{', i)
    depth, instr, esc = 0, False, False
    end = None
    for k in range(j, len(html)):
        c = html[k]
        if instr:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == '"': instr = False
        else:
            if c == '"': instr = True
            elif c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    end = k + 1
                    break
    if end is None:
        raise RuntimeError('could not brace-match chData literal')
    # absorb a trailing semicolon
    m = end
    while m < len(html) and html[m] in ' \t':
        m += 1
    if m < len(html) and html[m] == ';':
        m += 1
    return i, m

def main():
    merged = {}
    for f in sorted(glob.glob(LESSON_GLOB), key=chapter_num):
        merged.update(json.load(open(f, encoding='utf-8')))
    if not merged:
        sys.exit('no lesson JSON found')

    # one lesson per line, compact within each (generated asset, not hand-edited)
    lines = [json.dumps(k) + ':' + json.dumps(v, ensure_ascii=False, separators=(',', ':'))
             for k, v in merged.items()]
    block = 'var chData={\n' + ',\n'.join(lines) + '\n};'

    # guard against breaking the surrounding <script> tag
    if '</script' in block.lower():
        sys.exit('lesson content contains </script>; refusing to embed')

    html = open(LANDING, encoding='utf-8').read()
    a, b = find_chdata_span(html)
    new_html = html[:a] + block + html[b:]
    open(LANDING, 'w', encoding='utf-8').write(new_html)

    # verify round-trip: re-extract and compare semantically
    a2, b2 = find_chdata_span(new_html)
    got = json.loads(new_html[a2:b2][len('var chData='):].rstrip(';'))
    assert got == merged, 'round-trip mismatch'
    print(f'built {len(merged)} lessons into landing.html ({len(block)} bytes in chData block)')

if __name__ == '__main__':
    main()

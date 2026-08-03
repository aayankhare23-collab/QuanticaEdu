#!/usr/bin/env python3
"""Evaluate a workflow's pyChecks and compare each to the lesson's shipped answer.

The verify phase rewrites most items, so the blueprint's numbers are not what ships.
This closes the loop mechanically: every pyexpr is evaluated with exact Fraction
arithmetic and matched against the `ans` that is actually in the lesson file.

    python3 tools/verify_answers.py lesson.json pychecks.json

pychecks.json is the `pyChecks` array the workflow returns, entries shaped
{where, pyexpr, ans}. `where` is "block[i]" or "review[i]"; the answer is re-read
from the LESSON file at that index, never trusted from the pyChecks entry.
"""
import json, re, sys
from fractions import Fraction


def norm(a):
    return str(a).strip().lower().replace(' ', '').replace(',', '').lstrip('+').replace('−', '-')


def as_frac(s):
    try:
        return Fraction(norm(s))
    except Exception:
        return None


def main(lesson_path, checks_path):
    L = json.load(open(lesson_path, encoding='utf-8'))
    checks = json.load(open(checks_path, encoding='utf-8'))
    probs = [b for b in L['blocks'] if b.get('t') == 'prob']
    blocks_by_idx = {i: b for i, b in enumerate(L['blocks']) if b.get('t') == 'prob'}
    ok = fail = skip = 0
    for c in checks:
        m = re.match(r'(block|review)\[(\d+)\]', c.get('where', ''))
        if not m:
            print(f"  ?? unparseable where {c.get('where')!r}"); skip += 1; continue
        kind, i = m.group(1), int(m.group(2))
        item = blocks_by_idx.get(i) if kind == 'block' else (
            L['review'][i] if i < len(L['review']) else None)
        if item is None:
            print(f"  ?? {c['where']} not found in lesson"); skip += 1; continue
        expr = (c.get('pyexpr') or '').strip()
        if not expr:
            print(f"  -- {c['where']} no pyexpr (non-numeric), re-solve by hand"); skip += 1; continue
        try:
            val = eval(expr, {'__builtins__': {}}, {  # noqa: S307 - our own generated exprs
                'Fraction': Fraction, 'abs': abs, 'min': min, 'max': max, 'sum': sum,
                'round': round, 'int': int, 'len': len, 'range': range, 'sorted': sorted,
                'pow': pow, 'all': all, 'any': any, 'set': set, 'list': list})
        except Exception as e:
            print(f"  !! {c['where']} pyexpr failed: {e}  [{expr[:70]}]"); fail += 1; continue
        want = as_frac(item['ans'])
        got = val if isinstance(val, (int, Fraction)) else as_frac(val)
        same = (want is not None and got is not None and Fraction(got) == want) \
            or norm(val) == norm(item['ans'])
        if same:
            ok += 1
        else:
            fail += 1
            print(f"  MISMATCH {c['where']}: pyexpr -> {val!r}, lesson ans {item['ans']!r}")
            print(f"           {expr[:110]}")
    print(f'{ok} match, {fail} mismatch, {skip} needing a hand re-solve, of {len(checks)}')
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))

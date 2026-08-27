#!/usr/bin/env python3
"""Deterministic checks for a chapter PSET (practice + challenge).

Mirrors check_lesson.py but for the PSETS schema: 1 hint on practice, 2 on challenge,
legendary only on the last three challenge items, <p>-wrapped answer-first solutions,
and the literal-dollar KaTeX gotcha.

Usage: python3 check_pset.py pset.json
"""
import json, re, sys
from fractions import Fraction
from collections import Counter


def norm(a):
    """Mirror of normAns in landing.html, which is what actually grades a student.

    Kept in lockstep on purpose. More permissive than the grader and this invents
    redundancies that are not real; less permissive and it misses dead accept
    entries, which is how every lesson from Algebra I chapter 4 on ended up with
    both "-91.0" and "\u221291.0" in its accept list. Port any normAns change to
    BOTH this and check_lesson.py.
    """
    s = ('' if a is None else str(a)).strip()
    s = re.sub(r'[\u2212\u2013\u2014]', '-', s)          # U+2212 and the dashes are all a minus
    s = s.lower().replace(',', '')
    s = re.sub(r'^(-?)\$|^\$(-?)', r'\1\2', s, count=1)   # "$12", "-$3" and "$-3" shed the $
    m = re.match(r'^(-?)(\d{1,9})[ \t]+(\d{1,9})\s*/\s*(\d{1,9})\Z', s)
    if m:                                                 # "1 1/2" -> "3/2", BEFORE spaces go
        den = int(m.group(4))
        if den > 0:
            s = m.group(1) + str(int(m.group(2)) * den + int(m.group(3))) + '/' + str(den)
    return re.sub(r'^\+', '', re.sub(r'\s+', '', s), count=1)


def brace_span(s, i):
    d = 0
    while i < len(s):
        if s[i] == '{':
            d += 1
        elif s[i] == '}':
            d -= 1
            if d == 0:
                return i + 1
        i += 1
    return -1


def boxed_values(sol):
    out = []
    for m in re.finditer(r'\\boxed\s*\{', sol):
        j = brace_span(sol, m.end() - 1)
        out.append(None if j < 0 else sol[m.end():j - 1])
    return out


def latex_to_value(t):
    t = t.strip()
    # \boxed{4\tfrac{3}{5}} is a mixed number, but flattening it glues the parts into
    # "43/5", forty-three fifths. normAns only folds a mixed number when a space
    # separates the whole part, so put that space back before the general rule runs.
    t = re.sub(r'(\d)\s*\\[tdc]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}', r'\1 \2/\3', t)
    t = re.sub(r'\\[tdc]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}', r'\1/\2', t)
    # A word answer is boxed as \text{parallel}. check_lesson.py already strips this;
    # without the same rule here every word-answer item reads as \textparallel != parallel.
    t = re.sub(r'\\(?:text|mathrm|mbox)\s*\{([^{}]*)\}', r'\1', t)
    for junk in ('\\!', '\\,', '\\ ', '\\left', '\\right', '\\$', '{', '}'):
        t = t.replace(junk, '')
    # No whitespace collapse here: norm() strips it last, after the mixed-number fold.
    return t.replace('\u2212', '-').strip()


def numeric(s):
    try:
        return Fraction(norm(s).replace('−', '-'))
    except Exception:
        return None


def numbers_in(s):
    return tuple(sorted(Counter(int(m) for m in re.findall(r'\d+', s or '') if int(m) >= 2).items()))


def main(path):
    D = json.load(open(path, encoding='utf-8'))
    P, C = D['practice'], D['challenge']
    items = [(f'practice[{i}]', b, 1) for i, b in enumerate(P)] + [(f'challenge[{i}]', b, 2) for i, b in enumerate(C)]
    bad = []
    sig, seen_ans = {}, {}
    for where, p, want_hints in items:
        ans, sol = str(p.get('ans', '')), p.get('sol', '')
        bv = boxed_values(sol)
        if not bv:
            bad.append((where, 'no \\boxed in sol'))
        else:
            last = latex_to_value(bv[-1])
            na, nb = numeric(ans), numeric(last)
            if not ((na is not None and nb is not None and na == nb) or norm(last) == norm(ans)):
                bad.append((where, f'boxed {last!r} != ans {ans!r}'))
            if len(bv) > 1:
                bad.append((where, f'{len(bv)} boxed values in one sol'))
        h = p.get('hints') or []
        if len(h) != want_hints:
            bad.append((where, f'{len(h)} hints (want exactly {want_hints})'))
        acc = [norm(a) for a in (p.get('accept') or [])]
        if norm(ans) not in acc:
            bad.append((where, 'ans not in accept'))
        if len(acc) != len(set(acc)):
            bad.append((where, 'duplicate accept entries'))
        if norm(ans) in seen_ans:
            bad.append((where, f'answer {ans!r} duplicates {seen_ans[norm(ans)]}'))
        else:
            seen_ans[norm(ans)] = where
        n = numbers_in(p.get('x', ''))
        if n in sig:
            bad.append((where, f'same number multiset as {sig[n]}'))
        elif n:
            sig[n] = where
        if not sol.strip().startswith('<p>') or not sol.strip().endswith('</p>'):
            bad.append((where, 'sol not wrapped in <p>...</p>'))
        if len(sol) > 700:
            bad.append((where, f'sol {len(sol)} chars (>700)'))
        xl = len(p.get('x', ''))
        if not (110 <= xl <= 470):
            bad.append((where, f'x {xl} chars (want 110-470)'))
        for fname, s in [('x', p.get('x', '')), ('sol', sol)] + [(f'hints[{i}]', v) for i, v in enumerate(h)]:
            if '\\\\' in s:
                bad.append((where, f'{fname}: doubled backslash'))
            if re.search(r'(?<!\\)\$(?!\$)', re.sub(r'\$\$.*?\$\$', '', s, flags=re.S)):
                bad.append((where, f'{fname}: raw single-$ (KaTeX will treat it as a delimiter)'))
            if '—' in s:
                bad.append((where, f'{fname}: EM-DASH'))
            if s.count('\\(') != s.count('\\)'):
                bad.append((where, f'{fname}: unbalanced \\( \\)'))
            plain = re.sub(r'\$\$.*?\$\$', '', re.sub(r'\\\(.*?\\\)', '', s, flags=re.S), flags=re.S)
            plain = re.sub(r'<[^>]+>', '', plain)
            if ':' in plain:
                bad.append((where, f'{fname}: colon in prose'))

    # legendary must be exactly the last three challenge items
    legs = [i for i, c in enumerate(C) if c.get('legendary')]
    if legs != [len(C) - 3, len(C) - 2, len(C) - 1]:
        bad.append(('challenge', f'legendary at {legs}, want {[len(C)-3, len(C)-2, len(C)-1]}'))
    if any(p.get('legendary') for p in P):
        bad.append(('practice', 'legendary flag present on a practice item'))
    if len(P) != 12 or len(C) != 12:
        bad.append(('counts', f'practice {len(P)}, challenge {len(C)} (want 12 and 12)'))

    print(f'=== {path} ===')
    for w, m in bad:
        print(f'{w}: {m}')
    print(f'{len(bad)} issues | practice={len(P)} challenge={len(C)} legendary={len(legs)}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))

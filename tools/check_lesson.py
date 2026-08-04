#!/usr/bin/env python3
"""Deterministic checks that finalize_lesson.py does NOT do.

  boxed value == ans   (proper brace matcher, handles \frac{}{} nesting)
  exactly 2 hints everywhere
  accept contains ans, and no accept entry normalizes to something silly
  duplicate full number-sets across problems (collision detector)
  sol length targets
  raw single-$ math, stray \\ artifacts

Usage: python3 check_lesson.py lesson.json
"""
import json, re, sys
from fractions import Fraction
from collections import Counter


def norm(a):
    """Mirror landing.html normAns exactly. It does NOT map the unicode minus."""
    return str(a).strip().lower().replace(' ', '').replace(',', '').lstrip('+')


def brace_span(s, i):
    """s[i] == '{'; return index just past the matching '}'."""
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
        if j < 0:
            out.append(None)
        else:
            out.append(sol[m.end():j - 1])
    return out


def latex_to_value(t):
    """Reduce a boxed LaTeX payload to a comparable plain string."""
    t = t.strip()
    t = re.sub(r'\\[tdc]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}', r'\1/\2', t)
    t = re.sub(r'\\(?:text|mathrm|mbox)\s*\{([^{}]*)\}', r'\1', t)
    t = t.replace('\\!', '').replace('\\,', '').replace('\\ ', '')
    t = t.replace('\\left', '').replace('\\right', '')
    t = t.replace('{', '').replace('}', '')
    t = t.replace('\u2212', '-')
    t = re.sub(r'\s+', '', t)
    return t


def numeric(s):
    s = norm(s).replace('−', '-')
    try:
        if '/' in s:
            return Fraction(s)
        return Fraction(s)
    except Exception:
        return None


def numbers_in(s):
    s = re.sub(r'<svg.*?</svg>', '', s or '', flags=re.S)
    return tuple(sorted(Counter(int(m) for m in re.findall(r'\d+', s) if int(m) >= 2).items()))


# Bare tokens that are what is left of a \n-macro after a newline replace ate the
# backslash. finalize_lesson.py did exactly that to \neq and \ne.
DEAD_MACRO = re.compile(r'(?<![\\A-Za-z])(neq|eq|ne|nmid|abla)(?=[\s)])')


def math_hazards(where, field, s):
    """Two failures that render as silent damage rather than as a KaTeX error."""
    out = []
    if not s:
        return out
    for m in re.finditer(r'\\\((.*?)\\\)|\$\$(.*?)\$\$', s, flags=re.S):
        inner = m.group(1) or m.group(2) or ''
        # A raw '<' before a letter is eaten by the HTML parser as a tag before KaTeX
        # sees it, and the text vanishes with NO .katex-error. Use \lt and \gt.
        if re.search(r'<[A-Za-z]', inner):
            out.append((where, f'{field}: raw "<" before a letter inside math '
                               f'(HTML eats it as a tag; use \\lt)'))
        d = DEAD_MACRO.search(inner)
        if d:
            out.append((where, f'{field}: bare "{d.group(1)}" inside math, which is what a '
                               f'\\n-macro looks like after a newline replace ate the backslash'))
    return out


def main(path):
    L = json.load(open(path, encoding='utf-8'))
    items = [(f'blocks[{i}]', b) for i, b in enumerate(L['blocks']) if b.get('t') == 'prob']
    items += [(f'review[{i}]', r) for i, r in enumerate(L.get('review', []))]
    bad = []
    sig = {}
    for where, p in items:
        ans, sol = str(p.get('ans', '')), p.get('sol', '')
        bv = boxed_values(sol)
        if not bv:
            bad.append((where, 'no \\boxed in sol'))
        else:
            last = latex_to_value(bv[-1])
            na, nb = numeric(ans), numeric(last)
            same = (na is not None and nb is not None and na == nb) or norm(last) == norm(ans)
            if not same:
                bad.append((where, f'boxed {last!r} != ans {ans!r}'))
            if len(bv) > 1:
                bad.append((where, f'{len(bv)} boxed values in one sol'))
        h = p.get('hints') or []
        if len(h) != 2:
            bad.append((where, f'{len(h)} hints (want exactly 2)'))
        acc = [norm(a) for a in (p.get('accept') or [])]
        if norm(ans) not in acc:
            bad.append((where, 'ans not in accept'))
        if len(acc) != len(set(acc)):
            bad.append((where, 'duplicate accept entries after normalization'))
        for a in (p.get('accept') or []):
            if norm(a) == '':
                bad.append((where, 'empty accept entry'))
        n = numbers_in(p.get('x', ''))
        if n in sig:
            bad.append((where, f'same number multiset as {sig[n]}'))
        elif n:
            sig[n] = where
        if len(sol) > 620:
            bad.append((where, f'sol {len(sol)} chars (>620)'))
        xl = len(p.get('x', ''))
        if xl > 460:
            bad.append((where, f'x {xl} chars (>460)'))
        for f in ('x', 'sol', *[f'hints[{i}]' for i in range(len(h))]):
            s = p.get(f) if not f.startswith('hints') else h[int(f[6])]
            if s and re.search(r'(?<!\\)\$(?!\$)', re.sub(r'\$\$.*?\$\$', '', s, flags=re.S)):
                bad.append((where, f'{f}: raw single-$ math'))
            # A doubled backslash is a legitimate LaTeX ROW SEPARATOR inside array-like
            # environments. Only flag it outside those, where it is an escaping artifact.
            if s:
                stripped = re.sub(r'\\begin\{(array|aligned|matrix|[bpv]matrix|cases)\}.*?\\end\{\1\}', '', s, flags=re.S)
                if '\\\\' in stripped:
                    bad.append((where, f'{f}: doubled backslash'))
                # A raw '<' followed by a letter INSIDE math is eaten by the HTML parser
                # as a tag before KaTeX sees it, and the text silently vanishes. It raises
                # NO .katex-error, so a preview sweep will not catch it. Use \lt and \gt.
                bad += math_hazards(where, f, s)

    # Prose blocks were never scanned for escaping artifacts, which is exactly how a
    # destroyed \neq survived in an imp block through every gate and shipped.
    for i, b in enumerate(L['blocks']):
        if b.get('t') == 'prob':
            continue
        for f in ('x', 'cap'):
            if isinstance(b.get(f), str) and b.get('t') != 'fig':
                bad += math_hazards(f'blocks[{i}]', f, b[f])
            elif f == 'cap' and isinstance(b.get(f), str):
                bad += math_hazards(f'blocks[{i}]', f, b[f])

    # non-prob blocks
    for i, b in enumerate(L['blocks']):
        if b.get('t') == 'fig':
            svg = b.get('x', '')
            for m in re.findall(r'<text[^>]*>([^<]*)</text>', svg):
                if len(m) > 2 and m == m.upper() and re.search(r'[A-Z]{3}', m):
                    bad.append((f'blocks[{i}]', f'ALL-CAPS label in figure: {m!r}'))
            if 'font-family="Space Grotesk, sans-serif"' not in svg:
                bad.append((f'blocks[{i}]', 'figure missing Space Grotesk font-family'))
            for w in re.findall(r'font-weight="(\d+)"', svg):
                if int(w) > 700:
                    bad.append((f'blocks[{i}]', f'font-weight {w} > 700'))
            if not b.get('cap'):
                bad.append((f'blocks[{i}]', 'fig has no cap'))
        elif b.get('t') in ('p', 'imp', 'fact'):
            xl = len(b.get('x', ''))
            lim = {'p': (190, 360), 'imp': (340, 620), 'fact': (150, 260)}[b['t']]
            if not (lim[0] <= xl <= lim[1]):
                bad.append((f'blocks[{i}]', f"{b['t']} x is {xl} chars, target {lim[0]}-{lim[1]}"))

    # figure vs problem number collision
    figs = [(f'blocks[{i}]', b) for i, b in enumerate(L['blocks']) if b.get('t') == 'fig']
    for fw, fb in figs:
        # a label may carry a real minus sign U+2212, which int() cannot parse
        raw = (m.replace('\u2212', '-') for m in re.findall(r'>\s*([+\u2212-]?\d+)', fb.get('x', '')))
        fnums = set(int(m) for m in raw if abs(int(m)) >= 2)
        for where, p in items:
            pn = set(int(m) for m in re.findall(r'\d+', p.get('x', '')) if int(m) >= 2)
            common = fnums & pn
            # only a real spoiler if the figure and the problem share several salient values
            if len([c for c in common if c >= 12]) >= 2:
                bad.append((fw, f'shares numbers {sorted(common)} with {where}'))

    print(f'=== {path} ===')
    for w, m in bad:
        print(f'{w}: {m}')
    nprob = sum(1 for b in L['blocks'] if b.get('t') == 'prob')
    print(f'{len(bad)} issues | blocks={len(L["blocks"])} probs={nprob} review={len(L.get("review", []))}')
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))

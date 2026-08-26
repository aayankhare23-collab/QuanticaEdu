#!/usr/bin/env python3
"""Generate a ready-to-run PSET authoring workflow for one chapter.

    python3 tools/make_pset_workflow.py 7 --course algebra1 \
        --title "Graphing Lines" --covers covers.txt -o /tmp/pset7.workflow.js

The part that actually matters here is the FRESHNESS CATALOGUE. A chapter's problem
set has to avoid reusing any system, story or number set from the ~175 problems its
own lessons already spent, and the only reliable way to enforce that is to hand the
authoring agents every one of them. Building that list by hand is error-prone and is
the same work for every chapter from 7 to 15, so it is generated from the chapter
JSON instead.

The workflow body is taken verbatim from the shape that produced chapters 2 to 6:
3 diverse designs -> judge merge -> author in slot chunks -> adversarial per-item
verify -> practice and challenge audits.
"""
import argparse, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def catalogue(course, chapter):
    """Every problem the chapter's lessons already used, as `key P/R: stem -> ans`."""
    path = ROOT / 'lessons' / course / f'chapter-{chapter}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    lines = []
    for key in sorted(data, key=lambda s: [int(p) for p in s.split('.')]):
        L = data[key]
        for b in L['blocks']:
            if b.get('t') == 'prob':
                lines.append(f"{key}P: {squash(b['x'])} -> ans {b['ans']}")
        for r in L.get('review', []):
            lines.append(f"{key}R: {squash(r['x'])} -> ans {r['ans']}")
    return lines


def squash(s, n=150):
    s = ' '.join(s.split())
    return (s[:n] if len(s) > n else s).replace('\\', '\\\\').replace('`', "'").replace('$', '\\$')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('chapter')
    ap.add_argument('--course', default='algebra1')
    ap.add_argument('--title', required=True)
    ap.add_argument('--covers', help='file describing what the lessons taught, one bullet per lesson')
    ap.add_argument('--harder', default='', help='what the challenge set must go harder on')
    ap.add_argument('-o', '--out', required=True)
    a = ap.parse_args()

    used = catalogue(a.course, a.chapter)
    covers = pathlib.Path(a.covers).read_text().strip() if a.covers else \
        '(fill in what each lesson taught)'
    tmpl = (ROOT / 'tools/lesson-specs/pset6.workflow.js.bak').read_text()

    body = tmpl[tmpl.index('const STYLE_PS = `'):]
    n_lessons = len({l.split(':')[0][:-1] for l in used})

    # The body was NOT chapter-agnostic, despite the comment that used to sit here.
    # It carried chapter 6's own lesson count and chapter 6's systems-specific ramp
    # straight into the agent prompts, so every chapter without exactly six lessons
    # was told to cover six. Chapter 8 has five and shipped under that instruction.
    words = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six',
             7: 'seven', 8: 'eight'}
    n_word = words.get(n_lessons, str(n_lessons))
    for a_, b_ in (
        ('all six lessons of the chapter are represented across the 24 items, and that the '
         'practice set ramps gently from testing a pair to a three-letter system',
         f'all {n_word} lessons of the chapter are represented across the 24 items, and that '
         f'the practice set ramps gently from the simplest ask in the chapter to the hardest'),
        ('all six lessons represented', f'all {n_word} lessons represented'),
        ('Which of the six lessons', f'Which of the {n_word} lessons'),
        ('worked after all six lessons', f'worked after all {n_word} lessons'),
    ):
        body = body.replace(a_, b_)
    if 'six lessons' in body and n_lessons != 6:
        raise SystemExit('a hardcoded "six lessons" survived; fix the substitution table')
    # These phrases land inside single-quoted JS string literals, so an apostrophe in a
    # substituted phrase silently produces an unparseable script. Caught once already.
    for _, phrase in ((None, n_word),):
        if "'" in phrase:
            raise SystemExit(f'apostrophe in a substituted phrase: {phrase!r}')

    head = f'''export const meta = {{
  name: 'author-pset-{a.course}-ch{a.chapter}',
  description: 'Author the {a.course} chapter {a.chapter} Practice and Challenge problem sets',
  phases: [
    {{ title: 'Blueprint', detail: '3 designs, 1 judge merge' }},
    {{ title: 'Author', detail: '24 items in slot chunks' }},
    {{ title: 'Verify', detail: 'adversarial per-item verification' }},
    {{ title: 'Audit', detail: 'practice audit + challenge audit' }},
  ],
}}

const CHAPTER = '{a.chapter}'
const CHAPTER_TITLE = '{a.title}'
const USED = `{chr(10).join(used)}`
const SPEC = `
WHAT THIS IS. The per-chapter Practice and Challenge problem sets for Quantica
{a.course} chapter {a.chapter}, "{a.title}". These live in landing.html's PSETS_ALG1 object,
NOT in the lesson files. They are the chapter's capstone, worked after all its lessons.

EXACT SHAPE REQUIRED: 12 practice items and 12 challenge items.
- Practice items carry EXACTLY 1 hint each. Challenge items carry EXACTLY 2 hints each.
- The LAST 3 challenge items, and only those, carry "legendary": true.
- Every "sol" is wrapped in <p>...</p> and closes part 1 on \\\\(\\\\boxed{{...}}\\\\).

WHAT THE LESSONS TAUGHT, which the sets must span:
{covers}

COVERAGE RULE. Across the 24 items every one of the chapter's {n_lessons} lessons must be
represented, and the practice set alone must touch all of them. The challenge set goes
harder: {a.harder or 'combine two ideas per item and reward insight over grinding.'}

FRESHNESS, THE HARD RULE. Below is a catalogue of ALL {len(used)} problems already used in
this chapter's lessons. No item may reuse any of those systems, stories, or full number
sets. Invent everything fresh. Every answer in the 24 items must be distinct from every
other.

CATALOGUE OF PROBLEMS ALREADY USED (do not reuse any of these):
${{USED}}
`
'''
    out = pathlib.Path(a.out)
    out.write_text(head + body, encoding='utf-8')
    print(f'{out}  ({len(used)} problems catalogued from {n_lessons} lessons)')


if __name__ == '__main__':
    main()

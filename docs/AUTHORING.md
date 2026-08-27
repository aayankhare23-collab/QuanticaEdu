# Authoring Quantica lessons

How a lesson goes from an empty slot in the TOC to live on quanticaedu.com. Read this
whole file before authoring your first lesson. The house voice and non-obvious rules are
also captured in the memory files (see `CLAUDE.md` → Memory).

## The data model

Source of truth is one JSON file per chapter:

```
lessons/<course>/chapter-<N>.json     e.g. lessons/algebra1/chapter-1.json
lessons/<course>/toc.json             the chapter/lesson index for that course
```

`chapter-N.json` is `{ "1.1": {lesson}, "1.2": {lesson}, ... }`. A lesson is:

```json
{
  "title": "Order of Operations",
  "next": "1.3",
  "blocks": [ ...teaching blocks + try-it problems, in order... ],
  "review": [ ...standalone review problems... ]
}
```

Lesson data is **generated** from the chapter files by `tools/build_lessons.py`. It writes
one chunk per course, `data/lessons-<course>.js`, each assigning into
`window.__COURSEDATA = { "prealgebra": {...}, "algebra1": {...} }`, plus a `window.__CHDATA`
alias for back-compat. The app loads the chunks; the combined `data/lessons.js` is still
written but only `tools/gen_seo_pages.py` reads it. **Never hand-edit any generated file.**
Edit the chapter JSON and rebuild. (Memory: `lesson-data-lives-inline`.)

The app (`landing.html`) reads `__COURSEDATA`. `window.setCourse(slug)` repoints the app's
TOC/LESSONS/PSETS globals at one course. The whole rewards/workspace engine is
course-agnostic (keys prefixed by course slug), so a new course needs no per-course wiring.

### Block schema

| block  | fields                                             | notes |
|--------|----------------------------------------------------|-------|
| `p`    | `{t, x}`                                            | transition prose |
| `imp`  | `{t, x, label?}`                                    | key idea: **bold rule name** + statement + the WHY |
| `fact` | `{t, x, label?}`                                    | flavor/history aside |
| `fig`  | `{t, x, cap}`                                       | `x` is inline `<svg>`; prose goes in `cap`, never in the SVG |
| `prob` | `{t, xp, x, ans, accept[], hints[], sol}`           | a try-it problem inside the flow |

`review[]` items are **prob-shaped but carry NO `t` and NO `xp`**. They surface via the
"Practice this lesson" button.

Rules that the grader and renderer depend on:

- **Answers are a single typed value.** An integer, a lowest-terms fraction `a/b`, or a
  single word. The grader (`normAns` in `landing.html`) trims, lowercases, strips spaces and
  commas, and drops a leading `+`. It then compares the result to `ans` and to each `accept`
  entry, put through the same normalizer. `accept` must contain `ans` plus every reasonable
  typed variant (word forms like `four`, exact terminating decimal for a fraction, etc).
  Never ask for a list, a sentence, or "explain"; funnel to one value.

  **Exactly one answer, always.** A prompt that admits several correct values is broken
  even when the accept list covers them all, because two students can both be right and
  type different numbers. "Give a counterexample", "name a factor" and "find a number
  divisible by 2 and 6 but not 12" all fail this, and so does joining two questions into
  one answer box. Pin it with a slick move instead. The smallest or largest such value,
  the sum of all of them over a stated range, their product, how many there are, or how
  many digits the result has. The slick move usually makes the problem better, since it
  forces the student to characterise the whole family rather than stop at the first
  example.

  **The unicode minus is handled for you.** Since commit `ab324c5` (2026-08-14) `normAns`
  also maps `−`, `–` and `—` onto `-` and strips a leading `$`, so a negative answer does
  NOT need a separate `−6` entry. Two entries differing only by the minus glyph are dead
  weight. Older lessons are full of them because this file said the opposite until
  2026-08-26, and 908 such entries were stripped from the corpus on 2026-08-26.
  `tools/check_lesson.py` and `tools/check_pset.py` now mirror `normAns` exactly, so they
  DO flag the redundancy as a duplicate accept entry. Both must report 0 before a build.
  One more trap from the same commit: `normAns` folds `"1 1/2"` onto `"3/2"`, so the old
  whitespace-stripped spelling `"11/2"` is now a different number. Never put it in `accept`.
- **Solutions are answer-first, in two parts** (changed 2026-07-26, replaces the old
  "end on the box / name the trap first" rule):
  1. **The solve.** Do the problem directly and plainly, and close this part on
     `\(\boxed{...}\)` (the box must sit inside `\( \)` or `$$ $$`). No theory build-up, no
     naming the trap, no "Notice that" / "Let us begin". Just do it.
  2. **The why, optional and short.** One or two sentences *after* the box giving the insight,
     the general rule, or the common mistake. ~180 chars, hard cap ~320. Omit it entirely when
     the problem is trivial.

  The trap now lives in part 2, after the reader already has the answer. Length targets for the
  whole `sol`: easy ~120-320 chars, moderate ~250-450, genuinely hard multi-step ~350-600.
  Anything over 600 needs a real reason. (Rationale: solutions had drifted to theory-first walls
  of text, up to 2288 chars for an 85-char question, which buried the answer and bored the reader.)
- **Math** in `\( \)` inline or `$$ $$` display, **single backslashes** (`\frac`, `\sqrt`).
  Bold via `<b>...</b>`. No markdown.
- **xp** is 5 (easy) to 8 (hard) on try-it and review-in-flow problems; review items omit it.

## The quality bar

**`lessons/prealgebra/chapter-1.json` is the gold standard for problem quality and
pedagogy.** Read all six of its lessons before authoring. Four things make it the bar, and
they are what to copy:

1. **Problems teach, they do not test.** Each one is placed so that working it makes the next
   key idea obvious. The idea comes *after* the problems that earned it, never before.
2. **Derive, do not assert.** Where a rule could look arbitrary, reach it twice by
   independent routes. Prealgebra 2.3 walks a descending ladder to `a⁰ = 1` and then
   re-derives the same fact from the quotient rule.
3. **Exactly 2 hints per problem, specific to that problem, never generic nudges.** The first
   reframes, the second gets concrete.
4. **Answers are a single typed value.** An integer, a lowest-terms fraction, or one word.
   Never a list, a sentence, or "explain". If a question wants reasoning, funnel it to one
   value that only the right reasoning produces.

**What NOT to copy from chapter 1.** It was written before several conventions landed, and
the conventions win. Measured on 2026-08-02: of its 83 problems only 15 carry 2 hints, 38
carry 1 and 26 carry none; its xp runs to 18; it uses 616 single-`$` math delimiters and the
legacy `f`, `sub` and `goals` block types. New lessons use exactly 2 hints everywhere, xp 5
to 8 in Algebra I, `\( \)` or `$$` delimiters, and the block schema above. Take the problem
design from chapter 1 and the mechanics from this document.

For **prose length and register** specifically, the reference is
`lessons/prealgebra/chapter-2.json` (2.1, 2.2), which is tighter than chapter 1 and matches
the post-sweep house voice. See memory `verbosity-targets`.

## The voice (this is the part people get wrong)

Problem-first, plainspoken, warm but tight. AoPS-direct and conversational. Hard rules:

- **No em-dashes. Almost no colons in prose.** (Memory: `no-em-dashes`.)
- **No poetic/abstract register.** No strings or readers as characters ("two honest
  readers"), no personified conventions ("the agreement", "which operation speaks first"),
  no cute renamings ("the chant" for PEMDAS, "rungs of the ladder"), no dramatized verbs
  ("grabs", "grip", "seals", "balloon"). Say the plain thing. Name PEMDAS directly. A
  metaphor survives only if it teaches (a fraction bar acting like parentheses is fine).
  Commit `edca493` is the worked before/after of this fix.
- **No narrative filler** ("Imagine you...", "Last lesson we...").
- **Say the plain thing, never tease it.** No vague or riddling sentences that only make sense
  once the reader already knows the answer. Real offenders swept out on 2026-07-26: "The new
  work is finding the two places the laws stop" (name them), "Two things never move." (say
  what), "Four counts, one question." (cryptic slogan), "Nothing is being asked yet." (filler).
  If a sentence would confuse someone who has not yet learned the idea, rewrite or cut it.
  Conversational and warm is right; hinting and withholding is not. Analogies are welcome when
  they teach, but state the point outright alongside them.
- **Lengths** (chars in `x`): `p` 200-350, `imp` 350-600, `fact` ~200, `prob` 120-250 (up to
  ~450 if the ask needs pinning down). The enemy when trimming is filler, not substance.
  (Memory: `verbosity-targets`.)
- **Originality is required.** When a source (e.g. an AoPS screenshot) is given, it is a
  difficulty/coverage reference ONLY. Never reproduce, adapt, paraphrase, or mirror its
  examples, numbers, structure, or sequence. Invent fresh everything.

## Figures

Clean two-band SVGs. Full spec in `docs/figure-design-system.md`; lesson 4.4 is the worked
reference. The load-bearing constraints:

- `font-family="Space Grotesk, sans-serif"` (matches the app). **Never `Inter`** (legacy).
- **`font-weight` max 700.** Space Grotesk ships no 800; the browser fake-bolds it and the
  result reads as a generic AI-looking sans. `landing.html` has a `.modal svg text` CSS
  safety net for the family, but the weight cap is on you.
- viewBox width 560-600, explicit hex palette (not CSS vars), labels only, prose in `cap`.
- A figure's numbers must not collide with any nearby problem's numbers (it pre-solves it).

## The pipeline

Every lesson so far was built with a 4-phase multi-agent Workflow. The reusable template is
`tools/author_lesson.workflow.js`. Steps:

1. **Author.** Copy `tools/author_lesson.workflow.js`, fill in `COURSE_TITLE / KEY / TITLE /
   NEXT / SPEC`, and run it via the Workflow tool. It runs: 3 independent blueprint designs →
   a judge merge → parallel authoring of teach blocks + review set → adversarial per-problem
   verification (each verifier also emits a Python expression for the answer) → a whole-lesson
   audit. It returns `{ lesson, audit, fixedCount, pyChecks }`.
2. **Apply the audit.** Read `audit.findings`; apply each fix to the lesson JSON by hand.
   Common ones: a sol that talks past the box, a figure/problem number collision, an
   over-strong claim.
3. **Machine-verify every answer.** Evaluate each `pyChecks[].pyexpr` (exact `Fraction`
   arithmetic) and confirm it equals `ans`. This is non-negotiable before commit. For
   "find the max/insert parentheses" style problems, brute-force the search space too.
4. **Finalize + build.** Save the lesson object to a temp `.json`, then:
   ```
   python3 tools/finalize_lesson.py <temp>.json --course <c> --chapter <n> \
       --key <k> --title "<title>" --next <k2> --write
   python3 tools/build_lessons.py
   ```
   `finalize_lesson.py` collapses escaping artifacts, strips `t`/`xp` from review items,
   ensures `ans` is in `accept`, and flags em-dashes, prose colons, register words,
   unbalanced/unwrapped math, and figure font issues. Fix anything it reports, re-run.
5. **Preview-test.** Open the lesson in the app (`/?course=<c>&lesson=<k>`) and walk every
   workspace page; expect **0 `.katex-error`**. Confirm the figure renders on exactly one
   page in Space Grotesk, and that grading accepts the answer and rejects a trap value.
6. **Ship.** `git commit`, `git push origin main`, `firebase deploy --only hosting`. Then
   curl the live `data/lessons-<course>.js` for the course you touched to confirm the lesson
   is present. That is the file the app loads; the combined `data/lessons.js` is not.

A lesson going live automatically flips its course's in-app tab from "soon" to active and
updates progress counts; no extra wiring.

## Problem sets (Practice / Challenge)

Per-chapter problem sets live **in `landing.html`**, not the chapter JSON, in a `PSETS`
object (`Object.assign(PSETS, { N: { practice:[...], challenge:[...] } })`). Each item is
`{x, ans, accept, hints, sol, legendary?}`. Grading uses `normAns` (strips spaces/commas,
lowercases). The last few challenge items per chapter are tagged `legendary:true`. Gotcha: a
literal dollar sign inside KaTeX must be written `\\$` (e.g. `\\(\\$40\\)`). Full rules in
memory `pset-authoring`. `legendary` is only for chapter-ending challenge problems, never in
a lesson file (memory `legendary-tag-convention`).

## SEO pages

`tools/gen_seo_pages.py [course]` is course-aware and regenerates two things: a course **hub**
page at `/<course>` (written to `<course>.html` at the repo root, with Course/FAQ/Breadcrumb
structured data and a chapter grid that links live lessons and marks the rest "soon"), plus one
crawlable **lesson** page per live lesson under `/<course>/<slug>.html`. Per-course display
metadata (title, level, blurb, FAQ) lives in `COURSE_META` in the script; add an entry for a new
course. Run it after lesson content changes so the public pages match the app (they embed the
same figures). Both `prealgebra` and `algebra1` have pages. Two manual follow-ups the script does
NOT do: add the new URLs to `sitemap.xml`, and add a homepage link to the hub in `landing.html`.

## Historical build scripts

`tools/archive/` holds one-shot generators from the initial build (blog, OG images, the
`wembi` marketing region, a PSETS audit). They still reference the prior session's scratchpad
paths in places. Kept for reference; adapt before reuse.

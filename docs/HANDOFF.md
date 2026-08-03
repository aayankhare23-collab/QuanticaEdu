# Handoff, updated 2026-08-03

Read `CLAUDE.md` first for orientation and the golden rules, then `docs/AUTHORING.md` before
writing any lesson. This file is what a fresh session would otherwise have to rediscover.

## Where the courses stand

| | lessons | problem sets | notes |
|---|---|---|---|
| Prealgebra | 70 / 70, 12 chapters | all 12 chapters | complete |
| Algebra I | **35 / 81**, 15 chapters in the TOC | **chapters 1-6** | ch1-ch6 fully done, plus 7.2 |

**Next work, in order:**
1. **7.1 The Cartesian Plane, first.** 7.2 shipped ahead of it, so chapter 7 currently has a
   one-lesson gap: 7.1 shows greyed while 7.2 is live, and 6.6's "next: 7.1" falls back to
   "Finish lesson". Shipping 7.1 closes both. Its SPEC is ready at
   `tools/lesson-specs/author_7_1.head.js`.
2. Then 7.3 through 7.6, then chapters 8 to 15, then the per-chapter sets for 7 onward.

Chapter 6 and its problem sets shipped this session (6.1 Ratios Simple and Subtle, 6.2 Conversion Factors,
6.3 Percents, 6.4 Percent Problems, 6.5 Direct and Inverse Proportion, 6.6 Joint Proportion
and Rates). Chapter 5 and its sets shipped the same session.

## Start here: the tools that do the verifying

Two deterministic checkers now live in the repo. **Run both on every lesson and every set.**

```
python3 tools/check_lesson.py <lesson>.json     # a single lesson object
python3 tools/check_pset.py <pset>.json         # {"practice":[...], "challenge":[...]}
```

They catch what `finalize_lesson.py` does not: boxed-value vs `ans` (proper brace matcher),
exactly-2-hints, `accept` completeness under the real `normAns` semantics, duplicate answers,
cross-problem number-set collisions, block-length targets, figure font/weight/all-caps, and
raw single-`$` math. `check_lesson.py` runs clean on every shipped lesson, so a non-zero result
is a real finding.

**Two false positives were fixed in these checkers and must not be reintroduced:**
- A doubled backslash inside `\begin{array}` is a LaTeX **row separator**, not an escaping
  artifact. Collapsing it destroys data tables. The checker now strips array-like environments
  before scanning.
- `\text{inverse}` is a legitimate boxed value. The comparator strips `\text{...}` now.

## The pipeline

`tools/author_lesson.workflow.js` is the template. Copy it, fill in the `FILL THIS IN` block
(`COURSE_TITLE / KEY / TITLE / NEXT / REVIEW_N / OUTLINE / SPEC`), run it via the Workflow tool
with `scriptPath`. Authoring a lesson is a **SPEC + OUTLINE swap and nothing else**.

Worked SPECs are kept in `tools/lesson-specs/` (6.6, 7.1, 7.2). Copy the closest one and edit.
The assembled script is `head + STYLE + tail`, where STYLE and tail come from the template.

**Why it is chunked.** One agent cannot emit a whole lesson. A 25-block lesson with a 4KB
inline SVG, or a 17-item review set, is a large enough response that the connection closes
mid-response. This killed three runs before the fix. The author phase now runs many small
agents against **pre-labelled slot ids**, assembled deterministically from `OUTLINE`.

### The ship sequence, every time

1. Run the workflow. Extract `lesson`, `audit`, `pyChecks` from the task output file.
2. Collapse escaping artifacts and dedupe `accept` lists.
3. `python3 tools/check_lesson.py` until 0 issues.
4. **Re-solve every answer yourself from the FINAL text.** Non-negotiable.
5. Triage the audit. **Verify every proposed replacement before applying it.**
6. Re-run steps 3 and 4 after patching.
7. `tools/finalize_lesson.py ... --write`, then `tools/build_lessons.py`.
8. Preview: 0 `.katex-error` on every page **and** on the review set rendered separately.
9. Probe grading with a real trap value, not just the correct one.
10. Commit, push, `firebase deploy --only hosting`, curl the live file.

## Traps that cost real time

- **The verify phase rewrites 20 to 28 of 29 items per lesson.** The blueprint's numbers are
  NOT what ships. Re-solve from the final text or you will ship the wrong answer.
- **The verify phase can introduce a duplicate answer.** On 6.6 it moved an answer onto another
  item's after my distinctness check had already passed on the earlier draft. The audit caught
  it. This is the concrete reason the audit gate stays even though the math is verified by hand.
- **Do not run four workflows at once.** Four concurrent runs exhausted the session usage limit
  and killed every verify and audit agent in all four. Three is sustainable. If a run dies this
  way, `Workflow({scriptPath, resumeFromRunId})` replays cached agents free and re-runs only the
  failures; that recovered all four.
- **Openers quote the previous lesson's closer.** When authoring lessons in parallel that is
  impossible, so check the chain by hand at ship time and fix the opener or the closer. Three of
  four chained cleanly on chapter 6; one posed a question the next lesson never answered.
- **Escape SPECs properly.** Use a raw string or the workflow tool refuses the script.
- **Never leave thinking-out-loud in a SPEC.** It goes straight to the authoring agents.

## What the audits keep catching, so look for these yourself

Ranked by how often they were real:

1. **Scope leaks into the next lesson.** 6.1's closer handed over 6.2's central rule; 6.3's
   transition pre-empted its own key idea before the problems that earned it.
2. **A teaching block printing a nearby problem's numbers**, or a problem printing the value it
   asks for. 6.4's hardest problem described pure pigment as "100 percent pigment" when the
   answer was 100 litres.
3. **Assertions where the spec requires a derivation.** 6.4 expanded a product of two binomials,
   which chapter 9 owns and no reader has met.
4. **Statements that are simply false.** 6.3's key idea said a decimal repeats "when the
   denominator has a prime factor other than 2 or 5", which needs "in lowest terms" (3/6 = 0.5).
   6.5's closer said every problem came down to one constant when its own trap problem needs two.
5. **Story and template collisions** with the previous lesson or within the set.
6. **Verbs of agency on mathematical objects.** Standing rule, see `plain-not-overwrought`.

## Coverage against the reference text

The user supplied the AoPS *Introduction to Algebra* PDF (Desktop). It is a **coverage and
difficulty checklist only**, never a source to copy. `pdftotext` is not installed; use `pypdf`.
Details in memory `aops-reference-pdf`.

**`docs/reference-coverage-map.md` maps the reference's sections onto our chapters 6, 7 and 8.**
It is already written for chapter 7 and chapter 8, so those SPECs are fill-ins, not research.

One promise to keep: **5.1 explicitly tells the reader "Chapter 7 will draw what that looks
like"** about a system's three solution counts. Reference 8.6 is where that picture lives, so
**7.6 must deliver it**. Noted in the coverage map. **That picture is already drawn** and waiting
at `tools/lesson-figs/fig_7_6.svg`, see the next section.

## Graphs are drawn with manim now

Any figure on a set of axes is rendered with manim rather than hand-written as SVG. The kit is
`tools/manim_figs.py`, the full spec is in `docs/figure-design-system.md`, and manim installs
clean into `.venv-manim/` (gitignored) on Python 3.14 with no LaTeX needed.

**Chapter 7's six figures are already built and rendered** in `tools/lesson-figs/`. Apply one with

```
.venv-manim/bin/python tools/lesson-figs/fig_7_3.py
python3 tools/lesson-figs/apply_fig.py 7.3 --course algebra1 --write
```

then `build_lessons.py`. Eyeball every figure at
`/tools/lesson-figs/_preview.html?f=fig_7_3` before shipping it; the checker cannot see a label
sitting on an axis. `fig_7_2` is a spare, since 7.2 shipped a hand-authored figure that also shows
the substitution check.

Two traps if you ever rebuild this: manim reverses RGB for its ARGB32 image surface and that swap
must be undone for an SVG surface, and manim's own `Text` bakes glyphs to paths in whatever font
the machine has, so labels are emitted as live `<text>` in Space Grotesk instead.

**SPECs for 7.3, 7.4, 7.5 and 7.6 are written** and ready to run in `tools/lesson-specs/`
(`author_7_N.head.js`, assembled as head + STYLE + tail from `tools/author_lesson.workflow.js`).
Their banned-names chains are already threaded, Monge then Lambert then Halley then Euclid's fifth
postulate.

## In flight when this session ended

One workflow was running and will not survive the session. Relaunch it:
- 7.1 The Cartesian Plane (`tools/lesson-specs/author_7_1.head.js`)

7.2 finished and shipped, which is why chapter 7 has a gap until 7.1 lands.

7.1's SPEC **bans Descartes** even though it is the Cartesian-plane lesson; he is already spent
in Algebra I 1.5 for exponent notation. It uses Fermat instead. Keep the banned-names list
growing in each SPEC.

## Docs corrected this session

- `AUTHORING.md` claimed the grader normalizes the unicode minus. `normAns` does not touch it,
  so a negative answer needs both `-6` and `−6` in `accept`.
- `figure-design-system.md` prescribed uppercase letter-spaced band labels, which the
  product-wide all-caps ban retired. Band labels are lowercase, 13px, no letter-spacing.

## Still open

- 114 prealgebra figures use the old visual standard. The user said leave it.
- SEO pages have not been regenerated for Algebra I chapters 3 onward
  (`python3 tools/gen_seo_pages.py algebra1`), and sitemap/homepage links are manual.
- The Algebra I mascot is still the blue character while Prealgebra's is green.
- Prealgebra chapter 3 uses xp up to 12 against a documented 5 to 8. Flagged, not fixed.

## Standing rules worth repeating

No em-dashes, almost no colons in prose. No all-caps labels anywhere, including inside SVG
figures. Equations, letters, numbers and quantities do not act. Never touch `functions/.env`.
Deploy hosting only. Every math answer is machine-verified before it is committed.

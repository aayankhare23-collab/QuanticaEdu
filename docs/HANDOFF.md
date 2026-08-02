# Handoff, updated 2026-08-02

Read `CLAUDE.md` first for orientation and the golden rules, then `docs/AUTHORING.md` before
writing any lesson. This file covers what a fresh session would otherwise have to rediscover:
where the work stands, and the traps that cost real time last session.

## Where the courses stand

| | lessons | problem sets | notes |
|---|---|---|---|
| Prealgebra | 70 / 70, 12 chapters | all 12 chapters | complete |
| Algebra I | 25 / 81, 15 chapters in the TOC | chapters 1-4, all | ch1-ch4 done, ch5 is 3/6 |

**Next lesson to write is 5.4, Systems in Disguise.** Then 5.5 Word Problems with Systems,
5.6 Three or More Variables, then the chapter 5 Practice/Challenge sets, then chapter 6.

**Shipped across 2026-08-01 and 08-02:** 3.3, 3.4, 3.5 (chapter 3 complete), 4.1 through 4.5
(chapter 4 complete), 5.1, 5.2, 5.3, plus Practice/Challenge sets for chapters 1, 3, and 4
(12+12 with 3 legendary each), so every live chapter now has sets. Every lesson went through
the full workflow pipeline with all answers machine-verified in exact arithmetic and
preview-tested to 0 katex-error.

Four app/content bugs found and fixed along the way, all live:
- Stale `TOC_ALG1` chapters 1-2 in landing.html (missing 1.6 and 2.6, six wrong titles, so
  the app showed 79 lessons instead of 81 and mislabeled half of chapters 1-2).
- A CSS bug where the responsive figure rules (`.lessonfig svg`, `.page-lead svg`) caught
  KaTeX's glyph SVGs and forced `height:auto`, collapsing radical bars to ~0.1px inside
  figure captions. Affected 14 captions across both courses, all of prealgebra ch 8
  included. Fix was scoping the figure rule to the direct child plus a `height:inherit`
  override for `.katex svg`; note the override needs higher specificity than
  `.ws-page.page-text-only .page-lead svg` or it silently loses.
- Two lost backslashes on `\neq` in shipped 5.2 solutions, rendering as a stray italic "e".
- Two stale hints in 4.1's review referencing numbers from an earlier draft.

Chapters 6 to 15 of Algebra I have no lessons and correctly render as "coming soon", greyed and
unclickable, on both the dashboard and the contents page. Problem-set links for chapters without
sets do the same. Nothing to fix there.

## What this session learned about running the pipeline

- **Generate each lesson's workflow script from the previous one.** Copy the last lesson's
  script, swap `KEY / TITLE / NEXT` and the whole SPEC block, and adjust the two scope
  sentences in the verify and audit prompts. Writing a script from scratch each time
  re-introduces drift. `tools/author_lesson.workflow.js` is the canonical template and now
  carries the hardened voice rules.
- **A SPEC is worth the effort.** The lessons that needed the fewest post-audit fixes were
  the ones whose SPEC named the scope boundary explicitly (what the NEXT lesson owns), the
  exact handoff sentence from the previous lesson's closer, and which historical facts were
  already spent. List the reserved facts; the agents will otherwise reuse al-Khwarizmi.
- **Workflows die on the 5-hour usage window and on transient API errors.** They resume
  cleanly: `Workflow({scriptPath, resumeFromRunId})` replays every completed agent from
  cache and only re-runs what failed. Three lessons this session were finished that way.
  Do not restart from scratch.
- **The audit is not a formality.** It caught, per lesson, between one and five real issues,
  including a figure that spoiled a later problem's numbers, a figure whose two cancelled
  tiles both read `9y` when the whole teaching point was that they are opposite, a problem
  that taught 4.3's method inside 4.1, and a lesson-wide solution-value collision cluster.
  Apply the findings by hand and re-verify anything you renumber.
- **Number freshness is the most common real finding.** When an audit demands a renumber,
  build the banned set mechanically (every number >= 2 in the neighbouring chapters' problem
  statements and answers, plus the kept problems of the lesson in hand), then search for
  replacement systems whose salient values all miss it. Everything below about 44 is usually
  already spent by chapter 5, so expect landing values in the 40s and up.
- **Voice, the standing correction (2026-08-02).** The user rejected a closer that read
  "Every system in this lesson handed over a coefficient ... no letter qualifies, so ...
  fractions ride through every line that follows." Equations, letters, and numbers do not
  act. Say what is: the system has a letter with coefficient 1, or it does not; the
  isolation starts with a division; fractions appear in later steps. "Clarity first, then
  conversation second." The rule is in the workflow template and in the
  `plain-not-overwrought` memory with his exact rewrite. Sweep the assembled lesson yourself
  before shipping, since the per-problem verifiers catch most of these but not the ones in
  `p` and `imp` blocks.

## Writing a lesson

The pipeline is documented in `docs/AUTHORING.md` and it works. Summary:

1. Copy `tools/author_lesson.workflow.js`, fill in `COURSE_TITLE / KEY / TITLE / NEXT / SPEC`,
   run it through the Workflow tool with `scriptPath`.
2. Apply the audit findings by hand.
3. Machine-verify **every** answer. Non-negotiable.
4. `python3 tools/finalize_lesson.py <temp>.json --course <c> --chapter <n> --key <k> --title "<t>" --next <k2> --write`
5. `python3 tools/build_lessons.py`
6. Preview-test, expect 0 `.katex-error`.
7. Commit, push, `firebase deploy --only hosting`.

### Traps hit while writing 3.2 (still true)

- **The audit agent can die on an API error.** It did. Run its checks by hand if so, because it
  catches real things: 3.2's figure shipped with two all-caps band labels (`THE LADDER`,
  `BAR CROSSING`), which are a standing ban. The rest of the corpus has zero of those.
- **Escape your SPEC properly.** `\frac` and `\neq` written inside a non-raw Python string became
  a form feed and a newline, and the Workflow tool refused the script for containing control
  characters. Use a raw string.
- **`pyChecks` only covers numeric answers.** 3.2 had 10 numeric and 6 symbolic; the symbolic
  ones had to be re-derived in sympy separately. Do both.
- **Verify with a proper brace matcher.** A regex for `\boxed{...}` fails on nested braces like
  `\boxed{\frac{1}{h^{6}}}` and will report false mismatches.
- **Read the whole question before concluding something is missing.** A "missing" format hint was
  already there; appending a second one broke the problem until it was reverted.

### The quality bar

`lessons/prealgebra/chapter-2.json` 2.3 and 2.4 are the reference. Their shape is prose, two
problems, then the key idea those problems earned, repeated. They derive rather than assert:
2.3 walks a descending ladder to reach `a⁰ = 1` and then re-derives it from the quotient rule,
two independent routes to one fact. Every problem carries exactly 2 hints.

Algebra I uses xp 5 to 8. Prealgebra drifted up to 14. Follow the course, not the reference.

## What shipped on 2026-07-31

- **Tutor is Milo everywhere.** Three names were live at once (Sprout 40 uses, Cove 8, Milo 10),
  and Sprout/Cove were a deliberate per-course split. All user-facing strings now say Milo,
  including the 85 generated SEO pages, which the first pass missed because `gen_seo_pages.py`
  had the old name hardcoded. **CSS identifiers and theme variables still say sprout/cove on
  purpose** — they drive the per-course palette. Do not rename them.
- **Mobile side panels fixed.** Opening Milo on a phone was squeezing the lesson into a ~95px
  column, one word per line. Below 700px the panels are now sheets that overlay instead of
  displacing, with the scrim wired up. The scrim markup and its close handler already existed
  and had never been switched on.
- **A real 404 page.** There was none.
- **"Spaced review" removed from the pricing card.** It was advertised and does not exist, and
  cannot from the current data, since completion is stored as a bare boolean with no timestamp.
- **SEO.** All 83 lesson pages retitled to target search queries rather than chapter names
  ("How to Add and Subtract Fractions" not "Adding and Subtracting Fractions"). URLs unchanged
  on purpose. 94 sitemap URLs all carry real `lastmod` from git history.
- **Prose sweep.** 536 rewrites across all 523 prose blocks in both courses, to the
  define-don't-metaphor standard. See the memory of the same name.
- **Two blog posts**, divide by zero and negative times negative. Five posts total.
- **Ten shorts** built from scratch. See `tools/shorts/README.md`.

## The SEO situation, which is the important one

Search Console on 2026-07-31 showed **74 pages "Discovered, currently not indexed" and zero
"Crawled, currently not indexed."**

That distinction is the whole story. Google has not judged the content and found it wanting; it
has never fetched it. This is crawl budget, which tracks domain authority, which tracks inbound
links, of which there are almost none.

So: **more pages will not help. Links will.** Blog posts are worth writing because they get
shared and linked; more lesson pages are not, until the existing 83 get crawled.

Also note the dashboard runs about **8 days behind**, so anything read there describes a site
that no longer exists. Do not react to it same-week.

Manual indexing requests are the only lever that forces a crawl, roughly 10 per day. Eleven were
requested on 2026-07-31.

## Open items

- 114 prealgebra figures still use the old visual standard. The user said leave it.
- The Algebra I mascot image is still the blue character while Prealgebra's is green, even
  though both say Milo. Raised with the user, not yet decided.
- From a 20-item audit list the user supplied, **4 items were factually wrong** about the code
  (#6 pricing, #8 two UI systems, #9 reset confirm, #20 error analysis) and 8 more were partly
  wrong. Do not work that list without re-verifying each claim first.
- Prealgebra chapter 3 uses xp up to 12 against a documented 5 to 8. Flagged, not fixed.

## Standing rules worth repeating

No em-dashes, almost no colons in prose. No all-caps eyebrow or band labels anywhere, including
inside SVG figures. Never touch `functions/.env`. Deploy hosting only. Every math answer is
machine-verified before it is committed.

// ─────────────────────────────────────────────────────────────────────────────
// GUIDED LESSON-AUTHORING WORKFLOW  (template)
//
// This is the reusable shape of the 4-phase pipeline used to author every Quantica
// lesson (blueprint → author → adversarial verify → audit). It is NOT run directly;
// copy it, fill in the SPEC block for the lesson you are writing, and pass it to the
// Workflow tool via `script:` (or save-and-pass via `scriptPath:`). See docs/AUTHORING.md.
//
// After the workflow returns { lesson, audit, fixedCount, pyChecks }:
//   1. Read the audit findings; apply each fix to the lesson JSON by hand.
//   2. Machine-verify every answer with the emitted pyChecks (exact Fraction arithmetic).
//   3. Save the lesson object to a temp .json, then:
//        python3 tools/finalize_lesson.py <that>.json --course <c> --chapter <n> \
//          --key <k> --title "<title>" --next <k2> --write
//        python3 tools/build_lessons.py
//   4. Preview-test (open the lesson in the app, expect 0 .katex-error), then commit + deploy.
// ─────────────────────────────────────────────────────────────────────────────

export const meta = {
  name: 'author-lesson',
  description: 'Author one Quantica lesson via blueprint, author, verify, audit',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'teach blocks + review set' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'whole-lesson audit' },
  ],
}

// ── FILL THIS IN ─────────────────────────────────────────────────────────────
const COURSE_TITLE = 'Algebra I'          // human course name, e.g. 'Prealgebra'
const KEY = '1.3'                         // lesson key
const TITLE = 'When Order Matters'        // lesson title
const NEXT = '1.4'                        // next key (or '' for none)
const SPEC = `
- Topic checklist (cover ALL): ...
- SCOPE BOUNDARY (what this lesson must NOT teach, owned by a neighbor): ...
- Shape: N blocks with M prob blocks, plus K review items.
- A figure only if it earns its place per docs/figure-design-system.md.
`
// ─────────────────────────────────────────────────────────────────────────────

const STYLE = `
QUANTICA HOUSE STYLE (follow exactly):
- Voice: problem-first, plainspoken, warm but tight, exactly like AoPS. Read
  lessons/prealgebra/chapter-2.json (2.1, 2.2) for the voice+length bar, and the
  already-authored lessons in this course for continuity.
- NO em-dashes. Almost NO colons in prose. NO poetic/abstract register: no strings or
  readers as characters, no personified conventions ("the agreement"), no cute renamings
  ("the chant" for PEMDAS), no dramatized verbs ("grabs", "seals"). Say the plain thing.
  A metaphor survives only if it teaches. (See memory: no-em-dashes.)
- Math in \\( ... \\) inline, $$ ... $$ display. SINGLE backslashes. Bold with <b>...</b>.
- Lengths (chars in x): p 200-350; imp 350-600 (bold rule name + statement + the WHY);
  fact ~200; prob 120-250, up to ~450 if the ask needs pinning down.
- Figures: font-family "Space Grotesk, sans-serif", font-weight max 700, viewBox 560-600,
  explicit hex palette, labels only (prose goes in cap). Numbers must not collide with any
  problem's numbers.
- ORIGINALITY IS REQUIRED. Invent fresh numbers and framings; never mirror a source's
  sequence, examples, or numbers.

GRADING RULES:
- prob block: {"t":"prob","xp":5-8,"x","ans","accept":[...],"hints":[1-2],"sol"}
- review item: same but NO t and NO xp fields.
- Answers are a SINGLE typed value. Grader lowercases + strips spaces/commas; unicode minus
  normalized to hyphen. Canonical form in ans; every reasonable typed variant in accept
  (accept must include ans). Fractions lowest-terms a/b, plus exact terminating decimal.
- hints nudge without revealing. sol is 1-3 sentences of real reasoning ending ON the answer
  in \\(\\boxed{...}\\) inside \\( \\) or $$ $$.
`

phase('Blueprint')
const LENSES = [
  'HOOK-FIRST designer. Priority: the opening problem, so the core idea feels discovered not announced.',
  'STRESS designer. Priority: the problem set, especially the traps/edge cases a rote student misses. Each trap taught before it is tested.',
  'PROGRESSION designer. Priority: the cleanest arc and an honest figure decision (read docs/figure-design-system.md first).',
]
const designs = await parallel(LENSES.map((lens, i) => () =>
  agent(`You are designing (NOT writing) Quantica ${COURSE_TITLE} lesson ${KEY} "${TITLE}". ${lens}\n${STYLE}\nLESSON SPEC:${SPEC}\nReturn a compact design: hook idea, ordered block outline (type + one-line note), every prob and review question with exact ask, exact single-value answer, and xp, plus a figure decision and 2 sentences on why your design teaches best.`,
    { label: `design:${['hook', 'stress', 'progression'][i]}`, phase: 'Blueprint' })))

const blueprint = await agent(
  `You are the judge for Quantica ${COURSE_TITLE} lesson ${KEY} "${TITLE}". Merge the three designs into ONE final blueprint: strongest hook, strongest problems + review, strongest figure decision. COMPUTE every answer yourself, digit by digit. No two problems share numbers; a figure shares numbers with no problem. Respect the scope boundary. Return structured plain text.\n${STYLE}\nSPEC:${SPEC}\n\nA:\n${designs[0]}\n\nB:\n${designs[1]}\n\nC:\n${designs[2]}`,
  { label: 'judge:merge', phase: 'Blueprint' })

phase('Author')
const BLOCK_SCHEMA = { type: 'object', properties: { blocks: { type: 'array', items: { type: 'object', properties: {
  t: { type: 'string', enum: ['p', 'prob', 'imp', 'fact', 'fig'] }, x: { type: 'string' }, xp: { type: 'number' },
  ans: { type: 'string' }, accept: { type: 'array', items: { type: 'string' } }, hints: { type: 'array', items: { type: 'string' } },
  sol: { type: 'string' }, label: { type: 'string' }, cap: { type: 'string' } }, required: ['t', 'x'] } } }, required: ['blocks'] }
const REVIEW_SCHEMA = { type: 'object', properties: { review: { type: 'array', items: { type: 'object', properties: {
  x: { type: 'string' }, ans: { type: 'string' }, accept: { type: 'array', items: { type: 'string' } },
  hints: { type: 'array', items: { type: 'string' } }, sol: { type: 'string' } }, required: ['x', 'ans', 'accept', 'hints', 'sol'] } } }, required: ['review'] }

const [teach, reviewSet] = await parallel([
  () => agent(`Write the TEACH BLOCKS (everything except review) for Quantica ${COURSE_TITLE} lesson ${KEY}, exactly following this blueprint, final polished prose+math. Recompute every answer before writing its sol. If there is a fig, build the SVG to docs/figure-design-system.md.\n${STYLE}\nBLUEPRINT:\n${blueprint}\nReturn the blocks array only.`,
    { label: 'author:teach', phase: 'Author', schema: BLOCK_SCHEMA }),
  () => agent(`Write the REVIEW SET for Quantica ${COURSE_TITLE} lesson ${KEY}, exactly following this blueprint, ordered easy to hard, 1 hint each (2 for the hardest). Recompute every answer.\n${STYLE}\nBLUEPRINT:\n${blueprint}\nReturn the review array only.`,
    { label: 'author:review', phase: 'Author', schema: REVIEW_SCHEMA }),
])
const lesson = { title: TITLE, next: NEXT, blocks: teach.blocks, review: reviewSet.review }

phase('Verify')
const VERDICT_SCHEMA = { type: 'object', properties: {
  pass: { type: 'boolean' }, issues: { type: 'array', items: { type: 'string' } },
  corrected: { type: 'string', description: 'Full corrected block as a JSON string if pass=false, else "".' },
  pyexpr: { type: 'string', description: 'A single Python expression (Fraction from fractions if needed) equal to the answer, or "" if not numeric.' },
}, required: ['pass', 'issues', 'corrected', 'pyexpr'] }

const targets = []
lesson.blocks.forEach((b, i) => { if (b.t === 'prob') targets.push({ kind: 'block', idx: i, b }) })
lesson.review.forEach((b, i) => targets.push({ kind: 'review', idx: i, b }))

const verdicts = await parallel(targets.map(t => () =>
  agent(`Adversarially verify this single Quantica problem. BREAK it before passing.
1. Re-derive the answer independently, digit by digit. Match ans exactly? Unambiguous?
2. Grader lowercases + strips spaces/commas. Is ans in accept? Any accept variant that falsely accepts a wrong response? Any obvious correct form missing?
3. Hints don't reveal; sol reasons correctly and ends ON \\(\\boxed{...}\\) inside \\( \\) or $$.
4. KaTeX valid, single backslashes, no em-dashes, colon-free prose, no poetic register.
5. In pyexpr give one Python expression computing the answer mechanically (Fraction(a,b) for exact fractions, ** for powers, explicit parens). "" only if not a number.
If anything fails: pass=false, list issues, return the full corrected block JSON in "corrected".
PROBLEM (${t.kind} ${t.idx}):\n${JSON.stringify(t.b, null, 1)}`,
    { label: `verify:${t.kind}${t.idx}`, phase: 'Verify', schema: VERDICT_SCHEMA })))

let fixedCount = 0
const pyChecks = []
verdicts.forEach((v, k) => {
  if (!v) return
  const t = targets[k]
  if (!v.pass && v.corrected) {
    try {
      const nb = JSON.parse(v.corrected)
      if (nb && nb.x && nb.ans) {
        if (t.kind === 'block') { nb.t = 'prob'; lesson.blocks[t.idx] = nb }
        else { delete nb.t; delete nb.xp; lesson.review[t.idx] = nb }
        fixedCount++
      }
    } catch (e) { log(`verify:${t.kind}${t.idx} correction unparseable; issues: ${v.issues.join(' | ')}`) }
  }
  const fb = t.kind === 'block' ? lesson.blocks[t.idx] : lesson.review[t.idx]
  if (v.pyexpr) pyChecks.push({ where: `${t.kind}[${t.idx}]`, pyexpr: v.pyexpr, ans: fb.ans })
})
log(`verification done, ${fixedCount} corrected, ${pyChecks.length} python checks`)

phase('Audit')
const AUDIT_SCHEMA = { type: 'object', properties: {
  findings: { type: 'array', items: { type: 'object', properties: {
    severity: { type: 'string', enum: ['major', 'minor'] }, where: { type: 'string' }, issue: { type: 'string' }, fix: { type: 'string' },
  }, required: ['severity', 'where', 'issue', 'fix'] } }, verdict: { type: 'string' },
}, required: ['findings', 'verdict'] }

const audit = await agent(`Whole-lesson audit of Quantica ${COURSE_TITLE} lesson ${KEY} "${TITLE}" (final JSON below), the last gate before ship. Check: topic coverage vs the spec; scope boundary respected; lengths (p 200-350, imp 350-600, fact ~200, prob 120-450); style (no em-dash, colon-free prose, no poetic register, math delimited, single backslashes, every sol ends ON the boxed value); SPOILER CHECK (no teaching example or figure shares numbers with a nearby problem; no two problems share numbers; every trap taught before tested); arc (problem-first, ramps, review stands alone); and re-check every answer's arithmetic. Report findings with exact locations and concrete fixes.
SPEC:${SPEC}\nLESSON JSON:\n${JSON.stringify(lesson, null, 1)}`,
  { label: 'audit:whole-lesson', phase: 'Audit', schema: AUDIT_SCHEMA })

return { lesson, audit, fixedCount, pyChecks }

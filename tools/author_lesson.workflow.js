// ─────────────────────────────────────────────────────────────────────────────
// GUIDED LESSON-AUTHORING WORKFLOW  (template)
//
// The reusable shape of the 4-phase pipeline used to author every Quantica lesson
// (blueprint → author → adversarial verify → audit). It is NOT run directly; copy it,
// fill in the FILL THIS IN block, and pass it to the Workflow tool via `scriptPath:`.
// See docs/AUTHORING.md.
//
// WHY IT IS CHUNKED (learned 2026-08-02, cost three dead runs). One agent emitting a whole
// lesson (25 blocks including a 4KB inline SVG) or a whole 17-item review set produces a
// response large enough that the connection closes mid-response. Retrying does not help.
// So the author phase runs many SMALL agents, each writing a few PRE-LABELLED slots, and
// this script assembles the block order deterministically from OUTLINE. That also removes
// the array-index drift trap recorded in memory `answer-first-solutions`: no agent ever
// infers a position, it only copies a slot id it was handed.
//
// After the workflow returns { lesson, audit, fixedCount, pyChecks, missing }:
//   1. Read audit.findings; apply each fix by hand. Verify any replacement BEFORE applying it.
//   2. Machine-verify every answer, re-solved from the FINAL text (verifiers rewrite blocks,
//      so the blueprint's numbers are not what shipped). Non-negotiable.
//   3. python3 tools/finalize_lesson.py <temp>.json --course <c> --chapter <n> \
//        --key <k> --title "<title>" --next <k2> --write
//      python3 tools/build_lessons.py
//   4. Preview-test (0 .katex-error on every page AND on the review set), then commit + deploy.
// ─────────────────────────────────────────────────────────────────────────────

export const meta = {
  name: 'author-lesson',
  description: 'Author one Quantica lesson via blueprint, author, verify, audit',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

// ── FILL THIS IN ─────────────────────────────────────────────────────────────
const COURSE_TITLE = 'Algebra I'
const KEY = '1.3'
const TITLE = 'When Order Matters'
const NEXT = '1.4'
const REVIEW_N = 17

// Every block, in order. The bracketed id is what the author agents are handed.
// Types: 'p' | 'imp' | 'fact' | 'fig' | 'prob'. Exactly one 'fig' (or none).
const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'],
  // ... fill in the real outline; keep prob ids P1..Pn in order
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY: what the previous lessons taught, the EXACT closing sentence of the
previous lesson (this lesson's opener must keep it as a promise), and the stories/examples
already spent that must not be reused.

TOPIC CHECKLIST (cover ALL): ...

SCOPE BOUNDARY (must NOT appear, each owned by a neighbour): ...

MANDATED BLOCK OUTLINE: restate OUTLINE here in prose so the designers design against it.

FIGURE: what it shows, and why it earns its place. Prefer a figure carrying NO digits, which
makes it collision-proof against every problem.

HISTORICAL FACT: list every name already spent in this course as BANNED, and name the fresh one.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure shares
nothing with a nearby problem, (c) every answer in the lesson is distinct from every other,
(d) no system/example from the neighbouring lessons is reused.
`
// ─────────────────────────────────────────────────────────────────────────────

const STYLE = `
QUANTICA HOUSE STYLE (follow exactly):
- QUALITY BAR: read lessons/prealgebra/chapter-1.json, all six lessons, for problem quality and
  pedagogy. Problems teach rather than test, each placed so working it makes the next idea
  obvious, and the idea arrives AFTER the problems that earned it. Rules get derived twice by
  independent routes, never asserted. Do NOT copy chapter 1's mechanics, which predate the
  conventions below (1-hint problems, xp to 18, single-$ math). Take its problem design only.
- Voice: problem-first, plainspoken, warm but tight, exactly like AoPS. Read
  lessons/prealgebra/chapter-2.json (2.1, 2.2) for the prose length and register bar, and the
  already-authored lessons of this course for continuity of voice and notation.
- NO em-dashes. Almost NO colons in prose. NO poetic/abstract register: no strings or readers as
  characters, no personified conventions, no cute renamings, no dramatized verbs. Say the plain
  thing. A metaphor survives only if it teaches.
- EQUATIONS, LETTERS, NUMBERS AND QUANTITIES DO NOT ACT. Never write that a system "hands over" a
  coefficient, an equation "arrives", a letter "qualifies", fractions "ride through" lines, a pair
  "fixes" a dimension, or a method is a "recipe". State the fact directly. If a sentence gives a
  verb of agency to a mathematical object, rewrite it. Clarity first, conversation second.
- DEFINE, DO NOT METAPHOR. An explanatory block states plainly what the thing IS, names the term
  in the sentence where it first appears, and gives the concrete consequence rather than gesturing
  that it matters. Say it once and stop. "That is what gives", "which is exactly what makes" and
  "the real power of" are defective openings.
- NO all-caps eyebrow, kicker, tag or band labels anywhere, including inside SVG figures.
- Math in \\( ... \\) inline, $$ ... $$ display. SINGLE backslashes. Bold with <b>...</b>.
- Lengths (chars in x): p 200-350; imp 350-600 (bold rule name + statement + the WHY);
  fact ~200; prob 120-250, up to ~450 if the ask needs pinning down.
- Figures: font-family "Space Grotesk, sans-serif", font-weight max 700, viewBox width 560-600,
  explicit hex palette (blue #2f6fe0 / #2257c5 / #3b82f6, gold #fcd76a / #e0a52a / #8a5a08,
  grey #eef1f6 / #dbe1ea / #aab4c2, slate #475569, hairline #e4e9f1), role="img" plus aria-label,
  lowercase band labels, labels only, all prose in cap.
- ORIGINALITY IS REQUIRED. Invent fresh numbers and framings. If a reference text is mentioned it
  is a coverage and difficulty checklist ONLY; never mirror its examples, numbers or sequence.

GRADING RULES:
- prob block: {"t":"prob","xp":5-8,"x","ans","accept":[...],"hints":[exactly 2],"sol"}
- review item: same but NO t and NO xp fields, and still exactly 2 hints.
- Answers are a SINGLE typed value. The grader (normAns) trims, lowercases, strips spaces and
  commas, and drops a leading plus. It ALSO maps the unicode minus and the en/em dashes onto
  ASCII '-', strips a leading '$', and folds a mixed number like "1 1/2" onto "3/2". So a
  negative answer needs ONLY the ASCII spelling, and a separate unicode-minus entry is dead
  weight the grader can never reach. Never add the whitespace-stripped form of a mixed number
  ("21/2" for "2 1/2"); that now denotes ten and a half and grades a wrong answer correct.
  accept must contain ans plus every reasonable typed variant (word form, exact terminating
  decimal for a fraction, unit spellings).
- EXACTLY ONE ANSWER. A prompt that admits several correct values is broken even when accept
  covers them all, because two students can both be right and type different numbers. Never
  write "give a counterexample", "name a factor", or "find a number such that" when many
  qualify, and never join two questions into one answer box. Pin it with a slick move instead,
  the smallest or largest such value, the sum of all of them over a stated range, their
  product, how many there are, or how many digits the result has. The slick move usually makes
  the problem better, since it forces the student to characterise the whole family rather than
  stop at the first example.
- hints are 2, specific to that problem, never generic. The first reframes, the second gets
  concrete without handing over the answer.
- SOLUTIONS ARE ANSWER-FIRST, in two parts. Part 1 does the problem directly and closes ON
  \\(\\boxed{...}\\) inside \\( \\) or $$, with nothing trailing after the box in that sentence.
  Part 2 is optional, one or two short sentences AFTER the box giving the insight or the common
  mistake, ~180 chars, hard cap ~320. Whole sol: easy ~120-320, moderate ~250-450, hard ~350-600.
`

phase('Blueprint')
const LENSES = [
  'HOOK-FIRST designer. Priority: the opening problems, worked before any rule is stated, so the core idea feels discovered rather than announced.',
  'STRESS designer. Priority: the problem set, especially the traps a rote student misses. Each trap must be taught before it is tested, never introduced and tested in the same block.',
  'PROGRESSION designer. Priority: the cleanest arc, and an honest figure decision built to docs/figure-design-system.md.',
]
const designs = await parallel(LENSES.map((lens, i) => () =>
  agent(`You are designing (NOT writing) Quantica ${COURSE_TITLE} lesson ${KEY} "${TITLE}". ${lens}\n${STYLE}\nLESSON SPEC:${SPEC}\nReturn a compact design that fills EVERY slot id in the mandated outline: for each prob and review slot give the exact statement, the exact ask, the exact single-value answer, and xp. Plus the figure decision and 2 sentences on why your design teaches best.`,
    { label: `design:${['hook', 'stress', 'progression'][i]}`, phase: 'Blueprint' })))

const blueprint = await agent(
  `You are the judge for Quantica ${COURSE_TITLE} lesson ${KEY} "${TITLE}". Merge the three designs into ONE final blueprint filling every slot id in the mandated outline. COMPUTE every answer yourself, digit by digit, stating the full solve and the value actually asked for, and check each result back against the original statement. No two problems share a full number set; every answer in the lesson is distinct; the figure shares nothing with a nearby problem. Respect the scope boundary and every checklist item. Return structured plain text keyed by slot id.\n${STYLE}\nSPEC:${SPEC}\n\nA:\n${designs[0]}\n\nB:\n${designs[1]}\n\nC:\n${designs[2]}`,
  { label: 'judge:merge', phase: 'Blueprint' })

phase('Author')

// Transient API errors and stalls kill individual agents; retry each slot group.
async function tryAgent(prompt, opts, tries = 3) {
  for (let i = 0; i < tries; i++) {
    const r = await agent(prompt, i === 0 ? opts : { ...opts, label: `${opts.label}:r${i}` })
    if (r) return r
    log(`${opts.label} returned null, retry ${i + 1}/${tries - 1}`)
  }
  return null
}

const PROSE_SCHEMA = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, t: { type: 'string', enum: ['p', 'imp', 'fact'] }, x: { type: 'string' },
}, required: ['id', 't', 'x'] } } }, required: ['items'] }
const PROB_SCHEMA = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, xp: { type: 'number' }, x: { type: 'string' }, ans: { type: 'string' },
  accept: { type: 'array', items: { type: 'string' } }, hints: { type: 'array', items: { type: 'string' } },
  sol: { type: 'string' },
}, required: ['id', 'xp', 'x', 'ans', 'accept', 'hints', 'sol'] } } }, required: ['items'] }
const RITEM_SCHEMA = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, x: { type: 'string' }, ans: { type: 'string' },
  accept: { type: 'array', items: { type: 'string' } }, hints: { type: 'array', items: { type: 'string' } },
  sol: { type: 'string' },
}, required: ['id', 'x', 'ans', 'accept', 'hints', 'sol'] } } }, required: ['items'] }
const FIG_SCHEMA = { type: 'object', properties: {
  x: { type: 'string', description: 'the complete inline <svg>...</svg>' }, cap: { type: 'string' },
}, required: ['x', 'cap'] }

const COMMON = `${STYLE}\nLESSON SPEC:${SPEC}\nFINAL BLUEPRINT (authoritative; do NOT change any number, any answer, or any statement):\n${blueprint}\n
OUTPUT RULE: return ONLY the slots you were asked for, each carrying its "id" copied VERBATIM. Never renumber, never infer a position, never emit a slot you were not asked for, and never emit an extra hint or a note to yourself.`

const proseIds = OUTLINE.filter(([, t]) => t === 'p' || t === 'imp' || t === 'fact').map(([id]) => id)
const probIds = OUTLINE.filter(([, t]) => t === 'prob').map(([id]) => id)
const reviewIds = Array.from({ length: REVIEW_N }, (_, i) => 'R' + (i + 1))
const chunk = (a, n) => a.reduce((o, v, i) => (i % n ? o[o.length - 1].push(v) : o.push([v]), o), [])

const jobs = [
  () => tryAgent(`Write the PROSE blocks for Quantica ${COURSE_TITLE} lesson ${KEY} "${TITLE}", slot ids: ${proseIds.join(', ')}. The blueprint drafts each one. Finalize them into shipping prose: hold every length target (p 200-350 chars, imp 350-600, fact ~200), and make each imp name its term, state the rule, and give the concrete consequence. Sweep your own text for any verb of agency applied to an equation, letter, number or quantity, and rewrite it. No em-dashes, no prose colons.\n${COMMON}`,
    { label: 'author:prose', phase: 'Author', schema: PROSE_SCHEMA }),
]
for (const ids of chunk(probIds, 4)) {
  jobs.push(() => tryAgent(`Write in-lesson problem slots ${ids.join(', ')} for Quantica ${COURSE_TITLE} lesson ${KEY}, exactly as the blueprint specifies (same statements, same numbers, same answers, same xp). Finalize the wording, the accept list, EXACTLY 2 hints, and the answer-first sol. Do not change any number or answer.\n${COMMON}`,
    { label: `author:${ids[0]}-${ids[ids.length - 1]}`, phase: 'Author', schema: PROB_SCHEMA }))
}
for (const ids of chunk(reviewIds, 6)) {
  jobs.push(() => tryAgent(`Write review slots ${ids.join(', ')} for Quantica ${COURSE_TITLE} lesson ${KEY}, exactly as the blueprint specifies. The review set stands alone, so each item states everything it needs. EXACTLY 2 hints each, answer-first sol. Do not change any number or answer.\n${COMMON}`,
    { label: `author:${ids[0]}-${ids[ids.length - 1]}`, phase: 'Author', schema: RITEM_SCHEMA }))
}
const hasFig = OUTLINE.some(([, t]) => t === 'fig')
if (hasFig) {
  jobs.push(() => tryAgent(`Build the single FIGURE for Quantica ${COURSE_TITLE} lesson ${KEY}, exactly to the blueprint's figure section. Return the complete inline SVG in "x" and the caption in "cap". Hard requirements are in the style block above: Space Grotesk, no font-weight above 700, role="img" plus aria-label, explicit hex colours, lowercase band labels, NO all-caps label anywhere, no sentence inside the SVG, two bands separated by a full-width #e4e9f1 hairline.\n${COMMON}`,
    { label: 'author:fig', phase: 'Author', schema: FIG_SCHEMA }))
}

const parts = await parallel(jobs)
const fig = hasFig ? parts[parts.length - 1] : null
const bag = {}
const missing = []
for (const part of parts) {
  if (!part || !part.items) continue
  for (const it of part.items) bag[String(it.id).trim().toUpperCase()] = it
}
const blocks = []
for (const [id, kind] of OUTLINE) {
  if (kind === 'fig') {
    if (fig && fig.x) blocks.push({ t: 'fig', x: fig.x, cap: fig.cap })
    else missing.push('FIG')
    continue
  }
  const it = bag[id.toUpperCase()]
  if (!it) { missing.push(id); continue }
  const o = { t: kind, x: it.x }
  if (kind === 'prob') { o.xp = it.xp; o.ans = it.ans; o.accept = it.accept; o.hints = it.hints; o.sol = it.sol }
  blocks.push(o)
}
const review = []
for (const id of reviewIds) {
  const it = bag[id]
  if (!it) { missing.push(id); continue }
  review.push({ x: it.x, ans: it.ans, accept: it.accept, hints: it.hints, sol: it.sol })
}
if (missing.length) log(`MISSING SLOTS: ${missing.join(', ')}`)
log(`assembled ${blocks.length} blocks (${blocks.filter(b => b.t === 'prob').length} prob) + ${review.length} review`)
const lesson = { title: TITLE, next: NEXT, blocks, review }
if (blocks.length < OUTLINE.length - 4 || review.length < REVIEW_N - 3) {
  return { error: 'author stage incomplete', missing, lesson }
}

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
  tryAgent(`Adversarially verify this single Quantica ${COURSE_TITLE} ${KEY} problem. BREAK it before passing.
1. SOLVE IT YOURSELF from scratch, without following the given solution. Then read the question again to see WHICH value it asks for. Does your value match ans exactly?
2. AMBIGUITY. Could a careful reader read this statement a different way? Is every unit stated? Is the ask unmistakable about which single value to type? Could two students both be RIGHT while typing DIFFERENT numbers? If so the problem is broken and needs a slick move (smallest, largest, sum of all, product, how many, number of digits) to pin exactly one answer.
3. Grader (normAns) trims, lowercases, strips spaces and commas, drops a leading plus, maps the unicode minus and en/em dashes onto ASCII '-', strips a leading '$', and folds a mixed number like "1 1/2" onto "3/2". Is ans in accept? Any two accept entries that differ ONLY by one of those (dead weight the grader can never reach)? Any accept variant that falsely accepts a wrong response? Any obvious correct typed form missing?
4. EXACTLY 2 hints, specific to this problem, neither revealing the answer, and no note-to-self text. Sol is ANSWER-FIRST: part 1 closes ON \\(\\boxed{...}\\) with nothing trailing after the box in that sentence; part 2 optional and short. Flag any sol over ~600 chars.
5. KaTeX valid and balanced, SINGLE backslashes, no em-dashes, colon-free prose, no poetic register, no verb of agency on a mathematical object.
6. SCOPE: nothing owned by a neighbouring lesson or chapter.
7. In pyexpr give one Python expression computing the answer mechanically. "" only if not a number.
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

const AUDIT_PROMPT = `Whole-lesson audit of Quantica ${COURSE_TITLE} lesson ${KEY} "${TITLE}", the last gate before ship. Check, in this order:
1. TOPIC COVERAGE against every checklist item in the spec, naming which block covers each. Report any that is missing or only glanced at, and any block whose content does not match its mandated slot.
2. SCOPE BOUNDARY. Flag anything owned by a neighbouring lesson or chapter.
3. AMBIGUITY. For each problem, could a careful reader read it a different way? Is every unit and every ask stated exactly? Is any problem underdetermined by its own words?
4. GIVEAWAYS. Does any statement print the value it asks for, or does any teaching block print a nearby problem's numbers?
5. LENGTHS: p 200-350, imp 350-600, fact ~200, prob 120-450, sol under ~600.
6. STYLE: no em-dash, colon-free prose, no poetic register, NO VERB OF AGENCY ON A MATHEMATICAL OBJECT (quote any offender), single backslashes, every sol answer-first with part 1 closing ON the box, EXACTLY 2 hints everywhere and no note-to-self text, no all-caps label in the figure, figure weight never above 700.
7. COLLISIONS: no two problems share a full number set, no two answers in the lesson are equal, every trap is taught before it is tested and never in the same block.
8. ARC: problem-first, each idea after the problems that earned it, difficulty ramps, review stands alone, the opener keeps the previous lesson's stated promise and the closer hands off correctly.
9. RE-SOLVE EVERY PROBLEM and confirm the value asked for is the value in ans.
Report findings with exact locations (blocks[i] or review[i]) and concrete fixes. For any fix that changes numbers, state the full re-solve so it can be checked before it is applied.
SPEC:${SPEC}\n`

const [auditA, auditB] = await parallel([
  () => tryAgent(`${AUDIT_PROMPT}\nAudit the TEACH BLOCKS only.\nBLOCKS JSON:\n${JSON.stringify(lesson.blocks, null, 1)}`,
    { label: 'audit:blocks', phase: 'Audit', schema: AUDIT_SCHEMA }),
  () => tryAgent(`${AUDIT_PROMPT}\nAudit the REVIEW SET only, plus whether it stands alone and whether it duplicates any in-lesson problem. The in-lesson problems follow for collision checking only.\nREVIEW JSON:\n${JSON.stringify(lesson.review, null, 1)}\n\nIN-LESSON PROBLEMS FOR COLLISION CHECKING ONLY:\n${JSON.stringify(lesson.blocks.filter(b => b.t === 'prob').map(b => ({ x: b.x, ans: b.ans })), null, 1)}`,
    { label: 'audit:review', phase: 'Audit', schema: AUDIT_SCHEMA }),
])
const audit = {
  findings: [...((auditA && auditA.findings) || []).map(f => ({ ...f, where: `BLOCKS ${f.where}` })),
             ...((auditB && auditB.findings) || []).map(f => ({ ...f, where: `REVIEW ${f.where}` }))],
  verdict: `blocks: ${(auditA && auditA.verdict) || 'MISSING'} || review: ${(auditB && auditB.verdict) || 'MISSING'}`,
}

return { lesson, audit, fixedCount, pyChecks, missing }

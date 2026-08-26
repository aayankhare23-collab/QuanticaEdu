export const meta = {
  name: 'author-lesson-9-4',
  description: 'Author Algebra I 9.4 Roots, Sums, and Products',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '9.4'
const TITLE = 'Roots, Sums, and Products'
const NEXT = '9.5'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_lead', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_build', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_without', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Fourth lesson of chapter 9, Quadratics I, Factoring.
- 9.3's EXACT shipped closer is: "So far every root in this chapter was found the same way, factor
  first, then read each root off its factor. Lesson 9.4, Roots, Sums, and Products, works without
  that step. The sum and the product of a quadratic's roots can be read straight from its
  coefficients, so questions about the roots can be answered without ever finding them. That is
  new." The opener keeps that promise immediately, by DERIVING the two facts for a monic quadratic
  from the factored form the chapter already owns, in one or two plain sentences. Do NOT write
  "Last lesson we" or "Imagine".
- ESTABLISHED AND USED, NEVER RE-DERIVED: 9.1's double distribution and the forward pattern
  \\((x+r)(x+s)=x^2+(r+s)x+rs\\), 9.1's zero product property, 9.2's search and sign reasoning,
  9.3's leading-coefficient split and the fact that a factor \\(px+q\\) gives the root \\(-q/p\\).
- THE DERIVATION IS THE POINT. If \\(x^2+bx+c\\) has roots \\(r\\) and \\(s\\), then it equals
  \\((x-r)(x-s)\\), which expands to \\(x^2-(r+s)x+rs\\). Matching coefficients gives
  \\(r+s=-b\\) and \\(rs=c\\). Note the SIGN carefully, the roots of \\((x+r)(x+s)\\) are
  \\(-r\\) and \\(-s\\), so 9.2's search numbers are the NEGATIVES of the roots. That distinction
  is the single most common error in this material and must be attacked head on, not glossed.
- FRESHNESS: no factorization, number set or story from 9.1, 9.2 or 9.3 may reappear. Those
  lessons spent, among others, the quadratics 5x^2+29x+20, 11x^2+39x-20, 25x^2+75x+54,
  5x^2+53x+72, 30x^2-156x-144, 81x^2-100, 4x^2+13x+6, 4x^2+27x-40, 5x^2+22x-48, 144x^2+168x+49,
  24x^2-34x-45, 36x^2+13x-40, 5x^2+31x+44, 11x^2-38x-24, 6x^2+41x+30, 9x^2-31x-70, 4x^2+31x+60,
  5x^2+60x+160, 196x^2-169, 6x^2+5x+4, 6x^2-17x-114, 4x^2+9x-100, 25x^2-90x+81, 9x^2+16x-80,
  20x^2+45x-275, 20x^2-89x+80, 36x^2-60x-119, 20x^2+51x-90, 48x^2+26x-55, plus every monic
  quadratic from 9.2. Invent fresh coefficients everywhere.

TOPIC CHECKLIST (cover ALL):
 1. THE MONIC CASE. For \\(x^2+bx+c\\) the roots sum to \\(-b\\) and multiply to \\(c\\). Derived
    from \\((x-r)(x-s)\\), never asserted, and the sign on the sum stressed.
 2. THE GENERAL CASE. For \\(ax^2+bx+c\\) the roots sum to \\(-b/a\\) and multiply to \\(c/a\\).
    Reach it by dividing through by \\(a\\), which is one line given the monic case, and use it on
    a quadratic whose leading coefficient is not 1.
 3. BUILDING A QUADRATIC FROM ITS ROOTS. Given a sum and a product, the monic quadratic is
    \\(x^2-(\\text{sum})x+(\\text{product})\\). One problem builds one and asks for a coefficient.
 4. ANSWERING WITHOUT SOLVING, which is the lesson's whole reason to exist. Given a quadratic
    whose roots are ugly or unfindable by chapter 9's methods, compute things like \\(r+s\\),
    \\(rs\\), \\(\\frac{1}{r}+\\frac{1}{s}=\\frac{r+s}{rs}\\), \\(r^2+s^2=(r+s)^2-2rs\\), and
    \\((r-s)^2=(r+s)^2-4rs\\). Derive each rewriting the first time it is used. At least one
    problem must use a quadratic that does NOT factor over the integers, so the reader sees the
    method work where factoring cannot.
 5. THE SIGN TRAP, taught then tested. In \\(x^2+bx+c\\) the sum of the roots is \\(-b\\), NOT
    \\(b\\). Include a problem whose wrong answer is exactly the sign slip.
 6. FINDING A MISSING COEFFICIENT from a fact about the roots, for example given that one root is
    known, or that the roots are equal, or that the roots differ by a stated amount.
 7. A ROOT GIVEN, THE OTHER WANTED, obtained from the sum or the product in one step rather than
    by re-solving.
 8. THE HONEST LIMIT. These two facts do not by themselves produce the roots, and a pair with a
    given sum and product may not be real at all, for example sum 2 and product 5. Say that
    plainly and point to chapter 11 for what to do about it, no further.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO quadratic formula, NO completing the square, NO discriminant as a named tool or criterion,
  NO complex numbers. Chapter 11 owns all of it. Saying "such a pair is not real and chapter 11
  takes it up" is the maximum allowed.
- NO graphing, no vertex, no axis of symmetry (chapter 12).
- NO cubics and no sums or products of three or more roots (chapter 14 territory).
- Factoring is USED freely but no new factoring technique is taught.

ANSWER SHAPE. Every answer is a SINGLE typed value. Good asks are the sum of the roots, the
product of the roots, the value of a symmetric expression in the roots, one coefficient of a
built quadratic, a missing coefficient, or the second root when one is given. Every numeric
answer is an integer or a lowest-terms fraction, and negative answers need both the ASCII and
the unicode minus in accept.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener, derives the monic sum and product from \\((x-r)(x-s)\\)
  2 [P1] prob sum of the roots of a monic quadratic, where the sign of \\(-b\\) matters
  3 [P2] prob product of the roots of a monic quadratic with a negative constant
  4 [imp1] imp the monic rule, derived, with the sign on the sum stressed
  5 [P3] prob the sign trap head on, a monic quadratic with positive \\(b\\), sum asked for
  6 [P4] prob a leading coefficient above one, sum or product asked for as a lowest-terms fraction
  7 [imp2] imp the general rule, reached by dividing through by \\(a\\)
  8 [FIG] fig the coefficient-to-root-facts map, see below
  9 [p_lead] p reading the two facts off any quadratic
  10 [P5] prob build a monic quadratic from a stated sum and product, one coefficient asked for
  11 [P6] prob one root given, the other found from the sum
  12 [imp3] imp building from roots, \\(x^2-(\\text{sum})x+(\\text{product})\\)
  13 [p_build] p the point of all this, questions answered without the roots
  14 [P7] prob \\(\\frac{1}{r}+\\frac{1}{s}\\) on a quadratic that does not factor over the
     integers, the rewriting derived in the sol
  15 [fact] fact Albert Girard, see below
  16 [P8] prob \\(r^2+s^2\\) using \\((r+s)^2-2rs\\)
  17 [imp4] imp symmetric expressions rewritten in terms of the sum and the product
  18 [p_without] p why this beats solving even when solving is possible
  19 [P9] prob a missing coefficient from a stated fact about the roots
  20 [P10] prob equal roots, or roots differing by a stated amount, a coefficient asked for
  21 [imp5] imp finding a coefficient from a root fact, and the honest limit
  22 [p_close] p what the two facts can and cannot do
  23 [P11] prob a harder symmetric expression, \\((r-s)^2\\) or \\(r^2s+rs^2\\)
  24 [P12] prob the hardest closer, combining a built quadratic with a symmetric evaluation
  25 [closer] p hands off to 9.5, Factoring in Action, where the chapter's tools get applied

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): the rendered artwork is built separately with manim and swapped in later, so
your job for this slot is a clean, correct placeholder SVG plus the real caption. THE MAP FROM
COEFFICIENTS TO ROOT FACTS. Show \\(ax^2+bx+c\\) with its three coefficients marked, and two
labelled arrows leaving it, one to \\(-b/a\\) tagged sum and one to \\(c/a\\) tagged product,
with the middle coefficient's arrow carrying a visible minus sign so the picture itself teaches
the sign trap. The roots themselves appear nowhere in the figure, which is the whole point, the
facts are read off the coefficients without the roots. LETTERS ONLY, no digits anywhere.
Lowercase labels only, no sentence inside the SVG, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, Euclid's fifth postulate with Lobachevsky and Bolyai, Thomas
Harriot, Pierre Bouguer, Joseph Fourier, Leonid Kantorovich, George Dantzig, William Betz,
Rivest Shamir and Adleman, and Emmy Noether. NOTE that Viete is BANNED, so do NOT attribute these
relations to him even though they carry his name. Use Albert Girard, who in 1629 wrote down the
relations between a polynomial's coefficients and its roots in general form, several years before
the notation to state them cleanly existed. About 200 characters, plain claims only.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries
no digits, (c) every answer in the lesson is distinct from every other, (d) every numeric answer
is exact and every fraction is in lowest terms, (e) nothing from the 9.1, 9.2 or 9.3 spent lists
reappears.
`

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
- SINGLE BACKSLASHES, AND THIS IS THE ONE THAT KEEPS BREAKING. Write \\( not \\\\(, \\boxed
  not \\\\boxed, \\cdot not \\\\cdot. A doubled backslash does NOT render as math, it
  renders as literal source text on the page. Two blocks shipped broken this way in this chapter
  before being caught. If you are CORRECTING a block, re-check its escaping after the edit.
- INEQUALITY SYMBOLS INSIDE MATH ARE ALWAYS \\lt AND \\gt, NEVER A BARE < OR >. A raw < before
  a letter is eaten by the HTML parser as a tag and the rest of the sentence silently vanishes.
- ACCEPT LISTS: no two entries may normalize to the same string once spaces and commas are
  stripped and case is lowered, so never include both a plain and a comma-grouped spelling of one
  number, and never an unreduced fraction.
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
  commas, and drops a leading plus. It does NOT convert the unicode minus, so a negative answer
  needs BOTH the ASCII and the unicode spelling in accept. accept must contain ans plus every
  reasonable typed variant (word form, exact terminating decimal for a fraction, unit spellings).
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
2. AMBIGUITY. Could a careful reader read this statement a different way? Is every unit stated? Is the ask unmistakable about which single value to type?
3. Grader (normAns) trims, lowercases, strips spaces and commas, drops a leading plus, and does NOT convert the unicode minus. Is ans in accept? Any accept variant that falsely accepts a wrong response? Any obvious correct typed form missing?
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

export const meta = {
  name: 'author-lesson-9-5',
  description: 'Author Algebra I 9.5 Factoring in Action',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '9.5'
const TITLE = 'Factoring in Action'
const NEXT = '10.1'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_lead', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_build', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_choose', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Fifth and last lesson of chapter 9, Quadratics I, Factoring.
- 9.4's EXACT shipped closer is: "Every answer in this lesson's second half came off the coefficients, and four of those quadratics have no root chapter 9 can produce. Lesson 9.5, Factoring in Action, turns these tools on equations not written as \\(ax^2+bx+c=0\\). An equation can be a quadratic in some repeated piece, and naming that piece with one letter makes it one you can solve." The opener keeps that promise immediately,
  by taking an equation that is NOT written as a quadratic and naming its repeated piece. Do NOT write "Last lesson we" or "Imagine".
- ESTABLISHED AND USED, NEVER RE-DERIVED: 9.1's double distribution, the forward pattern
  \\((x+r)(x+s)=x^2+(r+s)x+rs\\) and the zero product property, 9.2's search and sign reasoning
  and the difference of two squares, 9.3's leading-coefficient split and the fact that a factor
  \\(px+q\\) gives the root \\(-q/p\\), 9.4's sum and product of the roots.
- THE POINT OF THE LESSON. An equation does not have to look like \\(ax^2+bx+c=0\\) to be a
  quadratic. It is a quadratic whenever it is a quadratic in SOME repeated piece, and naming that
  piece with a single letter turns it into one the reader can already solve. The second half of
  the lesson is the same move on equations that only become quadratics after the denominators are
  cleared, which is where extraneous solutions come from.
- FRESHNESS: no factorization, number set or story from 9.1 to 9.4 may reappear. Those lessons
  spent, among others, the quadratics 5x^2+29x+20, 11x^2+39x-20, 25x^2+75x+54, 5x^2+53x+72,
  30x^2-156x-144, 81x^2-100, 4x^2+13x+6, 4x^2+27x-40, 5x^2+22x-48, 144x^2+168x+49, 24x^2-34x-45,
  36x^2+13x-40, 5x^2+31x+44, 11x^2-38x-24, 6x^2+41x+30, 9x^2-31x-70, 4x^2+31x+60, 5x^2+60x+160,
  196x^2-169, 6x^2+5x+4, 6x^2-17x-114, 4x^2+9x-100, 25x^2-90x+81, 9x^2+16x-80, 20x^2+45x-275,
  20x^2-89x+80, 36x^2-60x-119, 20x^2+51x-90, 48x^2+26x-55, plus every monic quadratic from 9.2
  and every quadratic 9.4 spent, which is
  x^2-10x+21, x^2-17x+52, x^2+6x-91, x^2+23x+102, 8x^2+18x-5, 6x^2-13x-3, x^2-12x-85,
  5x^2-16x+3, 7x^2-5x-9, x^2-5x-8, 20x^2+x-12, x^2-2x+5, 4x^2+10x-21, 4x^2-12x-9,
  x^2-15x+26, x^2-8x-33, x^2+19x+34, 10x^2+11x-6, 8x^2+30x-7, x^2+6x-40, x^2-2x-63,
  6x^2-19x+14, 5x^2-14x+4, x^2-9x+11, x^2-6x-2, x^2-4x+9, x^2+30x+125, 25x^2-40x+16,
  x^2-14x+45, 2x^2-5x-6, x^2-7x+3, 2x^2-15x+18 and x^2-24x+128. Invent fresh coefficients everywhere.

TOPIC CHECKLIST (cover ALL):
 1. QUADRATIC IN A REPEATED PIECE. An equation like \\(x^4+bx^2+c=0\\) is a quadratic in
    \\(x^2\\). Name the piece, \\(u=x^2\\), solve the quadratic in \\(u\\), then UNDO the
    substitution. Derived by showing the equation and the quadratic side by side, not asserted.
 2. A COMPOUND REPEATED PIECE. The same move when the repeated piece is a binomial, for example
    an equation that is a quadratic in \\(2x-1\\). The piece does not have to be a power.
 3. UNDOING THE SUBSTITUTION IS PART OF THE PROBLEM. The single most common error here is
    stopping at the value of \\(u\\) and reporting it as the answer. Teach it, then test it with
    a problem whose wrong answer is exactly that.
 4. ONE u VALUE CAN GIVE TWO, ONE OR NO VALUES OF x. With \\(u=x^2\\), a positive \\(u\\) gives
    two, zero gives one, and a negative \\(u\\) gives none. At least one problem must have a
    \\(u\\) value that yields no real \\(x\\), so the count of solutions is not just doubled.
 5. CLEARING DENOMINATORS. An equation with the variable in a denominator becomes a quadratic
    once both sides are multiplied through. Show the multiplication explicitly.
 6. EXTRANEOUS SOLUTIONS, taught then tested. Any candidate that makes an original denominator
    zero is not a solution, however correctly it came out of the cleared equation. Include a
    problem where exactly one of the two candidates is extraneous, so the answer is the other one.
 7. A FACTOR THAT CANCELS. When a numerator factors and shares a factor with its denominator,
    the expression simplifies, and the value that zeroed the cancelled factor stays excluded.
 8. A QUADRATIC IN ONE OF SEVERAL LETTERS. An equation in two letters, for example one of the
    form \\(a^2+kab+mb^2=0\\), is a quadratic in \\(a\\) with \\(b\\) treated as a constant.
    Factoring it gives a ratio such as \\(a/b\\). One problem asks for such a ratio.
 9. CHOOSING THE TOOL. Sometimes 9.4's sum and product answer a question faster than factoring
    does. One problem is set up so that the root facts are clearly the shorter route.
10. THE HONEST LIMIT. Substitution only helps when the resulting quadratic can be factored, and
    plenty cannot. Say plainly that chapter 10 adds more factorizations and chapter 11 gives a
    method that works on every quadratic, and stop there.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO quadratic formula, NO completing the square, NO discriminant as a named tool, NO complex
  numbers. Chapter 11 owns all of it. "Chapter 11 takes that up" is the maximum allowed.
- NO sum or difference of cubes, NO squares-of-binomials patterns as a named factorization, NO
  Simon-style regrouping. Chapter 10 owns those.
- NO graphing, no vertex, no parabola (chapter 12). NO functions or function notation (chapter 13).
- NO radical equations and no squaring both sides. That is a second and different source of
  extraneous solutions and it would blur the one this lesson teaches.
- NO polynomial division and nothing of degree above four.

ANSWER SHAPE. Every answer is a SINGLE typed value. Good asks are one specified root (the
largest, the smallest, the positive one), the number of real solutions, the sum or product of the
solutions, a ratio, an excluded value, or the value of a coefficient. Every numeric answer is an
integer or a lowest-terms fraction, and negative answers need both the ASCII and the unicode
minus in accept. Never ask for a list of solutions.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener, an equation that is not a quadratic in x but is a quadratic in x^2
  2 [P1] prob a quadratic in x^2 solved by substitution, one specified root asked for
  3 [P2] prob a quadratic in a repeated binomial piece
  4 [imp1] imp naming the repeated piece and substituting, derived
  5 [P3] prob the undo-the-substitution trap head on
  6 [P4] prob a substitution where one u value yields no real x, the count of real solutions asked
  7 [imp2] imp undoing the substitution, and how many x each u value gives
  8 [FIG] fig the rename-the-repeated-piece picture, see below
  9 [p_lead] p spotting the repeated piece in an unfamiliar equation
 10 [P5] prob an equation with the variable in a denominator that clears to a quadratic
 11 [P6] prob exactly one candidate is extraneous, the surviving one asked for
 12 [imp3] imp clearing denominators and why a candidate can fail
 13 [p_build] p a factor shared by a numerator and a denominator
 14 [P7] prob a rational equation where factoring cancels a factor, the excluded value or the root asked
 15 [fact] fact Ludovico Ferrari, see below
 16 [P8] prob a two-letter equation treated as a quadratic in one letter, a ratio asked for
 17 [imp4] imp treating a multi-variable equation as a quadratic in one letter
 18 [p_choose] p picking between factoring, substituting, and the root facts
 19 [P9] prob a stated situation that becomes a quadratic, where one root is impossible and is discarded
 20 [P10] prob one where 9.4's sum or product is clearly the shorter route
 21 [imp5] imp choosing the tool, and what each of chapter 9's tools is for
 22 [p_close] p what chapter 9 now covers and what it still cannot do
 23 [P11] prob a harder substitution, the piece less obvious
 24 [P12] prob the hardest closer, combining a substitution with a discarded or extraneous candidate
 25 [closer] p hands off to chapter 10, Special Factorizations

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): the rendered artwork is built separately with manim and swapped in later, so
your job for this slot is a clean, correct placeholder SVG plus the real caption. RENAMING THE
REPEATED PIECE. Two rows. The top row shows an equation in which one piece appears twice, with
both copies of that piece filled in the same flat colour so the eye pairs them. The bottom row
shows the same skeleton with a single letter standing in both places, so the shape underneath is
plainly a quadratic. Nothing else changes between the rows, which is the whole point, so every
glyph outside the repeated piece sits at the same position in both rows. LETTERS ONLY, no digits
except an exponent and the zero on the right of the equals sign. Lowercase labels only, no sentence inside the SVG, all prose
in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, Euclid's fifth postulate with Lobachevsky and Bolyai, Thomas
Harriot, Pierre Bouguer, Joseph Fourier, Leonid Kantorovich, George Dantzig, William Betz,
Rivest Shamir and Adleman, Emmy Noether, and Albert Girard. Use Ludovico Ferrari, who around 1540
solved the general fourth-degree equation by a substitution that turns it into a third-degree one,
the same move this lesson makes on a smaller scale. Note that Cardano is BANNED, so do not route
the story through him even though he published Ferrari's work. About 200 characters, plain claims
only.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries no digits beyond an
exponent and a zero, (c) every answer in the lesson is distinct from every other, (d)
every numeric answer is exact and every fraction is in lowest terms, (e) nothing from the 9.1 to
9.4 spent lists reappears.
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
  commas, and drops a leading plus. It ALSO maps the unicode minus and the en/em dashes onto
  ASCII '-', strips a leading '$', and folds a mixed number like "1 1/2" onto "3/2". So a
  negative answer needs ONLY the ASCII spelling, and a separate unicode-minus entry is dead
  weight the grader can never reach. Never add the whitespace-stripped form of a mixed number
  ("21/2" for "2 1/2"); that now denotes ten and a half and grades a wrong answer correct.
  accept must contain ans plus every reasonable typed variant (word form, exact terminating
  decimal for a fraction, unit spellings).
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

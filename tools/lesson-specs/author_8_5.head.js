export const meta = {
  name: 'author-lesson-8-5',
  description: 'Author Algebra I 8.5 Optimization',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '8.5'
const TITLE = 'Optimization'
const NEXT = '9.1'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_two', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_region', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_int', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Fifth and LAST lesson of chapter 8, Inequalities. It closes the chapter.
- 8.1 gave the rules, 8.2 compared two numbers, 8.3 solved a linear inequality in one variable,
  8.4 drew the solutions, as a ray on a number line and as a half-plane in the plane, and found the
  overlap of several half-planes together with the corners where boundaries cross. 8.4 closes by
  handing off to this lesson. The opener picks that up in one or two plain sentences. Do NOT write
  "Last lesson we" or "Imagine".
- CHAPTER 5 and 7.6 both know how to find where two lines cross, which is how a corner is found
  here. Do NOT re-derive it.

TOPIC CHECKLIST (cover ALL):
 1. WHAT OPTIMIZATION ASKS. Not "what values work" but "of the values that work, which is largest",
    and the answer is a single number. Say that plainly at the start.
 2. THE TWO-PART ANSWER, which is the whole idea of the lesson and its hardest habit to build.
    Showing \\(x\\le 7\\) does NOT show that \\(7\\) is the maximum, only that nothing beats it.
    A maximum needs BOTH parts, a bound saying it cannot be exceeded AND a case showing the bound
    is actually reached. State this early, use it everywhere, and include a problem where a
    plausible bound is NOT attainable so the true maximum is smaller.
 3. BOUNDING A SINGLE VARIABLE. Rearranging a constraint into the form \\(x\\le\\) some number, then
    checking that the number is achievable.
 4. WHEN THE BOUND IS NOT ATTAINABLE because a quantity must be a WHOLE NUMBER. If \\(n\\le 7.4\\)
    and \\(n\\) counts objects, the maximum is \\(7\\), not \\(7.4\\). Include this explicitly,
    because it is the most common real version of the two-part answer.
 5. SEVERAL CONSTRAINTS AT ONCE on one variable. Every constraint gives a bound, and the binding
    one is the tightest. The maximum is the smallest of the upper bounds.
 6. OPTIMIZING A LINEAR EXPRESSION OVER A REGION. With two variables under a list of linear
    constraints, the largest and smallest values of a linear expression occur AT A CORNER of the
    region. State it as a usable fact, justify it by noting that moving along any edge changes the
    expression steadily so an interior point of an edge can never beat both of its ends, and then
    use it. Do NOT attempt a full proof.
 7. THE METHOD. Find the corners by intersecting boundary pairs, evaluate the expression at each,
    and take the best. One problem must run the full method on a region with three or four corners.
 8. MINIMIZING is the same work with the other end taken.

SCOPE BOUNDARY:
- Do NOT re-derive 8.1's rules, 8.3's isolation, or 8.4's half-plane picture. All are used.
- Do NOT teach the simplex method or anything algorithmic beyond checking every corner.
- Nothing quadratic, no absolute value. The closer hands off to chapter 9, Quadratics I, Factoring,
  opening with 9.1.

ANSWER SHAPE. Every answer is a SINGLE typed value, which optimization gives naturally, since the
answer to "what is the largest possible value" IS one number. Other good asks are the value of the
expression at the best corner, one coordinate of the corner where the best value occurs, the number
of corners of a region, or the largest whole number of items. Never ask for a region, a pair, or an
explanation. Every answer is an integer or a lowest-terms fraction, never a rounded decimal, and
when the answer must be a whole number the problem must say what is being counted.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob bound one variable and check the bound is reached
  3 [P2] prob a bound that is NOT reached, so the true maximum is smaller
  4 [imp1] imp a maximum needs a bound AND a case reaching it
  5 [P3] prob a whole-number quantity forcing the bound down
  6 [P4] prob several constraints, the tightest one binding
  7 [imp2] imp the smallest of the upper bounds is the one that binds
  8 [FIG] fig a region with its corners marked, and the best corner picked out
  9 [p_two] p two variables at once
  10 [P5] prob a corner found by intersecting two boundaries
  11 [P6] prob how many corners a stated region has
  12 [imp3] imp the best value of a linear expression sits at a corner, and why
  13 [p_region] p the method end to end
  14 [P7] prob evaluate at every corner and take the best
  15 [fact] fact George Dantzig, see below
  16 [P8] prob a minimum rather than a maximum
  17 [imp4] imp the method, and minimizing as the same work
  18 [p_int] p when the answer has to be a whole number
  19 [P9] prob a whole-number optimum inside a region
  20 [P10] prob a context where the binding constraint is not the obvious one
  21 [imp5] imp whole-number constraints, and checking attainability at the end
  22 [p_close] p putting the chapter together
  23 [P11] prob the full method on a four-corner region
  24 [P12] prob the hardest closer
  25 [closer] p closes chapter 8 and hands off to chapter 9, Quadratics I, Factoring, opening with 9.1

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): one shaded region in the first quadrant bounded by three or four straight edges,
with each corner marked by a dot, and ONE corner picked out in gold with a short lowercase label
reading "best here". The picture must say that only the corners need checking. Use LETTERS for the
boundaries and put NO DIGITS in the figure, which keeps it collision-proof against every problem.
Lowercase labels only, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, Euclid's fifth postulate with Lobachevsky and Bolyai, Thomas
Harriot, Pierre Bouguer, Joseph Fourier, and Leonid Kantorovich. Use George Dantzig, who arrived
late to a class in 1939, copied two problems off the board as homework, and handed in solutions to
what were in fact two open questions nobody had answered. About 200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries no
digits, (c) every answer in the lesson is distinct from every other, (d) every answer is exact.
`

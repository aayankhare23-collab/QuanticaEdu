export const meta = {
  name: 'author-lesson-9-3',
  description: 'Author Algebra I 9.3 Factoring ax^2+bx+c',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '9.3'
const TITLE = 'Factoring ax² + bx + c'
const NEXT = '9.4'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_cf', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_ns', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_solve', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Third lesson of chapter 9, Quadratics I, Factoring.
- 9.2's EXACT shipped closer is: "Every quadratic here began monic or became monic after a numeric
  factor came out. When the leading coefficient stays, as in \\(2x^2+7x+3\\), the sum and product
  clues are no longer enough on their own. Lesson 9.3, Factoring \\(ax^2+bx+c\\), extends the
  search to that case." The opener keeps that promise by factoring exactly that quadratic,
  \\(2x^2+7x+3=(2x+1)(x+3)\\), checked by a quick expansion, and states what changed, the leading
  coefficient must also be split between the factors. Do NOT write "Last lesson we" or "Imagine".
  The numbers 2, 7, 3, 1 of that example are SPENT and appear in no problem.
- ESTABLISHED AND USED, NEVER RE-DERIVED: 9.1's double distribution and identities, 9.2's
  sum-and-product search, sign reasoning, and common-factor-first habit, and the zero product
  property. Chapter divides fractions and reduces them to lowest terms as far back as prealgebra.
- FRESHNESS ACROSS LESSONS: no factor pair or example from 9.1 or 9.2 may reappear. Notable spent
  material: from 9.1 the products (x+3)(x+4), (x+5)(x+6), (x+10)(x-2), (x-5)(x-8), (8x-5)(2x+9),
  (x+8)^2, (6x-11)^2, (9x-5)^2, (2x+1)(5x+8), (2x-9)(8x-1), 61x59, 85x75; from 9.2 the pairs
  {2,6}, {7,-4}, {-2,-11}, 4(x+3)(x+10), x(x-14), (x+9)^2, (x-9)(x+5), (x+8)(x-3), (w+17)(w-11),
  3(x-5)(x-10), {3,13}, {2,8}, {3,12}, {-6,8}, {-5,-7}, 7(x+1)(x+5), x(x-22), (x+15)(x-15),
  29^2-21^2, 53^2-47^2, (x-16)^2, {4,-11}, (x-10)(x+7), (x-13)(x+5), x(x-19), 3(x+2)(x+7),
  (n+18)(n-17), 2(x-13)(x+13). Invent fresh factorizations everywhere.

TOPIC CHECKLIST (cover ALL):
 1. THE SHAPE. \\(ax^2+bx+c=(px+q)(rx+s)\\) needs \\(pr=a\\), \\(qs=c\\), and the cross products
    summing to the middle, \\(ps+qr=b\\). Derive it by expanding the general product with 9.1's
    double distribution, so the three conditions are read off, not handed down.
 2. THE FORCED SPLIT. When \\(a\\) is prime the leading terms can only split as \\(a\\cdot 1\\),
    which makes prime-\\(a\\) quadratics the easy entry case. Start there.
 3. THE ORGANIZED SEARCH. Leading pairs of \\(a\\) times constant pairs of \\(c\\), each candidate
    checked on its cross sum. The list is finite, and ONLY binomial pairs whose linear terms
    multiply to \\(ax^2\\) ever need trying.
 4. NARROWING. 9.2's sign reasoning carries over unchanged. Additionally the SIZE and PARITY of
    \\(b\\) prune candidates, for instance when \\(b\\) is odd an all-even candidate row is
    impossible, and a small \\(b\\) rules out pairings whose cross products are both large.
    Include one problem where a stated narrowing observation kills half the list before trying.
 5. COMMON FACTOR FIRST, STILL. A numeric common factor comes out before any search, and
    sometimes what remains is monic, handing the work back to 9.2's shorter method. One problem
    where the GCF reduces the leading coefficient but leaves it above \\(1\\).
 6. THE IDENTITIES SCALE UP. \\(9x^2-49=(3x+7)(3x-7)\\) is 9.1's conjugate identity with
    \\(3x\\) as the first term, and a perfect square like \\(25x^2+30x+9=(5x+3)^2\\) is the
    square identity the same way. One problem each, recognized rather than searched.
 7. NOT EVERYTHING FACTORS, still true with a leading coefficient, seen by a search coming up
    empty, with the honest pointer to chapter 11 and nothing more.
 8. SOLVING. Factor, zero product, and now FRACTION ROOTS appear, since \\(px+q=0\\) gives
    \\(x=-q/p\\). Every fraction answer is exact and in lowest terms. Include one equation
    arriving not set to zero.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO grouping or splitting-the-middle-term technique, and no ac-method. The method here is the
  organized candidate search with narrowing, which is what the reference teaches at this point.
  Grouping belongs to chapter 10.
- NO sum and product of roots as a named tool (9.4 owns it), no quadratic formula, completing
  the square, discriminants, complex numbers (chapter 11), no graphing (chapter 12).
- Difference of squares stays with perfect square terms on both ends.

ANSWER SHAPE. Every answer is a SINGLE typed value, and a factorization is never the typed
answer. Good asks are one constant inside a pinned factor (the ask fixes the factor by naming
its leading term, or asks for the larger or smaller constant), the greatest common numeric
factor, one root pinned exactly (the positive one, the negative one, the larger one) as an
integer or lowest-terms fraction, the word yes or no for factorability, or a COUNT of candidate
pairs a narrowing observation leaves alive.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener, the closer's example factored, and what changed named plainly
  2 [P1] prob prime \\(a\\), forced split, everything positive, one constant asked for
  3 [P2] prob prime \\(a\\) with a negative constant, one constant asked for
  4 [imp1] imp the shape, three conditions read off the general expansion
  5 [P3] prob composite \\(a\\), two leading splits genuinely in play, one constant asked for
  6 [P4] prob a narrowing observation stated and used, the COUNT of surviving candidates or a
     constant asked for
  7 [imp2] imp the organized search and what narrows it
  8 [FIG] fig the cross diagram, see below
  9 [p_cf] p the numeric factor still comes out first
  10 [P5] prob GCF out first, leading coefficient still above one after, one value asked for
  11 [P6] prob a scaled difference of squares, one constant asked for
  12 [imp3] imp common factor first, and the identities with \\(ax\\) as the first term
  13 [p_ns] p a search that ends empty
  14 [P7] prob yes or no factorability for a non-monic quadratic
  15 [fact] fact Emmy Noether, see below
  16 [P8] prob solve a factorable equation, the positive fraction root asked for
  17 [imp4] imp each factor \\(px+q\\) contributes the root \\(-q/p\\), fractions are normal now
  18 [p_solve] p rearrange to zero first, as always
  19 [P9] prob solve one arriving not set to zero, one root pinned
  20 [P10] prob a scaled perfect square, one value asked for
  21 [imp5] imp the full pipeline with the leading coefficient in it
  22 [p_close] p what the chapter's search can now handle
  23 [P11] prob a harder composite-\\(a\\) factorization, one constant asked for
  24 [P12] prob the hardest closer, a solve whose two roots are both fractions, one pinned
  25 [closer] p hands off to 9.4, Roots, Sums, and Products, answering questions about roots
     WITHOUT finding them, which is new

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): the rendered artwork is built separately with manim and swapped in later, so
your job for this slot is a clean, correct placeholder SVG plus the real caption. THE CROSS
DIAGRAM of the candidate check. The two binomials stacked, \\(px+q\\) above \\(rx+s\\), with
three marked readings: the left column product \\(pr\\) giving the leading coefficient, the
right column product \\(qs\\) giving the constant, and the two DIAGONALS \\(ps\\) and \\(qr\\)
crossing in the middle, picked out in gold, with their sum giving the middle coefficient. The
picture says the middle term is where the candidates pass or fail. LETTERS ONLY, no digits
anywhere. Lowercase labels only, no sentence inside the SVG, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, Euclid's fifth postulate with Lobachevsky and Bolyai, Thomas
Harriot, Pierre Bouguer, Joseph Fourier, Leonid Kantorovich, George Dantzig, William Betz, and
Rivest, Shamir and Adleman. Use Emmy Noether: her 1921 paper turned factoring itself into a
subject, asking in which number systems every factorization is unique, and much of modern
algebra descends from it. About 200 characters, plain claims only.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries
no digits, (c) every answer in the lesson is distinct from every other except a yes/no word
answer may coexist with numerics, (d) every numeric answer is exact and every fraction is in
lowest terms, (e) nothing from the 9.1 and 9.2 spent lists reappears, and the opener's 2, 7, 3,
1 example appears only in the opener.
`

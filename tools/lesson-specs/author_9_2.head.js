export const meta = {
  name: 'author-lesson-9-2',
  description: 'Author Algebra I 9.2 Factoring x^2+bx+c',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '9.2'
const TITLE = 'Factoring x² + bx + c'
const NEXT = '9.3'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_cf', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_ds', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_solve', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Second lesson of chapter 9, Quadratics I, Factoring.
- 9.1's EXACT shipped closer is: "Every product \\((x+r)(x+s)\\) expands to \\(x^2+(r+s)x+rs\\),
  the sum in the middle and the product at the end. Lesson 9.2, Factoring \\(x^2+bx+c\\), starts
  from the expanded form and recovers \\(r\\) and \\(s\\), a search with exactly two clues, the sum
  and the product." The opener keeps that promise, the two clues named and the search begun, in one
  or two plain sentences. Do NOT write "Last lesson we" or "Imagine".
- 9.1 established: double distribution, the forward pattern \\((x+r)(x+s)=x^2+(r+s)x+rs\\), the
  three identities \\((a+b)^2\\), \\((a-b)^2\\), \\((a+b)(a-b)=a^2-b^2\\), checking by substituting
  a value, and the ZERO PRODUCT PROPERTY with its zero-on-one-side trap. All of that is USED here
  and none of it is re-derived.
- Chapter 2 owns factoring out a common NUMERIC factor from a linear expression; here that move is
  applied to quadratics, extended, not re-taught.
- FRESHNESS ACROSS LESSONS: no factor pair from 9.1 may reappear. Spent there: (x+3)(x+4),
  (x+5)(x+6), (x+10)(x-2), (x-5)(x-8), (8x-5)(2x+9), (x+8)^2, 61x59, (x+6)(x+9), (x-10y)(x+8y),
  (x-8)(x+15), x(x-16), (10x-25)(2x+1), (6x-11)^2, (x+1)(x+9), (x-1)(x+14), (x-2)(x-9),
  (2x+1)(5x+8), (x+11)^2, (x-10)^2, 85x75, (x+20)(x-20), (2x-9)(8x-1), (x+6)(x+10), (x-6y)(x+15y),
  (x-13)(x+6), (x+16)(x+21), x(2x-15), (x-17)^2, (x-1)(x+13), (9x-5)^2. Invent fresh pairs.

TOPIC CHECKLIST (cover ALL):
 1. THE SEARCH. To factor \\(x^2+bx+c\\), find two numbers with sum \\(b\\) and product \\(c\\),
    then \\(x^2+bx+c=(x+r)(x+s)\\). This is 9.1's forward pattern read right to left, and the
    opener says exactly that. The efficient search runs through the FACTOR PAIRS OF \\(c\\), which
    are finitely many, checking each pair's sum, rather than through sums, which are endless.
 2. SIGN REASONING, derived rather than asserted. A positive \\(c\\) means \\(r\\) and \\(s\\)
    share a sign, and \\(b\\) tells which one. A negative \\(c\\) means they differ in sign, and
    \\(b\\) carries the sign of the one with larger absolute value. Reach it from the forward
    pattern, then use it to cut the search down.
 3. COMMON FACTOR FIRST. Before any search, pull out the greatest common numeric factor, so
    something like \\(3x^2+3bx+3c\\)-shaped input becomes 3 times a monic quadratic, and a
    quadratic with no constant term factors as \\(x\\) times a linear factor. Skipping this step
    is the most common practical error, so teach it, then test it.
 4. DIFFERENCE OF SQUARES, run backwards. \\(x^2-k^2=(x+k)(x-k)\\), recognized by the missing
    middle term and negative constant, which is 9.1's conjugate identity reversed. Include the
    arithmetic payoff in reverse, a value like \\(53^2-47^2\\) computed as
    \\((53-47)(53+47)\\) in one's head.
 5. A PERFECT SQUARE TRINOMIAL is the search's \\(r=s\\) case, recognized when \\(c\\) is a square
    and \\(b\\) is twice its root. One problem, treated as a case of the search, not a new rule.
 6. NOT EVERYTHING FACTORS. For some \\(b\\) and \\(c\\) no integer pair exists, seen by running
    the whole finite search and coming up empty. State plainly that such quadratics get their
    treatment in chapter 11, and no more than that.
 7. SOLVING EQUATIONS. Factor, then 9.1's zero product property splits the equation. Include one
    equation that arrives NOT set equal to zero, so the rearrangement earns its place, since the
    zero-on-one-side trap is already taught and this is where it pays.
 8. ONE APPLIED PROBLEM whose setup produces a quadratic equation, where only one root fits the
    context and the ask pins which.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO leading coefficients beyond a pulled-out common numeric factor. Factoring
  \\(ax^2+bx+c\\) with \\(a\\) not dividing out is 9.3, and the closer hands off to it.
- NO sum and product of roots as a named tool for answering questions about roots (9.4 owns
  Vieta-style reasoning; here the sum and product are clues for the SEARCH, not statements
  about roots).
- NO quadratic formula, completing the square, discriminants, complex numbers (chapter 11), no
  graphing (chapter 12), no cubes, no grouping, no two-variable factorizations (chapter 10).
- Difference of squares stays with perfect square constants; nothing like \\(x^2-20\\), whose
  factorization needs radicals.

ANSWER SHAPE. Every answer is a SINGLE typed value. A factorization is never the typed answer.
Good asks are one of the two constants in the factored form pinned exactly (the larger, the
smaller, or the positive one), the greatest common numeric factor pulled out, a numeric value
computed by the reversed identity, the word yes or no for whether an integer factorization
exists, one root of an equation pinned exactly, or the one context-fitting root of the applied
problem. Every numeric answer is an integer or a lowest-terms fraction.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener, the two clues from the closer, and the search stated
  2 [P1] prob pure search warm-up, two numbers with a given sum and product, the larger asked for
  3 [P2] prob factor \\(x^2+bx+c\\) with everything positive, one factor constant asked for
  4 [imp1] imp the search, the pattern read right to left, running the factor pairs of \\(c\\)
  5 [P3] prob negative \\(c\\), the two constants differ in sign, one of them asked for
  6 [P4] prob positive \\(c\\) with negative \\(b\\), both constants negative, one asked for
  7 [imp2] imp sign reasoning, derived from the forward pattern
  8 [FIG] fig the area model read inside out, see below
  9 [p_cf] p the common factor comes out first
  10 [P5] prob a quadratic with a greatest common numeric factor, the factor asked for
  11 [P6] prob no constant term, \\(x\\) itself comes out, a pinned value asked for
  12 [imp3] imp common factor first, every time, and why the search needs a monic quadratic
  13 [p_ds] p the missing middle term
  14 [P7] prob a numeric difference of two squares computed by the reversed identity
  15 [fact] fact Rivest, Shamir and Adleman, see below
  16 [P8] prob a quadratic with NO integer factorization, yes or no asked for, plus one perfect
     square trinomial recognized inside P8's statement or the neighbouring search problems
  17 [imp4] imp difference of squares backwards, the perfect square case, and the honest note
     that some quadratics need chapter 11
  18 [p_solve] p factoring meets the zero product property
  19 [P9] prob solve a factorable equation already set to zero, one root pinned
  20 [P10] prob solve one that must be rearranged to zero first, one root pinned
  21 [imp5] imp the full pipeline, rearrange, common factor, search, split, and check one root by
     substitution
  22 [p_close] p what the chapter can now do, and what it cannot yet
  23 [P11] prob the applied problem, a context where only one root fits
  24 [P12] prob the hardest closer, combining a common factor with a sign-reasoned search or a
     reversed identity, one pinned value asked for
  25 [closer] p hands off to 9.3, Factoring \\(ax^2+bx+c\\), where the leading coefficient stays

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): the rendered artwork is built separately with manim and swapped in later, so
your job for this slot is a clean, correct placeholder SVG plus the real caption. The AREA MODEL
READ INSIDE OUT, the reverse of 9.1's figure. The same rectangle cut into four cells, the cells
now labelled with what the expansion gives, \\(x^2\\) in the top left, \\(rx\\) and \\(sx\\) in
the two cross cells, \\(rs\\) in the last, and the SIDE LENGTHS \\(x+r\\) and \\(x+s\\) picked
out in gold as the unknowns factoring recovers. The picture says that the expanded form is the
inside of the rectangle and the factors are its sides. LETTERS ONLY, no digits anywhere, which
makes the figure collision-proof against every problem. Lowercase labels only, no sentence inside
the SVG, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, Euclid's fifth postulate with Lobachevsky and Bolyai, Thomas
Harriot, Pierre Bouguer, Joseph Fourier, Leonid Kantorovich, George Dantzig, and William Betz.
Use Rivest, Shamir and Adleman: in 1977 they built the RSA encryption system on the fact that
multiplying two enormous numbers is quick while recovering the factors from the product is
enormously slow, so much of internet security rests on factoring being hard. About 200
characters, and do NOT overclaim that factoring is proven hard, say that no fast method is known.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries
no digits, (c) every answer in the lesson is distinct from every other except a yes/no word answer
may coexist with numerics, (d) every numeric answer is exact, (e) no factor pair from the 9.1 list
above reappears anywhere.
`

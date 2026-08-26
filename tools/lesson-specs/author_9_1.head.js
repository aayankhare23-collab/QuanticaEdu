export const meta = {
  name: 'author-lesson-9-1',
  description: 'Author Algebra I 9.1 Meet the Quadratic',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '9.1'
const TITLE = 'Meet the Quadratic'
const NEXT = '9.2'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_sq', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_check', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_zero', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. First lesson of chapter 9, Quadratics I, Factoring. It opens the chapter.
- Chapter 8 closed with 8.5, whose EXACT shipped closer is: "Every boundary in this chapter was a
  straight line because every expression was linear. Chapter 9 turns to expressions where a letter
  is multiplied by itself. Lesson 9.1 opens Quadratics I with factoring, writing \\(x^2+7x+12\\) as
  \\((x+3)(x+4)\\), two linear factors, so the straight-line work just finished stays in use."
  The opener keeps that promise by MULTIPLYING the product \\((x+3)(x+4)\\) back out to confirm it
  really equals \\(x^2+7x+12\\), then says plainly that this lesson owns the forward direction,
  multiplying, and the next lesson learns to reverse it. Do NOT write "Last lesson we" or "Imagine".
  The numbers 3, 4, 7, 12 of that continuity example are SPENT and no problem may reuse them.
- Chapter 2 owns the distributive property and chapter 3 owns exponent rules. Both are USED here
  and neither is re-derived. Multiplying two binomials is the distributive property applied twice,
  and saying exactly that is how imp1 earns the rule.
- The word QUADRATIC is new. Define it plainly, an expression of the form \\(ax^2+bx+c\\) with
  \\(a\\) not zero, named where it first appears.

TOPIC CHECKLIST (cover ALL):
 1. MULTIPLYING TWO BINOMIALS. \\((x+r)(x+s)\\) by distributing twice, so every term of the first
    multiplies every term of the second, four products in all, then like terms are collected.
    Derive it, do not hand down a recipe.
 2. THE FORWARD PATTERN. In \\((x+r)(x+s)=x^2+(r+s)x+rs\\) the middle coefficient is the SUM and
    the constant is the PRODUCT. State it as a fact about multiplying. Do NOT run it backwards,
    9.2 owns finding \\(r\\) and \\(s\\) from the expansion.
 3. LEADING COEFFICIENTS. Products like \\((2x+5)(3x-4)\\), where the \\(x^2\\) coefficient is a
    product too and collecting the middle takes more care.
 4. THE THREE NAMED SQUARES AND THE CONJUGATE PRODUCT, forward direction only:
    \\((a+b)^2=a^2+2ab+b^2\\), \\((a-b)^2=a^2-2ab+b^2\\), \\((a+b)(a-b)=a^2-b^2\\). Each earned by
    the same double distribution, never asserted. Include the classic arithmetic payoff, a product
    like \\(32\\times 28\\) computed as \\((30+2)(30-2)\\) in one's head.
 5. CHECKING BY SUBSTITUTION. An expansion must agree with the original at EVERY value of the
    letter, so evaluating both sides at one value catches most mistakes. Use it on a claimed
    expansion that is wrong.
 6. TWO VARIABLES. One product like \\((x+3y)(x-2y)\\), same rule, nothing new but the bookkeeping.
 7. THE ZERO PRODUCT PROPERTY. A product is zero exactly when at least one factor is zero, because
    the product of two nonzero numbers is never zero. This is what makes factored form worth
    having, it turns \\((x-2)(x+9)=0\\) into two linear equations, chapter 4's work.
 8. THE ZERO-ON-ONE-SIDE TRAP. \\((x-a)(x-b)=c\\) with \\(c\\) not zero says nothing about either
    factor. The property needs zero on one side. Teach it, then test it.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO FACTORING. Never ask the student to produce factors from an expanded quadratic. Presenting a
  factored form and asking to expand it or solve it is fine, going the other way is 9.2 and 9.3.
- NO quadratic formula, no completing the square, no complex numbers (chapter 11), no graphing
  parabolas (chapter 12), no sum and product of ROOTS as a topic (9.4), no cubes or grouping
  (chapter 10).
- The one borderline ask allowed: matching against a named identity in the forward direction,
  such as finding \\(b\\) so that \\(x^2+bx+81\\) is exactly \\((x+9)^2\\), where the reader
  expands the square and compares. That is identity use, not trinomial factoring.

ANSWER SHAPE. Every answer is a SINGLE typed value. Good asks are one coefficient of an expansion
(the ask names which power), the constant term, the value of a product computed by an identity,
the value of an expression at a stated number, one solution of a factored equation (the ask pins
which one, the larger, the smaller, or the positive one), or a COUNT of solutions. Every numeric
answer is an integer or a lowest-terms fraction.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener, multiplies the closer's product back out and names the quadratic
  2 [P1] prob a first product \\((x+r)(x+s)\\), the coefficient of \\(x\\) asked for
  3 [P2] prob a second product with a subtraction in it, the constant term asked for
  4 [imp1] imp the rule, distribute twice so every term meets every term, derived from chapter 2
  5 [P3] prob a product where both signs are negative, the coefficient of \\(x\\) asked for
  6 [P4] prob a leading-coefficient product \\((ax+b)(cx+d)\\), the coefficient of \\(x\\) asked for
  7 [imp2] imp the forward pattern, middle is the sum and constant is the product
  8 [FIG] fig the area model, see below
  9 [p_sq] p three products worth knowing by name
  10 [P5] prob expand \\((x+k)^2\\), the coefficient of \\(x\\) asked for
  11 [P6] prob a two-digit arithmetic product computed as \\((n+d)(n-d)\\), the value asked for
  12 [imp3] imp the three identities, each from the same double distribution
  13 [p_check] p checking an expansion by substituting one value
  14 [P7] prob a CLAIMED expansion with one wrong coefficient, caught by substitution, the correct
     coefficient asked for
  15 [fact] fact William Betz and FOIL, see below
  16 [P8] prob the two-variable product, one named coefficient asked for
  17 [imp4] imp the zero product property and the why, a product of nonzero numbers is not zero
  18 [p_zero] p what factored form buys, two linear equations
  19 [P9] prob solve \\((x-m)(x+n)=0\\), the larger solution asked for
  20 [P10] prob solve one with \\(x\\) itself as a factor, the COUNT of solutions asked for
  21 [imp5] imp two factors give at most two solutions, a repeated factor gives one, and the
     zero-on-one-side trap stated plainly
  22 [p_close] p multiplying is now mechanical, and the chapter's prize is reversing it
  23 [P11] prob a factored equation with fraction solutions, \\((px-q)(rx+s)=0\\), the positive
     solution asked for as a lowest-terms fraction
  24 [P12] prob the hardest closer, an identity-matching ask in the forward direction
  25 [closer] p hands off to 9.2, Factoring \\(x^2+bx+c\\), going backwards

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): the rendered artwork is built separately with manim and swapped in later, so
your job for this slot is a clean, correct placeholder SVG plus the real caption. The AREA MODEL
of a two-binomial product. One large rectangle whose top side is split into lengths \\(a\\) and
\\(b\\) and whose left side is split into lengths \\(c\\) and \\(d\\), cut into four cells, each
cell carrying its own product label, ac, ad, bc, bd, in italic letters. The picture says that the
whole rectangle is the sum of the four cells, which is exactly why every term multiplies every
term. LETTERS ONLY, no digits anywhere, so the figure is collision-proof against every problem.
Lowercase labels only, no sentence inside the SVG, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, Euclid's fifth postulate with Lobachevsky and Bolyai, Thomas
Harriot, Pierre Bouguer, Joseph Fourier, Leonid Kantorovich, and George Dantzig. Use William
Betz: the acronym FOIL, First Outer Inner Last, first appeared in his 1929 textbook Algebra for
Today, so the label is younger than the method by centuries, and the method needs no acronym,
it is the distributive property used twice. About 200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries
no digits, (c) every answer in the lesson is distinct from every other, (d) every numeric answer
is exact, (e) the continuity example 3, 4, 7, 12 from the 8.5 closer appears ONLY in the opener
prose, never in a problem.
`

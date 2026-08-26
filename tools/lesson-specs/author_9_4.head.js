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

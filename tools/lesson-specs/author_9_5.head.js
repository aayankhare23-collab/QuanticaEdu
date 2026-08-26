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

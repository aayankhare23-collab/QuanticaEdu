export const meta = {
  name: 'author-lesson-8-4',
  description: 'Author Algebra I 8.4 Graphing Inequalities',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '8.4'
const TITLE = 'Graphing Inequalities'
const NEXT = '8.5'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_two', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_side', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_system', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Fourth lesson of chapter 8, Inequalities.
- 8.1 gave the rules, 8.2 used them to compare two numbers, 8.3 solved a linear inequality in one
  variable and described the answer as something like \\(x>4\\), deliberately without drawing it.
  8.3 closes by handing off to this lesson, which draws it. The opener picks that up in one or two
  plain sentences. Do NOT write "Last lesson we" or "Imagine".
- CHAPTER 7 gave the plane, the graph of an equation as the set of points satisfying it, the fact
  that \\(ax+by=c\\) graphs as a straight line, the intercepts, slope, and horizontal and vertical
  lines. Every one of those is USED here and none is re-derived. In particular 7.2's idea, that a
  graph is exactly the points that make the statement true, carries over word for word from
  equations to inequalities, and that is the hinge of this lesson.

TOPIC CHECKLIST (cover ALL):
 1. ON A NUMBER LINE. The solutions of \\(x>4\\) are a ray. An OPEN circle marks a boundary that is
    excluded and a FILLED circle one that is included, so \\(>\\) and \\(\\ge\\) draw differently at
    exactly one point. Students reverse this, so test it directly.
 2. A CHAIN such as \\(a<x\\le b\\) is a segment, closed at one end and open at the other.
 3. IN THE PLANE. The graph of \\(y>mx+b\\) is a half-plane. Derive it rather than asserting it.
    The line \\(y=mx+b\\) holds the points where the two sides are equal, and directly ABOVE any
    point of that line \\(y\\) is larger while the right side is unchanged, so the whole region
    above the line satisfies it and the whole region below fails it.
 4. DASHED OR SOLID. A strict inequality draws the boundary line dashed because its points are not
    solutions, and \\(\\ge\\) or \\(\\le\\) draws it solid. This is the number line's open and
    filled circle again, one dimension up, and saying so ties the two halves of the lesson together.
 5. WHICH SIDE. TESTING ONE POINT settles the whole half-plane. The origin is the easiest test
    point whenever the boundary does not pass through it. Include a problem where the boundary DOES
    pass through the origin so another test point is forced.
 6. INEQUALITIES NOT SOLVED FOR \\(y\\), such as \\(ax+by\\le c\\). Either solve for \\(y\\) first,
    remembering 8.1's flip when \\(b\\) is negative, or test a point. Both routes must appear.
 7. VERTICAL AND HORIZONTAL BOUNDARIES, \\(x\\ge k\\) and \\(y<k\\) in the plane, which are
    half-planes left or right and below or above.
 8. TWO OR MORE INEQUALITIES AT ONCE. The points satisfying all of them are the OVERLAP of the
    half-planes, and the corners of that region are where two boundary lines cross, which chapter 5
    and 7.6 already know how to find.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO maximum or minimum of an expression over a region, and NO optimization. 8.5 owns that and it
  is the very next lesson. The region may be described and its corners found, but nothing is
  maximized over it.
- Do NOT re-derive 8.1's rules, 8.3's isolation procedure, or any of chapter 7. All are used.
- Nothing quadratic, no absolute value.

ANSWER SHAPE. Every answer is a SINGLE typed value, so NEVER ask for a graph, a region, or an
inequality. Good asks are the boundary value, whether a stated point is in the region as a one-word
answer among yes and no, a COUNT of how many of several listed points satisfy it, the number of
LATTICE POINTS with integer coordinates inside a small bounded region, one coordinate of a corner
where two boundaries cross, or the word dashed or solid for how a boundary is drawn. Every numeric
answer is an integer or a lowest-terms fraction.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob a ray on the number line, boundary asked for
  3 [P2] prob open against filled, the word asked for
  4 [imp1] imp the number line picture, open excluded and filled included
  5 [P3] prob a chain as a segment      6 [P4] prob is a stated point a solution, yes or no
  7 [imp2] imp a graph is the points that make the statement true, carried from 7.2
  8 [FIG] fig a boundary line with one side shaded, plus the number line case beneath it
  9 [p_two] p moving up into the plane
  10 [P5] prob which side, tested from the origin      11 [P6] prob dashed or solid, the word asked for
  12 [imp3] imp the half-plane, derived by moving up from a point of the boundary
  13 [p_side] p testing one point settles everything
  14 [P7] prob a boundary through the origin, forcing another test point
  15 [fact] fact Leonid Kantorovich, see below
  16 [P8] prob an inequality not solved for y, with a negative coefficient
  17 [imp4] imp solving for y with the flip, or testing a point instead
  18 [p_system] p more than one at once
  19 [P9] prob a vertical or horizontal boundary      20 [P10] prob count listed points in an overlap
  21 [imp5] imp the overlap of half-planes, and corners where boundaries cross
  22 [p_close] p putting it together
  23 [P11] prob a lattice-point count in a small bounded region
  24 [P12] prob the hardest closer
  25 [closer] p hands off to 8.5 Optimization

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): two bands. The top band is a set of axes with ONE straight boundary line drawn
DASHED and the region on one side of it filled with a light blue wash, and a small open dot on the
line to say its points are excluded. The bottom band is a single number line carrying the same idea
in one dimension, one open circle with a ray shaded to its right, and beside it a filled circle with
a ray shaded to its left, so the two conventions sit next to each other. Label with lowercase words
only. Keep digits out of the figure entirely, using letters for the boundary, which makes it
collision-proof against every problem. All prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, Euclid's fifth postulate with Lobachevsky and Bolyai, Thomas
Harriot, Pierre Bouguer, and Joseph Fourier. Use Leonid Kantorovich, who in 1939 was asked how to
cut plywood with the least waste and turned it into a question about the region of plans allowed by
a list of inequalities. About 200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries no
digits, (c) answers repeat only where the ask is a word such as yes, no, dashed or solid, and where
they do the problems must differ completely in their numbers, (d) every numeric answer is exact.
`

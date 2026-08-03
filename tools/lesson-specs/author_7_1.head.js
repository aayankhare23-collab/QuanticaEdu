export const meta = {
  name: 'author-lesson-7-1',
  description: 'Author Algebra I 7.1 The Cartesian Plane',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '7.1'
const TITLE = 'The Cartesian Plane'
const NEXT = '7.2'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_quad', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_dist', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_mid', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. This OPENS chapter 7, Graphing Lines, of Algebra I.
- 6.6's closing sentence, which this opener must pick up, is exactly: "Every relationship in this
  lesson had one constant and several quantities that change, and the work was always to gather
  the changing ones on one side of the bar and read the constant off the other. Distance, work
  rate and closing rate all have that shape. That closes chapter 6. Chapter 7, Graphing Lines,
  opens with 7.1, The Cartesian Plane."
  Open from that in one or two plain sentences. Do NOT write "Last lesson we" or "Imagine".
- PREALGEBRA 10.7 covered reading tables and graphs informally, and prealgebra chapter 11 covered
  segments and the Pythagorean theorem, so the Pythagorean theorem may be USED and named but must
  not be re-derived.
- 5.1 promised that a system's solution counts would get a picture in chapter 7. That promise is
  kept in 7.6, NOT here. Do not preview it.

TOPIC CHECKLIST (cover ALL):
 1. An ordered pair names a point. Two number lines at right angles, the horizontal one the
    \\(x\\)-axis and the vertical one the \\(y\\)-axis, meeting at the origin. \\((a,b)\\) means
    go \\(a\\) along and \\(b\\) up, and the ORDER MATTERS, so \\((3,7)\\) and \\((7,3)\\) are
    different points. Include a problem that turns on the order.
 2. Negative coordinates, and reading a point's coordinates off a described position.
 3. THE FOUR QUADRANTS, numbered counterclockwise from the upper right, and deciding which
    quadrant a point is in from the SIGNS of its coordinates alone. Include a problem where only
    the signs are known, not the values.
 4. Points ON an axis belong to no quadrant, and a point with \\(x=0\\) is on the \\(y\\)-axis
    while a point with \\(y=0\\) is on the \\(x\\)-axis. Students reliably reverse this, so test
    it directly.
 5. DISTANCE between two points that share a coordinate, which is a subtraction, and then the
    general distance \\(\\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}\\), derived from the Pythagorean theorem
    by dropping a right triangle. Keep every distance answer exact, so choose Pythagorean triples
    or leave the answer as a simplified radical, which chapter 3 already taught.
 6. THE MIDPOINT \\(\\left(\\frac{x_1+x_2}{2},\\frac{y_1+y_2}{2}\\right)\\), derived as the
    average of the coordinates rather than asserted. Include a problem that runs it BACKWARDS,
    giving one endpoint and the midpoint and asking for the other endpoint.
 7. Because an answer must be a SINGLE typed value, never ask for a point. Ask for one coordinate,
    a distance, a quadrant number, or a count.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO graphing of equations, no plotting a line from an equation, no tables of values feeding a
  line. 7.2 owns all of that, and it is the very next lesson.
- NO slope, no steepness, no rise over run. 7.3 owns slope.
- NO equation of a line in any form, no y=mx+b, no Ax+By=C. 7.4 and 7.5 own those.
- NO parallel or perpendicular lines. 7.6 owns them.
- NO systems of equations and NO pictures of intersecting lines. 7.6 owns that too.
- NO inequalities (chapter 8), nothing quadratic (chapter 9).

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob read a coordinate from a described position
  3 [P2] prob a problem that turns on the ORDER of the pair
  4 [imp1] imp axes, origin, ordered pair, order matters
  5 [P3] prob negative coordinates      6 [P4] prob a point on an axis
  7 [imp2] imp points on an axis belong to no quadrant
  8 [FIG] fig the plane with the four quadrants numbered and one point placed
  9 [p_quad] p the quadrants
  10 [P5] prob quadrant from signs alone      11 [P6] prob quadrant of a point built from another
  12 [imp3] imp the four quadrants and their sign patterns
  13 [p_dist] p distance between two points
  14 [P7] prob distance along a shared coordinate
  15 [fact] fact Descartes is BANNED, see below
  16 [P8] prob the general distance, exact answer
  17 [imp4] imp the distance formula from the Pythagorean theorem
  18 [p_mid] p the midpoint
  19 [P9] prob a midpoint coordinate      20 [P10] prob midpoint run backwards
  21 [imp5] imp the midpoint as an average of coordinates
  22 [p_close] p putting the three together
  23 [P11] prob distance and midpoint combined      24 [P12] prob the hardest closer
  25 [closer] p hands off to 7.2 Graphing Linear Equations

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): the plane itself. One clean set of axes with arrowheads, the origin marked,
the four quadrants labelled with the WORDS one, two, three and four in lowercase (never Roman
numerals in all caps, which the all-caps ban forbids), and ONE point plotted with its coordinates
shown. Ticks unlabelled or labelled sparsely. Use a point that appears in NO problem. Lowercase
band labels, all prose in cap. This is the one figure in the lesson, so make it the reference
picture of the plane.

HISTORICAL FACT (slot fact): DESCARTES IS ALREADY SPENT in this course (Algebra I 1.5 uses him
for exponent notation) and is BANNED here despite the lesson's name. Also banned: Cardano,
Servois, Hamilton, Viete, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde,
al-Khwarizmi, Fibonacci, Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine
Chapters, Simon Stevin, Alcuin of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the
Roman centesima rerum venalium, the origin of the percent sign, Boyle, and Kepler. Use Pierre de
Fermat, who worked out coordinate geometry independently and slightly earlier than Descartes, in
a manuscript circulated among mathematicians in 1636 but not printed until after his death, so
the idea arrived twice. About 200 characters, and do not name Descartes even in passing.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure's point
appears in no problem, (c) every answer in the lesson is distinct from every other, (d) every
distance answer is EXACT, either a whole number from a Pythagorean triple or a simplified
radical, never a rounded decimal.
`

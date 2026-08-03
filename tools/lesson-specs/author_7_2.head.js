export const meta = {
  name: 'author-lesson-7-2',
  description: 'Author Algebra I 7.2 Graphing Linear Equations',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '7.2'
const TITLE = 'Graphing Linear Equations'
const NEXT = '7.3'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_line', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_int', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_special', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Second lesson of chapter 7, Graphing Lines.
- 7.1 established the plane: axes, the origin, ordered pairs with the order mattering, the four
  quadrants and their sign patterns, points on an axis belonging to no quadrant, distance between
  two points, and the midpoint. 7.1 closes by handing off to this lesson. The opener picks that up
  in one or two plain sentences. Do NOT write "Last lesson we" or "Imagine".
- 5.1 established that a two-variable equation has ENDLESSLY many solution pairs, one for each
  chosen \\(x\\). That is the fact this lesson turns into a picture, and it should be named as
  the reason a graph is worth drawing. Do NOT re-derive it.

TOPIC CHECKLIST (cover ALL):
 1. THE GRAPH OF AN EQUATION is the set of all points whose coordinates satisfy it. A point is ON
    the graph exactly when substituting its coordinates makes the equation true, which is 5.1's
    check. Include problems that TEST a point rather than plot one, since testing funnels to a
    single typed value cleanly.
 2. Plotting from a table. Choose values of \\(x\\), compute \\(y\\), get pairs, and the pairs all
    fall on one straight line. State plainly that the graph of \\(ax+by=c\\) with \\(a\\) and
    \\(b\\) not both zero is a straight line, which is why two points determine it.
 3. Because two points determine a line, plotting a third is a CHECK. Include a problem where a
    stated third point does not fall on the line, and the reader must find which one is wrong.
 4. THE INTERCEPTS. Setting \\(y=0\\) gives the \\(x\\)-intercept and setting \\(x=0\\) gives the
    \\(y\\)-intercept. Students reverse this constantly, so derive it from 7.1's fact that a point
    on the \\(x\\)-axis has \\(y=0\\). Include a problem where the reversed reading gives a
    specific wrong number, and name that number.
 5. Intercepts are the fastest two points to plot for \\(ax+by=c\\).
 6. HORIZONTAL AND VERTICAL LINES. \\(y=c\\) is horizontal and \\(x=c\\) is vertical, and students
    reverse these too. Derive each from what the equation says about every point on it. Note that
    \\(x=c\\) has no \\(y\\)-intercept unless \\(c=0\\).
 7. Reading a required coordinate off a line, given the equation and one coordinate of a point on
    it, which is 5.1's substitute-and-solve.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO slope, no steepness, no rise over run, no comparing how steep two lines are, and NO use of
  the letter \\(m\\) for a coefficient. 7.3 owns slope entirely and it is the very next lesson.
- NO \\(y=mx+b\\) as a named form. 7.5 owns it. Equations solved for \\(y\\) are fine as long as
  the form is not named and no coefficient is called a slope.
- NO finding the equation of a line from two points. 7.4 owns it.
- NO parallel or perpendicular lines, NO systems, NO intersecting-line pictures. 7.6 owns those.
- NO inequalities (chapter 8), nothing quadratic (chapter 9).
- Do NOT re-teach the plane, quadrants, distance or midpoint. 7.1 owns them.

ANSWER SHAPE. Every answer is a SINGLE typed value, so never ask for a point or for a sketch.
Ask for one coordinate, a count of points, which of several labelled points lies on the line, or
a value of a constant.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob test whether a point is on a graph
  3 [P2] prob find the missing coordinate of a point on a graph
  4 [imp1] imp the graph is the set of points that satisfy the equation
  5 [P3] prob build a table and identify a pair      6 [P4] prob which of several points is not on the line
  7 [imp2] imp the graph of ax+by=c is a straight line, so two points fix it
  8 [FIG] fig one line drawn on axes with a few of its points marked
  9 [p_line] p two points determine a line, a third is a check
  10 [P5] prob find a constant so a given point lies on the line
  11 [P6] prob a point stated to be on the line that is not
  12 [imp3] imp plotting from a table, and the third point as a check
  13 [p_int] p the intercepts
  14 [P7] prob the x-intercept, with the reversed reading's number named
  15 [fact] fact a fresh graphing-history fact
  16 [P8] prob the y-intercept
  17 [imp4] imp setting y=0 and x=0, derived from 7.1
  18 [p_special] p horizontal and vertical lines
  19 [P9] prob a horizontal line      20 [P10] prob a vertical line
  21 [imp5] imp y=c is horizontal, x=c is vertical, and why
  22 [p_close] p putting it together
  23 [P11] prob intercepts of a line in a less friendly form
  24 [P12] prob the hardest closer
  25 [closer] p hands off to 7.3 Slope

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): one straight line drawn on a clean set of axes, with three of its points
marked as small dots and their coordinates labelled, so the picture says the line is exactly the
points that satisfy the equation. Show the equation once as a label. Use an equation and points
that appear in NO problem in this lesson. Axes with arrowheads, origin marked, sparse ticks.
Lowercase band labels, never all-caps, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, and Fermat. Use William Playfair, who in 1786
published the first line graphs of economic data in his Commercial and Political Atlas, putting
time along the bottom and money up the side so a trend could be seen rather than read off a
table. About 200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure's
equation and points appear in no problem, (c) every answer in the lesson is distinct from every
other, (d) keep every intercept and coordinate exact, using integers or lowest-terms fractions,
never a rounded decimal.
`

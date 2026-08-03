export const meta = {
  name: 'author-lesson-7-3',
  description: 'Author Algebra I 7.3 Slope',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '7.3'
const TITLE = 'Slope'
const NEXT = '7.4'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_sign', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_special', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_use', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Third lesson of chapter 7, Graphing Lines.
- 7.1 established the plane, ordered pairs, the four quadrants, distance between two points and
  the midpoint. 7.2 established that the graph of an equation is the set of points satisfying it,
  that the graph of \\(ax+by=c\\) is a straight line so two points fix it, the two intercepts, and
  horizontal and vertical lines. 7.2 closes by handing off to this lesson, which is where the
  measure of steepness finally gets a name. The opener picks that up in one or two plain
  sentences. Do NOT write "Last lesson we" or "Imagine".
- Chapter 6 taught direct proportion, constant rates and \\(d=rt\\). Slope is the same constant
  ratio idea read off a graph, and saying so once is worth it. Do NOT re-derive proportion.
- This lesson INTRODUCES the letter \\(m\\) for slope. 7.2 was forbidden from using it.

TOPIC CHECKLIST (cover ALL):
 1. SLOPE DEFINED. For two points on a line, \\(m=\\frac{y_2-y_1}{x_2-x_1}\\), the change in
    \\(y\\) divided by the change in \\(x\\). Name it slope in the sentence where it first appears.
 2. The ratio is THE SAME for every pair of points on one line. Derive this rather than assert it,
    using similar right triangles drawn under the line, or by taking two different pairs on one
    line and getting the same ratio twice. Reaching it twice by independent routes is the bar.
 3. CONSISTENT ORDER. Either point may be first, but the same point must lead in both the
    numerator and the denominator. Subtracting in opposite orders flips the sign. Include a
    problem where the reversed order produces a specific wrong number, and name that number.
 4. THE SIGN OF THE SLOPE. Positive means the line rises from left to right, negative means it
    falls, and zero means it is horizontal. Include a problem where only the sign can be decided.
 5. A VERTICAL LINE HAS NO SLOPE. The denominator is \\(0\\), and division by zero is undefined,
    so the slope is undefined and is NOT zero. Students reliably swap the horizontal and vertical
    cases, so test both directly. Answers here are the words undefined and zero.
 6. SLOPE AS STEEPNESS. The larger \\(|m|\\) is, the steeper the line. Compare two lines by
    comparing the absolute values of their slopes, including one positive against one negative.
 7. COLLINEARITY. Three points lie on one line exactly when the slope from the first to the second
    equals the slope from the second to the third. Include a problem that solves for an unknown
    coordinate making three points collinear.
 8. SLOPE AS A RATE OF CHANGE in context, where the units of the slope are the units of \\(y\\)
    per one unit of \\(x\\). One problem should ask for that rate from two stated readings.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO deriving the equation of a line from a point and a slope, and NO point-slope form. 7.4 owns
  it and it is the very next lesson.
- NO naming \\(y=mx+b\\) as slope-intercept form and NO naming \\(Ax+By=C\\) as standard form, and
  do NOT state the rule that the slope of \\(Ax+By=C\\) is \\(-A/B\\). 7.5 owns all of that. A line
  already written as \\(y=\\) something may be used, but do not name the form and do not teach
  reading the slope off the coefficient as a rule.
- NO parallel or perpendicular lines, NO comparing two lines for intersection, NO systems. 7.6.
- Do NOT re-teach the plane, quadrants, distance, the midpoint or the intercepts.
- NO inequalities (chapter 8), nothing quadratic (chapter 9).

ANSWER SHAPE. Every answer is a SINGLE typed value. A slope is an integer or a lowest-terms
fraction. Where the answer is that a slope does not exist, the typed answer is the word
undefined, and accept must carry "undefined", "none", "no slope" and "does not exist". Never ask
for a point, a pair, or a sketch. Ask for a slope, one coordinate, a count, or a word.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob slope from two given points, an easy whole number
  3 [P2] prob the same line, a DIFFERENT pair of points, same slope
  4 [imp1] imp slope defined, and the same for every pair of points on the line
  5 [P3] prob a negative slope      6 [P4] prob the reversed-order trap, with the wrong number named
  7 [imp2] imp consistent order, and what flipping it does
  8 [FIG] fig one line with a rise and a run drawn as a right triangle in two places on it
  9 [p_sign] p what the sign tells you
  10 [P5] prob decide the sign from a description alone      11 [P6] prob a slope that is a fraction
  12 [imp3] imp positive, negative and zero slopes, and steepness by \\(|m|\\)
  13 [p_special] p the horizontal and the vertical case
  14 [P7] prob a horizontal line, answer zero
  15 [fact] fact Gaspard Monge, see below
  16 [P8] prob a vertical line, answer the word undefined
  17 [imp4] imp a vertical line has no slope, and why that is not zero
  18 [p_use] p slope in problems
  19 [P9] prob slope as a rate of change in context      20 [P10] prob compare two lines by steepness
  21 [imp5] imp collinearity, three points and two equal slopes
  22 [p_close] p putting it together
  23 [P11] prob solve for a coordinate making three points collinear
  24 [P12] prob the hardest closer
  25 [closer] p hands off to 7.4 Finding the Equation of a Line

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): one straight line on a clean set of axes, with a right triangle drawn under it
between two marked points showing the run along the bottom and the rise up the side, and a SECOND
smaller right triangle drawn the same way further along the same line, so the picture says the
ratio does not depend on which pair you pick. Label the two legs with the words rise and run in
lowercase. Use a line and points that appear in NO problem. Axes with arrowheads, origin marked,
sparse ticks, lowercase labels only, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, and William Playfair. Use Gaspard Monge,
who around 1795 set out descriptive geometry, a method of pinning a three-dimensional object down
by its projections onto two perpendicular planes. France treated it as a military secret for years
before it was taught openly at the Ecole Polytechnique. About 200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure's line
and points appear in no problem, (c) every answer in the lesson is distinct from every other,
(d) every slope is exact, an integer or a lowest-terms fraction, never a rounded decimal.
`

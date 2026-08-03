export const meta = {
  name: 'author-lesson-7-4',
  description: 'Author Algebra I 7.4 Finding the Equation of a Line',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '7.4'
const TITLE = 'Finding the Equation of a Line'
const NEXT = '7.5'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_two', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_either', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_special', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Fourth lesson of chapter 7, Graphing Lines.
- 7.1 gave the plane, distance and the midpoint. 7.2 gave the graph of an equation, the fact that
  \\(ax+by=c\\) graphs as a straight line so two points fix it, the intercepts, and horizontal and
  vertical lines. 7.3 gave slope, \\(m=\\frac{y_2-y_1}{x_2-x_1}\\), the same for every pair of
  points on the line, its sign, steepness by \\(|m|\\), a horizontal line having slope \\(0\\) and a
  vertical line having no slope at all, and collinearity by equal slopes. 7.3 closes by handing off
  to this lesson. The opener picks that up in one or two plain sentences. Do NOT write "Last lesson
  we" or "Imagine".
- 7.2 already said two points determine a line. This lesson turns that from a fact into a method.

TOPIC CHECKLIST (cover ALL):
 1. FROM A POINT AND A SLOPE. Take a known point \\((x_1,y_1)\\) and a general point \\((x,y)\\) on
    the same line. The slope between them is \\(m\\), so \\(\\frac{y-y_1}{x-x_1}=m\\), and
    multiplying through gives \\(y-y_1=m(x-x_1)\\). DERIVE it exactly that way from 7.3's
    definition. Name it POINT-SLOPE FORM in the sentence where it first appears.
 2. Using it. Substituting the point and the slope gives an equation, and expanding gives the line
    solved for \\(y\\).
 3. FROM TWO POINTS. Compute the slope first, then use point-slope with either point.
 4. EITHER POINT GIVES THE SAME LINE. Do this concretely, once, with both points on one example,
    and show the two results agree. Do not assert it.
 5. Reading a value off the line once you have it. Given two data points, find the equation, then
    predict \\(y\\) at a third \\(x\\) or find the \\(x\\) that gives a stated \\(y\\).
 6. THE VERTICAL CASE. Two points with the same \\(x\\)-coordinate have no slope, so point-slope
    does not apply, and the line is \\(x=k\\). Test it directly, because students try to force the
    formula. Include a problem whose answer is that constant.
 7. A LINEAR RELATIONSHIP IN CONTEXT. Two readings of a quantity that changes at a constant rate
    determine the whole relationship, including its value at a moment not measured.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- Do NOT name \\(y=mx+b\\) as slope-intercept form, do NOT name \\(Ax+By=C\\) as standard form, do
  NOT teach converting between named forms, and do NOT state the rule that the slope of
  \\(Ax+By=C\\) is \\(-A/B\\). 7.5 owns every one of those and it is the very next lesson. Writing a
  line solved for \\(y\\) is fine as an ordinary result, but never as a named form.
- Do NOT teach the intercepts as a topic. 7.2 introduced them and 7.5 owns them properly. An
  intercept may be a step inside a problem, never the lesson's subject.
- NO parallel or perpendicular lines, NO comparing two lines, NO systems. 7.6 owns those.
- Do NOT re-derive slope. 7.3 owns it. Do not re-teach the plane, distance or the midpoint.
- NO inequalities (chapter 8), nothing quadratic (chapter 9).

ANSWER SHAPE. Every answer is a SINGLE typed value, so NEVER ask for an equation. Ask for the
coefficient of \\(x\\) once the line is solved for \\(y\\), the constant term, the value of
\\(y\\) at a stated \\(x\\), the \\(x\\) giving a stated \\(y\\), a missing coordinate, or a
constant that makes a stated point lie on the line. Every such value is an integer or a
lowest-terms fraction, never a rounded decimal.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob a point and a slope, find y at a stated x
  3 [P2] prob a point and a slope, find the constant term when solved for y
  4 [imp1] imp point-slope form, derived from the slope definition
  5 [P3] prob a negative slope through a point      6 [P4] prob a fractional slope through a point
  7 [imp2] imp using point-slope, and what expanding it gives
  8 [FIG] fig one known point, a slope triangle from it, and the whole line drawn through
  9 [p_two] p from two points
  10 [P5] prob two points, find a value on the line      11 [P6] prob two points, find a coordinate
  12 [imp3] imp two points, slope first then point-slope
  13 [p_either] p either point works
  14 [P7] prob worked with the second point, matching the first
  15 [fact] fact Johann Heinrich Lambert, see below
  16 [P8] prob a line through two points, predict at a third x
  17 [imp4] imp both points give the same line, and why
  18 [p_special] p when the two points share an x-coordinate
  19 [P9] prob the vertical case      20 [P10] prob a constant making a point lie on a line
  21 [imp5] imp two points with the same x give \\(x=k\\), which has no slope
  22 [p_close] p putting it together
  23 [P11] prob a linear relationship from two readings, in context
  24 [P12] prob the hardest closer
  25 [closer] p hands off to 7.5 Intercepts and Standard Forms

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): one marked point on a clean set of axes with a small slope triangle drawn from
it showing the run and the rise, and the full line drawn through the point in both directions past
the triangle, so the picture says one point plus one slope pins the whole line. Label the point
with its coordinates and label the two legs with the words run and rise in lowercase. Use a point
and a slope that appear in NO problem. Axes with arrowheads, origin marked, sparse ticks, lowercase
labels only, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, and Gaspard Monge. Use
Johann Heinrich Lambert, who in the 1760s drew a straight line through measurements that did not
sit exactly on one, then read values off the line at points he had never measured. About 200
characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure's point
and slope appear in no problem, (c) every answer in the lesson is distinct from every other,
(d) every answer is exact, an integer or a lowest-terms fraction.
`

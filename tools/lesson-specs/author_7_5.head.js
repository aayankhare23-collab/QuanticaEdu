export const meta = {
  name: 'author-lesson-7-5',
  description: 'Author Algebra I 7.5 Intercepts and Standard Forms',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '7.5'
const TITLE = 'Intercepts and Standard Forms'
const NEXT = '7.6'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_std', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_convert', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_fast', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Fifth lesson of chapter 7, Graphing Lines.
- 7.1 gave the plane, distance and the midpoint. 7.2 gave the graph of an equation, the straight
  line of \\(ax+by=c\\), the two intercepts found by setting one variable to \\(0\\), and horizontal
  and vertical lines. 7.3 gave slope and the fact that a vertical line has none. 7.4 gave
  point-slope form and how to build a line from a point and a slope or from two points. 7.4 closes
  by handing off to this lesson. The opener picks that up in one or two plain sentences. Do NOT
  write "Last lesson we" or "Imagine".
- This lesson is where the two standard ways of writing a line finally get their names, and where
  the slope becomes something you read off an equation instead of computing from two points.

TOPIC CHECKLIST (cover ALL):
 1. SLOPE-INTERCEPT FORM \\(y=mx+b\\), NAMED here for the first time. Derive both readings rather
    than asserting them. Setting \\(x=0\\) gives \\(y=b\\), so \\(b\\) is the \\(y\\)-intercept.
    Taking any two points on it, the slope works out to \\(m\\), so \\(m\\) is the slope. Do the
    slope derivation concretely with two points, not by pointing at the letter.
 2. Reading the slope and the \\(y\\)-intercept straight off an equation already in that form,
    including when the coefficient is negative or fractional.
 3. STANDARD FORM \\(Ax+By=C\\), NAMED here. Solving it for \\(y\\) gives
    \\(y=-\\frac{A}{B}x+\\frac{C}{B}\\) when \\(B\\neq 0\\), so THE SLOPE IS \\(-\\frac{A}{B}\\).
    Derive it by doing the division, then state the rule. Include a problem where reading \\(A/B\\)
    without the minus sign gives a specific wrong number, and name that number.
 4. THE INTERCEPTS FROM STANDARD FORM. Setting \\(y=0\\) gives \\(x=\\frac{C}{A}\\) and setting
    \\(x=0\\) gives \\(y=\\frac{C}{B}\\), which is 7.2's rule applied to this form.
 5. CONVERTING BETWEEN THE FORMS both ways, including clearing fractions so \\(A\\), \\(B\\) and
    \\(C\\) come out as integers.
 6. WHEN \\(B=0\\) the equation is \\(Ax=C\\), a vertical line, which has no slope, so the
    \\(-A/B\\) rule does not apply. Test it directly.
 7. Intercepts are the fastest two points to plot for a line in standard form.
 8. USING THE MEANING. In a context where \\(y\\) changes at a constant rate, \\(b\\) is the
    starting amount and \\(m\\) is the rate, and reading them off answers the question with no
    algebra. One problem must turn on that.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO parallel or perpendicular lines, NO comparing two lines, NO systems of equations, NO counting
  a system's solutions. 7.6 owns every one of those and it is the very next lesson.
- Do NOT re-derive slope from two points as the lesson's subject. 7.3 owns that. It may be used.
- Do NOT re-derive point-slope form. 7.4 owns it. It may be used.
- Do NOT re-teach the plane, quadrants, distance or the midpoint.
- NO inequalities (chapter 8), nothing quadratic (chapter 9).

ANSWER SHAPE. Every answer is a SINGLE typed value, so NEVER ask for an equation. Ask for the
slope, the \\(y\\)-intercept, the \\(x\\)-intercept, one of \\(A\\), \\(B\\) or \\(C\\) after a
stated normalization, the value of \\(y\\) at a stated \\(x\\), or a count. Where an answer is that
a slope does not exist, the typed answer is the word undefined and accept must carry "undefined",
"none", "no slope" and "does not exist". Every numeric answer is an integer or a lowest-terms
fraction, never a rounded decimal. When a problem asks for a coefficient of a line in standard
form, PIN IT DOWN completely, for example by requiring \\(A\\), \\(B\\) and \\(C\\) to be integers
with no common factor above \\(1\\) and \\(A>0\\), or the answer is not unique.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob read the y-intercept off a line already solved for y
  3 [P2] prob read the slope off a line already solved for y, with a fractional coefficient
  4 [imp1] imp slope-intercept form named, both readings derived
  5 [P3] prob a negative coefficient      6 [P4] prob find y at a stated x from that form
  7 [imp2] imp reading a line in that form at sight
  8 [FIG] fig one line with its two intercepts marked on the axes
  9 [p_std] p the other standard way of writing a line
  10 [P5] prob the x-intercept of a line in standard form
  11 [P6] prob the slope of a line in standard form, with the missing-minus number named
  12 [imp3] imp standard form named, and the slope \\(-A/B\\) derived by solving for y
  13 [p_convert] p moving between the two forms
  14 [P7] prob convert to standard form and report a pinned-down coefficient
  15 [fact] fact Edmond Halley, see below
  16 [P8] prob convert the other way and report the slope
  17 [imp4] imp converting both ways, and clearing fractions to integer coefficients
  18 [p_fast] p intercepts as the two quickest points
  19 [P9] prob the case \\(B=0\\), answer the word undefined
  20 [P10] prob both intercepts of one line, asking for one stated value
  21 [imp5] imp when \\(B=0\\) the line is vertical and the \\(-A/B\\) rule does not apply
  22 [p_close] p putting it together
  23 [P11] prob a context where the starting amount and the rate are read off
  24 [P12] prob the hardest closer
  25 [closer] p hands off to 7.6 Parallel, Perpendicular, Comparing Lines

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): one straight line on a clean set of axes crossing both axes clearly, with the
\\(x\\)-intercept and the \\(y\\)-intercept each marked as a dot on its axis and labelled with its
coordinate value only, and a short lowercase word naming each one. The picture must say that the
two intercepts are the two easiest points to plot. Use a line whose equation and intercepts appear
in NO problem. Axes with arrowheads, origin marked, sparse ticks, lowercase labels only, all prose
in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, and Johann
Heinrich Lambert. Use Edmond Halley, who in 1701 published a chart of the Atlantic on which curves
joined all the places where a compass needle was off true north by the same amount, the first
printed map to draw lines of equal value. About 200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure's line
and its intercepts appear in no problem, (c) every answer in the lesson is distinct from every
other, (d) every answer is exact.
`

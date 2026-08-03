export const meta = {
  name: 'author-lesson-7-6',
  description: 'Author Algebra I 7.6 Parallel, Perpendicular, Comparing Lines',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '7.6'
const TITLE = 'Parallel, Perpendicular, Comparing Lines'
const NEXT = '8.1'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_counts', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_perp', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_decide', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Sixth and LAST lesson of chapter 7, Graphing Lines. It closes the chapter.
- 7.1 gave the plane, distance and the midpoint. 7.2 gave the graph of an equation and the straight
  line of \\(ax+by=c\\). 7.3 gave slope, its sign, steepness by \\(|m|\\), and the vertical line
  having no slope. 7.4 gave point-slope form. 7.5 named slope-intercept form \\(y=mx+b\\) and
  standard form \\(Ax+By=C\\) with slope \\(-\\frac{A}{B}\\), and the intercepts. 7.5 closes by
  handing off to this lesson. The opener picks that up in one or two plain sentences. Do NOT write
  "Last lesson we" or "Imagine".
- A PROMISE TO KEEP, AND IT IS THE POINT OF THIS LESSON. Chapter 5 taught that a system of two
  linear equations has exactly one solution, no solution, or infinitely many, and 5.1 told the
  reader in as many words that chapter 7 would draw what that looks like. THIS LESSON DELIVERS
  THAT PICTURE. Say so plainly when you get there, and make the three cases the spine of the
  middle of the lesson. Do NOT re-derive the algebra of solving a system, chapter 5 owns it.

TOPIC CHECKLIST (cover ALL):
 1. TWO DISTINCT LINES WITH THE SAME SLOPE NEVER MEET, and are called PARALLEL. Derive it rather
    than assert it. Set the two right-hand sides equal, the \\(mx\\) terms cancel, and what is left
    is \\(b_1=b_2\\), which is false for distinct lines, so there is no \\(x\\) where they meet.
 2. SAME SLOPE AND SAME \\(y\\)-INTERCEPT MEANS THE SAME LINE, not two lines. Every point on one is
    on the other.
 3. DIFFERENT SLOPES MEANS THE LINES CROSS EXACTLY ONCE, because setting the right-hand sides equal
    gives \\((m_1-m_2)x=b_2-b_1\\) with \\(m_1-m_2\\neq 0\\), which has exactly one solution.
 4. THE THREE SOLUTION COUNTS, DRAWN. Exactly one solution is a crossing pair, no solution is a
    parallel pair, infinitely many is one line drawn twice. Tie each case explicitly back to what
    chapter 5 found algebraically. This is the promised picture and it must be unmistakable.
 5. SPOTTING THE CASE FROM THE EQUATIONS in standard form. The coefficients being proportional all
    the way through, \\(A_2/A_1=B_2/B_1=C_2/C_1\\), means the same line, while proportional in
    \\(A\\) and \\(B\\) but not in \\(C\\) means parallel. Include a problem finding the constant
    that makes a system have no solution.
 6. PERPENDICULAR LINES. If two lines are perpendicular and neither is horizontal or vertical, the
    product of their slopes is \\(-1\\), so one slope is \\(-\\frac{1}{m}\\) of the other. DERIVE
    it, do not assert it. Take a right triangle with run \\(a\\) and rise \\(b\\) under one line.
    Turning that triangle a quarter turn sends run \\(a\\) and rise \\(b\\) to run \\(-b\\) and
    rise \\(a\\), so the second slope is \\(-\\frac{a}{b}\\), and the product is \\(-1\\).
 7. THE EXCEPTION. A horizontal line and a vertical line are perpendicular, but one has no slope,
    so the product rule says nothing about that pair. State it and test it.
 8. DECIDING from two given equations whether the lines are parallel, perpendicular, the same line,
    or none of those, including when they are given in different forms.
 9. Finding a constant that makes two lines parallel, or perpendicular, or identical.

SCOPE BOUNDARY:
- Do NOT re-teach substitution or elimination. Chapter 5 owns solving systems. A crossing point may
  be found when a problem needs it, but the lesson is about the geometry, not the method.
- Do NOT re-derive slope, point-slope form, or the named forms. 7.3, 7.4 and 7.5 own them.
- Do NOT re-teach the plane, distance or the midpoint.
- NO inequalities (chapter 8), nothing quadratic (chapter 9). The closer hands off to chapter 8.

ANSWER SHAPE. Every answer is a SINGLE typed value, so never ask for an equation or a pair. Ask for
a slope, a constant, one coordinate of the crossing point, or a COUNT OF SOLUTIONS, which is the
natural single value for the three cases. For infinitely many, ask instead how many of a stated
finite list of points satisfy both equations, since "infinitely many" is not typeable. Where a
one-word answer is right, use parallel, perpendicular, same, or neither, and put every reasonable
spelling in accept.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob two lines with the same slope, how many crossing points
  3 [P2] prob two lines with different slopes, find one coordinate of the crossing
  4 [imp1] imp same slope means parallel or the same line, derived
  5 [P3] prob same slope and same intercept, a count over a listed set of points
  6 [P4] prob find the constant making two lines parallel
  7 [imp2] imp different slopes means exactly one crossing, derived
  8 [FIG] fig THE PROMISED PICTURE, three small panels for the three solution counts
  9 [p_counts] p the three cases, named as chapter 5's three counts
  10 [P5] prob decide the number of solutions from two equations in standard form
  11 [P6] prob find the constant giving no solution
  12 [imp3] imp the three counts, each tied to what chapter 5 found
  13 [p_perp] p lines meeting at a right angle
  14 [P7] prob the slope of a line perpendicular to a given one
  15 [fact] fact Euclid's fifth postulate, see below
  16 [P8] prob find the constant making two lines perpendicular
  17 [imp4] imp the product of slopes is \\(-1\\), derived by turning a slope triangle
  18 [p_decide] p deciding from two equations
  19 [P9] prob parallel, perpendicular or neither, a one-word answer
  20 [P10] prob the horizontal and vertical exception
  21 [imp5] imp the exception, and how to decide from proportional coefficients
  22 [p_close] p putting the chapter together
  23 [P11] prob a constant that could make either case, asking for one of them
  24 [P12] prob the hardest closer
  25 [closer] p closes chapter 7 and hands off to chapter 8, Inequalities, opening with 8.1

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): THE PICTURE CHAPTER 5 WAS PROMISED. Three small panels side by side, each a
clean pair of axes with two lines drawn. The first panel shows two lines crossing at one point,
with the crossing marked. The second shows two parallel lines that never meet. The third shows one
line drawn twice, one stroke over the other, so it reads as a single line. Under each panel a
lowercase label giving the count, "one solution", "no solution", "infinitely many". Do NOT put any
equation or number inside the figure, which keeps it collision-proof against every problem. All
prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, and Edmond Halley. Use Euclid's fifth postulate, the assumption that through a
point off a given line exactly one parallel can be drawn. Mathematicians spent about two thousand
years trying to prove it from the other four before Lobachevsky and Bolyai showed independently in
the 1820s and 1830s that it cannot be proved, since consistent geometries exist without it. About
200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries no
digits at all, (c) every answer in the lesson is distinct from every other, (d) every answer is
exact, an integer, a lowest-terms fraction, or a single word.
`

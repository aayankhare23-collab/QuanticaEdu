export const meta = {
  name: 'author-lesson-6-6',
  description: 'Author Algebra I 6.6 Joint Proportion and Rates',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '6.6'
const TITLE = 'Joint Proportion and Rates'
const NEXT = '7.1'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_rt', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_work', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_two', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. SIXTH AND LAST lesson of chapter 6, Ratios, Percents and Proportion.
- 6.5 taught direct proportion (\\(\\frac{y}{x}\\) constant, \\(y=kx\\)) and inverse proportion
  (\\(xy\\) constant), how to tell them apart, and scaling without finding \\(k\\). 6.5 closes by
  handing off to this lesson. The opener picks that up in one or two plain sentences: one
  quantity can depend on SEVERAL others at once. Do NOT write "Last lesson we" or "Imagine".
- This lesson CLOSES chapter 6, so its final block hands off to chapter 7, Graphing Lines, whose
  first lesson is 7.1 The Cartesian Plane. Do not preview chapter 7's content beyond naming it.
- PREALGEBRA 7.3 taught unit rates and speed, so \\(d=rt\\) may be used directly.

TOPIC CHECKLIST (cover ALL):
 1. JOINT PROPORTION. A quantity proportional to two or more others at once, \\(x=kyz\\), and the
    mixed case where it is proportional to some and inversely proportional to others,
    \\(x=\\frac{kyz}{w}\\). Derive the form by holding one variable fixed at a time.
 2. FINDING \\(k\\) from one complete set of values, then answering about another set. Also the
    faster route, which is to apply each variable's scale factor in turn without ever computing
    \\(k\\), with the solution noting both work.
 3. GROUPING. Put every varying quantity on one side and the constant on the other, so a joint
    relationship becomes "this combination is the same at every set of values". State this as the
    general move, since it is what makes all of these one idea.
 4. \\(d=rt\\) as a joint relationship, distance proportional to rate and to time together.
    At least two problems.
 5. WORK RATE. Someone who finishes a job in \\(n\\) hours does \\(\\frac{1}{n}\\) of it per hour,
    so two workers together do \\(\\frac{1}{a}+\\frac{1}{b}\\) per hour and finish in the
    reciprocal of that. Derive it from the amount of work done rather than asserting it. Two
    problems, one of them asking for the combined time.
 6. TWO OBJECTS MOVING. One problem where two move toward each other and the closing rate is the
    SUM of the speeds, and one where one chases another and the closing rate is the DIFFERENCE.
    Say why the rates add or subtract rather than asserting it.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO percents (6.3, 6.4), NO unit conversion as a topic (6.2), though a single conversion inside
  a rate problem is fine if the problem states the fact it needs.
- NO re-deriving direct or inverse proportion. 6.5 owns them; use them by name.
- NO graphing, no axes, no plotted points, no slope, no straight lines described as graphs.
  Chapter 7 owns graphing and this lesson hands off to it. The word "graph" must not appear.
- NO inequalities (chapter 8), nothing quadratic to solve (chapter 9). A problem whose algebra
  reduces to a quadratic is OUT OF SCOPE, so choose numbers where every solve stays linear.
- NO systems with more than three letters.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob a quantity proportional to two others, one variable changed
  3 [P2] prob both variables changed at once
  4 [imp1] imp joint proportion, x equals k y z
  5 [P3] prob the mixed case, proportional to one and inversely to another
  6 [P4] prob find k from a full set, then use it
  7 [imp2] imp grouping the varying quantities on one side
  8 [FIG] fig the grouped combination staying fixed across two sets of values
  9 [p_rt] p distance as rate times time
  10 [P5] prob a d equals rt problem      11 [P6] prob a harder d equals rt problem
  12 [imp3] imp d equals rt is a joint relationship
  13 [p_work] p work rate, the fraction of a job done per hour
  14 [P7] prob one worker's rate from a stated time
  15 [fact] fact a fresh rates-history fact
  16 [P8] prob two workers together, combined time asked for
  17 [imp4] imp adding rates, not adding times
  18 [p_two] p two objects moving
  19 [P9] prob moving toward each other, rates add
  20 [P10] prob one chasing another, rates subtract
  21 [imp5] imp closing rate as a sum or a difference
  22 [p_close] p what carried through chapter 6
  23 [P11] prob a joint proportion closer      24 [P12] prob the hardest closer
  25 [closer] p closes chapter 6 and hands off to chapter 7, Graphing Lines, starting at 7.1 The Cartesian Plane

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): the grouped combination staying fixed. Two bands. The top band shows one set
of values with the varying quantities gathered on one side of a bar and the constant alone on the
other. The bottom band shows a DIFFERENT set of values with the same combination landing on the
same constant. Use letters only and NO digits at all, which keeps it clear of every problem.
Lowercase band labels, never all-caps, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, and Boyle. Use Kepler's third law, published 1619, that the square
of a planet's orbital period is proportional to the cube of its mean distance from the sun, a
joint statement that held for every planet then known. About 200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries
no digits, (c) every answer in the lesson is distinct from every other, (d) avoid the dollar
SYMBOL entirely, write "dollars" as a word, (e) choose work-rate and motion numbers so every
solve stays linear and every answer is exact, never a rounded decimal.
`

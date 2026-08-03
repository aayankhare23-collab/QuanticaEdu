export const meta = {
  name: 'author-lesson-8-3',
  description: 'Author Algebra I 8.3 Solving Linear Inequalities',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '8.3'
const TITLE = 'Solving Linear Inequalities'
const NEXT = '8.4'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_flip', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_chain', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_special', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Third lesson of chapter 8, Inequalities.
- 8.1 gave the rules, including the one that multiplying or dividing by a negative reverses the
  sign. 8.2 used them to decide which of two numbers is bigger. 8.2 closes by handing off to this
  lesson, where the unknown comes back and the job is to find every value that works. The opener
  picks that up in one or two plain sentences. Do NOT write "Last lesson we" or "Imagine".
- CHAPTER 4 taught solving linear equations by isolating the variable. The procedure here is the
  same procedure with 8.1's one changed rule bolted on, and saying that once is worth it. Do NOT
  re-derive equation solving.

TOPIC CHECKLIST (cover ALL):
 1. WHAT A SOLUTION IS. An equation usually has one solution, a linear inequality usually has
    endlessly many, and solving means describing them all by a single simple inequality such as
    \\(x>4\\). Say that plainly at the start, because it is the real change from chapter 4.
 2. ISOLATE THE VARIABLE the same way as for an equation, adding, subtracting, multiplying and
    dividing on both sides, with the one rule from 8.1 in force.
 3. DIVIDING BY A NEGATIVE COEFFICIENT flips the sign. This is where nearly every mistake happens.
    Include a problem where forgetting to flip yields a specific wrong description, and name it.
 4. THE VARIABLE ON BOTH SIDES. Gather the variable terms on one side. Choosing the side that
    leaves a POSITIVE coefficient avoids the flip entirely, which is a real tactic worth stating.
 5. SIMPLIFY FIRST. Distribute and combine like terms before isolating, and clear fractional
    coefficients by multiplying by a positive common denominator, which does not flip.
 6. CHECKING. Substituting one value from the described solution and one value outside it confirms
    both the boundary and the direction. Make one problem depend on this check.
 7. A COMPOUND INEQUALITY, the chain form \\(a<expression<b\\), solved by doing the same operation
    to all three parts at once.
 8. THE TWO DEGENERATE CASES. The variable terms can cancel and leave a statement that is always
    true, so every number works, or always false, so no number does. These mirror chapter 4's
    infinitely-many and no-solution cases and must be named as that echo.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO number-line pictures of a solution set as a topic, NO open and closed circles, NO shading, and
  nothing in two variables. 8.4 Graphing Inequalities owns all of that and it is the very next
  lesson. Solutions here are described in words and symbols, never drawn.
- NO maximum or minimum and NO optimization. 8.5 owns those.
- Do NOT re-derive 8.1's rules, and do NOT re-run 8.2's which-is-bigger tactics.
- Nothing quadratic, no absolute value.

ANSWER SHAPE. Every answer is a SINGLE typed value, so NEVER ask for an inequality or an interval.
Ask for the BOUNDARY VALUE, the largest or smallest INTEGER that satisfies it, the NUMBER OF
INTEGER solutions in a stated range, the wrong number produced by a missed flip, or a one-word
answer. For the two degenerate cases, ask how many of a stated finite list of values satisfy the
inequality, since "all of them" and "none" then come out as a count. Every numeric answer is an
integer or a lowest-terms fraction, never a rounded decimal. When asking for a boundary, make the
problem say whether the boundary itself counts, or the ask is ambiguous.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob a one-step inequality, boundary asked for
  3 [P2] prob a two-step inequality with a positive coefficient
  4 [imp1] imp what solving an inequality means, and endlessly many solutions
  5 [P3] prob largest integer satisfying one      6 [P4] prob divide by a negative, wrong number named
  7 [imp2] imp the same isolation as an equation, with the one changed rule
  8 [FIG] fig two solved inequalities side by side, one whose step flipped and one whose did not
  9 [p_flip] p keeping the coefficient positive
  10 [P5] prob the variable on both sides      11 [P6] prob gather to the side that avoids a flip
  12 [imp3] imp gathering variable terms, and choosing the side deliberately
  13 [p_chain] p simplifying before isolating
  14 [P7] prob distribute and combine first
  15 [fact] fact Joseph Fourier, see below
  16 [P8] prob clear a fractional coefficient
  17 [imp4] imp simplify first, and clearing denominators by a positive multiplier
  18 [p_special] p when the variable disappears
  19 [P9] prob a chain inequality      20 [P10] prob a degenerate case, asked as a count
  21 [imp5] imp always true and always false, echoing chapter 4's two cases
  22 [p_close] p putting it together
  23 [P11] prob a count of integer solutions in a range      24 [P12] prob the hardest closer
  25 [closer] p hands off to 8.4 Graphing Inequalities

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): two short solution ladders side by side, each three or four lines, one where the
final step divides by a POSITIVE number and the sign stays put, and one where it divides by a
NEGATIVE number and the sign turns over, with the turning sign drawn in gold on the line where it
happens. Use letters and a single small coefficient rather than a full worked example with several
digits, so it cannot pre-solve a problem. Lowercase band labels, no all-caps, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, Euclid's fifth postulate with Lobachevsky and Bolyai, Thomas
Harriot, and Pierre Bouguer. Use Joseph Fourier, who in 1826 published a way to take a whole system
of linear inequalities and eliminate one unknown at a time from it, the same idea as elimination
for equations. About 200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure shares no
numbers with any problem, (c) every answer in the lesson is distinct from every other, (d) every
answer is exact.
`

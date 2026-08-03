export const meta = {
  name: 'author-lesson-8-2',
  description: 'Author Algebra I 8.2 Which Is Bigger',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '8.2'
const TITLE = 'Which Is Bigger'
const NEXT = '8.3'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_third', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_recip', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_back', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. Second lesson of chapter 8, Inequalities.
- 8.1 gave the rules: transitivity, adding a constant, adding two inequalities that point the same
  way, multiplying by a positive, MULTIPLYING OR DIVIDING BY A NEGATIVE REVERSING THE SIGN, the
  caution about a letter of unknown sign, \\(x^2\\ge 0\\), and the reciprocal rule for two numbers
  of the same sign. 8.1 closes by handing off to this lesson. The opener picks that up in one or
  two plain sentences. Do NOT write "Last lesson we" or "Imagine".
- This lesson is the USE of those rules, not more of them. The question is always the same, which
  of two given numbers is bigger, and the work is finding a comparison that settles it without
  computing either number.

TOPIC CHECKLIST (cover ALL):
 1. WHY NOT JUST COMPUTE. Some pairs are chosen so that computing both is slow or impossible by
    hand, and the point of the lesson is a route that avoids it. Say this plainly once, early.
 2. COMPARE BY SUBTRACTING. Whichever of \\(a-b\\) and \\(0\\) is bigger settles it, so the whole
    job can become deciding the sign of one expression.
 3. COMPARE THROUGH A THIRD NUMBER. If \\(a>c\\) and \\(c>b\\) then \\(a>b\\), so a well-chosen
    middle number settles a pair neither of which is easy against the other. Choosing that middle
    number is the skill, and a good choice is usually a round number or a simple fraction between
    them. Include a problem where the reader is handed the pair and must decide via a third.
 4. COMPARE BY A COMMON FORM. Put both into the same shape and only the differing part matters.
    Two fractions with the same numerator compare by their denominators, IN REVERSE. Two powers
    compare by rewriting them with a common base or a common exponent.
 5. COMPARE BY RECIPROCALS. For two numbers of the same sign, the bigger number has the smaller
    reciprocal, so a hard pair can become an easy pair. This is 8.1's rule used as a tactic.
    The same-sign condition must be checked, and one problem must turn on that check.
 6. WORKING BACKWARDS, and the catch. Assuming the answer and simplifying until something obvious
    appears is a good way to FIND which is bigger, but the steps then have to run FORWARDS to be a
    proof, because a reversed step may not be reversible. State that plainly and make one problem
    depend on it.
 7. A comparison that only \\(x^2\\ge 0\\) settles, carried over from 8.1.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- Do NOT re-derive 8.1's rules. They are used here, never re-proved.
- NO solving an inequality for a variable and reporting a solution set. 8.3 owns that.
- NO number-line or shaded-region pictures of a solution set, nothing in two variables. 8.4.
- NO maximum or minimum, no optimization. 8.5.
- Nothing quadratic beyond using \\(x^2\\ge 0\\) as a fact.

ANSWER SHAPE. Every answer is a SINGLE typed value. The natural ask is WHICH of two labelled
quantities is bigger, so label them \\(A\\) and \\(B\\) and have the reader type the letter, with
accept carrying both cases. Where they are equal the answer is the word equal. Other good asks are
a count of how many of several listed comparisons are true, the smallest integer that beats a given
quantity, or the value of a difference. Never ask for an inequality or an explanation.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob a pair settled by subtracting
  3 [P2] prob a pair where computing both is clearly the slow route
  4 [imp1] imp comparing by the sign of the difference
  5 [P3] prob two fractions with the same numerator      6 [P4] prob two powers by a common base
  7 [imp2] imp putting both into a common form, and the same-numerator reversal
  8 [FIG] fig two quantities and a third between them on a number line, letters only
  9 [p_third] p going through a middle number
  10 [P5] prob choose a middle number and decide      11 [P6] prob a pair needing a fraction between
  12 [imp3] imp comparing through a third number, and how to pick it
  13 [p_recip] p flipping to an easier pair
  14 [P7] prob a pair settled by reciprocals
  15 [fact] fact Pierre Bouguer, see below
  16 [P8] prob reciprocals where the same-sign check is what decides it
  17 [imp4] imp the reciprocal tactic and the condition it needs
  18 [p_back] p working backwards, and running it forwards
  19 [P9] prob found by working backwards      20 [P10] prob a comparison only \\(x^2\\ge 0\\) settles
  21 [imp5] imp working backwards finds the answer, running forwards proves it
  22 [p_close] p putting it together
  23 [P11] prob a pair with two viable routes      24 [P12] prob the hardest closer
  25 [closer] p hands off to 8.3 Solving Linear Inequalities

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): a single horizontal number line carrying three marked points labelled with
LETTERS only, one quantity well to the left, one well to the right, and a third sitting between
them, with a short bracket under each of the two gaps. The picture must say that knowing each gap
separately settles the outer pair. NO DIGITS ANYWHERE in the figure, which makes it collision-proof
against every problem. Lowercase labels, all prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, Euclid's fifth postulate with Lobachevsky and Bolyai, and Thomas
Harriot. Use Pierre Bouguer, who in 1734 wrote the first signs for "less than or equal to" and
"greater than or equal to", a century after the plain \\(<\\) and \\(>\\) were in print. About 200
characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries no
digits, (c) every answer in the lesson is distinct from every other where it can be, and where
several answers are the letter A or B the PROBLEMS must differ completely in their numbers,
(d) every numeric answer is exact.
`

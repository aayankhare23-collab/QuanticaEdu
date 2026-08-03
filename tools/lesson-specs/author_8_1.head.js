export const meta = {
  name: 'author-lesson-8-1',
  description: 'Author Algebra I 8.1 The Basics of Inequality',
  phases: [
    { title: 'Blueprint', detail: '3 independent designs, 1 judge merge' },
    { title: 'Author', detail: 'prose, problems, figure, review, in slots' },
    { title: 'Verify', detail: 'adversarial per-problem verification' },
    { title: 'Audit', detail: 'blocks audit + review audit' },
  ],
}

const COURSE_TITLE = 'Algebra I'
const KEY = '8.1'
const TITLE = 'The Basics of Inequality'
const NEXT = '8.2'
const REVIEW_N = 17

const OUTLINE = [
  ['op', 'p'], ['P1', 'prob'], ['P2', 'prob'], ['imp1', 'imp'], ['P3', 'prob'], ['P4', 'prob'],
  ['imp2', 'imp'], ['FIG', 'fig'], ['p_neg', 'p'], ['P5', 'prob'], ['P6', 'prob'], ['imp3', 'imp'],
  ['p_combine', 'p'], ['P7', 'prob'], ['fact', 'fact'], ['P8', 'prob'], ['imp4', 'imp'], ['p_square', 'p'],
  ['P9', 'prob'], ['P10', 'prob'], ['imp5', 'imp'], ['p_close', 'p'], ['P11', 'prob'], ['P12', 'prob'],
  ['closer', 'p'],
]

const SPEC = `
CONTEXT AND CONTINUITY. This OPENS chapter 8, Inequalities, of Algebra I.
- Chapter 7 (Graphing Lines) has just closed with 7.6, Parallel, Perpendicular, Comparing Lines,
  whose closer hands off to this lesson. The opener picks that up in one or two plain sentences.
  Do NOT write "Last lesson we" or "Imagine".
- Chapter 4 taught solving linear EQUATIONS by doing the same thing to both sides. This chapter is
  that idea again with one rule changed, and naming that once up front is worth it. Do NOT
  re-derive equation solving.
- PREALGEBRA covered ordering integers and the number line, so \\(<\\) and \\(>\\) may be used and
  read without ceremony. What is new here is what SURVIVES an operation applied to both sides.

TOPIC CHECKLIST (cover ALL):
 1. What an inequality says, and TRANSITIVITY. If \\(a>b\\) and \\(b>c\\) then \\(a>c\\). State it
    and use it, since it is the engine behind comparing through a third quantity later.
 2. ADDING OR SUBTRACTING the same number on both sides leaves the direction alone. Derive it from
    what \\(x>y\\) means, namely that \\(x-y\\) is positive, which adding \\(c\\) to both sides
    does not change.
 3. ADDING TWO INEQUALITIES that point the same way is allowed. If \\(x>y\\) and \\(a>b\\) then
    \\(x+a>y+b\\). SUBTRACTING them is NOT, and one problem must show a concrete case where
    subtracting gives a false statement.
 4. MULTIPLYING OR DIVIDING BY A POSITIVE number leaves the direction alone.
 5. MULTIPLYING OR DIVIDING BY A NEGATIVE NUMBER REVERSES THE SIGN. This is THE rule of the
    chapter. Derive it, do not assert it. Take \\(x>y\\), so \\(x-y\\) is positive; multiplying a
    positive by a negative gives a negative, so \\(-x+y\\) is negative, so \\(-x<-y\\). Then test
    it with a problem where forgetting to flip produces a specific wrong number, and name that
    number.
 6. THE TRAP THAT FOLLOWS. You may only multiply both sides by a letter when you know its sign.
    If the sign is unknown the direction is unknown. State this plainly and test it.
 7. \\(x^2\\ge 0\\) FOR EVERY REAL \\(x\\), with equality exactly when \\(x=0\\). Name it the
    trivial inequality. Derive it from the sign rules rather than asserting it. Use it once to
    settle a comparison that no amount of rearranging settles.
 8. RECIPROCALS. If \\(x>y\\) and both have the SAME sign, then \\(\\frac{1}{x}<\\frac{1}{y}\\).
    The same-sign condition is load-bearing, so include a problem where dropping it breaks.

SCOPE BOUNDARY (each owned by a neighbour, do NOT teach here):
- NO comparing two specific awkward numbers by relating both to a third, and no reciprocal-
  comparison strategy as a method. 8.2 Which Is Bigger owns that. The reciprocal RULE belongs
  here; using it as a comparison tactic belongs there.
- NO solving a linear inequality for a variable and reporting a solution set. 8.3 owns that. This
  lesson is about what each operation does to the sign, not about isolating a letter.
- NO number-line or shaded-region pictures of a solution set, and nothing in two variables. 8.4.
- NO optimization, no maximum or minimum. 8.5.
- Nothing quadratic beyond \\(x^2\\ge 0\\) itself, which is used as a fact and never solved.

ANSWER SHAPE. Every answer is a SINGLE typed value. Good asks are the number that a wrong flip
produces, which of several listed statements must be true given as a COUNT, the smallest or
largest integer satisfying a stated condition, or a one-word answer among greater, less, equal and
unknown. Where the honest answer is that the direction cannot be decided, the typed answer is the
word unknown and accept must carry "unknown", "cannot tell", "neither" and "undetermined". Never
ask for an inequality, an interval, or a set.

MANDATED BLOCK OUTLINE, exactly 25 blocks in exactly this order:
  1 [op] p opener      2 [P1] prob transitivity through a third quantity
  3 [P2] prob add the same number to both sides
  4 [imp1] imp what an inequality says, transitivity, adding a constant
  5 [P3] prob add two inequalities pointing the same way
  6 [P4] prob subtracting two inequalities, showing it fails
  7 [imp2] imp adding two is allowed, subtracting two is not, and why
  8 [FIG] fig a number line showing one multiplication by a negative reflecting the order
  9 [p_neg] p multiplying both sides
  10 [P5] prob multiply by a positive      11 [P6] prob divide by a negative, wrong-flip number named
  12 [imp3] imp multiplying or dividing by a negative reverses the sign, derived
  13 [p_combine] p a letter of unknown sign
  14 [P7] prob a letter whose sign is not known, answer the word unknown
  15 [fact] fact Thomas Harriot, see below
  16 [P8] prob a count of which listed statements must be true
  17 [imp4] imp you may only multiply by a letter whose sign you know
  18 [p_square] p a fact that holds for every real number
  19 [P9] prob use \\(x^2\\ge 0\\)      20 [P10] prob reciprocals with a same-sign condition
  21 [imp5] imp the trivial inequality and the reciprocal rule
  22 [p_close] p putting it together
  23 [P11] prob several rules at once      24 [P12] prob the hardest closer
  25 [closer] p hands off to 8.2 Which Is Bigger

Plus a review array of 17 items [R1] to [R17], easy to hard, standing alone.

FIGURE (slot FIG): a single horizontal number line with two marked points on it, and beneath it a
second number line showing where those same two points land after both are multiplied by a
negative number, with a curved arrow from each point on the top line to its image on the bottom
line so the crossing of the two arrows IS the reversal. Mark the two points with letters, not
digits, which keeps the figure collision-proof against every problem. Lowercase labels only, all
prose in cap.

HISTORICAL FACT (slot fact): already spent and BANNED: Cardano, Servois, Hamilton, Viete,
Descartes, Stifel, Wallis, Oresme, Rudolff, the Pythagoreans, Recorde, al-Khwarizmi, Fibonacci,
Bhaskara II, Diophantus, the Babylonian tablets, the Chinese Nine Chapters, Simon Stevin, Alcuin
of York, Gauss, Eudoxus, the metre and Delambre and Mechain, the Roman centesima rerum venalium,
the origin of the percent sign, Boyle, Kepler, Fermat, William Playfair, Gaspard Monge, Johann
Heinrich Lambert, Edmond Halley, and Euclid's fifth postulate with Lobachevsky and Bolyai. Use
Thomas Harriot, whose \\(<\\) and \\(>\\) signs first appeared in a book published in 1631, ten
years after he died, edited from his papers by other hands. About 200 characters.

NUMBER AND ANSWER FRESHNESS: (a) no two problems share a full number set, (b) the figure carries
no digits, (c) every answer in the lesson is distinct from every other, (d) every answer is exact,
an integer, a lowest-terms fraction, or a single word.
`

# Algebra I — Syllabus (15 chapters, 79 lessons)

Course 2 of the Quantica path. Named **Algebra I** to match school curricula.
Machine-readable source of truth: `lessons/algebra1/toc.json`.

Design rule: the reference sequence (a 22-chapter intro-algebra text) was used as a
**coverage checklist only**. All chapter groupings, titles, lesson names, and (later)
all content, examples, problems, and figures are original. Topic coverage is preserved
nearly completely; 22 chapters condense to 15 by merging natural neighbors.

## The 15 chapters

| # | Chapter | Lessons | Condenses reference chapters |
|---|---------|---------|------------------------------|
| 1 | The Language of Algebra | 5 | 1 (rules/order), 2 (expressions intro) |
| 2 | Working with Expressions | 5 | 2 (manipulation), 4 (multi-variable expressions) |
| 3 | Exponents and Radicals | 5 | 1 (exponents, fractional exponents, radicals), 11.4 (rationalizing) |
| 4 | Linear Equations | 5 | 3 (all), 4.5 |
| 5 | Systems of Equations | 6 | 5 (all) |
| 6 | Ratios, Percents, and Proportion | 6 | 6 + 7 (all) |
| 7 | Graphing Lines | 6 | 8 (all) |
| 8 | Inequalities | 5 | 9 (all) |
| 9 | Quadratics I, Factoring | 5 | 10 (all) |
| 10 | Special Factorizations | 4 | 11 (minus rationalizing, moved to ch. 3) |
| 11 | Quadratics II, Formula and Complex Numbers | 5 | 12 + 13 |
| 12 | Graphing Quadratics | 5 | 14 + 15 |
| 13 | Functions | 6 | 16 + 17 |
| 14 | Polynomials, Exponentials, and Logarithms | 5 | 18 + 19 |
| 15 | Special Functions and Sequences | 6 | 20 + 21 + 22 |

## Coverage notes

- Every section of the reference maps somewhere. The only relocations:
  rationalizing denominators joins Exponents and Radicals (ch. 3); radical
  functions join Radical and Rational Functions (15.3); the "special
  manipulations" material (raising to powers, self-similarity, symmetry)
  becomes Telescoping and Symmetry Tricks (15.6).
- The xy-term factoring technique is covered in 10.4 "Clever Factoring Tricks"
  under our own name.
- Per-chapter "Summary" sections are dropped; Quantica chapters end in
  Practice + Challenge problem sets instead (same system as Prealgebra).
- Chapters 13–15 (logs, sequences, special functions) run past a typical
  school Algebra I into honors/Algebra 2 territory. Kept deliberately: it
  matches the "complete, rigorous" positioning, and the chapters are ordered
  so a school-aligned student can stop after ch. 12 with Algebra I fully met.

## Build order (when authoring begins)

Same pipeline as Prealgebra: `lessons/algebra1/chapter-N.json` as source of
truth, problem-first lessons with try-it problems + review sets, per-chapter
PSETS, figures in the house SVG style, every answer machine-verified before
commit.

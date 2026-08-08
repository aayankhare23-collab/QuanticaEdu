# Landing + product craft brief

Founder brief, 2026-08-05. Goal: stop reading as vibe-coded. Four themes, tighten the
visual system, remove prototype-looking states, make the product feel deeper than the
landing page, and add distinctive brand decisions.

## The eight workstreams

1. **Education-specific layout, not SaaS sections.** Show real lesson interactions, worked
   examples, mastery maps, quizzes, tutor conversations, student progress. Not marketing cards.
2. **A stricter design system.** A small fixed set of spacing values, radii, type sizes,
   button styles, shadows, component rules. Used everywhere, no exceptions.
3. **Less AI-startup language.** Drop broad claims like "personalized learning" and
   "AI-powered tutoring". Say exactly what Milo does, when it intervenes, and what makes the
   pedagogy different.
4. **Hide unfinished features.** A smaller product that looks complete beats a broad roadmap
   exposed in production.
5. **Fix every empty, loading and error state.** "0 of 0 lessons", skeletons, generic toasts,
   inconsistent forms, broken mobile spacing.
6. **Bespoke visual identity.** Custom illustrations, diagrams, iconography, lesson graphics,
   a recognisable academic visual language. Not another gradient.
7. **Course pages are the strongest thing on the site.** Clicking into Prealgebra should feel
   like a purpose-built learning product, not a CMS page with AI bolted on.
8. **Subtle craft.** Keyboard nav, transitions, hover/focus states, URL structure, fast page
   transitions, responsive tables and math, metadata, zero console errors.

## Two things that need a founder decision first

**"Soon" labels are load-bearing right now.** Measured in production 2026-08-05:
38 soon lessons on /courses, 6 "coming soon" in the app TOC, 2 "soon" course tabs. The
/courses page shipped earlier the same day deliberately shows the full 81-lesson Algebra I
syllabus with 38 marked unwritten, on the reasoning that an honest roadmap builds trust.
Workstream 4 says the opposite. Both are defensible and they cannot both be done:

- *Hide* → catalog shows only the 43 written lessons, Algebra I reads complete-as-far-as-it-goes,
  and the chapter count drops from 15 to 8. Looks deliberate, hides the ambition.
- *Keep* → looks like a roadmap, which some buyers like and some read as unfinished.
- *Middle* → show chapter titles for unwritten chapters but not lesson-level "soon" rows,
  so the shape of the course is visible without 38 greyed lines.

**Tutor naming.** The brief says "Sprout". The tutor is **Milo** everywhere, renamed
2026-07-30, and 0 instances of "Sprout" remain in user-facing copy. CSS identifiers and theme
variables still carry the old word, which is internal and drives the per-course palette. No
action needed, noted so the brief is not read as a rename request.

## Sequencing

Ordered by leverage per unit of risk, not by the brief's order.

1. **Design tokens (2).** Everything else compounds off it. Extract the real spacing, radii,
   type sizes and shadows in use today, collapse to a small set, apply. Mechanical and safe.
2. **Empty and error states (5).** Concrete, verifiable, and the most direct "generated" tell.
   Needs an inventory pass first: every state that can render with zero data.
3. **Copy (3).** Cheap and high signal. Needs the founder's voice, so draft and review.
4. **Soon labels (4).** Blocked on the decision above.
5. **Course pages (7) and education-specific landing sections (1).** The largest pieces. Both
   want real product screenshots or live embeds, which means deciding what to show.
6. **Bespoke identity (6).** The manim figure kit at tools/manim_figs.py is already the seed
   of this; extend it to landing diagrams rather than starting over.
7. **Craft pass (8).** Last, because it is polish on whatever the above settles.

## Notes for whoever picks this up

- landing.html is ~450KB and live. Prefer additive, verifiable changes; today several bugs
  came from removing something whose dependents were not checked first.
- The app and marketing page now share a masthead and the Chillax face; keep them in step or
  the seam reopens.
- Console is clean on / and /landing as of 2026-08-05. That is the baseline for workstream 8,
  so any regression is new.

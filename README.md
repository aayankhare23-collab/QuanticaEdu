# Quantica

Problem-first mathematics at [quanticaedu.com](https://quanticaedu.com). Students learn by
solving guided problems with an AI tutor ("Milo") on every problem, AoPS-grade rigor
delivered the way Brilliant delivers it. Free while in early access.

## Working on this project

Start with **[`CLAUDE.md`](CLAUDE.md)** — it is the orientation doc (architecture, golden
rules, common tasks, current status). Then:

- **[`docs/AUTHORING.md`](docs/AUTHORING.md)** — how to author a lesson end to end.
- **[`docs/figure-design-system.md`](docs/figure-design-system.md)** — the figure spec.
- **[`docs/algebra1-syllabus.md`](docs/algebra1-syllabus.md)** — the Algebra I plan.

## Repo layout

- `landing.html` — the entire front end (marketing region + course app SPA), single file, no
  build step.
- `data/lessons.js` — generated lesson content (`window.__COURSEDATA`). Do not hand-edit.
- `lessons/<course>/` — source of truth: `chapter-N.json` + `toc.json`.
- `tools/` — `build_lessons.py`, `finalize_lesson.py`, `gen_seo_pages.py`, the
  `author_lesson.workflow.js` template, and `archive/` (historical one-shot builders).
- `prealgebra/*.html` — generated SEO pages.
- `functions/` — Firebase Cloud Functions backend (Stripe, Firestore). **Never deploy
  functions or touch `functions/.env`.**

## Deploy

```
python3 tools/build_lessons.py          # after any chapter JSON change
git add -A && git commit -m "..." && git push
firebase deploy --only hosting          # hosting ONLY, never functions
```

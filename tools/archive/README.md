# tools/archive

One-shot generators from Quantica's initial build, preserved from the prior session's
scratchpad so the knowledge is not lost. They are **not** part of the routine lesson loop and
several still hardcode that scratchpad path. Read and adapt before reusing.

- `gen_prealgebra.py` — built the `prealgebra.html` course overview page.
- `gen_blog.py` — built `blog.html` and the blog post pages from the founder essay.
- `gen_og.py`, `gen_blog_og.py` — generated the Open Graph share images (`og-*.png`).
- `build_wembi.py` — generated the `.wmb` marketing region now baked into `landing.html`.
- `psets_audit.mjs` — a one-off audit pass over the PSETS problem sets.

For the live pipeline see `../build_lessons.py`, `../finalize_lesson.py`,
`../gen_seo_pages.py`, and `../author_lesson.workflow.js` (documented in `docs/AUTHORING.md`).

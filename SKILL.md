---
name: doc-driven-dev
description: Documentation-driven development on Quarto with sinopia diagrams-as-code. Stand up a single-entry doc library, keep it evergreen (current and planned state only; history rides git), run architecture discussions as gitignored site-themed drafts that reflow into the main docs once settled, and generate theme-aware figures from Python. Use when setting up or restructuring a project's docs site, writing evergreen docs with one auto-discovered entry point, capturing a design discussion as a reviewable draft, deciding what belongs in docs versus git history, or generating diagrams-as-code; or when the user mentions 文档牵引开发 / evergreen 文档 / 建文档站 / 把讨论沉淀进文档.
---

# Documentation-Driven Development

This skill *is* this project: `src/sinopia/` is a diagrams-as-code package, and `docs/` is
a Quarto site that documents its own method with the very workflow and tools it teaches.
The site doubles as the reference and the worked example. The pages carry the skill — read
their `.qmd` source:

- **`docs/workflow.qmd`** — the method: the discuss → draft → review → reflow loop, the
  evergreen discipline (current plus planned state only; history rides git), running a
  discussion as a gitignored draft, the draft shapes, and reflowing once settled.
- **`docs/authoring.qmd`** — the mechanics: Quarto vocabulary (fenced divs, callouts, grid,
  the `compare-option` filter, includes, cross-references, extensions), the page
  conventions, and the evergreen voice rules.
- **`docs/sinopia.qmd`** — diagrams as code: composing a figure as a tree of themed models
  and inlining it so its colors follow the site's light/dark theme.

The figure engine is `src/sinopia/`: a tree of first-class pydantic models — `Box` anchors,
themed shape models, the computed `Route` connector, and stretchable-backed `Row` / `Col` /
`Grid` layout. The project's pixi environment installs it editable; `import sinopia as S`
from a figure cell.

To adopt the workflow in another project, copy the site machinery (`docs/_quarto.yml`,
`docs/_filters/`, `docs/_styles/`, `docs/index.qmd`, `docs/drafts/_template.qmd`), edit
`_quarto.yml`'s title and the `index.qmd` home, then write pages following
`docs/authoring.qmd`. The figure helpers in `docs/figkit.py` are this site's own vocabulary
over the sinopia engine; keep your project's helpers beside its figures, not in sinopia.

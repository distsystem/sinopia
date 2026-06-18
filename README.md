# doc-driven-dev

A documentation workflow where the docs are the working surface, paired with **sinopia**, a
diagrams-as-code package whose figures are generated — not hand-drawn — and follow the page's
light/dark theme. This repository documents itself with these tools: every figure on the docs
site is produced by sinopia at build time, so the docs double as a worked example.

## Two tools

- **The workflow** — a single-entry [Quarto](https://quarto.org) library that holds the *current
  and intended* state. Discussions happen as gitignored drafts that look exactly like the real
  docs and reflow into the evergreen pages once settled; history and rationale ride git, not the
  docs. See [the workflow](docs/workflow.qmd).
- **sinopia** — compose figures in Python as a tree of first-class models (`Box` anchors, themed
  shapes, a computed `Route` connector, declarative `Row` / `Col` / `Grid` layout), then inline the
  SVG so `var(--bs-*)` colors follow the theme. See [sinopia](docs/sinopia.qmd).

## The loop

```
  discuss ──▶ draft ──▶ review ──▶ reflow ──▶ evergreen docs
            drafts/<slug>.qmd      (agreed)    (current state)
            gitignored                │
                                      ▼
                            rationale ──▶ git commit / PR
```

## Run the docs

```bash
cd docs
pixi run preview     # http://localhost:4850, hot reload
pixi run render      # one-shot static build to _site/
```

The docs env carries Quarto plus an editable install of `sinopia`, so figure cells execute and
inline their SVG during the build.

---
name: sinopia
description: Diagrams as code — a figure is a tree of first-class Python models (Box anchors, themed shapes, the computed Route connector, declarative Row/Col/Grid layout) that renders to inline SVG whose colors follow the page's light/dark theme. Use when generating diagrams or figures as code, composing theme-aware SVG, drawing architecture/flow/box-and-arrow diagrams programmatically, or when the user mentions diagrams-as-code / 图表即代码 / sinopia.
---

# sinopia

Diagrams as code: a figure is a tree of first-class pydantic models, each rendering itself
to themed SVG. The engine is the `sinopia` package in `../../../src/sinopia/`. Read
`sinopia.qmd` for the usage guide:

- The two ways to place geometry: hand-placed `Box` rendered through `Figure`, or
  declarative `Row` / `Col` / `Grid` whose coordinates `layout()` computes.
- The named anchors (`box.right`, `node.bottom`, `at(fx, fy)`) that feed the `Route`
  connector, so edges reference geometry instead of literal coordinates.
- Inlining a figure with a `{=html}` raw block so its `var(--bs-*)` colors follow the
  site's light/dark theme; `sinopia.quarto.emit` handles that transport for Quarto.

Closed-set params (`kind` / `shape` / `align`) are typed, so a typo is a construction-time
error rather than a silent mis-render. Colors resolve to `var(--bs-*)` by default; fill
`PALETTE` with hex only for a self-contained `<img>` figure.

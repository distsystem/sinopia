# Evergreen Voice & Structure

How project docs read in a doc-driven workflow. The docs describe the *current
and intended* state; everything historical rides git instead.

## What evergreen means

A reader arriving at any point in time should read the docs as present fact, with
no stale risk. Docs carry **what is true** and **what is planned**. They never
narrate how the design got here.

Change history, decision evolution, and discussion belong to **commit messages and
PR descriptions**, not the docs. When a decision lands, update the docs to the new
state and put the *why* in the commit/PR body. Keep no separate ADR/decision log in
the docs unless the project already maintains one.

## Marking planned content

Docs hold implemented and planned state side by side, so every heading whose behavior is
not yet in the code carries a marker. A reader then tells at a glance what exists from
what is intended, without a separate roadmap.

- **Marker**: append a badge to the heading: `## Cache layer [PLAN]{.badge .text-bg-secondary}`.
  Use `[TODO]` for a small, scoped gap and `[PLAN]` for a designed-but-unbuilt section.
  Nested planned headings each carry their own badge.
- **Body stays present-tense**: describe the planned design as if it exists (`The cache
  stores …`), not as a future promise (`will add a cache`). The badge alone signals "not
  built", so reflow is a one-line edit: delete the badge when the feature lands.
- **Not change-voice**: a `[PLAN]` badge states present intent, it does not narrate
  history, so it stays compatible with the evergreen rule. Remove it in the same change
  that ships the feature.

Granularity: a section inside an otherwise-live page takes a heading badge. A whole
document that is designed but unlanded is a normal page in the main docs carrying a
`[PLAN]` title badge; the badge drops when it ships. Planned work stays in the main docs,
not a separate `docs/proposals/` tree.

## Anti-patterns (the "change-voice")

- **Relative time anchors**: `currently`, `now`, `recently`, `no longer`, `previously`, `used to`.
- **Change verbs**: `added`, `dropped`, `replaced with`, `renamed to`, `reverted`, `removed`.
- **Past-tense reporting**: `we tested`, `verified earlier`, `as measured before`.
- **Comparison to old designs**: `same as the old X`, `formerly called Y`, `like the X we dropped`.

## Write instead

- **State of fact**: `X is Y`, `X does not inherit Z`, `X is implemented via Y`.
- **Design principle**: `does not introduce X`, `has no Y` (present-tense negatives that
  do not imply something once existed).
- **History via links, not prose**: cite an ADR or commit hash from a callout/sidebar;
  keep the body timeless.

## Voice

Declarative and precise. Avoid three habits:

- **Em dashes** as asides or appositives: use a colon, semicolon, period, or recast the sentence.
- **Shorthand**: symbols (`=`, `+`, `→`) and ad-hoc abbreviations stay inside formulas or
  code blocks; in prose write the words.
- **Colloquialisms**: replace chatty filler with plain written statements.

This applies to user-facing docs (README, design docs, API reference, handbook, glossary).
**Exception**: CHANGELOG / release notes / migration guides *are* change history, so the
evergreen rule does not apply to them.

## Problem-driven structure

Docs lead with the reader's problem, not a pitch. Each section first shows what the
ordinary approach does and exactly where it stalls (before), then the project's shape
(after). Do not pass judgment on the ordinary approach before showing it.

A common three-page shape:

- **Thin README home** that doubles as the GitHub front page and is `{{< include >}}`d into `index.qmd`.
- **Paradigm / how-to** page: one section per pain point, each before/after.
- **Mechanism / model** page: the underlying model; diagrams without before/after, since there is no ordinary counterpart.

before/after pairs read well as a `::: {.grid}` of a `.callout-warning` (the ordinary
trap) beside a `.callout-tip` (the project's answer).

## Page-title convention

Main doc pages use a **bare `#` heading** and **no YAML `title:`**. That keeps every page's
h1 the same size (the in-body `section.level1` h1). Adding frontmatter `title:` to one page
switches it to the larger title block and breaks the visual match across pages.

The home `index.qmd` is the exception: it carries frontmatter (`title:`, `description:`,
`toc: false`). Drafts under `drafts/` may also carry `title:`/`subtitle:` since
they are drafts, not part of the uniform page set.

## Authoring vocabulary (reuse, do not hand-roll)

Prefer Bootstrap 5.3 + Quarto-native classes over custom SCSS. Reuse patterns through a
Lua filter, not by re-pasting utility-class strings.

| Use | Syntax |
|---|---|
| 3-way verdict compare | `::: {.compare-option verdict=danger\|warning\|success tag="..." title="..." label="..."}` |
| Callout | `.callout-{note,tip,important,caution,warning}`, optional `collapse=true title="..."` |
| Two columns | `::: {.grid}` + `::: {.g-col-12 .g-col-md-6}` |
| Inline badge | `[text]{.badge .text-bg-{danger,warning,success,secondary}}` (`secondary` for a `[PLAN]`/`[TODO]` heading marker) |
| Definition list | `[term]{.smallcaps}` then a line starting with `: definition` |

Avoid:

- Hardcoded color in the Markdown body: inline `style` color or hex literals break the
  light↔dark toggle. Generated SVG diagrams (SVG-as-code, see below) are the sanctioned raw-HTML exception.
- Long Bootstrap utility-class strings (7+ classes) for alignment: write a Lua filter instead
  (see `_filters/compare-option.lua`).
- `.panel-tabset` for option comparison: it hides unselected tabs, losing the side-by-side view.
- Markdown headings (`####`) inside a `.card`: Pandoc wraps them in `<section>` and breaks the flex layout.

## Diagrams: SVG-as-code

Generate non-trivial diagrams with Python (the `sinopia` package), not by hand-typing SVG
XML. A figure is a tree of first-class models, each rendering itself. Compose positioned
`Box`es with named anchors and let the models *compute* layout: one `Route` connector (shape
codes `line` / `sweep` / orthogonal elbows `-|` `|-` `z` / U-routes `n` `c`, with an optional
floating `label=`), declarative `Row` / `Col` / `Grid` layout (coordinates computed; anchors
read back after `layout`), plus `Rect` / `Text` / `Card` / `Band` / `Markers`. A figure's whole
input is a few dozen calls; drop to a raw `RawPath` for any flourish. The floor equals
hand-written SVG, so it can always at least match it — while the computed control points and
anchors remove the coordinate labor.

The output is SVG and must survive both themes and Pandoc:

- Inline it — a ```` ```{=html} ```` raw block (paste the generated SVG), or a filter that
  inlines a referenced `.svg`. An `<img>`-referenced SVG is isolated from page CSS, so
  `var(--bs-*)` will not resolve there; only an inlined SVG is theme-aware. For a deliberately
  self-contained `<img>` figure, fill `sinopia.PALETTE` with hex (mutate in place: `.update({…})`).
- The raw block also stops Pandoc lowercasing camelCase attributes (`viewBox`,
  `markerWidth`) that would otherwise break the diagram.
- Color only with `var(--bs-body-color)` and `var(--bs-<semantic>)` (`primary`/`success`/
  `warning`/`danger`/`info`), using `fill-opacity` for soft box fills — `sinopia.color()` does
  this. Inline sizing on the `<svg>` (`width`/`max-width`/`font-size`) is fine. Never hardcode
  hex (except a deliberate self-contained `PALETTE`); never use `--bs-*-bg-subtle` /
  `--bs-*-text-emphasis` (the dark theme does not remap them).

A trivial one-shape diagram can still be a hand-written inline SVG under the same color rules.

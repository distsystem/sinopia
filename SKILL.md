---
name: doc-driven-dev
description: Documentation-driven development workflow built on Quarto. Stands up a single-entry project doc library, keeps docs evergreen (current state plus plans only; history lives in git), and runs architecture discussions as gitignored, site-themed Quarto drafts that reflow into the main docs once settled. Use when: (1) setting up or scaffolding a project's documentation site/library, (2) writing or restructuring project docs and wanting one entry point that discovers everything, (3) capturing an architecture or design discussion as a reviewable draft before committing it, (4) deciding what belongs in docs versus git history, (5) the user mentions evergreen docs, documentation-driven development, building a docs site, or 文档牵引开发 / 建文档站 / evergreen 文档 / 把讨论沉淀进文档.
---

# Documentation-Driven Development

Make the project's documentation the working surface: a single-entry Quarto library
holds the *current and intended* state, discussions happen as gitignored drafts that
look exactly like the real docs, and once a discussion settles it reflows into the
evergreen pages. History and rationale ride git, not the docs.

## The loop

```
  discuss ──▶ draft ──▶ review ──▶ reflow ──▶ evergreen docs
            docs/drafts/<slug>.qmd    (agreed)   (current state)
            gitignored, site-themed      │
                                         ▼
                               rationale ──▶ git commit / PR
                                           (history, never docs)
```

> Terminology: a **draft** is the gitignored discussion artifact under `drafts/`. It is
> distinct from `quarto preview`, Quarto's live-render command (which renders the whole
> site, drafts included). The draft is *what* you write; `quarto preview` is *how* you view it.

This skill is self-contained: it folds in the draft shapes and review discipline of a
visual-draft workflow and the Quarto authoring mechanics it needs, so it does not
depend on other skills.

## Step 1 — Stand up the doc library

Copy the scaffold into the project, then make it the project's own:

1. `cp -r <skill>/assets/quarto-site <project-root>/docs` (skip if `docs/` already a Quarto site).
2. Edit `docs/_quarto.yml` (`title`, `description`, footer `PROJECT_NAME`) and the
   `title`/`description` frontmatter in `docs/index.qmd`.
3. Pick the home: keep `docs/index.qmd` including `../README.md` (README doubles as the
   GitHub front page and the doc home), or replace the include with a hand-written home.
4. Run it: `cd docs && pixi run preview` (port 4850, hot reload; `setup` auto-fetches
   extensions on first run, so a fresh clone is immediately usable).

The **single entry point** is the sidebar (`contents: auto`, which auto-lists every page)
plus navbar overlay search. Adding a `docs/<page>.md` is all it takes for a doc to be
discoverable; no index to maintain.

The scaffold ships: a self-contained `pixi.toml` (isolated Quarto env), `_quarto.yml`
(website, light↔dark `flatly`/`darkly` + SCSS tokens, filters registered), `index.qmd`,
the `compare-option` and `rebase-readme-links` Lua filters, the theme SCSS, a `.gitignore`,
and `drafts/_template.qmd`.

## Step 2 — Keep docs evergreen

Docs state what is true and what is planned. They never narrate how the design got
here. Decision evolution, discussion, and change history live in **commit messages and PR
descriptions**. When a decision lands, update the docs to the new state and record the
*why* in the commit/PR body.

Full voice, structure, page-title, vocabulary, and theme-aware-SVG rules:
**read `references/evergreen-voice.md`** before writing or restructuring docs. The
essentials:

- No change-voice: avoid `currently` / `now` / `added` / `dropped` / `renamed to` /
  `previously`. Write state-of-fact (`X is Y`) and present-tense negatives (`has no Y`).
- Mark planned content: a not-yet-built section's heading carries a `[PLAN]`/`[TODO]`
  badge so readers tell intended from implemented; the body stays present-tense and the
  badge drops when the feature lands.
- Problem-driven: each section shows the ordinary approach and where it stalls (before),
  then the project's shape (after). Do not judge the ordinary approach before showing it.
- Main pages use a bare `#` heading and no YAML `title:` (uniform h1); `index.qmd` is the
  exception.

## Step 3 — Run discussions as drafts

When a discussion is substantial enough to need visual structure (an architecture, a
proposal, a tradeoff, a plan), capture it as a draft instead of editing the real docs:

1. Copy `drafts/_template.qmd` to `docs/drafts/<slug>.qmd`. Derive a short kebab-case
   slug from the topic once and reuse it all session, so the open tab just reloads.
2. Shape it to the discussion (see **Draft shapes** below) using the authoring
   vocabulary: `.compare-option` cards, callouts, `.grid`, and theme-aware SVG.
3. It renders with the **site theme**, so it already looks like a real doc page. That is
   the point: reflow later is near-free. `quarto preview` hot-reloads on every save, so no
   browser plumbing is needed; the user keeps one tab open.

Drafts are gitignored (`/drafts/*`, with `_template.qmd` kept). They are local-only
review artifacts and never reach the published site.

**Review discipline**: a draft is a discussion artifact, not the source of truth.
After writing or revising one, do not auto-reflow into the docs and do not start writing
code. Iterate framing, naming, scope, and emphasis until the user confirms.

## Step 4 — Reflow when settled

Once the user agrees on the shape:

- Move the agreed structure into the evergreen main docs, in evergreen voice. Delete the
  `docs/drafts/<slug>.qmd` draft; its job is done.
- Record the rationale in the commit/PR that lands the change, not in the doc.
- Planned-but-not-landed work stays **in the main docs** under a `[PLAN]`/`[TODO]` badge
  (Step 2); the badge drops when it lands. Do not split it into a separate proposal file —
  no `docs/proposals/` by default.

## Draft shapes

Pick the shape that fits the discussion; use fewer sections when the topic is narrow.

- **RFC board**: thesis, problem, options (`.compare-option` row), proposed shape, risks/non-goals, open questions.
- **Decision matrix**: options as `.compare-option` cards with verdicts, then a recommendation.
- **Architecture map**: system boundary, component bands, interface arrows (SVG-as-code), failure points.
- **Plan draft**: goal, phases, acceptance criteria, rollback/defer points.
- **Concept explainer**: intuition, formal core, examples, limits.

## Authoring vocabulary

Reuse Bootstrap 5.3 + Quarto-native classes; do not hand-roll CSS. Full table and
mechanics in `references/quarto-cheatsheet.md` and `references/evergreen-voice.md`. Key
moves:

- 3-way verdict compare: `::: {.compare-option verdict=danger|warning|success tag="..." title="..." label="..."}` inside a `::: {.grid}`.
- Callouts (`.callout-{note,tip,important,caution,warning}`), two columns (`.grid` + `.g-col-md-6`), inline badges, definition lists.
- Keep hardcoded color out of the Markdown body: no inline `style` color, no hex literals
  (they break light↔dark). A repeated 7+ utility-class pattern becomes a Lua filter (see
  `_filters/compare-option.lua`).
- Diagrams are generated, not hand-typed: compose them in Python with the `sinopia` package as a
  tree of first-class models (positioned `Box` anchors + the computed-control-point `Route`
  connector + declarative `Row` / `Col` / `Grid` layout), then inline the SVG in a
  ```` ```{=html} ```` raw block so `var(--bs-*)` colors follow the theme. Color only via
  `var(--bs-body-color)` / `var(--bs-<semantic>)` + `fill-opacity`; never hardcode hex (except a
  deliberate self-contained `PALETTE`) or use `--bs-*-bg-subtle`. See `references/evergreen-voice.md`
  → "Diagrams: SVG-as-code".
- Figure vocabulary lives in the project, not in `sinopia`. The package is the engine: themed shape
  models (`Rect` / `Band` / `Card` / `Text` / `RichText`), `Box` anchors, the `Route` connector, and
  `Row` / `Col` / `Grid` layout, with no editorial presets. Recurring box recipes — a titled section
  band, a header region, a domain card (a Neovim window, a Zed editor) — are thin helpers over
  `Node(...)` defined beside the figures (a shared module next to `figures.py`) and reused across that
  project's diagrams. They encode the doc's taste (fills, sizes, colors) and its domain names, so they
  stay project-local. Rule of thumb: a helper that still makes sense in an unrelated project belongs in
  `sinopia`; one named after your domain belongs in your figures.

## Bundled resources

- `assets/quarto-site/` — the drop-in Quarto scaffold (Step 1).
- `src/sinopia/` — installable diagrams-as-code package: a tree of first-class pydantic models — `Box` anchors, themed shape models, the computed `Route` connector, and stretchable-backed `Row` / `Col` / `Grid` layout. Add it to the docs env (`pixi add --pypi sinopia@git+…` or `pip install -e <repo>`) and `import sinopia as S` from generation scripts.
- `references/evergreen-voice.md` — what evergreen means, voice, structure, page conventions, SVG-as-code.
- `references/quarto-cheatsheet.md` — Quarto authoring mechanics (divs, callouts, grid, crossref, citations, includes, extensions).

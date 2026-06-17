# Quarto Authoring Cheatsheet

The Quarto mechanics this workflow leans on. Scope is document/website authoring;
revealjs slide syntax is out of scope unless explicitly requested.

- [Project & config](#project--config)
- [Render & preview](#render--preview)
- [Fenced divs & attributes](#fenced-divs--attributes)
- [Callouts](#callouts)
- [Grid layout](#grid-layout)
- [Cross-references](#cross-references)
- [Citations](#citations)
- [Includes & shortcodes](#includes--shortcodes)
- [Executable code](#executable-code)
- [Extensions](#extensions)
- [Official docs](#official-docs)

## Project & config

A directory is a Quarto website project when it has `_quarto.yml` with
`project: type: website` and one or more `*.qmd`/`*.md`. The scaffold's `_quarto.yml`
sets the navbar, a docked sidebar with `contents: auto` (every page auto-listed from
one entry point), overlay search, and a light/dark theme pair (`flatly` + `darkly`)
layered with the local SCSS token files. Follow the existing config rather than
introducing new formats or filters.

## Render & preview

Drive through the pixi tasks shipped in the scaffold (they auto-run `setup`, which
fetches extensions idempotently):

```bash
cd docs
pixi run preview     # http://localhost:4850, hot reload on save
pixi run render      # one-shot static build to _site/
```

Raw Quarto equivalents, when not using the tasks:

```bash
quarto check                 # sanity-check the environment
quarto preview               # whole project, hot reload
quarto preview path/doc.qmd  # a single input
quarto render path/doc.qmd   # one file
```

`quarto preview` watches the project and reloads the browser on every save, including
files under `drafts/`. No browser automation is needed; the user keeps one tab open.

## Fenced divs & attributes

Structure comes from fenced divs (`::: {.class key=value}`) and Pandoc attribute lists
(`{#id .class key=value}`). Nest divs by adding colons to the fence:

```markdown
::::: {.grid}
:::: {.g-col-12 .g-col-md-6}
left column
::::
:::: {.g-col-12 .g-col-md-6}
right column
::::
:::::
```

## Callouts

```markdown
::: {.callout-tip}
body
:::

::: {.callout-important appearance="simple"}
a one-liner with no title bar
:::

::: {.callout-note collapse="true" title="Details"}
collapsible body
:::
```

Kinds: `note`, `tip`, `important`, `caution`, `warning`.

## Grid layout

Quarto ships a 12-column Bootstrap grid. `::: {.grid}` is the row; children carry
`.g-col-{n}` plus responsive variants like `.g-col-md-6`. The `.compare-option` filter
emits `.g-col-12 .g-col-md-4` cards, so three of them fill a row on desktop and stack
on mobile.

## Cross-references

Give the target a typed id, then reference with `@id`:

```markdown
![caption](img.png){#fig-x}

See @fig-x.
```

```markdown
$$
E = mc^2
$$ {#eq-energy}
```

Id prefixes: `#fig-`, `#tbl-`, `#eq-`, `#sec-` (needs `number-sections`), `#thm-`.
Custom kinds (algorithms, appendix tables) go under `crossref:` in YAML.

## Citations

Set `bibliography:` in YAML, cite with `[@key]` / `@key`, and place the reference list:

```markdown
# References {.unnumbered}

::: {#refs}
:::
```

For one-off external sources in a problem-driven page, prefer **footnotes** scattered
into the section that uses them over a central references page.

## Includes & shortcodes

```markdown
{{< include ../README.md >}}
```

The home `index.qmd` includes the repo README so GitHub and the site share one front
page; the `rebase-readme-links` filter rewrites the README's `docs/X.md` links to
resolve inside the site.

## Executable code

Static fenced blocks (```` ```python ````) are fine for illustration and need no engine.
For executed cells, use cell options with `#|`:

```python
#| label: fig-plot
#| fig-cap: "A figure"
```

Most evergreen prose docs use static blocks; reach for executable cells only when the
output must be computed from real code.

## Extensions

Declare each extension in the `setup` task with a `test -d` idempotency guard:

```toml
[tasks.setup]
cmd = """
mkdir -p _extensions &&
test -d _extensions/owner/repo || quarto add --no-prompt owner/repo
"""
```

Add one line per extension; the next `pixi run preview` fetches it. `_extensions/` is
gitignored, so a fresh clone downloads on first setup.

## Official docs

- Markdown basics: https://quarto.org/docs/authoring/markdown-basics.html
- Cross-references: https://quarto.org/docs/authoring/cross-references.html
- Footnotes & citations: https://quarto.org/docs/authoring/footnotes-and-citations.html
- Website navigation: https://quarto.org/docs/websites/website-navigation.html
- Projects: https://quarto.org/docs/projects/quarto-projects.html

// kami.typ — the kami print theme: wire the shared component factory to kami's
// tokens, then apply kami's global skin. Include from a .qmd via
//   format: typst: { include-in-header: <path>/kami.typ }
// The #set/#show rules style the whole document; the bound #let names
// (#eyebrow #swatches #card #stat #quote #tag) are available in {=typst} blocks.
// Root-absolute imports resolve from the Quarto project root (docs/).
#import "/_typst/kami-tokens.typ": theme
#import "/_typst/components.typ": components

#let k = components(theme)
#let eyebrow   = k.eyebrow
#let swatches  = k.swatches
#let card      = k.card
#let stat      = k.stat
#let quote     = k.quote
#let tag       = k.tag
#let steps     = k.steps
#let timeline  = k.timeline
#let hero      = k.hero
#let dash-list = k.dash-list

// ---- global skin ----
#set page(fill: theme.surface)
#set text(fill: theme.text, font: theme.serif, lang: "zh", size: 11pt)
#set par(justify: true, leading: 0.9em)
#show link: set text(fill: theme.accent)
#show raw.where(block: false): set text(fill: theme.accent)   // inline code in accent

// headings: serif Medium, accent; H2 carries kami's signature brand left-bar.
#show heading: set text(fill: theme.accent, weight: "medium")
#show heading.where(level: 2): it => block(
  width: 100%, above: 1.5em, below: 0.6em,
  stroke: (left: 2.5pt + theme.accent), inset: (left: 8pt),
)[#text(fill: theme.accent, weight: "medium", size: 1.4em)[#it.body]]

// components.typ — the print-side component vocabulary, theme-neutral.
// `components(theme)` returns the #let functions bound to one theme's tokens;
// the theme entry (kami.typ) wires them to bare names. Mirrors the CSS component
// layer (_styles/_base/components.scss) one-to-one; the components.lua filter
// lowers `::: {.X}` semantic divs to these calls on the typst target.
#let components(theme) = (
  // small accent section label, e.g. #eyebrow[03 · Color]
  eyebrow: t => text(fill: theme.accent, size: 9pt, weight: "medium")[#upper(t)],

  // a row of colour swatches: #swatches((("Parchment","#f5f4ed"), ...))
  swatches: items => grid(
    columns: items.len(), gutter: 10pt,
    ..items.map(it => stack(
      rect(
        width: 100%, height: 40pt, radius: 3pt, fill: rgb(it.at(1)),
        stroke: if it.at(0) in ("Parchment", "Ivory") { 0.5pt + theme.border } else { none },
      ),
      v(4pt),
      text(size: 8pt)[#it.at(0)],
      text(size: 7pt, fill: theme.text-subtle)[#it.at(1)],
    )),
  ),

  // raised card with a soft border; the bold lead lives in the body: #card[*Title* …]
  card: body => block(
    fill: theme.surface-raised, stroke: 0.5pt + theme.border, radius: 8pt, inset: 14pt, width: 100%,
  )[#body],

  // stat: serif accent number over a muted label
  stat: (value, label) => box[
    #text(size: 20pt, weight: "medium", fill: theme.accent)[#value] #linebreak()
    #text(size: 8pt, fill: theme.text-muted)[#label]
  ],

  // quote with an accent left rule + muted text
  quote: body => block(
    stroke: (left: 2pt + theme.accent), inset: (left: 10pt, y: 3pt),
  )[#text(fill: theme.text-muted)[#body]],

  // accent-wash tag, three tiers: #tag[中文] · #tag(tier: "strong")[…]
  tag: (t, tier: "default") => box(
    fill: if tier == "faint" { theme.accent-wash } else if tier == "strong" { theme.accent-wash-3 } else { theme.accent-wash-2 },
    inset: (x: 5pt, y: 1pt), radius: 2pt,
  )[#text(fill: theme.accent, size: 8pt, weight: "medium")[#t]],

  // numbered process: #steps[ + an enum body ]
  steps: body => {
    set enum(numbering: n => text(fill: theme.accent, weight: "bold")[#n.])
    body
  },

  // dated events down an accent rule: #timeline[ + a list body ]
  timeline: body => block(
    stroke: (left: 2pt + theme.border), inset: (left: 12pt, y: 2pt),
  )[#body],

  // page masthead: #hero[ + a title + lead ]
  hero: body => block(width: 100%, below: 1.2em)[
    #body
    #v(0.5em)
    #line(length: 100%, stroke: 0.5pt + theme.border-soft)
  ],

  // em-dash leaders instead of bullets: #dash-list[ + a list body ]
  dash-list: body => {
    set list(marker: text(fill: theme.accent)[–])
    body
  },
)

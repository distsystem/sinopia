// components.typ — the print-side component vocabulary, theme-neutral.
// `components(theme)` returns the #let functions bound to one theme's tokens;
// the theme entry (kami.typ) wires them to bare names. Mirrors the CSS
// component layer (_styles/_base/components.scss) one-to-one.
#let components(theme) = (
  // small accent section label, e.g. #eyebrow("03 · Color")
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

  // raised card with a soft border: #card("Title")[body]
  card: (title, body) => block(
    fill: theme.surface-raised, stroke: 0.5pt + theme.border, radius: 8pt, inset: 14pt, width: 100%,
  )[#text(weight: "medium")[#title] #v(5pt) #body],

  // stat: serif accent number over a muted label
  stat: (value, label) => box[
    #text(size: 20pt, weight: "medium", fill: theme.accent)[#value] #linebreak()
    #text(size: 8pt, fill: theme.text-muted)[#label]
  ],

  // quote with an accent left rule + muted text
  quote: body => block(
    stroke: (left: 2pt + theme.accent), inset: (left: 10pt, y: 3pt),
  )[#text(fill: theme.text-muted)[#body]],

  // accent-wash tag: #tag[中文]
  tag: t => box(fill: theme.accent-wash, inset: (x: 5pt, y: 1pt), radius: 2pt)[
    #text(fill: theme.accent, size: 8pt, weight: "medium")[#t]
  ],
)

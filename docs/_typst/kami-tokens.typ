// kami-tokens.typ — the kami palette as a semantic token dict (print side).
// Keys mirror the CSS semantic contract (_styles/_base/contract.scss); a second
// Typst theme is a parallel dict with the same keys. Values trace to kami's
// CHEATSHEET. LXGW WenKai (Regular 400 + Medium 500) is the serif.
#let theme = (
  accent:         rgb("#1b365d"),  // single ink-blue accent (<= 5% of the page)
  surface:        rgb("#f5f4ed"),  // page background, never pure white
  surface-raised: rgb("#faf9f5"),  // card / lifted surface
  surface-sunken: rgb("#e8e6dc"),  // interactive surface
  text:           rgb("#141413"),  // primary text
  text-secondary: rgb("#3d3d3a"),  // secondary text
  text-muted:     rgb("#504e49"),  // subtext / quotes
  text-subtle:    rgb("#6b6a64"),  // tertiary / metadata
  border:         rgb("#e8e6dc"),
  border-soft:    rgb("#e5e3d8"),
  accent-wash:    rgb("#eef2f7"),  // tag faint / code wash (ink-blue at ~0.08)
  accent-wash-2:  rgb("#e4ecf5"),  // tag default
  accent-wash-3:  rgb("#d0dce9"),  // tag strong
  error:          rgb("#b53333"),
  serif:          "LXGW WenKai",
)

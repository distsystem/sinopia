"""Closed-set vocabulary + shared aliases. A closed set is a closed union (Literal), so a
typo'd value is a validation error, not a silent mis-render."""
from typing import Literal

# Open: a semantic role name (primary/success/…) or a raw var(--bs-*) / hex string.
Role = str

Kind = Literal["card", "rect", "band"]
Shape = Literal["line", "sweep", "arc", "-|", "|-", "z", "z|", "n", "c"]
Ends = Literal["none", "start", "end", "both"]
Align = Literal["start", "end", "center", "stretch"]
Justify = Literal["start", "end", "center", "between"]
Anchor = Literal["start", "middle", "end"]

Point = tuple[float, float]
Seg = tuple[str, dict]              # a styled text segment: (text, opts)
Line = str | Seg | list[Seg]       # a Node line: plain / styled / rich

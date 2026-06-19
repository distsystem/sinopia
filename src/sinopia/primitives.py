"""Themed SVG as first-class models. Each shape is a frozen `Drawable` whose `render()`
returns its SVG string; a figure is a tree of these, rendered at the end. Pure-string output,
so colors stay `var(--bs-*)` (theme-aware when inlined) unless `PALETTE` is filled with hex.
"""
import pathlib

from pydantic import BaseModel, ConfigDict

from sinopia.types import Anchor, Ends, Point, Role, Seg

# Role → CSS color. Override PALETTE in place (`.update({...})`) with hex for self-contained figures.
PALETTE: dict[str, str] = {}


def color(role: str) -> str:
    if role in PALETTE:
        return PALETTE[role]
    if role in ("ink", "body"):
        return "var(--bs-body-color)"
    if role in ("bg", "panel"):
        return "var(--bs-body-bg)"
    if role == "mut":
        return "color-mix(in srgb, var(--bs-body-color) 55%, transparent)"
    if role == "white":
        return "white"  # for text on a solid-filled band (readable in both themes)
    return f"var(--bs-{role})"  # primary / success / warning / danger / info / secondary


def _n(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _g(v: float) -> str:
    """Format a size/width attribute, stripping insignificant zeros (9.0 → "9", 1.6 → "1.6")."""
    return f"{v:g}"


def _textw(s: str, size: float) -> float:
    # CJK glyphs are roughly square; latin ~0.56em. Enough for label-box sizing.
    return sum(size * (1.05 if ord(c) > 0x2E80 else 0.56) for c in s)


def mid(a: Point, b: Point) -> Point:
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


class Box(BaseModel):
    """A positioned rectangle exposing anchor points so connectors reference geometry,
    not literal coordinates."""
    model_config = ConfigDict(frozen=True)

    x: float
    y: float
    w: float
    h: float

    def __init__(self, x: float, y: float, w: float, h: float):
        super().__init__(x=x, y=y, w=w, h=h)

    def at(self, fx: float, fy: float) -> Point:
        return (self.x + self.w * fx, self.y + self.h * fy)

    @property
    def left(self) -> Point: return self.at(0, 0.5)
    @property
    def right(self) -> Point: return self.at(1, 0.5)
    @property
    def top(self) -> Point: return self.at(0.5, 0)
    @property
    def bottom(self) -> Point: return self.at(0.5, 1)
    @property
    def center(self) -> Point: return self.at(0.5, 0.5)
    @property
    def nw(self) -> Point: return self.at(0, 0)
    @property
    def ne(self) -> Point: return self.at(1, 0)
    @property
    def sw(self) -> Point: return self.at(0, 1)
    @property
    def se(self) -> Point: return self.at(1, 1)


class Drawable(BaseModel):
    """A figure element that renders to an SVG string. Behavior lives on the type:
    each subtype overrides `render`."""
    model_config = ConfigDict(frozen=True)

    def render(self) -> str:
        raise NotImplementedError


def _render(part: object) -> str:
    return part.render() if isinstance(part, Drawable) else str(part)


class Rect(Drawable):
    """Soft translucent box: role-tinted fill + role stroke."""
    box: Box
    role: Role = "body"
    fill: float = 0.08
    stroke_width: float = 1.6
    rx: float = 9
    dash: str | None = None

    def __init__(self, box: Box, role: Role = "body", *, fill: float = 0.08,
                 stroke_width: float = 1.6, rx: float = 9, dash: str | None = None):
        super().__init__(box=box, role=role, fill=fill, stroke_width=stroke_width, rx=rx, dash=dash)

    def render(self) -> str:
        b, c = self.box, color(self.role)
        d = f' stroke-dasharray="{self.dash}"' if self.dash else ""
        return (f'<rect x="{_n(b.x)}" y="{_n(b.y)}" width="{_n(b.w)}" height="{_n(b.h)}" rx="{_g(self.rx)}" '
                f'fill="{c}" fill-opacity="{self.fill}" stroke="{c}" stroke-width="{_g(self.stroke_width)}"{d}/>')


class Band(Drawable):
    """Solid role-filled box (title bands, badges)."""
    box: Box
    role: Role
    rx: float = 6

    def __init__(self, box: Box, role: Role, *, rx: float = 6):
        super().__init__(box=box, role=role, rx=rx)

    def render(self) -> str:
        b = self.box
        return (f'<rect x="{_n(b.x)}" y="{_n(b.y)}" width="{_n(b.w)}" height="{_n(b.h)}" '
                f'rx="{_g(self.rx)}" fill="{color(self.role)}"/>')


class Card(Drawable):
    """Opaque card: body-bg fill + role stroke — occludes what is behind it."""
    box: Box
    role: Role
    stroke_width: float = 1.6
    rx: float = 9
    dash: str | None = None

    def __init__(self, box: Box, role: Role, *, stroke_width: float = 1.6,
                 rx: float = 9, dash: str | None = None):
        super().__init__(box=box, role=role, stroke_width=stroke_width, rx=rx, dash=dash)

    def render(self) -> str:
        b = self.box
        d = f' stroke-dasharray="{self.dash}"' if self.dash else ""
        return (f'<rect x="{_n(b.x)}" y="{_n(b.y)}" width="{_n(b.w)}" height="{_n(b.h)}" rx="{_g(self.rx)}" '
                f'fill="{color("bg")}" stroke="{color(self.role)}" stroke-width="{_g(self.stroke_width)}"{d}/>')


class Text(Drawable):
    x: float
    y: float
    s: str
    role: Role = "ink"
    size: float = 12
    weight: bool = False
    anchor: Anchor = "start"
    mono: bool = False
    opacity: float = 1.0

    def __init__(self, x: float, y: float, s: str, *, role: Role = "ink", size: float = 12,
                 weight: bool = False, anchor: Anchor = "start", mono: bool = False, opacity: float = 1.0):
        super().__init__(x=x, y=y, s=s, role=role, size=size, weight=weight,
                         anchor=anchor, mono=mono, opacity=opacity)

    def render(self) -> str:
        fw = ' font-weight="700"' if self.weight else ""
        fam = ' font-family="ui-monospace,monospace"' if self.mono else ""
        op = f' fill-opacity="{self.opacity}"' if self.opacity != 1.0 else ""
        return (f'<text x="{_n(self.x)}" y="{_n(self.y)}" font-size="{_g(self.size)}" fill="{color(self.role)}" '
                f'text-anchor="{self.anchor}"{fw}{fam}{op}>{self.s}</text>')


class RichText(Drawable):
    """A single <text> line with mixed-style segments. Each seg is (str, opts) where opts may set
    role / weight / size / mono."""
    x: float
    y: float
    segs: list[Seg]
    size: float = 11.5
    anchor: Anchor = "start"

    def __init__(self, x: float, y: float, segs: list[Seg], *, size: float = 11.5, anchor: Anchor = "start"):
        super().__init__(x=x, y=y, segs=segs, size=size, anchor=anchor)

    def render(self) -> str:
        parts = []
        for t, st in self.segs:
            attrs = f'fill="{color(st.get("role", "ink"))}"'
            if st.get("weight"):
                attrs += ' font-weight="700"'
            if "size" in st:
                attrs += f' font-size="{st["size"]}"'
            if st.get("mono"):
                attrs += ' font-family="ui-monospace,monospace"'
            parts.append(f"<tspan {attrs}>{t}</tspan>")
        return (f'<text x="{_n(self.x)}" y="{_n(self.y)}" font-size="{_g(self.size)}" '
                f'text-anchor="{self.anchor}">{"".join(parts)}</text>')


class RawPath(Drawable):
    """Raw SVG path with themed stroke + optional arrowheads — the escape hatch for any curve
    (paste hand-tuned bezier control points into `d`)."""
    d: str
    role: Role = "body"
    width: float = 1.4
    fill: str = "none"
    opacity: float = 1.0
    dash: str | None = None
    ends: Ends = "none"

    def __init__(self, d: str, role: Role = "body", *, width: float = 1.4, fill: str = "none",
                 opacity: float = 1.0, dash: str | None = None, ends: Ends = "none"):
        super().__init__(d=d, role=role, width=width, fill=fill, opacity=opacity, dash=dash, ends=ends)

    def render(self) -> str:
        da = f' stroke-dasharray="{self.dash}"' if self.dash else ""
        op = f' opacity="{self.opacity}"' if self.opacity != 1.0 else ""
        ms = f' marker-start="url(#a-{self.role})"' if self.ends in ("start", "both") else ""
        me = f' marker-end="url(#a-{self.role})"' if self.ends in ("end", "both") else ""
        fc = color(self.role) if self.fill != "none" else "none"
        return (f'<path d="{self.d}" fill="{fc}" stroke="{color(self.role)}" '
                f'stroke-width="{_g(self.width)}"{op}{da}{ms}{me}/>')


class Markers(Drawable):
    """Arrowhead markers, one per role; referenced by `Route` as `#a-<role>`."""
    roles: tuple[Role, ...]

    def __init__(self, *roles: Role):
        super().__init__(roles=tuple(roles))

    def render(self) -> str:
        out = ["<defs>"]
        for r in self.roles:
            out.append(
                f'<marker id="a-{r}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color(r)}"/></marker>')
        out.append("</defs>")
        return "".join(out)


class Figure(Drawable):
    """The <svg> root: composes a tree of drawables (or raw strings)."""
    width: float
    height: float
    parts: tuple[Drawable | str, ...] = ()
    cls: str = "zfig"

    def __init__(self, width: float, height: float, *parts: Drawable | str, cls: str = "zfig"):
        super().__init__(width=width, height=height, parts=parts, cls=cls)

    def render(self) -> str:
        body = "\n".join(_render(p) for p in self.parts if p)
        return (f'<svg class="{self.cls}" viewBox="0 0 {_n(self.width)} {_n(self.height)}" '
                f'xmlns="http://www.w3.org/2000/svg" '
                f'font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\','
                f"'Noto Sans CJK SC',sans-serif\">\n" + body + "\n</svg>\n")

    def _repr_html_(self) -> str:
        return self.render()

    def save(self, path: str | pathlib.Path) -> None:
        pathlib.Path(path).write_text(self.render(), encoding="utf-8")

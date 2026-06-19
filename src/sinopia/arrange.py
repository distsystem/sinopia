"""Declarative layout on stretchable (Taffy) as first-class models: nested Row/Col/Grid of boxes
and labels; coordinates are *computed*. Each element is a frozen pydantic model (its config is a
Value); the layout pass writes computed geometry into a private `_box`, and anchor properties read
it, so connectors reference geometry (`node.right`) instead of literal coordinates.
"""
from typing import Any

from pydantic import BaseModel, ConfigDict, PrivateAttr
from stretchable import Edge
from stretchable import Node as StNode
from stretchable.style import (
    AUTO,
    AlignItems,
    Display,
    FlexDirection,
    JustifyContent,
    JustifyItems,
)

from sinopia.primitives import (
    Band,
    Box,
    Card,
    Figure,
    Rect,
    RichText,
    Text,
    _render,
    _textw,
)
from sinopia.types import Align, Justify, Kind, Point, Role

LINE_H = 16.0   # default text line height inside a Node
PAD = 8.0       # default inner padding of a content box

_ALIGN = {"start": AlignItems.START, "end": AlignItems.END,
          "center": AlignItems.CENTER, "stretch": AlignItems.STRETCH}
_JUSTIFY = {"start": JustifyContent.START, "end": JustifyContent.END,
            "center": JustifyContent.CENTER, "between": JustifyContent.SPACE_BETWEEN}
_JUSTIFY_ITEMS = {"start": JustifyItems.START, "end": JustifyItems.END,
                  "center": JustifyItems.CENTER, "stretch": JustifyItems.STRETCH}


def _seg(ln):
    return ln if isinstance(ln, tuple) else (ln, {})


class Element(BaseModel):
    """Base layout element: frozen config + a private computed `_box`. Leaves implement
    `_content` (intrinsic size); every element implements `_build` (build a stretchable node)."""
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    w: float | None = None
    h: float | None = None
    _box: Box | None = PrivateAttr(default=None)

    def _content(self) -> tuple[float, float]:
        return (0.0, 0.0)

    def _build_leaf(self, pairs, **extra):
        mw, mh = self._content()
        size = (self.w if self.w is not None else AUTO, self.h if self.h is not None else AUTO)
        min_size = (0.0 if self.w is not None else mw, 0.0 if self.h is not None else mh)
        n = StNode(size=size, min_size=min_size, **extra)
        pairs.append((self, n))
        return n

    def _build(self, pairs, **extra):
        raise NotImplementedError

    def _read_box(self, box: Box) -> None:
        self._box = box

    def at(self, fx: float, fy: float) -> Point:
        return self._box.at(fx, fy)

    @property
    def box(self) -> Box: return self._box
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


def _bg(el: "Row | Col | Grid") -> str:
    """A container's background box (role, opts), drawn behind its children."""
    if el.bg is None:
        return ""
    role, opts = el.bg
    return Rect(el._box, role, **opts).render()


class Label(Element):
    """A single line of text, no box; sizes to the text."""
    s: str
    role: Role = "ink"
    size: float = 12
    weight: bool = False
    anchor: str = "start"
    mono: bool = False

    def __init__(self, s, *, role="ink", size=12, weight=False, anchor="start", mono=False):
        super().__init__(s=s, role=role, size=size, weight=weight, anchor=anchor, mono=mono)

    def _content(self):
        return (_textw(self.s, self.size), self.size * 1.35)

    def _build(self, pairs, **extra):
        return self._build_leaf(pairs, **extra)

    def render(self):
        b = self._box
        tx = {"start": b.x, "middle": self.center[0], "end": b.x + b.w}[self.anchor]
        return Text(tx, b.y + self.size, self.s, role=self.role, size=self.size,
                    weight=self.weight, anchor=self.anchor, mono=self.mono).render()


class Node(Element):
    """A content box of stacked text lines; auto-sized unless w/h given. Each line is a str or
    (str, opts) with role/size/weight/mono/anchor; a line whose content is a list of (str, opts)
    segments renders as one mixed-style (rich) line. `kind`: "card" (opaque) / "rect" (soft) /
    "band" (solid fill)."""
    lines: tuple[Any, ...]
    role: Role = "body"
    kind: Kind = "card"
    pad: float = PAD
    line_h: float = LINE_H
    name: str | None = None
    fill: float = 0.08
    dash: str | None = None
    rx: float = 9

    def __init__(self, *lines, role="body", kind="card", w=None, h=None,
                 pad=PAD, line_h=LINE_H, name=None, fill=0.08, dash=None, rx=9):
        super().__init__(lines=tuple(_seg(ln) for ln in lines), role=role, kind=kind, w=w, h=h,
                         pad=pad, line_h=line_h, name=name, fill=fill, dash=dash, rx=rx)

    def _line_w(self, t, o):
        if isinstance(t, list):
            base = o.get("size", 11.5)
            return sum(_textw(s, st.get("size", base)) for s, st in t)
        return _textw(t, o.get("size", 12))

    def _content(self):
        mw = max((self._line_w(t, o) for t, o in self.lines), default=0) + 2 * self.pad
        mh = len(self.lines) * self.line_h + 2 * self.pad
        return (mw, mh)

    def _build(self, pairs, **extra):
        return self._build_leaf(pairs, **extra)

    def render(self):
        b = self._box
        if self.kind == "band":
            shape = Band(b, self.role, rx=self.rx).render()
        elif self.kind == "rect":
            shape = Rect(b, self.role, fill=self.fill, rx=self.rx, dash=self.dash).render()
        else:
            shape = Card(b, self.role, rx=self.rx, dash=self.dash).render()
        out = [shape]
        ty = b.y + self.pad
        for t, o in self.lines:
            a = o.get("anchor", "start")
            tx = {"start": b.x + self.pad, "middle": self.center[0], "end": b.x + b.w - self.pad}[a]
            if isinstance(t, list):
                out.append(RichText(tx, ty + o.get("size", 11.5), t, size=o.get("size", 11.5), anchor=a).render())
            else:
                out.append(Text(tx, ty + o.get("size", 12), t, role=o.get("role", "ink"),
                                size=o.get("size", 12), weight=o.get("weight", False),
                                anchor=a, mono=o.get("mono", False)).render())
            ty += self.line_h
        return "".join(out)


class Spacer(Element):
    """Fixed empty space — the gap a connector runs through."""
    def __init__(self, w=0, h=0):
        super().__init__(w=w, h=h)

    def _build(self, pairs, **extra):
        return self._build_leaf(pairs, **extra)

    def render(self):
        return ""


class Row(Element):
    """Horizontal flex container. justify='between' spreads children across the row width
    (set wider by a stretching parent)."""
    children: tuple[Element, ...]
    gap: float = 8.0
    align: Align = "center"
    justify: Justify = "start"
    pad: float = 0.0
    bg: tuple[Role, dict] | None = None

    def __init__(self, *children, gap=8.0, align="center", justify="start", pad=0.0, bg=None):
        super().__init__(children=tuple(children), gap=gap, align=align, justify=justify, pad=pad, bg=bg)

    def _build(self, pairs, **extra):
        n = StNode(display=Display.FLEX, flex_direction=FlexDirection.ROW,
                   align_items=_ALIGN[self.align], justify_content=_JUSTIFY[self.justify],
                   gap=self.gap, padding=self.pad, **extra)
        for c in self.children:
            n.add(c._build(pairs))
        pairs.append((self, n))
        return n

    def render(self):
        return _bg(self) + "".join(c.render() for c in self.children)


class Col(Element):
    """Vertical flex container. align='stretch' widens each child to the column width."""
    children: tuple[Element, ...]
    gap: float = 8.0
    align: Align = "start"
    justify: Justify = "start"
    pad: float = 0.0
    bg: tuple[Role, dict] | None = None

    def __init__(self, *children, gap=8.0, align="start", justify="start", pad=0.0, bg=None):
        super().__init__(children=tuple(children), gap=gap, align=align, justify=justify, pad=pad, bg=bg)

    def _build(self, pairs, **extra):
        n = StNode(display=Display.FLEX, flex_direction=FlexDirection.COLUMN,
                   align_items=_ALIGN[self.align], justify_content=_JUSTIFY[self.justify],
                   gap=self.gap, padding=self.pad, **extra)
        for c in self.children:
            n.add(c._build(pairs))
        pairs.append((self, n))
        return n

    def render(self):
        return _bg(self) + "".join(c.render() for c in self.children)


class Cell(BaseModel):
    """A grid cell wrapping a child with a column span (use inside a `Grid` row)."""
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
    el: Element
    span: int = 1

    def __init__(self, el, span=1):
        super().__init__(el=el, span=span)


class Grid(Element):
    """CSS-grid container declared by rows. Columns default to equal `1fr` tracks (override with
    `col_tracks`/`row_tracks`); cross-row columns align. A `Cell(el, span=n)` widens a cell across
    n columns."""
    rows: tuple[tuple[Any, ...], ...]
    cols: int
    col_gap: float = 8.0
    row_gap: float = 8.0
    align: Align = "stretch"
    justify: Align = "stretch"
    col_tracks: list[str] | None = None
    row_tracks: list[str] | None = None
    pad: float = 0.0
    bg: tuple[Role, dict] | None = None

    def __init__(self, *rows, cols=None, col_gap=8.0, row_gap=8.0, align="stretch",
                 justify="stretch", col_tracks=None, row_tracks=None, pad=0.0, bg=None):
        rws = tuple(tuple(r) for r in rows)
        ncols = cols or max((sum(getattr(c, "span", 1) for c in r) for r in rws), default=0)
        super().__init__(rows=rws, cols=ncols, col_gap=col_gap, row_gap=row_gap, align=align,
                         justify=justify, col_tracks=col_tracks, row_tracks=row_tracks, pad=pad, bg=bg)

    def _build(self, pairs, **extra):
        cols = self.col_tracks or ["1fr"] * self.cols
        rows = self.row_tracks or ["auto"] * len(self.rows)
        n = StNode(display=Display.GRID, grid_template_columns=cols, grid_template_rows=rows,
                   gap=(self.col_gap, self.row_gap), align_items=_ALIGN[self.align],
                   justify_items=_JUSTIFY_ITEMS[self.justify], padding=self.pad, **extra)
        for ri, row in enumerate(self.rows, 1):
            ci = 1
            for cell in row:
                el = cell.el if isinstance(cell, Cell) else cell
                span = cell.span if isinstance(cell, Cell) else 1
                n.add(el._build(pairs, grid_column=f"{ci} / span {span}", grid_row=str(ri)))
                ci += span
        pairs.append((self, n))
        return n

    def render(self):
        out = [_bg(self)]
        for row in self.rows:
            for cell in row:
                out.append((cell.el if isinstance(cell, Cell) else cell).render())
        return "".join(out)


def _render_part(p) -> str:
    if callable(p):
        p = p()
    if isinstance(p, (list, tuple)):
        return "".join(_render(x) for x in p)
    return _render(p)


def layout(root, *parts, pad=16.0, cls="zfig") -> Figure:
    """Build + compute `root`'s layout, then compose it plus extra `parts` (drawables, strings, or
    thunks that read placed elements' anchors — e.g. connectors) into a `Figure`. The same terminal
    object as `Figure(...)`: call `.render()` for the SVG string, or rely on `_repr_html_`."""
    pairs = []
    st_root = StNode(padding=pad).add(root._build(pairs))
    st_root.compute_layout()
    for el, n in pairs:
        b = n.get_box(Edge.BORDER, relative=False)
        el._read_box(Box(b.x, b.y, b.width, b.height))
    rb = st_root.get_box(Edge.BORDER, relative=False)
    body = root.render() + "".join(_render_part(p) for p in parts)
    return Figure(rb.width, rb.height, body, cls=cls)

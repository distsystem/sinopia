"""Route — one connector model for every figure edge: straight, computed-bezier, orthogonal
elbows, and U-routes. Control points and bend joints are *computed* from the two anchors and a
shape code, so cross-container edges need no hand-tuned coordinates. `a`/`b`/`points` are anchor
tuples (e.g. `node.right`); `label=` floats a panel label at arc-length fraction `label_at`.

Shapes:
    line         straight segment a→b (use `points=[…]` for a multi-bend polyline)
    sweep / arc  cubic bezier with horizontal ease (control points from `k`)
    -|           elbow: horizontal then vertical      |-  vertical then horizontal
    z            S double-elbow, split on x (mx = ax + dx·k)
    z|           S double-elbow, split on y (my = ay + dy·k)
    n            U-route up   (out, across, back; stub = k·max(40,|dx|))
    c            U-route left (out, across, back; stub = k·max(40,|dy|))
"""
import math

from sinopia.primitives import Box, Drawable, Text, _g, _n, _textw, color
from sinopia.types import Ends, Point, Role, Seg, Shape


def _poly_d(pts: list[Point]) -> str:
    return "M" + " L".join(f"{_n(x)},{_n(y)}" for x, y in pts)


def _poly_point(pts: list[Point], t: float) -> Point:
    segs = [(pts[i], pts[i + 1], math.dist(pts[i], pts[i + 1])) for i in range(len(pts) - 1)]
    total = sum(d for *_, d in segs) or 1.0
    target, acc = t * total, 0.0
    for p0, p1, d in segs:
        if acc + d >= target:
            f = (target - acc) / d if d else 0.0
            return (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
        acc += d
    return pts[-1]


def _bezier_point(p0: Point, c1: Point, c2: Point, p1: Point, t: float) -> Point:
    mt = 1 - t
    return (mt**3 * p0[0] + 3 * mt**2 * t * c1[0] + 3 * mt * t**2 * c2[0] + t**3 * p1[0],
            mt**3 * p0[1] + 3 * mt**2 * t * c1[1] + 3 * mt * t**2 * c2[1] + t**3 * p1[1])


def _elbow_points(shape: str, p0: Point, p1: Point, dx: float, dy: float, k: float) -> list[Point]:
    (ax, ay), (bx, by) = p0, p1
    if shape == "line":
        return [p0, p1]
    if shape == "-|":
        return [p0, (bx, ay), p1]
    if shape == "|-":
        return [p0, (ax, by), p1]
    if shape == "z":
        mx = ax + dx * k
        return [p0, (mx, ay), (mx, by), p1]
    if shape == "z|":
        my = ay + dy * k
        return [p0, (ax, my), (bx, my), p1]
    if shape == "n":
        ey = min(ay, by) - k * max(40, abs(dx))
        return [p0, (ax, ey), (bx, ey), p1]
    if shape == "c":
        ex = min(ax, bx) - k * max(40, abs(dy))
        return [p0, (ex, ay), (ex, by), p1]
    raise ValueError(f"unknown route shape: {shape!r}")


def _panel_label(center: Point, s: str, *, role: Role, size: float, pad: float) -> str:
    cx, cy = center
    w = _textw(s, size) + pad * 2
    box = Box(cx - w / 2, cy - 11, w, 22)
    return (f'<rect x="{_n(box.x)}" y="{_n(box.y)}" width="{_n(box.w)}" height="22" rx="6" '
            f'fill="{color("bg")}" fill-opacity="0.94" stroke="{color("mut")}" stroke-width="0.8"/>'
            + Text(cx, cy + 4, s, role=role, size=size, anchor="middle").render())


class Route(Drawable):
    a: Point | None = None
    b: Point | None = None
    role: Role = "primary"
    shape: Shape = "line"
    k: float = 0.5
    width: float = 2.2
    ends: Ends = "end"
    dash: str | None = None
    opacity: float = 1.0
    points: list[Point] | None = None
    label: str | Seg | None = None
    label_at: float = 0.5
    label_role: Role | None = None
    label_size: float = 10.5
    label_pad: float = 9

    def __init__(self, a: Point | None = None, b: Point | None = None, role: Role = "primary", *,
                 shape: Shape = "line", k: float = 0.5, width: float = 2.2, ends: Ends = "end",
                 dash: str | None = None, opacity: float = 1.0, points: list[Point] | None = None,
                 label: str | Seg | None = None, label_at: float = 0.5, label_role: Role | None = None,
                 label_size: float = 10.5, label_pad: float = 9):
        super().__init__(a=a, b=b, role=role, shape=shape, k=k, width=width, ends=ends, dash=dash,
                         opacity=opacity, points=points, label=label, label_at=label_at,
                         label_role=label_role, label_size=label_size, label_pad=label_pad)

    def render(self) -> str:
        if self.points is not None:
            pts = list(self.points)
            d = _poly_d(pts)
            lpt = _poly_point(pts, self.label_at)
        elif self.shape in ("sweep", "arc"):
            (ax, ay), (bx, by) = self.a, self.b
            dx = bx - ax
            c1, c2 = (ax + dx * self.k, ay), (bx - dx * self.k, by)
            d = f"M{_n(ax)},{_n(ay)} C{_n(c1[0])},{_n(c1[1])} {_n(c2[0])},{_n(c2[1])} {_n(bx)},{_n(by)}"
            lpt = _bezier_point((ax, ay), c1, c2, (bx, by), self.label_at)
        else:
            p0, p1 = self.a, self.b
            pts = _elbow_points(self.shape, p0, p1, p1[0] - p0[0], p1[1] - p0[1], self.k)
            d = _poly_d(pts)
            lpt = _poly_point(pts, self.label_at)

        da = f' stroke-dasharray="{self.dash}"' if self.dash else ""
        op = f' opacity="{self.opacity}"' if self.opacity != 1.0 else ""
        ms = f' marker-start="url(#a-{self.role})"' if self.ends in ("start", "both") else ""
        me = f' marker-end="url(#a-{self.role})"' if self.ends in ("end", "both") else ""
        out = (f'<path d="{d}" fill="none" stroke="{color(self.role)}" stroke-width="{_g(self.width)}"'
               f'{op}{da}{ms}{me}/>')
        if self.label is not None:
            s, st = self.label if isinstance(self.label, tuple) else (self.label, {})
            out += _panel_label(lpt, s, role=self.label_role or st.get("role", self.role),
                                size=st.get("size", self.label_size), pad=self.label_pad)
        return out

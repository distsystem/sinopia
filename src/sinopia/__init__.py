"""sinopia — diagrams as code.

A figure is a tree of first-class pydantic models, each rendering itself to themed SVG. The name
is the reddish underdrawing of a fresco: you declare the geometry (the *sinopia*), and it renders
into the final picture. Positioned `Box`es expose named anchors, shape models are themed, and the
`Route` connector computes its own control points and bend joints (not hand-typed). The floor
equals hand-written SVG (drop to a raw `RawPath` any time); the helpers turn "place coordinates by
hand" into "compute coordinates". Closed-set params (`kind`/`shape`/`align`/…) are `Literal`s, so a
typo is a `ValidationError` at construction.

Theme-aware by default: colors resolve to `var(--bs-*)`, so an *inlined* figure follows the site's
light/dark theme. For a self-contained `<img>` figure, fill the palette with hex in place:
`sinopia.PALETTE.update({"primary": "#4263eb", ...})`.

Two ways to place geometry:

- Hand-placed `Box` + computed `Route` (no layout engine); render the `Figure`:
    import sinopia as S
    a, b = S.Box(40, 40, 200, 70), S.Box(440, 120, 200, 70)
    svg = S.Figure(720, 260,
        S.Markers("primary", "success"),
        S.Rect(a, "success"), S.Text(*a.at(.5, .4), "Neovim", role="success", weight=True, anchor="middle"),
        S.Rect(b, "primary"),
        S.Route(a.right, b.left, "primary", shape="sweep", label="winid ⟷ Editor"),
    ).render()

- Declarative `Row`/`Col`/`Grid` layout (coordinates computed); read anchors after layout:
    root = S.Col(S.Node("ZED", role="primary", kind="rect"),
                 S.Node("NEOVIM", role="success", kind="rect"), gap=20, align="stretch")
    svg = S.layout(root, S.Markers("primary"),
                   lambda: S.Route(root.children[0].bottom, root.children[1].top, "primary", shape="sweep"))
"""
from sinopia.arrange import PAD as PAD
from sinopia.arrange import LINE_H as LINE_H
from sinopia.arrange import Cell as Cell
from sinopia.arrange import Col as Col
from sinopia.arrange import Element as Element
from sinopia.arrange import Grid as Grid
from sinopia.arrange import Label as Label
from sinopia.arrange import Node as Node
from sinopia.arrange import Row as Row
from sinopia.arrange import Spacer as Spacer
from sinopia.arrange import layout as layout
from sinopia.primitives import PALETTE as PALETTE
from sinopia.primitives import Band as Band
from sinopia.primitives import Box as Box
from sinopia.primitives import Card as Card
from sinopia.primitives import Drawable as Drawable
from sinopia.primitives import Figure as Figure
from sinopia.primitives import Markers as Markers
from sinopia.primitives import RawPath as RawPath
from sinopia.primitives import Rect as Rect
from sinopia.primitives import RichText as RichText
from sinopia.primitives import Text as Text
from sinopia.primitives import color as color
from sinopia.primitives import mid as mid
from sinopia.route import Route as Route

__version__ = "0.3.0"

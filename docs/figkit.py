"""Figure helpers for these docs: the project's figure vocabulary (`stage`, `band` — thin
recipes over sinopia.Node that encode this site's taste, not the engine's) plus `show`, which
emits a figure for the carrier filter to inline. The vocabulary lives here beside the figures,
not in sinopia."""
import sinopia as S


def show(figure) -> None:
    """Print a figure as a ```{=html}``` raw block, for a `#| output: asis` cell. The
    `_filters/sinopia-carrier.lua` filter catches that block and stashes the SVG in a <script>,
    so it survives Quarto's deno-dom HTML post-processor (which lowercases camelCase attributes
    like viewBox). Accepts a sinopia model (rendered here) or an already-rendered SVG string."""
    svg = figure.render() if hasattr(figure, "render") else figure
    print("```{=html}\n" + svg + "\n```")


def band(text: str, role: str = "primary") -> S.Node:
    """A solid title band with centered white text."""
    return S.Node((text, {"role": "white", "weight": True, "size": 13, "anchor": "middle"}),
                  role=role, kind="band", rx=7, h=30)


def stage(title: str, *subs: str, role: str = "primary") -> S.Node:
    """A soft titled card: bold centered title over muted centered sub-lines."""
    lines = [(title, {"weight": True, "size": 12, "anchor": "middle"})]
    lines += [(s, {"role": "mut", "size": 9, "anchor": "middle"}) for s in subs]
    return S.Node(*lines, role=role, kind="rect", fill=0.07)

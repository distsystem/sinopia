"""Figure vocabulary for these docs — thin recipes over sinopia.Node. It lives beside the
figures, not in sinopia: these encode this site's taste (fills, sizes), not the engine's."""
import sinopia as S


def show(figure) -> None:
    """Emit a figure inside a ```{=html}``` raw block so Quarto inlines the SVG verbatim —
    camelCase attributes (viewBox, markerWidth) survive Pandoc. Use in a `#| output: asis` cell.
    Accepts a sinopia model (rendered here) or an already-rendered SVG string."""
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

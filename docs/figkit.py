"""Figure helpers for these docs: this site's figure vocabulary (`stage`, `band` — thin recipes
over sinopia.Node that encode this site's taste, not the engine's). The vocabulary lives here
beside the figures, not in sinopia; the Quarto inlining transport is the engine's own
`sinopia.quarto.emit`."""
import sinopia as S


def band(text: str, role: str = "primary") -> S.Node:
    """A solid title band with centered white text."""
    return S.Node((text, {"role": "white", "weight": True, "size": 13, "anchor": "middle"}),
                  role=role, kind="band", rx=7, h=30)


def stage(title: str, *subs: str, role: str = "primary") -> S.Node:
    """A soft titled card: bold centered title over muted centered sub-lines."""
    lines = [(title, {"weight": True, "size": 12, "anchor": "middle"})]
    lines += [(s, {"role": "mut", "size": 9, "anchor": "middle"}) for s in subs]
    return S.Node(*lines, role=role, kind="rect", fill=0.07)

"""Quarto adapter: inline a sinopia figure into a Quarto page, theme-aware.

Opt-in integration. The core engine emits plain SVG strings and is unaware of this transport;
import this module only from a Quarto figure cell. It pairs with `_filters/sinopia-carrier.lua`,
which stashes the SVG in a non-executable `<script>` so it survives Quarto's deno-dom HTML
post-processor (which would otherwise lowercase camelCase attributes like `viewBox` and break
scaling and markers).
"""
from sinopia.primitives import Figure


def emit(figure: Figure) -> None:
    """Print a figure as a ```{=html}``` raw block, for a `#| output: asis` cell. The carrier
    filter catches that block and stashes the SVG, so var(--bs-*) resolves against the live page."""
    print("```{=html}\n" + figure.render() + "\n```")

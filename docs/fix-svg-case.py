#!/usr/bin/env python3
"""Quarto post-render fix: Quarto's HTML post-processor parses inline SVG as HTML and
lowercases camelCase attributes (viewBox, markerWidth, …), which breaks figure scaling and
arrowheads. SVG attribute names are case-sensitive, so restore them in the built HTML."""
import os
import pathlib

CAMEL = {"viewbox=": "viewBox=", "markerwidth=": "markerWidth=", "markerheight=": "markerHeight=",
         "refx=": "refX=", "refy=": "refY="}

out = pathlib.Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
for html in out.rglob("*.html"):
    text = html.read_text()
    fixed = text
    for lower, camel in CAMEL.items():
        fixed = fixed.replace(lower, camel)
    if fixed != text:
        html.write_text(fixed)

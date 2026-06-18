"""Figures for the docs, drawn with sinopia — the live, self-referential examples. Each function
returns an inline SVG string; a .qmd cell renders it via `IPython.display.HTML(figures.x())`."""
import figkit as K

import sinopia as S


def loop() -> str:
    """The doc-driven-dev loop: a linear flow of stages, with rationale branching to git."""
    spec = [("discuss", "secondary", ()),
            ("draft", "primary", ("drafts/<slug>.qmd",)),
            ("review", "primary", ()),
            ("reflow", "success", ("when settled",)),
            ("evergreen", "success", ("current + intended",))]
    stages = [K.stage(name, *subs, role=role) for name, role, subs in spec]
    flow = S.Row(*stages, gap=38, align="center")
    git = K.stage("git: commit / PR", "history · rationale", role="warning")
    root = S.Col(flow, S.Spacer(h=46), git, gap=0, align="center")

    def edges():
        out = [S.Route(stages[i].right, stages[i + 1].left, "mut", shape="line", ends="end")
               for i in range(len(stages) - 1)]
        out.append(S.Route(stages[3].bottom, git.top, "warning", shape="sweep", ends="end",
                           label=("rationale", {"role": "warning", "size": 9.5})))
        return out

    return S.layout(root, S.Markers("mut", "warning"), edges, pad=18)


def model_tree() -> str:
    """sinopia's shape: a Figure composes a tree of frozen Drawable + Element models that render to SVG."""
    fig = K.stage("Figure", "the svg root", role="primary")
    shapes = S.Node(("Drawable models", {"weight": True, "size": 11.5}),
                    ("Rect · Band · Card", {"role": "mut", "size": 9.5}),
                    ("Text · RichText · RawPath", {"role": "mut", "size": 9.5}),
                    ("Route · Markers", {"role": "mut", "size": 9.5}),
                    role="primary", kind="card")
    elements = S.Node(("Element models", {"weight": True, "size": 11.5}),
                      ("Row · Col · Grid", {"role": "mut", "size": 9.5}),
                      ("Node · Label · Spacer · Cell", {"role": "mut", "size": 9.5}),
                      ("layout() computes geometry", {"role": "mut", "size": 9.5}),
                      role="success", kind="card")
    groups = S.Row(shapes, elements, gap=40, align="start")
    out = K.band("render() → themed SVG · var(--bs-*)", role="secondary")
    root = S.Col(fig, S.Spacer(h=28), groups, S.Spacer(h=24), out, gap=0, align="center")

    def edges():
        return [S.Route(fig.bottom, shapes.top, "mut", shape="sweep", ends="end"),
                S.Route(fig.bottom, elements.top, "mut", shape="sweep", ends="end"),
                S.Route(shapes.bottom, out.top, "mut", shape="sweep", ends="end"),
                S.Route(elements.bottom, out.top, "mut", shape="sweep", ends="end")]

    return S.layout(root, S.Markers("mut"), edges, pad=18)


def layout_engine() -> str:
    """Declarative layout: declare a tree, layout() computes coordinates, anchors feed connectors."""
    declare = K.stage("declare", "Row / Col / Grid", "of Box + Node", role="primary")
    compute = K.stage("layout()", "stretchable computes", "x / y / w / h", role="success")
    connect = K.stage("anchors", "node.right / .center", "feed Route", role="warning")
    flow = S.Row(declare, compute, connect, gap=44, align="center")

    def edges():
        return [S.Route(declare.right, compute.left, "mut", shape="line", ends="end"),
                S.Route(compute.right, connect.left, "mut", shape="line", ends="end")]

    return S.layout(flow, S.Markers("mut"), edges, pad=18)

#!/usr/bin/env python3
"""channels 图,声明式:Col[band, Row[5×channel], band] + 锚点连线。
坐标全由 layout 算;加一条通道 = 往 CHANNELS 加一项,整图自动重排。"""
import pathlib

import sinopia as S

S.PALETTE.update({"success": "#2f9e44", "primary": "#4263eb", "warning": "#e8590c",
                  "secondary": "#adb5bd", "ink": "#212529", "body": "#212529",
                  "bg": "#ffffff", "mut": "#868e96"})  # standalone hex, for file:// 预览
NV, ZD, CU = "success", "primary", "warning"

CHANNELS = [
    ("按键",        "nvim_input",       "down", ZD, "key-routing"),
    ("文本回流",    "on_lines",         "up",   NV, "sync-engine"),
    ("状态 / 高亮", "redraw push",      "up",   NV, "render-channel"),
    ("文本下推",    "buf_set_text",     "down", ZD, "sync-engine"),
    ("双向桥",      "zed.action/query", "bi",   CU, "bridge-api"),
]

cols, gaps = [], []
for title, mono, direction, role, name in CHANNELS:
    sp = S.Spacer(h=170)
    cols.append(S.Col(
        S.Label(title, weight=True, anchor="middle"),
        S.Label(mono, role="mut", size=9.5, mono=True, anchor="middle"),
        sp,
        S.Label(name, role=role, size=10, anchor="middle"),
        gap=5, align="center"))
    gaps.append((sp, direction, role))

mid = S.Row(*cols, gap=64, align="start", justify="between")
zed = S.Node(("ZED — 内容真相 · 渲染", {"role": ZD, "weight": True, "size": 14}),
             ("text::Buffer / MultiBuffer · EditorElement · LSP / AI / git", {"role": "mut", "size": 11}),
             role=ZD, kind="rect", fill=0.05, h=60)
nv = S.Node(("NEOVIM (--embed, headless) · user init.lua", {"role": NV, "weight": True, "size": 14}),
            ("模态 / motion / operator / text-object 引擎", {"role": "mut", "size": 11}),
            role=NV, kind="rect", fill=0.05, h=58)
root = S.Col(zed, mid, nv, gap=20, align="stretch")


def conns():
    out = []
    for sp, direction, role in gaps:
        cx, sy, h = sp.center[0], sp.box.y, sp.box.h
        a, b = ((cx, sy + h), (cx, sy)) if direction == "up" else ((cx, sy), (cx, sy + h))
        out.append(S.Route(a, b, role, shape="line", width=2.4, opacity=1.0,
                           ends=("both" if direction == "bi" else "end")))
    return out


svg = S.layout(root, S.Markers(NV, ZD, CU), conns, pad=16)
pathlib.Path(__file__).with_name("channels.svg").write_text(svg)
print("wrote channels.svg", len(svg), "B")

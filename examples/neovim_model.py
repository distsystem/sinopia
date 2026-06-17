#!/usr/bin/env python3
"""neovim_model 图,声明式移植(验收 artifact):Col[band, engine, instance, buffer, cells]
+ 锚点连线。坐标全由 layout 算,跨树指向线由 route 算控制点——零手填 box 坐标、零手调 bezier。"""
import pathlib

import sinopia as S

S.PALETTE.update({"success": "#2f9e44", "primary": "#4263eb", "warning": "#e8590c",
                  "secondary": "#adb5bd", "ink": "#212529", "body": "#212529",
                  "bg": "#ffffff", "mut": "#868e96"})  # standalone hex, for file:// 预览
NV = "success"

title = S.Node(("NEOVIM 模型 · 单一文本引擎 + 全局窗口",
                {"role": "white", "weight": True, "size": 13, "anchor": "middle"}),
               kind="band", role=NV, rx=7, h=30)

engine = S.Node(
    ("编辑引擎 · 模态状态机", {"role": NV, "weight": True, "size": 12.5}),
    ("normal ⇄ insert ⇄ visual ⇄ operator-pending ⇄ cmdline", {"role": "mut", "size": 10, "mono": True}),
    ("motion / operator / text-object 以 buffer 文本为输入;headless 无 UI 也完整运行 ciw · d/foo · >ip",
     {"role": "mut", "size": 9.5}),
    role=NV)


def window(name, sub, look):
    return S.Node((name, {"weight": True, "size": 11.5}),
                  (sub, {"role": "mut", "size": 9.5}),
                  (look, {"size": 10, "mono": True}),
                  role=NV, kind="rect", fill=0.06, rx=7, h=74)


winA = window("window A · winid", "视口:光标 / topline / 窗口局部选项", "→ 看 buf 3")
winB = window("window B · winid", "视口:光标 / topline", "→ 看 buf 7")
windows = S.Grid([winA, winB], col_gap=12)

instance = S.Col(
    S.Label("tabpage · 一组 window 的布局(tab 列表也是全局)", role=NV, size=11),
    windows,
    gap=8, align="stretch", pad=12)

buffer = S.Node(
    ("全局 buffer-list · 持久 · bufnr 唯一", {"role": NV, "weight": True, "size": 12.5}),
    ("buffer 独立于窗口存在,可被 0..N 窗口同时显示,关窗后仍作 hidden buffer 留存", {"role": "mut", "size": 9.5}),
    role=NV)


def cell(label, *, hidden=False):
    if hidden:
        return S.Node((label, {"role": "mut", "size": 10.5, "mono": True, "anchor": "middle"}),
                      role="secondary", kind="card", w=118, h=24, rx=5, dash="3 3", pad=4, line_h=14)
    return S.Node((label, {"size": 10.5, "mono": True, "anchor": "middle"}),
                  role=NV, kind="rect", fill=0.06, w=78, h=24, rx=5, pad=4, line_h=14)


buf3, buf7 = cell("buf 3"), cell("buf 7")
cells = S.Row(cell("buf 1"), buf3, buf7, cell("buf 9 (hidden)", hidden=True), gap=32, align="start")

caption = S.Label("window 与 buffer 多对多;buffer 承载文本,window 只是视口。"
                  ":e / :b / :split / :tabnew 改的都是这套结构。", role="mut", size=9.5)

root = S.Col(title, engine, instance, buffer, cells, caption, gap=12, align="stretch")


def deco():
    return [
        S.Rect(instance.box, NV, fill=0.0, stroke_width=1.4, rx=10, dash="5 4"),
        S.Route(winA.bottom, buf3.top, NV, shape="line", width=1.3, opacity=0.7),
        S.Route(winB.bottom, buf7.top, NV, shape="sweep", width=1.3, opacity=0.7),
    ]


svg = S.layout(root, S.Markers(NV), deco, pad=16)
pathlib.Path(__file__).with_name("neovim_model.svg").write_text(svg)
print("wrote neovim_model.svg", len(svg), "B")

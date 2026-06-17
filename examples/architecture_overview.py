#!/usr/bin/env python3
"""architecture_overview 图,声明式移植(Grid 主场):两个 plane 等宽并列(各带 bg 底色),
每个 plane 一列节点,跨平面 route(sweep) 带标签连接,底部光标交界带。
坐标全由 layout 算,跨平面控制点由 route 算——零手填 box 坐标、零手调 bezier。"""
import pathlib

import sinopia as S

S.PALETTE.update({"success": "#2f9e44", "primary": "#4263eb", "warning": "#e8590c",
                  "secondary": "#adb5bd", "ink": "#212529", "body": "#212529",
                  "bg": "#ffffff", "mut": "#868e96"})  # standalone hex, for file:// 预览
NV, ZD, CU = "success", "primary", "warning"


def header(title, sub, role):
    return S.Node((title, {"role": role, "weight": True, "size": 14}),
                  (sub, {"role": "mut", "size": 11.5}),
                  role=role, kind="rect", fill=0.08, rx=10)


def colband(text, role):
    return S.Node((text, {"role": "white", "weight": True, "size": 13, "anchor": "middle"}),
                  role=role, kind="band", rx=7, h=28)


def viewport(name, sub, cursor):
    return S.Node((name, {"weight": True, "size": 11}),
                  (sub, {"role": "mut", "size": 9}),
                  (cursor, {"role": CU, "size": 9.5, "mono": True}),
                  role=NV, kind="rect", fill=0.06, rx=6)


# ── Neovim 控制平面（左）─────────────────────────────────────────────
nv_band = colband("NEOVIM · headless --embed", NV)
engine = S.Node(
    ("编辑引擎 · 模态状态机", {"role": NV, "weight": True, "size": 12.5}),
    ("normal ⇄ insert ⇄ visual ⇄ op-pending ⇄ cmdline", {"role": "mut", "size": 10, "mono": True}),
    ("在 bufnr 镜像上算 motion / operator → 结果落入 window 光标", {"role": "mut", "size": 9.5}),
    role=NV)
winA = viewport("window 1", "winid · 视口", "光标₁ / topline")
winB = viewport("window 2", "winid · 视口", "光标₂ / topline")
windows = S.Grid([winA, winB], col_gap=14)
bufnr = S.Node(
    ("bufnr X · 扁平镜像", {"role": NV, "weight": True, "size": 12}),
    ("文本只一份 · 两个 window 同看(无收敛问题)", {"role": "mut", "size": 9.5}),
    ("on_lines ↑   ·   buf_set_text ↓", {"role": "mut", "size": 10, "mono": True}),
    role=NV)
instance = S.Col(
    S.Label("Neovim 实例 i · headless(不维护 window/tab/buffer-list)", role=NV, size=11),
    windows,
    S.Label("buffer ↔ window = 1:N", role="mut", size=9, anchor="middle"),
    bufnr,
    gap=8, align="stretch", pad=12, bg=(NV, {"fill": 0.0, "stroke_width": 1.4, "rx": 10, "dash": "5 4"}))
nv_help = S.Node(
    (":help / :Man / 插件 scratch", {"role": NV, "weight": True, "size": 12}),
    ("Neovim 自造 buffer · truth = Neovim", {"role": "mut", "size": 10}),
    role=NV)
nv_plane = S.Col(
    nv_band, engine, instance, nv_help,
    S.Label("window / tab / buffer-list 委托 Zed:实例只当“单 buffer 引擎”。", role="mut", size=9.5),
    gap=10, align="stretch", pad=14, bg=(NV, {"fill": 0.04, "stroke_width": 0, "rx": 14}))

# ── Zed 数据平面（右）───────────────────────────────────────────────
zd_band = colband("ZED · 视图 / 内容 两棵树", ZD)
pane = S.Node([("Pane", {"weight": True}), (" · tab 条 · 布局委托 Zed", {"role": "mut", "size": 10})],
              role=ZD, kind="card", rx=6)


def editor(name, cursor):
    return S.Node((name, {"weight": True, "size": 11.5}),
                  ("视图 · tab item", {"role": "mut", "size": 9}),
                  (cursor, {"role": CU, "size": 9.5, "mono": True}),
                  role=ZD, kind="rect", fill=0.06, rx=8)


editorA, editorB = editor("Editor A", "光标₁ / scroll"), editor("Editor B", "光标₂ / scroll")
editors = S.Grid([editorA, editorB], col_gap=14)
language = S.Node([("language::Buffer", {"weight": True}), (" ≤1 file · BufferStore 去重(真相)", {"role": "mut", "size": 9})],
                  role=ZD, kind="card", rx=6)
textbuf = S.Node([("text::Buffer", {"weight": True}), (" CRDT rope", {"role": "mut", "size": 9})],
                 role=ZD, kind="card", rx=6)
multibuffer = S.Col(
    S.Label("MultiBuffer · 主键", role=CU, size=12.5, weight=True),
    S.Label("拼 1..N buffer · 绑定 ↔ 一个 (实例, nvim bufnr)", role="mut", size=9.5),
    language, textbuf,
    gap=6, align="stretch", pad=10, bg=(CU, {"fill": 0.10, "stroke_width": 2.4, "rx": 9}))
projection = S.Node(
    ("只读投影 Editor", {"role": NV, "weight": True, "size": 12}),
    (":help 投影 · 活镜像(on_lines 跟随)· 可导航", {"role": "mut", "size": 9.5}),
    role=NV)
zd_plane = S.Col(
    zd_band, pane, editors,
    S.Label("MultiBuffer ↔ Editor = 1:N(分屏 clone 共享)", role=ZD, size=9.5, anchor="middle"),
    multibuffer, projection,
    gap=10, align="stretch", pad=14, bg=(ZD, {"fill": 0.04, "stroke_width": 0, "rx": 14}))

# ── 光标交界带（底部，跨两平面）──────────────────────────────────────
cursor_band = S.Row(
    S.Col(S.Label("Neovim 侧", role=NV, size=11.5, weight=True),
          S.Label("motion / operator 算出 → 存入 window 光标 → 镜像给 Zed 渲染", role="ink", size=11),
          gap=4, align="start"),
    S.Col(S.Label("Zed 侧", role=ZD, size=11.5, weight=True, anchor="end"),
          S.Label("鼠标 / 搜索 / LSP 跳转发起 → 写回 Neovim 对应 window", role="ink", size=11, anchor="end"),
          gap=4, align="end"),
    justify="between", align="center", pad=14, bg=(CU, {"fill": 0.10, "stroke_width": 2.4, "rx": 12}))
cursor_section = S.Col(
    S.Label("光标 · 唯一双向交界(corner case 集中此处,其余皆单向)", role=CU, size=12.5, anchor="middle"),
    cursor_band, gap=8, align="stretch")

# ── 组装：两 plane 等宽 Grid + 表头 + 光标带（GAP 留中央通道给跨平面弧线）──
GAP = 340
headers = S.Grid([header("控制平面 · truth = Neovim", "模态 / motion / operator / 窗口生命周期 / 光标逻辑", NV),
                  header("数据平面 · truth = Zed", "内容 / 文件 I/O / undo / LSP / git / 协作 / MultiBuffer", ZD)],
                 col_gap=GAP)
bodies = S.Grid([nv_plane, zd_plane], col_gap=GAP)
root = S.Col(headers, bodies, cursor_section, gap=14, align="stretch", pad=16)


def links():
    return [
        S.Route(windows.right, editors.left, ZD, shape="sweep", ends="both", width=1.8,
                label=("window ⟷ Editor · N 视图收束同一 buffer · 各持光标", {"role": ZD, "size": 10})),
        S.Route(bufnr.right, multibuffer.left, ZD, shape="sweep", ends="both", width=3,
                label=("绑定主键脊柱:nvim bufnr ⟷ MultiBuffer · 一份扁平镜像 + 回声基线", {"role": ZD, "size": 10.5})),
        S.Route(nv_help.right, projection.left, NV, shape="sweep", ends="both", width=2,
                label=("zed_buf_event · 只读可导航 · teardown 双向", {"role": NV, "size": 10})),
        S.Route(cursor_band.at(0.30, 0.5), cursor_band.at(0.70, 0.5), CU, shape="line",
                ends="both", width=2.6),
    ]


svg = S.layout(root, S.Markers(NV, ZD, CU), links, pad=16)
pathlib.Path(__file__).with_name("architecture_overview.svg").write_text(svg)
print("wrote architecture_overview.svg", len(svg), "B")

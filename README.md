# doc-driven-dev

把项目文档当作工作面的工作流,配上 **sinopia**:一个 diagrams-as-code 包,图由代码生成而非手绘,
并跟随页面的明暗主题。本仓库用这套工具给自己写文档:文档站上每张图都由 sinopia 在构建期生成,
所以这份文档本身就是一份可用的样例。

## 两件工具

- **工作流** —— 单一入口的 [Quarto](https://quarto.org) 文档库,只装*当前与计划中*的状态。讨论以
  gitignore 的草稿进行,草稿和正式文档长得一模一样,谈定后回流进 evergreen 页面;历史与缘由交给
  git,不进文档。见[工作流](docs/doc-driven-dev/workflow.qmd)。
- **sinopia** —— 在 Python 里把图组合成一棵一等模型的树(`Box` 锚点、带主题的形状、自算控制点的
  `Route` 连接器、声明式 `Row` / `Col` / `Grid` 布局),再把 SVG 内联进来,让 `var(--bs-*)` 颜色
  跟随主题。见 [sinopia](docs/sinopia/sinopia.qmd)。

## 循环

```
  讨论 ──▶ 草稿 ──▶ 评审 ──▶ 回流 ──▶ evergreen 文档
        drafts/<slug>.qmd      (谈定)     (当前状态)
        gitignored                │
                                  ▼
                        缘由 ──▶ git commit / PR
```

## 运行文档

```bash
pixi run render      # 静态构建到 _site/
pixi run open        # render 后用浏览器打开 _site/index.html
```

项目环境自带 Quarto 和一个 editable 安装的 sinopia,所以图表 cell 会执行并内联其 SVG。

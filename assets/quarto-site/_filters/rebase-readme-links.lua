--- Pandoc Lua filter — rewrite docs/X.md → X.md inside the included README.
---
--- README.md (at repo root) writes links like [page](docs/page.md) so they
--- resolve on GitHub. When included into docs/index.qmd via
--- {{< include ../README.md >}}, the docs/ prefix becomes wrong.

local function rewrite(target)
  return (target:gsub("^docs/", ""))
end

function Link(el)
  el.target = rewrite(el.target)
  return el
end

function Image(el)
  el.src = rewrite(el.src)
  return el
end

--- components.lua — on the typst target, lower the semantic component divs/spans
--- (styled by CSS on HTML via _styles/_base) into the kami.typ #function calls.
--- HTML and other formats are untouched: the bare classes are handled by CSS.
--- Bottom-up traversal means nested components (a .stat inside a .card) are already
--- lowered to typst raws by the time their container is rendered.

if not quarto.doc.isFormat("typst") then return {} end

local stringify = pandoc.utils.stringify

local function typst_of(blocks)
  return pandoc.write(pandoc.Pandoc(blocks), "typst")
end

local function q(s)
  return '"' .. s:gsub('\\', '\\\\'):gsub('"', '\\"') .. '"'
end

local function stat_parts(div)
  local num, lab = "", ""
  pandoc.walk_block(div, { Span = function(s)
    if s.classes:includes("num") then num = stringify(s)
    elseif s.classes:includes("lab") then lab = stringify(s) end
  end })
  return num, lab
end

local function Div(div)
  local c = div.classes
  if c:includes("card") then
    return pandoc.RawBlock("typst", "#card[\n" .. typst_of(div.content) .. "]")
  elseif c:includes("stat") then
    local num, lab = stat_parts(div)
    return pandoc.RawBlock("typst", "#stat(" .. q(num) .. ", " .. q(lab) .. ")")
  elseif c:includes("hero") then
    return pandoc.RawBlock("typst", "#hero[\n" .. typst_of(div.content) .. "]")
  elseif c:includes("steps") then
    return pandoc.RawBlock("typst", "#steps[\n" .. typst_of(div.content) .. "]")
  elseif c:includes("timeline") then
    return pandoc.RawBlock("typst", "#timeline[\n" .. typst_of(div.content) .. "]")
  elseif c:includes("dash") then
    return pandoc.RawBlock("typst", "#dash-list[\n" .. typst_of(div.content) .. "]")
  end
  return nil
end

local function Span(s)
  local c = s.classes
  if c:includes("eyebrow") then
    return pandoc.RawInline("typst", "#eyebrow[" .. stringify(s) .. "]")
  elseif c:includes("tag") then
    local tier = c:includes("faint") and "faint" or (c:includes("strong") and "strong" or nil)
    if tier then
      return pandoc.RawInline("typst", "#tag(tier: " .. q(tier) .. ")[" .. stringify(s) .. "]")
    end
    return pandoc.RawInline("typst", "#tag[" .. stringify(s) .. "]")
  end
  return nil
end

return { { Div = Div, Span = Span } }

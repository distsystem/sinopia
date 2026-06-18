--- Quarto Lua filter — `.compare-option` directive
---
--- ::: {.compare-option verdict=success tag="Option C" title="..."}
--- content
--- :::
---
--- → grid column wrapping a Bootstrap card with:
---     · tag (small monospace label, top)
---     · title (h5 styled span)
---     · content (any markdown)
---     · verdict badge (bottom-left, auto-aligned via mt-auto)
---
--- Verdict drives both the top-border color and the badge color.
--- Wrap multiple `.compare-option` in `::: {.grid}` to get a row.

local default_labels = {
  success = "Adopted",
  warning = "Trade-off",
  danger  = "Rejected",
  info    = "Note",
}

local function span(text, classes)
  return pandoc.Plain({
    pandoc.Span(pandoc.Str(text), pandoc.Attr("", classes))
  })
end

local function compare_option(div)
  if not div.classes:includes("compare-option") then return nil end

  local verdict = div.attributes["verdict"] or "primary"
  local tag     = div.attributes["tag"]     or ""
  local title   = div.attributes["title"]   or ""
  local label   = div.attributes["label"]   or default_labels[verdict] or verdict

  local body = pandoc.List()
  if tag   ~= "" then body:insert(span(tag,   {"text-muted", "small", "font-monospace", "text-uppercase"})) end
  if title ~= "" then body:insert(span(title, {"h5", "fw-semibold", "mb-2", "d-block"})) end
  for _, b in ipairs(div.content) do body:insert(b) end
  body:insert(span(label, {"badge", "text-bg-" .. verdict, "mt-auto", "align-self-start"}))

  local card_body = pandoc.Div(body, pandoc.Attr("", {"card-body", "d-flex", "flex-column"}))
  local card      = pandoc.Div({card_body}, pandoc.Attr("", {
    "card", "border-0", "border-top", "border-3", "border-" .. verdict, "h-100"
  }))
  return pandoc.Div({card}, pandoc.Attr("", {"g-col-12", "g-col-md-4", "d-flex"}))
end

return { { Div = compare_option } }

--- Carry sinopia figures past Quarto's deno-dom HTML post-processor, which lowercases
--- inline-SVG camelCase attributes (viewBox, markerWidth, …) and breaks scaling/markers.
---
--- The SVG is stashed in a non-executable <script> (raw-text element → deno-dom leaves its
--- content verbatim, camelCase intact); a one-time injector sets it into a placeholder div
--- at load, where the browser's HTML parser applies the SVG foreign-content adjustment
--- (restoring camelCase) and var(--bs-*) resolves against the live page for theming.
---
--- Docs-side only: sinopia (src/) just emits SVG strings and is unaware of this transport.

local injected = false

function RawBlock(el)
  if el.format == "html" and el.text:match("^%s*<svg") then
    injected = true
    return pandoc.RawBlock("html",
      '<div class="sinopia-fig"></div>\n'
      .. '<script type="application/sinopia">' .. el.text .. '</script>')
  end
end

function Pandoc(doc)
  if injected then
    doc.blocks:insert(pandoc.RawBlock("html", [[<script>
document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll('script[type="application/sinopia"]').forEach(function (s) {
    var fig = s.previousElementSibling;
    if (fig && fig.classList.contains("sinopia-fig")) fig.innerHTML = s.textContent;
  });
});
</script>]]))
  end
  return doc
end

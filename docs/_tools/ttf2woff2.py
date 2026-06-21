"""Regenerate the LXGW WenKai woff2 from the installed TTF.

Run on LXGW version bumps:  pixi run make-fonts

Output goes to docs/fonts/, committed to this repo and served via jsDelivr-gh
(cdn.jsdelivr.net/gh/<owner>/<repo>@<ref>/docs/fonts/...), which kami's @font-face
references with local() first. It is NOT self-hosted in _site. The official LXGW
repo can't be used directly: its fonts are git-LFS/Release, unreachable via jsDelivr.
"""

import glob
from pathlib import Path

from fontTools.ttLib import TTFont

FONT_DIRS = (
    "/usr/share/fonts",
    str(Path.home() / ".local/share/fonts"),
    str(Path.home() / ".fonts"),
)
OUT = Path("docs/fonts")
WEIGHTS = ("Regular", "Medium")


def find_ttf(weight: str) -> Path:
    for base in FONT_DIRS:
        hits = glob.glob(f"{base}/**/LXGWWenKai-{weight}.ttf", recursive=True)
        if hits:
            return Path(hits[0])
    raise SystemExit(f"LXGWWenKai-{weight}.ttf not found; install lxgw-wenkai or edit FONT_DIRS")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for weight in WEIGHTS:
        font = TTFont(find_ttf(weight))
        font.flavor = "woff2"
        dst = OUT / f"LXGWWenKai-{weight}.woff2"
        font.save(dst)
        print(f"{dst} ({dst.stat().st_size / 1048576:.1f} MB)")


if __name__ == "__main__":
    main()

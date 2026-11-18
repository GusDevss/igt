#!/usr/bin/env python3
"""Extrae los iconos usados (Font Awesome Pro/Brands, Caseicon, Flaticon del tema) a SVG individuales.

Se ejecuta una sola vez; el resultado queda versionado en site/icons/.
"""
import os
import re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, "source", "assets")
OUT = os.path.join(ROOT, "site", "icons")
FA = os.path.join(A, "plugins/bravis-addons/assets/libs/font-awesome-pro")
FA_CSS = open(os.path.join(FA, "css/all.min.css")).read()
FONTS = {
    "fal": os.path.join(FA, "webfonts/fa-light-300.ttf"),
    "far": os.path.join(FA, "webfonts/fa-regular-400.ttf"),
    "fas": os.path.join(FA, "webfonts/fa-solid-900.ttf"),
    "fab": os.path.join(FA, "webfonts/fa-brands-400.ttf"),
    "caseicon": os.path.join(A, "theme/assets/fonts/caseicon/caseicon.ttf"),
    "flaticon": os.path.join(A, "theme/assets/fonts/flaticon/fonts/flaticon.ttf"),
}
CSS = {
    "caseicon": open(os.path.join(A, "theme/assets/css/caseicon.css")).read(),
    "flaticon": open(os.path.join(A, "theme/assets/fonts/flaticon/css/flaticon.css")).read(),
}

ICONS = """
far dumbbell; fas dumbbell; fal dumbbell; far piggy-bank; far weight-hanging; fas weight-hanging; far ruler-triangle; far recycle;
far layer-group; far landmark; far house-return; far hotel; far hospital-user; far heartbeat; far graduation-cap;
far child; fal child; far briefcase; fal tools; far tools; fal building; fab instagram; fab facebook-f; fab whatsapp;
far angle-double-right; far clock; fal phone-rotary; fal map-marker-alt; fal envelope; far shield-check; far shipping-fast;
far search; far plus; fal award; far user-shield; far handshake-alt; far gem; far exclamation-triangle; far cubes; fal user-check;
caseicon search; caseicon long-arrow-right-three; caseicon play1; caseicon angle-arrow-down; caseicon close;
flaticon right-chevron; flaticon weight; flaticon virtual-reality-fitness; flaticon gym; flaticon pass
"""

_fonts = {}


def font(key):
    if key not in _fonts:
        _fonts[key] = TTFont(FONTS[key])
    return _fonts[key]


def codepoint(style, name):
    if style in CSS:
        m = re.search(r"\.%s-%s:+before\s*\{\s*content:\s*[\"']\\([0-9a-fA-F]+)" % (style, re.escape(name)), CSS[style])
    else:
        m = re.search(r"\.fa-%s:before\{content:\"\\([0-9a-f]+)\"" % re.escape(name), FA_CSS)
    if not m:
        raise SystemExit(f"sin codepoint: {style} {name}")
    return int(m.group(1), 16)


def to_svg(style, name):
    f = font(style)
    cmap = f.getBestCmap()
    gname = cmap[codepoint(style, name)]
    gs = f.getGlyphSet()
    g = gs[gname]
    bp = BoundsPen(gs)
    g.draw(bp)
    xmin, ymin, xmax, ymax = bp.bounds
    upm = f["head"].unitsPerEm
    asc = f["hhea"].ascent
    desc = f["hhea"].descent
    pen = SVGPathPen(gs)
    g.draw(pen)
    # viewBox con el ancho de avance y la altura de línea de la fuente (como se ve el glifo en texto)
    adv = g.width
    h = asc - desc
    path = pen.getCommands()
    vb = f"0 {-asc} {adv} {h}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">'
            f'<path transform="scale(1,-1)" d="{path}"/></svg>'), adv / h


def main():
    os.makedirs(OUT, exist_ok=True)
    for item in ICONS.replace("\n", " ").split(";"):
        item = item.strip()
        if not item:
            continue
        style, name = item.split()
        try:
            svg, ratio = to_svg(style, name)
        except SystemExit as e:
            print(e)
            continue
        fn = f"{style}-{name}.svg"
        open(os.path.join(OUT, fn), "w").write(svg)
        print(fn, round(ratio, 3), len(svg))


if __name__ == "__main__":
    main()

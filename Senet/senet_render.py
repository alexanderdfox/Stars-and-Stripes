"""Layered full-body senator SVG (1200×2400) for 3D pipelines."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from era_clothing import (  # noqa: E402
    coat_for_era,
    legs_breeches_stockings,
    legs_trousers,
    military_extras,
    neckwear_layer,
    shoes,
    shirt_layer,
    torso_base,
    trouser_color,
    uses_breeches,
    vest_color_for,
    waist_band,
    waistcoat,
    arms_for_era,
    shows_vest,
)
from generate_presidents import (  # noqa: E402
    COAT_COLORS,
    SKIN,
    head_face,
    render_brows,
    render_ears,
    render_face_extras,
    render_facial_hair,
    render_glasses,
    render_hair,
    render_neck,
    render_nose,
    skin_tones,
    face_ellipse,
    hair_temple_band,
    top_hat_crown,
    top_hat_brim,
)
from mesh_ready import finalize_svg_for_3d  # noqa: E402
from presidents_look import Look  # noqa: E402
from senators_look import props_for  # noqa: E402

VIEWBOX = "0 0 1200 2400"
WIDTH, HEIGHT = 1200, 2400
SCALE_X, SCALE_Y = 1.5, 2.0
CHROMA_BG = "#3cb868"
OUTLINE = "#0d0d0d"
OUTLINE_W = 2.4


def _gradients() -> str:
    return """
  <defs>
    <linearGradient id="skin-shade" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#000" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="coat-shade" x1="0.5" y1="0" x2="0.5" y2="1">
      <stop offset="0%" stop-color="#fff" stop-opacity="0.08"/>
      <stop offset="55%" stop-color="#000" stop-opacity="0"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0.12"/>
    </linearGradient>
    <pattern id="fabric-weave" width="8" height="8" patternUnits="userSpaceOnUse">
      <rect width="4" height="8" fill="#000" fill-opacity="0.03"/>
    </pattern>
  </defs>"""


def _outline_wrap(inner: str, scale: float = 1.0) -> str:
    """Duplicate filled geometry as hairline stroke for print/3D edge reference."""
    if not inner.strip():
        return ""
    sw = OUTLINE_W / scale
    return f'<g id="outlines" fill="none" stroke="{OUTLINE}" stroke-width="{sw}" stroke-linejoin="round" opacity="0.85">\n{inner}\n  </g>'


def _split_head(look: Look, s: tuple) -> tuple[str, str, str]:
    head, hand, _, _, nose_c, mouth_c = s
    rx, ry, cy = face_ellipse(look)
    hc = look.hair_color
    neck = render_neck(look, head, cy, ry, rx)
    mouth = f'<path fill="{mouth_c}" d="M375 408 Q400 418 425 408 Q420 412 400 414 Q380 412 375 408 Z"/>'
    hair = render_hair(look, hc, head)
    beard = render_facial_hair(look, hc)

    if look.top_hat:
        hair_block = f"""{hair}
  {top_hat_crown(cy, ry, rx)}
  {beard}
  {top_hat_brim(cy, ry, rx)}"""
    else:
        hair_block = f"""{hair_temple_band(look, hc, head, cy, ry)}
  {hair}
  {beard}"""

    head_g = f"""
  <ellipse fill="{head}" ry="{ry}" rx="{rx}" cy="{cy}" cx="400"/>
  {neck}
  {render_ears(look, head)}
  <ellipse fill="#1a2a4a" ry="13" rx="8" cy="348" cx="372"/>
  <ellipse fill="#1a2a4a" ry="13" rx="8" cy="348" cx="428"/>
  {render_brows(look)}
  {render_nose(look, nose_c)}
  {mouth}
  {render_face_extras(look, head)}"""

    hair_g = hair_block.strip()
    acc_g = render_glasses(look)
    return head_g.strip(), hair_g, acc_g


def render_body(look: Look, s: tuple) -> str:
    if uses_breeches(look):
        return legs_breeches_stockings(look, s)
    return legs_trousers(look, trouser_color(look, COAT_COLORS.get(look.coat, COAT_COLORS["charcoal"])[0]))


def render_clothing_layers(look: Look, main: str, trim: str, s: tuple) -> str:
    parts = [
        shoes(look),
        waist_band(look, trouser_color(look, main) if not uses_breeches(look) else s[1]),
        torso_base(look, s),
        shirt_layer(look),
    ]
    if shows_vest(look):
        parts.append(waistcoat(look, vest_color_for(look)))
    parts.extend(
        [
            arms_for_era(look, s, main),
            coat_for_era(look, main, trim),
            neckwear_layer(look),
        ]
    )
    return "\n".join(parts)


def generate_senator_svg(look: Look, record_name: str, primary_year: int) -> str:
    main, _, trim = COAT_COLORS.get(look.coat, COAT_COLORS["charcoal"])
    s = skin_tones(look)
    body = render_body(look, s)
    clothing = render_clothing_layers(look, main, trim, s)
    head, hair, accessories = _split_head(look, s)
    props = props_for(look)
    mil = military_extras(look)
    accessories = "\n".join(x for x in (accessories, mil, props) if x.strip())

    desc = (
        f"Full-body portrait of {record_name}, U.S. Senator (primary service from {primary_year}). "
        "Likeness informed by historical portraits and photographs. Mesh-ready layered SVG."
    )

    figure_inner = f"""
    <g id="body" fill-rule="nonzero">
{body}
    </g>
    <g id="clothing" fill-rule="nonzero">
{clothing}
    </g>
    <g id="head" fill-rule="nonzero">
{head}
    </g>
    <g id="hair" fill-rule="nonzero">
{hair}
    </g>
    <g id="accessories" fill-rule="nonzero">
{accessories}
    </g>"""

    # Outlines mirror major filled groups (scaled space)
    outline_src = f"{body}\n{clothing}\n{head}\n{hair}"

    raw = f'''<svg xmlns="http://www.w3.org/2000/svg"
  viewBox="{VIEWBOX}"
  width="{WIDTH}" height="{HEIGHT}"
  shape-rendering="geometricPrecision"
  aria-labelledby="title desc">
  <title id="title">{record_name} — U.S. Senator ({primary_year})</title>
  <desc id="desc">{desc}</desc>
  <metadata>
    Senet collection v1. Coordinate space 1200×2400; inner figure scaled 1.5×2 from 800×1200 rig.
    Layers: body, clothing, head, hair, accessories. Optimized for Blender/Unity extrusion.
  </metadata>
{_gradients()}
  <g id="background">
    <rect width="{WIDTH}" height="{HEIGHT}" fill="{CHROMA_BG}"/>
  </g>
  <g id="figure" transform="scale({SCALE_X} {SCALE_Y})">
{figure_inner}
  </g>
  <g transform="scale({SCALE_X} {SCALE_Y})">
{_outline_wrap(outline_src)}
  </g>
</svg>
'''
    return finalize_svg_for_3d(raw)

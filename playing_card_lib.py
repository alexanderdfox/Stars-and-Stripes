#!/usr/bin/env python3
"""Shared USD playing-card builder (textures, materials, geometry, deck assembly)."""

from __future__ import annotations

import json
import math
import os
import re
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Standard poker card proportions (meters)
CARD_W = 0.0635
CARD_H = 0.0889
CARD_T = 0.0005
HALF_W = CARD_W / 2
HALF_H = CARD_H / 2
HALF_T = CARD_T / 2

# ~3.2 mm corner radius (standard poker card)
CORNER_RADIUS = 0.0032
CORNER_SEGMENTS = 6

TEXTURE_SIZE = (630, 882)  # 2.5:3.5 aspect
CORNER_RADIUS_PX = max(8, round(CORNER_RADIUS / CARD_W * TEXTURE_SIZE[0]))
CARD_BORDER_PX = 14
FACE_BORDER_COLOR = (248, 246, 242)

RANK_LABELS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUIT_NAMES = ["Spades", "Hearts", "Diamonds", "Clubs"]
SUIT_ALIASES = {
    "s": "Spades",
    "spades": "Spades",
    "spade": "Spades",
    "h": "Hearts",
    "hearts": "Hearts",
    "heart": "Hearts",
    "d": "Diamonds",
    "diamonds": "Diamonds",
    "diamond": "Diamonds",
    "c": "Clubs",
    "clubs": "Clubs",
    "club": "Clubs",
}
SUIT_COLORS = {
    "Spades": "#1a1a22",
    "Hearts": "#b91c1c",
    "Diamonds": "#b91c1c",
    "Clubs": "#1a1a22",
}
SUIT_BG = {
    "Spades": "#f8f6f2",
    "Hearts": "#fff5f5",
    "Diamonds": "#fff8f8",
    "Clubs": "#f4faf4",
}


@dataclass(frozen=True)
class CardSpec:
    name: str
    slug: str
    rank_label: str
    suit_name: str
    emoji: str
    label: str = ""
    metadata: dict[str, str] = field(default_factory=dict)

    @property
    def display_label(self) -> str:
        return self.label or self.name


def slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", text.strip())
    return slug.strip("_") or "Card"


def normalize_rank(rank: str) -> str:
    rank = rank.strip().upper()
    if rank in RANK_LABELS:
        return rank
    if rank.isdigit():
        n = int(rank)
        if 1 <= n <= 10:
            return RANK_LABELS[n - 1]
        raise ValueError(f"Invalid rank number: {rank}")
    raise ValueError(f"Invalid rank: {rank!r} (use A, 2–10, J, Q, K)")


def normalize_suit(suit: str) -> str:
    key = suit.strip().lower()
    if key in SUIT_ALIASES:
        return SUIT_ALIASES[key]
    title = suit.strip().title()
    if title in SUIT_NAMES:
        return title
    raise ValueError(f"Invalid suit: {suit!r} (use Spades, Hearts, Diamonds, Clubs)")


def emoji_for_rank_suit(rank_label: str, suit_name: str) -> str:
    rank_i = RANK_LABELS.index(rank_label)
    suit_i = SUIT_NAMES.index(suit_name)
    code = 0x1F0A0 + suit_i * 0x10 + (rank_i + 1)
    return chr(code)


def emoji_for_index(card_index: int) -> tuple[str, str, str]:
    """Map 0-based index to Unicode playing-card glyph, rank, suit."""
    suit_i = card_index // 13
    rank_i = card_index % 13
    if suit_i >= len(SUIT_NAMES):
        raise ValueError(f"Index {card_index} exceeds a 52-card deck")
    rank_label = RANK_LABELS[rank_i]
    suit_name = SUIT_NAMES[suit_i]
    return emoji_for_rank_suit(rank_label, suit_name), rank_label, suit_name


def make_card_spec(
    name: str,
    *,
    slug: str = "",
    rank: str = "",
    suit: str = "",
    index: int | None = None,
    emoji: str = "",
    label: str = "",
    metadata: dict[str, str] | None = None,
) -> CardSpec:
    if index is not None:
        auto_emoji, rank_label, suit_name = emoji_for_index(index)
    else:
        if not rank or not suit:
            raise ValueError("Provide --rank and --suit, or --index")
        rank_label = normalize_rank(rank)
        suit_name = normalize_suit(suit)
        auto_emoji = emoji_for_rank_suit(rank_label, suit_name)

    return CardSpec(
        name=name,
        slug=slug or slugify(name),
        rank_label=rank_label,
        suit_name=suit_name,
        emoji=emoji or auto_emoji,
        label=label,
        metadata=metadata or {},
    )


def card_paths(output_dir: Path) -> dict[str, Path]:
    paths = {
        "base": output_dir,
        "cards": output_dir / "cards",
        "face_tex": output_dir / "textures" / "faces",
        "back_tex": output_dir / "textures" / "backs",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def texture_asset(path: Path) -> str:
    """Absolute texture path so deck.usda and card files both resolve reliably."""
    return path.resolve().as_posix()


def rel_asset(path: Path, from_file: Path) -> str:
    rel = os.path.relpath(path.resolve(), from_file.parent.resolve()).replace(os.sep, "/")
    return rel if rel.startswith(".") else f"./{rel}"


def _indent(block: str, spaces: int) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line else "" for line in block.strip("\n").splitlines())


def _hex_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _load_fonts() -> tuple[ImageFont.FreeTypeFont | ImageFont.ImageFont, ImageFont.FreeTypeFont | ImageFont.ImageFont]:
    emoji_paths = [
        "/System/Library/Fonts/Apple Color Emoji.ttc",
        "/System/Library/Fonts/Supplemental/Apple Color Emoji.ttc",
        "/Library/Fonts/Apple Color Emoji.ttc",
    ]
    label_paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    emoji_font: ImageFont.FreeTypeFont | ImageFont.ImageFont = ImageFont.load_default()
    label_font: ImageFont.FreeTypeFont | ImageFont.ImageFont = ImageFont.load_default()
    for path in emoji_paths:
        if os.path.isfile(path):
            try:
                emoji_font = ImageFont.truetype(path, size=220)
                break
            except OSError:
                continue
    for path in label_paths:
        if os.path.isfile(path):
            try:
                label_font = ImageFont.truetype(path, size=56)
                break
            except OSError:
                continue
    return emoji_font, label_font


_EMOJI_FONT, _LABEL_FONT = _load_fonts()


def _rounded_corner_mask(size: tuple[int, int] = TEXTURE_SIZE) -> Image.Image:
    w, h = size
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=CORNER_RADIUS_PX, fill=255)
    return mask


def _apply_card_mask(im: Image.Image, bg: tuple[int, int, int] = FACE_BORDER_COLOR) -> Image.Image:
    """Clip texture to rounded card silhouette with alpha for USD opacity."""
    rgba = im.convert("RGBA")
    mask = _rounded_corner_mask(rgba.size)
    out = Image.new("RGBA", rgba.size, (*bg, 255))
    out.paste(rgba, mask=mask)
    alpha = Image.new("L", rgba.size, 0)
    alpha.paste(mask, mask=mask)
    out.putalpha(alpha)
    return out


def rounded_rect_outline(hw: float, hh: float, radius: float, segments: int) -> list[tuple[float, float]]:
    """CCW outline of a rounded rectangle centered at the origin."""
    r = min(radius, hw, hh)
    corners = [
        (-hw + r, -hh + r, math.pi, 1.5 * math.pi),
        (hw - r, -hh + r, 1.5 * math.pi, 2.0 * math.pi),
        (hw - r, hh - r, 0.0, 0.5 * math.pi),
        (-hw + r, hh - r, 0.5 * math.pi, math.pi),
    ]
    pts: list[tuple[float, float]] = []
    for cx, cy, a0, a1 in corners:
        for i in range(segments):
            t = i / segments
            ang = a0 + (a1 - a0) * t
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def _uv_for_point(x: float, y: float, hw: float, hh: float) -> tuple[float, float]:
    u = (x + hw) / (2.0 * hw)
    v = (hh - y) / (2.0 * hh)
    return u, v


def _fan_triangulate(
    outline: list[tuple[float, float]],
    z: float,
    hw: float,
    hh: float,
    *,
    reverse: bool = False,
) -> tuple[list[tuple[float, float, float]], list[int], list[int], list[tuple[float, float]], list[tuple[float, float, float]]]:
    """Fan triangulation from center for a convex rounded-rect outline."""
    center = (0.0, 0.0, z)
    ring = [(x, y, z) for x, y in outline]
    points = [center] + ring
    uvs = [(0.5, 0.5)] + [_uv_for_point(x, y, hw, hh) for x, y in outline]
    n = len(ring)
    indices: list[int] = []
    order = range(1, n + 1) if not reverse else range(n, 0, -1)
    idx_list = list(order)
    for i in range(len(idx_list)):
        a = 0
        b = idx_list[i]
        c = idx_list[(i + 1) % len(idx_list)]
        indices.extend([a, b, c])
    nz = 1.0 if z > 0 else -1.0
    normals = [(0.0, 0.0, nz)] * len(points)
    return points, [3] * n, indices, uvs, normals


def _edge_strip(
    outline: list[tuple[float, float]],
    z_front: float,
    z_back: float,
) -> tuple[list[tuple[float, float, float]], list[int], list[int], list[tuple[float, float, float]]]:
    """Side quads connecting front and back outlines."""
    n = len(outline)
    front = [(x, y, z_front) for x, y in outline]
    back = [(x, y, z_back) for x, y in outline]
    points = front + back
    counts: list[int] = []
    indices: list[int] = []
    normals: list[tuple[float, float, float]] = []
    for i in range(n):
        j = (i + 1) % n
        bi, bj = i + n, j + n
        counts.append(4)
        indices.extend([i, j, bj, bi])
        dx = outline[j][0] - outline[i][0]
        dy = outline[j][1] - outline[i][1]
        length = math.hypot(dx, dy) or 1.0
        nx, ny = dy / length, -dx / length
        edge_normal = (nx, ny, 0.0)
        normals.extend([edge_normal] * 4)
    return points, counts, indices, normals


def _fmt_points(points: list[tuple[float, float, float]]) -> str:
    inner = ", ".join(f"({x:.6f}, {y:.6f}, {z:.6f})" for x, y, z in points)
    return f"[{inner}]"


def _fmt_vec2(points: list[tuple[float, float]]) -> str:
    inner = ", ".join(f"({u:.6f}, {v:.6f})" for u, v in points)
    return f"[{inner}]"


def _fmt_vec3(points: list[tuple[float, float, float]]) -> str:
    inner = ", ".join(f"({x:.6f}, {y:.6f}, {z:.6f})" for x, y, z in points)
    return f"[{inner}]"


def _fmt_ints(values: list[int]) -> str:
    return "[" + ", ".join(str(v) for v in values) + "]"


def _mesh_extent(points: list[tuple[float, float, float]]) -> str:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]
    return f"[({min(xs):.6f}, {min(ys):.6f}, {min(zs):.6f}), ({max(xs):.6f}, {max(ys):.6f}, {max(zs):.6f})]"


def usd_card_geometry() -> str:
    outline = rounded_rect_outline(HALF_W, HALF_H, CORNER_RADIUS, CORNER_SEGMENTS)
    front_pts, front_counts, front_idx, front_uv, front_n = _fan_triangulate(
        outline, HALF_T, HALF_W, HALF_H, reverse=False
    )
    back_pts, back_counts, back_idx, back_uv, back_n = _fan_triangulate(
        outline, -HALF_T, HALF_W, HALF_H, reverse=True
    )
    edge_pts, edge_counts, edge_idx, edge_n = _edge_strip(outline, HALF_T, -HALF_T)

    return textwrap.dedent(
        f"""
        def Mesh "Front" (
            prepend apiSchemas = ["MaterialBindingAPI"]
        )
        {{
            uniform bool doubleSided = 1
            float3[] extent = {_mesh_extent(front_pts)}
            int[] faceVertexCounts = {_fmt_ints(front_counts)}
            int[] faceVertexIndices = {_fmt_ints(front_idx)}
            point3f[] points = {_fmt_points(front_pts)}
            normal3f[] normals = {_fmt_vec3(front_n)} (
                interpolation = "vertex"
            )
            texCoord2f[] primvars:st = {_fmt_vec2(front_uv)} (
                interpolation = "vertex"
            )
            uniform token subdivisionScheme = "none"
            rel material:binding = <../../Face>
        }}

        def Mesh "Back" (
            prepend apiSchemas = ["MaterialBindingAPI"]
        )
        {{
            uniform bool doubleSided = 1
            float3[] extent = {_mesh_extent(back_pts)}
            int[] faceVertexCounts = {_fmt_ints(back_counts)}
            int[] faceVertexIndices = {_fmt_ints(back_idx)}
            point3f[] points = {_fmt_points(back_pts)}
            normal3f[] normals = {_fmt_vec3(back_n)} (
                interpolation = "vertex"
            )
            texCoord2f[] primvars:st = {_fmt_vec2(back_uv)} (
                interpolation = "vertex"
            )
            uniform token subdivisionScheme = "none"
            rel material:binding = <../../CardBack>
        }}

        def Mesh "Edges" (
            prepend apiSchemas = ["MaterialBindingAPI"]
        )
        {{
            float3[] extent = {_mesh_extent(edge_pts)}
            int[] faceVertexCounts = {_fmt_ints(edge_counts)}
            int[] faceVertexIndices = {_fmt_ints(edge_idx)}
            point3f[] points = {_fmt_points(edge_pts)}
            normal3f[] normals = {_fmt_vec3(edge_n)} (
                interpolation = "vertex"
            )
            uniform token subdivisionScheme = "none"
            rel material:binding = <../../Edge>
        }}"""
    )


def render_emoji_back(spec: CardSpec, png_path: Path) -> None:
    w, h = TEXTURE_SIZE
    bg = _hex_rgb(SUIT_BG[spec.suit_name])
    color = _hex_rgb(SUIT_COLORS[spec.suit_name])
    img = Image.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)
    inset = CARD_BORDER_PX
    draw.rounded_rectangle(
        (inset, inset, w - inset, h - inset),
        radius=CORNER_RADIUS_PX - 4,
        outline="#c9a227",
        width=8,
    )
    suit_mark = {"Spades": "♠", "Hearts": "♥", "Diamonds": "♦", "Clubs": "♣"}[spec.suit_name]
    corners = [
        (52, 56, spec.rank_label, suit_mark),
        (w - 52, 56, spec.rank_label, suit_mark),
        (52, h - 56, spec.rank_label, suit_mark),
        (w - 52, h - 56, spec.rank_label, suit_mark),
    ]
    for x, y, rank, mark in corners:
        anchor = "ls" if x < w // 2 else "rs"
        draw.text((x, y), rank, font=_LABEL_FONT, fill=color, anchor=anchor)
        draw.text((x, y + 52), mark, font=_LABEL_FONT, fill=color, anchor=anchor)
    draw.text(
        (w // 2, h // 2),
        spec.emoji,
        font=_EMOJI_FONT,
        fill=color,
        anchor="mm",
        embedded_color=True,
    )
    _apply_card_mask(img, bg).save(png_path, format="PNG", optimize=True)


def prepare_face_texture(src: Path, dst: Path) -> None:
    """Center-crop source image to card aspect, add border, clip to rounded card."""
    tw, th = TEXTURE_SIZE
    with Image.open(src) as im:
        im = im.convert("RGB")
        src_ar = im.width / im.height
        tgt_ar = tw / th
        if src_ar > tgt_ar:
            new_w = int(im.height * tgt_ar)
            left = (im.width - new_w) // 2
            im = im.crop((left, 0, left + new_w, im.height))
        else:
            new_h = int(im.width / tgt_ar)
            top = (im.height - new_h) // 2
            im = im.crop((0, top, im.width, top + new_h))
        im = im.resize((tw, th), Image.Resampling.LANCZOS)

    canvas = Image.new("RGB", (tw, th), FACE_BORDER_COLOR)
    inset = CARD_BORDER_PX
    inner = (
        inset,
        inset,
        tw - inset,
        th - inset,
    )
    portrait = im.resize(
        (inner[2] - inner[0], inner[3] - inner[1]),
        Image.Resampling.LANCZOS,
    )
    canvas.paste(portrait, (inner[0], inner[1]))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(
        inner,
        radius=CORNER_RADIUS_PX - 4,
        outline="#c9a227",
        width=6,
    )
    _apply_card_mask(canvas, FACE_BORDER_COLOR).save(dst, format="PNG", optimize=True)


def usd_material(name: str, texture_path: str) -> str:
    return textwrap.dedent(f"""
        def Material "{name}"
        {{
            token outputs:surface.connect = <PreviewSurface.outputs:surface>

            def Shader "PreviewSurface"
            {{
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor.connect = <../DiffuseTex.outputs:rgb>
                float inputs:opacity.connect = <../DiffuseTex.outputs:a>
                float inputs:roughness = 0.4
                float inputs:metallic = 0
                token outputs:surface
            }}

            def Shader "DiffuseTex"
            {{
                uniform token info:id = "UsdUVTexture"
                asset inputs:file = @{texture_path}@
                token inputs:sourceColorSpace = "sRGB"
                float2 inputs:st.connect = <../StReader.outputs:result>
                float3 outputs:rgb
                float outputs:a
            }}

            def Shader "StReader"
            {{
                uniform token info:id = "UsdPrimvarReader_float2"
                string inputs:varname = "st"
                float2 outputs:result
            }}
        }}""")


def _asset_info_block(spec: CardSpec) -> str:
    lines = [
        f'        string name = "{spec.display_label}"',
        f'        string playingCard = "{spec.rank_label} of {spec.suit_name}"',
        f'        string emojiBack = "{spec.emoji}"',
    ]
    for key, value in spec.metadata.items():
        safe_key = re.sub(r"[^A-Za-z0-9_]", "", key)
        if not safe_key:
            continue
        safe_val = str(value).replace('"', '\\"')
        lines.append(f'        string {safe_key} = "{safe_val}"')
    return "\n".join(lines)


def write_card_usda(spec: CardSpec, paths: dict[str, Path]) -> Path:
    usda_path = paths["cards"] / f"{spec.slug}.usda"
    face_tex = texture_asset(paths["face_tex"] / f"{spec.slug}.png")
    back_tex = texture_asset(paths["back_tex"] / f"{spec.slug}.png")

    edge_mat = textwrap.dedent("""
        def Material "Edge"
        {
            token outputs:surface.connect = <Shader.outputs:surface>
            def Shader "Shader"
            {
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = (0.94, 0.91, 0.85)
                float inputs:roughness = 0.5
                token outputs:surface
            }
        }""")

    body = f"""#usda 1.0
(
    defaultPrim = "Card"
    doc = "Playing card: {spec.name} (front) / {spec.rank_label} of {spec.suit_name} (back)"
    metersPerUnit = 1
    upAxis = "Y"
    kilogramsPerUnit = 1
)

def Xform "Card" (
    kind = "component"
    assetInfo = {{
{_asset_info_block(spec)}
    }}
)
{{
{_indent(usd_material("Face", face_tex), 4)}
{_indent(usd_material("CardBack", back_tex), 4)}
{_indent(edge_mat, 4)}

    def Xform "Geometry"
    {{
{_indent(usd_card_geometry(), 8)}
    }}
}}
"""
    usda_path.write_text(body, encoding="utf-8")
    return usda_path


def build_card(spec: CardSpec, face_source: Path, paths: dict[str, Path]) -> Path:
    """Prepare textures and write one card .usda file."""
    face_dst = paths["face_tex"] / f"{spec.slug}.png"
    back_dst = paths["back_tex"] / f"{spec.slug}.png"
    prepare_face_texture(face_source, face_dst)
    render_emoji_back(spec, back_dst)
    return write_card_usda(spec, paths)


def write_deck_usda(
    specs: list[CardSpec],
    card_paths_list: list[Path],
    deck_path: Path,
    *,
    deck_name: str = "Playing Card Deck",
) -> None:
    cols = 8
    spacing_x = CARD_W * 1.35
    spacing_y = CARD_H * 1.35
    refs: list[str] = []

    for i, (spec, card_usda) in enumerate(zip(specs, card_paths_list)):
        row, col = divmod(i, cols)
        x = col * spacing_x
        y = -row * spacing_y
        rel = rel_asset(card_usda, deck_path)
        refs.append(
            f'''    def Xform "Card_{spec.slug}" (
        prepend references = @{rel}@</Card>
    )
    {{
        double3 xformOp:translate = ({x:.4f}, {y:.4f}, 0)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }}'''
        )

    deck = f"""#usda 1.0
(
    defaultPrim = "Deck"
    doc = "{deck_name}"
    metersPerUnit = 1
    upAxis = "Y"
)

def Xform "Deck" (
    kind = "assembly"
)
{{
{chr(10).join(refs)}
}}
"""
    deck_path.write_text(deck, encoding="utf-8")


def load_manifest(path: Path) -> tuple[str, list[tuple[CardSpec, Path]]]:
    """Load a JSON manifest. Returns (deck_name, [(spec, face_path), ...])."""
    data = json.loads(path.read_text(encoding="utf-8"))
    deck_name = data.get("deck_name", "Playing Card Deck")
    cards: list[tuple[CardSpec, Path]] = []
    manifest_dir = path.parent

    for i, entry in enumerate(data.get("cards", [])):
        face = Path(entry["face"])
        if not face.is_absolute():
            face = (manifest_dir / face).resolve()

        spec = make_card_spec(
            name=entry["name"],
            slug=entry.get("slug", ""),
            rank=entry.get("rank", ""),
            suit=entry.get("suit", ""),
            index=entry.get("index", i if "rank" not in entry and "suit" not in entry else None),
            emoji=entry.get("emoji", ""),
            label=entry.get("label", ""),
            metadata=entry.get("metadata", {}),
        )
        cards.append((spec, face))
    return deck_name, cards


def specs_from_card_dir(cards_dir: Path) -> list[CardSpec]:
    """Rebuild CardSpec list from existing card .usda files (for deck rebuild)."""
    specs: list[CardSpec] = []
    for usda in sorted(cards_dir.glob("*.usda")):
        text = usda.read_text(encoding="utf-8")
        name_m = re.search(r'doc = "Playing card: (.+?) \(front\)', text)
        card_m = re.search(r'string playingCard = "(.+?) of (.+?)"', text)
        emoji_m = re.search(r'string emojiBack = "(.+?)"', text)
        if not name_m or not card_m:
            continue
        rank, suit = card_m.group(1), card_m.group(2)
        specs.append(
            CardSpec(
                name=name_m.group(1),
                slug=usda.stem,
                rank_label=rank,
                suit_name=suit,
                emoji=emoji_m.group(1) if emoji_m else emoji_for_rank_suit(rank, suit),
            )
        )
    return specs

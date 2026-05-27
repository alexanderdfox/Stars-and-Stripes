# Senet SVG Style Guide

Uniform rules for all U.S. senator portraits (1789–present).

## Canvas

| Property | Value |
|----------|--------|
| `viewBox` | `0 0 1200 2400` |
| `width` / `height` | `1200` × `2400` |
| Figure rig | 800×1200 logical space, scaled `1.5×` / `2.0` |
| Background | `#3cb868` (chroma key for 3D extraction) |

## Layers (in paint order)

1. `background` — solid chroma rect  
2. `figure` — scaled group containing:  
   - `body` — legs, skin, hands (topology base)  
   - `clothing` — shoes, trousers/breeches, shirt, waistcoat, coat, arms, neckwear  
   - `head` — face, neck, eyes, brows, nose, mouth  
   - `hair` — hair and facial hair (below hat brim when applicable)  
   - `accessories` — glasses, military gear, iconic props  
3. `outlines` — stroke-only duplicate of major silhouettes (`#0d0d0d`, ~2.4px at rig scale)  
4. Global `skin-shade` gradient overlay (subtle depth)

## Line & fill

- Filled paths only for mesh export (no semi-transparent fills on figure).  
- Outlines are optional for 3D; hide `outlines` group when extruding.  
- Era-appropriate coat colors from shared `COAT_COLORS` / `era_clothing` module.  
- Skin tones from `SKIN` palette keyed by complexion trait.

## File naming

`{firstname-lastname}-{primary-senate-year}.svg`  
Example: `daniel-webster-1827.svg`

## 3D import (Blender / Unity)

1. Import SVG with **SVG Curves** or **Import Vector Graphics**.  
2. Hide or delete `background` and `outlines` for mesh workflows.  
3. Extrude `body` / `clothing` / `head` / `hair` separately for material slots.  
4. Use chroma green only for automated masking, not as final albedo.

## Data

- Index: `SENATORS_INDEX.md`, `senators.json`  
- Source biographies: [congress-legislators](https://github.com/unitedstates/congress-legislators)  
- Curated likenesses: `senators_look.py` (`CURATED` + `PROPS`)

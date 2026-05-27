# House SVG Style Guide

Uniform rules for all U.S. House representative portraits (1789–present).

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

## Line & fill

- Filled paths only for mesh export (no semi-transparent fills on figure).  
- Outlines are optional for 3D; hide `outlines` group when extruding.  
- Era-appropriate coat colors from shared `COAT_COLORS` / `era_clothing` module.  
- Skin tones from `SKIN` palette keyed by complexion trait.

## File naming

`{firstname-lastname}-{state}-{primary-house-year}.svg`  
Example: `henry-clay-kentucky-1811.svg`

State slugs use full lowercase hyphenated names (`new-york`, `north-carolina`).

## 3D import (Blender / Unity)

1. Import SVG with **SVG Curves** or **Import Vector Graphics**.  
2. Hide or delete `background` and `outlines` for mesh workflows.  
3. Extrude `body` / `clothing` / `head` / `hair` separately for material slots.  
4. Use chroma green only for automated masking, not as final albedo.

## Historical eras (index grouping)

| Era | Primary service years |
|-----|----------------------|
| Founding | 1789–1799 |
| Antebellum | 1800–1860 |
| Civil War | 1861–1865 |
| Reconstruction | 1866–1876 |
| Gilded Age | 1877–1896 |
| Progressive | 1897–1916 |
| New Deal | 1917–1945 |
| Post-WWII | 1946–1968 |
| Modern | 1969–1994 |
| Contemporary | 1995–present |

## Data

- Index: `HOUSE_INDEX.md`, `representatives.json`  
- Source biographies: [congress-legislators](https://github.com/unitedstates/congress-legislators)  
- Curated likenesses: `representatives_look.py` (`CURATED` + `PROPS`)

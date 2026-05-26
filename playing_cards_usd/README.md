# Presidents Playing Cards (USD)

46 double-sided playing cards for 3D pipelines (Omniverse, Blender, Maya, etc.).

## Layout

| Side | Content |
|------|---------|
| **Front** (`Face`) | President portrait from `generated_png/` |
| **Back** (`CardBack`) | Unicode playing-card glyph (🂡–🂿) with rank/suit |

## Files

- `deck.usda` — master assembly (grid layout)
- `cards/*.usda` — one component per president
- `textures/faces/` — front portraits
- `textures/backs/` — rasterized emoji card faces

## Card size

Poker standard: 63.5 mm × 88.9 mm × 0.50 mm thick

## Regenerate presidents deck

```bash
python3 generate_playing_cards.py
```

## Custom cards

```bash
python3 make_card.py --face photo.png --name "Someone" --rank A --suit Spades
```

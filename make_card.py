#!/usr/bin/env python3
"""Create new USD playing cards from portrait images."""

from __future__ import annotations

import argparse
from pathlib import Path

from playing_card_lib import (
    build_card,
    card_paths,
    load_manifest,
    make_card_spec,
    specs_from_card_dir,
    write_deck_usda,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build USD playing cards (portrait front + emoji card back).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # One card with explicit rank and suit
  python3 make_card.py --face portrait.png --name "Ada Lovelace" --rank Q --suit Hearts

  # Auto-assign rank/suit from deck position (0 = A♠, 1 = 2♠, …)
  python3 make_card.py --face portrait.png --name "Ada Lovelace" --index 12

  # Batch from JSON manifest
  python3 make_card.py --manifest my_deck.json --output my_deck_usd

  # Rebuild deck.usda from cards already in output/cards/
  python3 make_card.py --rebuild-deck --output playing_cards_usd
""",
    )
    parser.add_argument("--face", type=Path, help="Front portrait image (PNG/JPG/…)")
    parser.add_argument("--name", help="Card subject name")
    parser.add_argument("--slug", help="Filesystem-safe id (default: derived from name)")
    parser.add_argument("--rank", help="Card rank: A, 2–10, J, Q, K")
    parser.add_argument("--suit", help="Card suit: Spades, Hearts, Diamonds, Clubs")
    parser.add_argument(
        "--index",
        type=int,
        help="0-based deck index for auto rank/suit (0=A♠, 13=A♥, …)",
    )
    parser.add_argument("--emoji", help="Override Unicode playing-card back glyph")
    parser.add_argument("--label", help="Display label stored in USD assetInfo")
    parser.add_argument(
        "--metadata",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Extra assetInfo metadata (repeatable)",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="JSON manifest with a cards[] list (see cards.example.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("custom_cards_usd"),
        help="Output directory (default: custom_cards_usd)",
    )
    parser.add_argument(
        "--deck-name",
        default="",
        help="Title for deck.usda (manifest deck_name used when batching)",
    )
    parser.add_argument(
        "--rebuild-deck",
        action="store_true",
        help="Rebuild deck.usda from existing cards/*.usda in --output",
    )
    parser.add_argument(
        "--no-deck",
        action="store_true",
        help="Skip writing deck.usda",
    )
    return parser.parse_args()


def parse_metadata(pairs: list[str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise SystemExit(f"Invalid --metadata (expected KEY=VALUE): {pair!r}")
        key, value = pair.split("=", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def main() -> None:
    args = parse_args()
    output = args.output.resolve()
    paths = card_paths(output)

    if args.rebuild_deck:
        specs = specs_from_card_dir(paths["cards"])
        if not specs:
            raise SystemExit(f"No card .usda files found in {paths['cards']}")
        card_usdas = [paths["cards"] / f"{spec.slug}.usda" for spec in specs]
        deck_name = args.deck_name or "Playing Card Deck"
        write_deck_usda(specs, card_usdas, paths["base"] / "deck.usda", deck_name=deck_name)
        print(f"Rebuilt deck with {len(specs)} cards → {paths['base'] / 'deck.usda'}")
        return

    entries: list[tuple] = []
    deck_name = args.deck_name or "Playing Card Deck"

    if args.manifest:
        deck_name, entries = load_manifest(args.manifest.resolve())
    elif args.face and args.name:
        if not args.face.is_file():
            raise SystemExit(f"Face image not found: {args.face}")
        spec = make_card_spec(
            args.name,
            slug=args.slug or "",
            rank=args.rank or "",
            suit=args.suit or "",
            index=args.index,
            emoji=args.emoji or "",
            label=args.label or "",
            metadata=parse_metadata(args.metadata),
        )
        entries = [(spec, args.face.resolve())]
    else:
        raise SystemExit("Provide --face and --name, or --manifest, or --rebuild-deck")

    card_usdas = []
    specs = []
    for spec, face_src in entries:
        if not face_src.is_file():
            raise SystemExit(f"Face image not found: {face_src}")
        usda = build_card(spec, face_src, paths)
        card_usdas.append(usda)
        specs.append(spec)
        print(f"  {spec.display_label}  →  {spec.emoji} {spec.rank_label} {spec.suit_name}")
        print(f"    {usda}")

    if not args.no_deck:
        deck_path = paths["base"] / "deck.usda"
        write_deck_usda(specs, card_usdas, deck_path, deck_name=deck_name)
        print(f"\nDeck: {deck_path}")

    print(f"Wrote {len(specs)} card(s) to {paths['base']}/")


if __name__ == "__main__":
    main()

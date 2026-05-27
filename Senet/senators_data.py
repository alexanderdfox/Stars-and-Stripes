"""Load U.S. senators (1789–present) from congress-legislators JSON."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent


@dataclass(frozen=True)
class SenatorRecord:
    bioguide: str
    name: str
    birth_year: str
    death_year: str
    primary_year: int
    state: str
    party: str

    @property
    def slug(self) -> str:
        base = re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")
        return f"{base}-{self.primary_year}"

    @property
    def filename(self) -> str:
        return f"{self.slug}.svg"


def _full_name(name: dict) -> str:
    parts = [name.get("first", ""), name.get("middle", ""), name.get("last", "")]
    full = " ".join(p for p in parts if p).strip()
    if name.get("suffix"):
        full = f"{full} {name['suffix']}"
    return full


def load_legislators() -> list[dict]:
    out: list[dict] = []
    for fname in ("legislators-historical.json", "legislators-current.json"):
        path = DATA_DIR / fname
        if path.exists():
            out.extend(json.loads(path.read_text(encoding="utf-8")))
    return out


def load_senators() -> list[SenatorRecord]:
    seen: set[str] = set()
    records: list[SenatorRecord] = []

    for leg in load_legislators():
        sen_terms = [t for t in leg.get("terms") or [] if t.get("type") == "sen"]
        if not sen_terms:
            continue
        bid = (leg.get("id") or {}).get("bioguide")
        if not bid or bid in seen:
            continue
        seen.add(bid)

        years = [int(t["start"][:4]) for t in sen_terms if t.get("start", "")[:4].isdigit()]
        primary = min(years) if years else 0
        first_term = min(sen_terms, key=lambda t: t.get("start", ""))
        bio = leg.get("bio") or {}
        bday = bio.get("birthday") or ""
        birth = bday[:4] if len(bday) >= 4 else ""
        death = ""
        if bio.get("deathday"):
            death = str(bio["deathday"])[:4]

        records.append(
            SenatorRecord(
                bioguide=bid,
                name=_full_name(leg.get("name") or {}),
                birth_year=birth,
                death_year=death,
                primary_year=primary,
                state=first_term.get("state", ""),
                party=first_term.get("party", ""),
            )
        )

    records.sort(key=lambda r: (r.primary_year, r.name))
    return records

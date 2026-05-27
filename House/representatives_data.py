"""Load U.S. House representatives (1789–present) from congress-legislators JSON."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

STATE_NAMES: dict[str, str] = {
    "AL": "alabama",
    "AK": "alaska",
    "AZ": "arizona",
    "AR": "arkansas",
    "CA": "california",
    "CO": "colorado",
    "CT": "connecticut",
    "DE": "delaware",
    "FL": "florida",
    "GA": "georgia",
    "HI": "hawaii",
    "ID": "idaho",
    "IL": "illinois",
    "IN": "indiana",
    "IA": "iowa",
    "KS": "kansas",
    "KY": "kentucky",
    "LA": "louisiana",
    "ME": "maine",
    "MD": "maryland",
    "MA": "massachusetts",
    "MI": "michigan",
    "MN": "minnesota",
    "MS": "mississippi",
    "MO": "missouri",
    "MT": "montana",
    "NE": "nebraska",
    "NV": "nevada",
    "NH": "new-hampshire",
    "NJ": "new-jersey",
    "NM": "new-mexico",
    "NY": "new-york",
    "NC": "north-carolina",
    "ND": "north-dakota",
    "OH": "ohio",
    "OK": "oklahoma",
    "OR": "oregon",
    "PA": "pennsylvania",
    "RI": "rhode-island",
    "SC": "south-carolina",
    "SD": "south-dakota",
    "TN": "tennessee",
    "TX": "texas",
    "UT": "utah",
    "VT": "vermont",
    "VA": "virginia",
    "WA": "washington",
    "WV": "west-virginia",
    "WI": "wisconsin",
    "WY": "wyoming",
    "DC": "district-of-columbia",
    "AS": "american-samoa",
    "GU": "guam",
    "MP": "northern-mariana-islands",
    "PR": "puerto-rico",
    "VI": "virgin-islands",
    # Historical / territorial codes in congress-legislators
    "DK": "dakota-territory",
    "OL": "orleans-territory",
    "PI": "philippines",
}


def era_for_year(year: int) -> str:
    if year < 1800:
        return "Founding"
    if year < 1861:
        return "Antebellum"
    if year < 1866:
        return "Civil War"
    if year < 1877:
        return "Reconstruction"
    if year < 1897:
        return "Gilded Age"
    if year < 1917:
        return "Progressive"
    if year < 1946:
        return "New Deal"
    if year < 1969:
        return "Post-WWII"
    if year < 1995:
        return "Modern"
    return "Contemporary"


@dataclass(frozen=True)
class RepresentativeRecord:
    bioguide: str
    name: str
    birth_year: str
    death_year: str
    primary_year: int
    state: str
    state_slug: str
    party: str
    era: str

    @property
    def slug(self) -> str:
        base = re.sub(r"[^a-z0-9]+", "-", self.name.lower()).strip("-")
        return f"{base}-{self.state_slug}-{self.primary_year}"

    @property
    def filename(self) -> str:
        return f"{self.slug}.svg"


def _full_name(name: dict) -> str:
    parts = [name.get("first", ""), name.get("middle", ""), name.get("last", "")]
    full = " ".join(p for p in parts if p).strip()
    if name.get("suffix"):
        full = f"{full} {name['suffix']}"
    return full


def _state_slug(abbr: str) -> str:
    key = (abbr or "").upper()
    if key in STATE_NAMES:
        return STATE_NAMES[key]
    return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-") or "unknown"


def load_legislators() -> list[dict]:
    out: list[dict] = []
    for fname in ("legislators-historical.json", "legislators-current.json"):
        path = DATA_DIR / fname
        if not path.exists():
            alt = DATA_DIR.parent / "Senet" / fname
            if alt.exists():
                path = alt
        if path.exists():
            out.extend(json.loads(path.read_text(encoding="utf-8")))
    return out


def load_representatives() -> list[RepresentativeRecord]:
    seen: set[str] = set()
    records: list[RepresentativeRecord] = []

    for leg in load_legislators():
        rep_terms = [t for t in leg.get("terms") or [] if t.get("type") == "rep"]
        if not rep_terms:
            continue
        bid = (leg.get("id") or {}).get("bioguide")
        if not bid or bid in seen:
            continue
        seen.add(bid)

        years = [int(t["start"][:4]) for t in rep_terms if t.get("start", "")[:4].isdigit()]
        primary = min(years) if years else 0
        first_term = min(rep_terms, key=lambda t: t.get("start", ""))
        state = first_term.get("state", "")
        bio = leg.get("bio") or {}
        bday = bio.get("birthday") or ""
        birth = bday[:4] if len(bday) >= 4 else ""
        death = ""
        if bio.get("deathday"):
            death = str(bio["deathday"])[:4]

        records.append(
            RepresentativeRecord(
                bioguide=bid,
                name=_full_name(leg.get("name") or {}),
                birth_year=birth,
                death_year=death,
                primary_year=primary,
                state=state,
                state_slug=_state_slug(state),
                party=first_term.get("party", ""),
                era=era_for_year(primary),
            )
        )

    records.sort(key=lambda r: (r.primary_year, r.name))
    return records

"""
Generate a synthetic poetry corpus for Lyra development and testing.
Produces: data/synthetic/poets.json, poems.json

Run: python data/synthetic/generate_corpus.py
"""

import json
import uuid
from pathlib import Path

# ── Poets ──────────────────────────────────────────────────────────────────
POETS = [
    {"name": "Aarav Mehta",    "birth_year": 1940, "death_year": 2018, "nationality": "Indian",      "traditions": ["Urdu ghazal", "Hindi kavita"], "bio": "Celebrated Urdu ghazal poet from Lucknow."},
    {"name": "Yuki Tanaka",    "birth_year": 1965, "death_year": None, "nationality": "Japanese",    "traditions": ["haiku", "tanka"],               "bio": "Contemporary haiku poet exploring urban solitude."},
    {"name": "Amara Osei",     "birth_year": 1952, "death_year": 2010, "nationality": "Ghanaian",    "traditions": ["oral praise poetry", "adinkra verse"], "bio": "Oral tradition poet and cultural preservationist."},
    {"name": "Lena Vasquez",   "birth_year": 1978, "death_year": None, "nationality": "Mexican",     "traditions": ["free verse", "sonnet"],          "bio": "Diasporic poet writing on memory and borders."},
    {"name": "Rumi Al-Rashid", "birth_year": 1901, "death_year": 1975, "nationality": "Iraqi",       "traditions": ["qasida", "muwashshah"],          "bio": "Classical Arabic poet reviving the qasida form."},
    {"name": "Seo-Yeon Park",  "birth_year": 1990, "death_year": None, "nationality": "South Korean","traditions": ["sijo", "free verse"],            "bio": "Poet blending traditional sijo with digital themes."},
    {"name": "Elena Volkov",   "birth_year": 1935, "death_year": 2005, "nationality": "Russian",     "traditions": ["acmeism", "elegy"],              "bio": "Post-war elegist in the Akhmatova tradition."},
    {"name": "James Okafor",   "birth_year": 1968, "death_year": None, "nationality": "Nigerian",    "traditions": ["Igbo oral verse", "protest poetry"], "bio": "Environmental protest poet and linguist."},
]

# ── Poems ──────────────────────────────────────────────────────────────────
RAW_POEMS = [
    {
        "title": "The Monsoon Ghazal",
        "body": (
            "The rains have come again, washing the dust from every stone, Mehta.\n"
            "I wait at the window, counting drops like lost years, every stone.\n"
            "My father's voice returns with thunder — do not forget where you began.\n"
            "Even the river forgets its source, yet always returns to its stone.\n"
            "Separation is the name we give to love we cannot hold, Mehta.\n"
            "The rains have come again, washing the dust from every stone."
        ),
        "poet_name": "Aarav Mehta",
        "year": 1979,
        "language": "en",
        "form": "ghazal",
        "tags": ["monsoon", "memory", "separation", "Urdu tradition"],
    },
    {
        "title": "Neon Puddle",
        "body": (
            "Convenience store sign—\n"
            "its reflection shivers\n"
            "in the rain-drenched street"
        ),
        "poet_name": "Yuki Tanaka",
        "year": 2011,
        "language": "en",
        "form": "haiku",
        "tags": ["urban", "solitude", "reflection", "neon"],
    },
    {
        "title": "Praise Song for the Baobab",
        "body": (
            "You are older than the kingdom's first sorrow.\n"
            "Your roots drink from rivers we have forgotten to name.\n"
            "Beneath your canopy, the elders spoke in proverbs;\n"
            "your bark remembers the hands of every season.\n"
            "Do not tell me you are just a tree —\n"
            "I have seen you hold an entire village's grief\n"
            "in one night of harmattan."
        ),
        "poet_name": "Amara Osei",
        "year": 1988,
        "language": "en",
        "form": "praise poem",
        "tags": ["baobab", "oral tradition", "ancestry", "Ghana", "nature"],
    },
    {
        "title": "Border Sonnet",
        "body": (
            "They ask me which side of the river I belong.\n"
            "I say: both banks, and the current between.\n"
            "My grandmother's tongue is a bridge I cross each dawn,\n"
            "my mother's silence, the toll I pay at dusk.\n"
            "There is a map inside my chest — its borders shift\n"
            "each time I say a word in the language I was taught to forget.\n"
            "I have drawn and redrawn the line: here, origin;\n"
            "here, arrival; here, the long uncertain drift.\n"
            "Do not ask me to choose one horizon only.\n"
            "The eye holds east and west without apology.\n"
            "I am the hyphen in the official form, the comma\n"
            "between two countries that have never met.\n"
            "Borders are fictions that bleed. I am the scar\n"
            "and the healed skin both."
        ),
        "poet_name": "Lena Vasquez",
        "year": 2015,
        "language": "en",
        "form": "sonnet",
        "tags": ["diaspora", "identity", "borders", "language", "memory"],
    },
    {
        "title": "Ode to the Euphrates",
        "body": (
            "O Euphrates, keeper of the first alphabet,\n"
            "your waters wrote the names of gods before gods had names.\n"
            "I have walked your banks at dawn when the mist\n"
            "turned the world back to clay — formless, waiting.\n"
            "Every city you fed has fallen; you outlasted them all.\n"
            "What is empire to a river? What is glory to water?\n"
            "Flow on. Flow on. We are the temporary ones."
        ),
        "poet_name": "Rumi Al-Rashid",
        "year": 1961,
        "language": "en",
        "form": "qasida-inspired ode",
        "tags": ["Euphrates", "history", "impermanence", "Mesopotamia"],
    },
    {
        "title": "Algorithm Sijo",
        "body": (
            "The machine learns my face before I know my own reflection—\n"
            "I type my grief in search bars; it sells me grief in return.\n"
            "Who taught the river to only flow toward the advertised sea?"
        ),
        "poet_name": "Seo-Yeon Park",
        "year": 2022,
        "language": "en",
        "form": "sijo",
        "tags": ["technology", "surveillance", "digital age", "identity"],
    },
    {
        "title": "Elegy for a Leningrad Courtyard",
        "body": (
            "The courtyard remembers what the city has paved over:\n"
            "a linden tree, its roots still splitting the stones.\n"
            "We played there, Nina and I, the summer before everything.\n"
            "Now Nina is in the ground. The linden is gone.\n"
            "Only the stone remembers, and stone does not speak —\n"
            "yet I come back each year to press my hand against it,\n"
            "reading the cold the way a blind woman reads a face."
        ),
        "poet_name": "Elena Volkov",
        "year": 1971,
        "language": "en",
        "form": "elegy",
        "tags": ["loss", "memory", "Leningrad", "war", "childhood"],
    },
    {
        "title": "The River Does Not Forget",
        "body": (
            "They dammed the Niger in the name of progress;\n"
            "the fish did not receive the memorandum.\n"
            "We signed our names on papers we could not read,\n"
            "and woke to find the river wearing new clothes.\n"
            "But the river does not forget its old name —\n"
            "it whispers it in flood season, every time,\n"
            "reclaiming every field they thought they owned."
        ),
        "poet_name": "James Okafor",
        "year": 2003,
        "language": "en",
        "form": "free verse",
        "tags": ["environmental justice", "Niger", "colonialism", "resistance", "rivers"],
    },
]


def build_poets() -> list[dict]:
    return [{"id": str(uuid.uuid4()), **p} for p in POETS]


def build_poems(poet_lookup: dict[str, str]) -> list[dict]:
    poems = []
    for p in RAW_POEMS:
        poet_id = poet_lookup.get(p["poet_name"], "")
        poems.append({
            "id": str(uuid.uuid4()),
            "title": p["title"],
            "body": p["body"],
            "poet_id": poet_id,
            "year": p["year"],
            "language": p["language"],
            "form": p["form"],
            "tags": p["tags"],
            "collection_id": None,
        })
    return poems


def main():
    out = Path(__file__).parent
    poets = build_poets()
    lookup = {p["name"]: p["id"] for p in poets}
    poems = build_poems(lookup)

    (out / "poets.json").write_text(json.dumps(poets, indent=2, ensure_ascii=False))
    (out / "poems.json").write_text(json.dumps(poems, indent=2, ensure_ascii=False))
    print(f"Generated {len(poets)} poets and {len(poems)} poems → {out}")


if __name__ == "__main__":
    main()

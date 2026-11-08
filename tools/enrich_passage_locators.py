# Archived scaffolder: its unconditional writes would destroy later editorial work.
raise SystemExit('Retired generator: edit canonical JSON or implement a reviewed staging-only generator.')

import json, re, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

L = {
"odin-wisdom": {"pg-18947": ("Prose Edda—Odin’s pursuit of wisdom", "Odin"), "pg-73533": ("Hávamál—Odin, wisdom, and sacrifice", "Odin")},
"thor-protection": {"pg-18947": ("Prose Edda—Thor and threats to the gods", "Thor"), "pg-73533": ("Þrymskviða—Thor, hammer, and recovery", "Thrym")},
"loki-ambiguity": {"pg-18947": ("Prose Edda—Loki’s shifting role", "Loki"), "pg-73533": ("Lokasenna—Loki among the gods", "Loki")},
"freyja-power": {"pg-18947": ("Prose Edda—Freyja among the gods", "Freyja"), "pg-73533": ("Þrymskviða/Hyndluljóð—Freyja", "Freyja")},
"ragnarok-fate": {"pg-18947": ("Gylfaginning—Ragnarök and fate", "Ragnarok"), "pg-73533": ("Völuspá—creation and Ragnarök", "Ragnarok")},
"osiris-renewal": {"pg-9411": ("Legends of the Gods—Osiris traditions", "Osiris"), "pg-15932": ("Book of the Dead—Osiris and judgment", "Osiris")},
"ra-order": {"pg-9411": ("Legends of the Gods—Ra traditions", "Ra"), "pg-15932": ("Hymns to the Sky-goddess and Sun-god", "Sun")},
"isis-restoration": {"pg-9411": ("Legends of the Gods—Isis and restoration", "Isis"), "pg-15932": ("Lamentations of Isis and Nephthys", "Isis")},
"judgment-dead": {"pg-9411": ("Osiris traditions—death and kingship", "judgment"), "pg-15932": ("The Book of the Dead—The Great Judgment", "judgment")},
"thoth-knowledge": {"pg-9411": ("Egyptian gods—Thoth and sacred knowledge", "Thoth"), "pg-15932": ("Thoth, the Author of Egyptian Literature", "Thoth")},
"pwyll-otherworld": {"pg-5160": ("Pwyll Prince of Dyved", "Pwyll"), "pg-16464": ("Táin—comparative Irish epic context", "Cú Chulainn")},
"branwen-sovereignty": {"pg-5160": ("Branwen daughter of Llyr", "Branwen"), "pg-16464": ("Táin—royal rivalry and consequence", "Medb")},
"manawydan-patience": {"pg-5160": ("Manawydan son of Llyr", "Manawydan"), "pg-16464": ("Táin—endurance and heroic defense", "Ulster")},
"math-sovereignty": {"pg-5160": ("Math son of Mathonwy", "Math"), "pg-16464": ("Táin—kingship and contested authority", "king")},
"taliesin-change": {"pg-5160": ("Taliesin—poetry and transformation", "Taliesin"), "pg-16464": ("Táin—bardic and epic transmission", "Fergus")},
"baba-yaga": {"pg-22373": ("Russian Fairy Tales—The Baba Yaga", "Baba"), "pg-48761": ("Slavonic variants—witch and helper figures", "Baba")},
"koschei-hidden-death": {"pg-22373": ("Koshchei the Deathless", "Koshchei"), "pg-48761": ("Slavonic variants—deathless antagonists", "deathless")},
"vasilissa-wise": {"pg-22373": ("Vasilissa tales—tasks and judgment", "Vasilissa"), "pg-48761": ("Slavonic variants—Vasilissa-type heroines", "Vasilissa")},
"water-king-bargain": {"pg-22373": ("The Water King and Vasilissa the Wise", "Water King"), "pg-48761": ("Slavonic variants—water and bargain motifs", "water")},
"firebird-quest": {"pg-22373": ("Firebird and quest motifs", "Fire"), "pg-48761": ("Slavonic variants—wonder and pursuit", "bird")},
"creation": {"pg-46863": ("Old-World Japan—creation, Izanagi, and Izanami", "Izanagi"), "pg-4018": ("Japanese Fairy Tales—comparative popular tradition", "Urashima")},
"amaterasu-light": {"pg-46863": ("Old-World Japan—Amaterasu and divine light", "Amaterasu"), "pg-4018": ("Japanese Fairy Tales—supernatural order and restoration", "light")},
"susanoo-storm": {"pg-46863": ("Old-World Japan—Susanoo and the storm figure", "Susanoo"), "pg-4018": ("Japanese Fairy Tales—comparative supernatural trials", "dragon")},
"kami-boundaries": {"pg-46863": ("Old-World Japan—the God-period and kami traditions", "kami"), "pg-4018": ("Japanese Fairy Tales—supernatural beings and boundaries", "spirit")},
"izanami-boundary": {"pg-46863": ("Old-World Japan—Izanami, death, and the underworld", "Izanami"), "pg-4018": ("Japanese Fairy Tales—return and supernatural boundaries", "return")},
"ovid-change": {"roman-pg-21765": ("Metamorphoses I–VII—creation and transformation", "changed"), "roman-pg-26073": ("Metamorphoses VIII–XV—transformation continues", "changed")},
"jupiter-reception": {"roman-pg-21765": ("Metamorphoses I–VII—Jupiter/Jove and divine power", "Jove"), "roman-pg-26073": ("Metamorphoses VIII–XV—Roman divine authority", "Jove")},
"venus-desire": {"roman-pg-21765": ("Metamorphoses I–VII—Venus and desire", "Venus"), "roman-pg-26073": ("Metamorphoses VIII–XV—love, lineage, and legacy", "Venus")},
"mars-war-state": {"roman-pg-21765": ("Metamorphoses I–VII—Mars and Roman identity", "Mars"), "roman-pg-26073": ("Metamorphoses VIII–XV—Roman heroic and state themes", "Mars")},
"metamorphosis-reception": {"roman-pg-21765": ("Metamorphoses I–VII—Ovid’s opening project", "Metamorphoses"), "roman-pg-26073": ("Metamorphoses VIII–XV—Roman reworking and closure", "Metamorphoses")}
}

def norm(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c)).lower()

def excerpt(path, keyword):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        ntext, nkey = norm(text), norm(keyword)
        pos = ntext.find(nkey)
        if pos < 0: pos = text.find("*** START")
        start = max(0, pos - 100); end = min(len(text), pos + 260)
        snippet = re.sub(r"\s+", " ", text[start:end]).strip()
        return snippet[:420]
    except Exception:
        return "Local source file available for inspection."

for lesson_path in (ROOT / "content/lessons").rglob("*.json"):
    if "greek" in lesson_path.parts:
        continue
    lesson = json.loads(lesson_path.read_text(encoding="utf-8"))
    slug = lesson["id"].split(".")[-1]
    if slug == "odin-wisdom" and lesson["id"].startswith("nor."): slug = "odin-wisdom"
    spec = L.get(slug)
    if not spec:
        continue
    manifest = json.loads((ROOT / f"content/corpus/{lesson['pantheon']}/manifest.json").read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in manifest["records"]}
    for ref in lesson["sourceReferences"].values():
        rid = ref.get("recordId")
        if rid not in spec or rid not in by_id:
            continue
        locator, keyword = spec[rid]
        ref["locator"] = locator
        ref["excerpt"] = excerpt(ROOT / "content/corpus" / lesson["pantheon"] / by_id[rid]["localPath"], keyword)
        ref["note"] = "Passage-level locator added for the starter lesson; compare with the full local source before expanding the claim."
    lesson_path.write_text(json.dumps(lesson, indent=2) + "\n", encoding="utf-8")
    print("enriched", lesson_path.relative_to(ROOT))

"""One-time, digest-guarded revision of the Norse Gods starter lessons.

Canonical lesson JSON remains authoritative once these documents reach version 2.
The default is a read-only preview; an exact source digest is required to apply.
"""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import normalize, source_segments

ROOT = Path(__file__).resolve().parents[1]

PROSE = "pg-18947"
POETIC = "pg-73533"

PACK = [
    {
        "slug": "odin-wisdom",
        "title": "Odin: Wisdom Has a Price",
        "subtitle": "Two different sacrifices for knowledge",
        "objectives": [
            ("obj.odin.wisdom", "Explain the eye pledge in Snorri's Mimer's Well episode."),
            ("obj.edda.source", "Distinguish that prose episode from Havamal's rune ordeal."),
        ],
        "sources": [
            {
                "id": "mimer",
                "recordId": PROSE,
                "work": "Gylfaginning (in the Prose Edda)",
                "locator": "Mimer's Well in Gylfaginning",
                "start": "The owner of the well hight Mimer.",
                "end": "So it is said in the Vala’s Prophecy:",
            },
            {
                "id": "runes",
                "recordId": POETIC,
                "work": "Havamal (in the Poetic Edda)",
                "locator": "Havamal, stanzas 139-140",
                "start": "139. I ween that I hung",
                "end": "141. Nine mighty songs",
            },
        ],
        "cards": [
            ("context", "An eye for a drink", "In Gylfaginning, Mimer's well contains wisdom. Odin receives a drink only after leaving one eye as a pledge.", ["mimer"], "wisdom"),
            ("source", "Snorri's account", None, ["mimer"], "source"),
            ("source", "A different ordeal in Havamal", None, ["runes"], "wisdom"),
            ("method", "Keep the episodes separate", "The prose account concerns Mimer's well; Havamal 139-140 describes Odin hanging, being wounded, and taking up runes. These are distinct literary episodes.", ["mimer", "runes"], "source"),
            ("synthesis", "Wisdom has a cost", "Both texts link knowledge with sacrifice, but their shared theme does not make their episodes the same event or a record of one historical rite.", ["mimer", "runes"], "wisdom"),
        ],
        "questions": [
            ("What does Odin pledge at Mimer's well in Gylfaginning?", "One eye", ["His spear", "His mead horn"], "Snorri says Mimer grants the drink after Odin leaves one eye as a pledge.", ["mimer"], "wisdom"),
            ("Which work tells of Odin hanging on the tree and taking up runes?", "Havamal, stanzas 139-140", ["Gylfaginning's Mimer's Well passage", "Grimnismal's list of divine halls"], "The rune ordeal is narrated in Havamal; Snorri's Mimer passage tells a different sacrifice.", ["runes", "mimer"], "source"),
        ],
    },
    {
        "slug": "thor-protection",
        "title": "Thor: The Hammer's Recovery",
        "subtitle": "A theft, a condition, and a comic disguise",
        "objectives": [
            ("obj.thor-protection.concept", "Trace the theft of Mjollnir and the condition Thrym sets for its return."),
            ("obj.thor-protection.source", "Explain how Þrymskviða uses disguise and comic reversal."),
        ],
        "sources": [
            {
                "id": "loss",
                "recordId": POETIC,
                "work": "Þrymskviða (in the Poetic Edda)",
                "locator": "Þrymskviða, stanzas 1-7",
                "start": "1. Wild was Vingthor",
                "end": "8. Then Loki flew",
            },
            {
                "id": "disguise",
                "recordId": POETIC,
                "work": "Þrymskviða (in the Poetic Edda)",
                "locator": "Þrymskviða, stanzas 16-20",
                "start": "16. Then Thor the mighty",
                "end": "21.",
            },
            {
                "id": "return",
                "recordId": POETIC,
                "work": "Þrymskviða (in the Poetic Edda)",
                "locator": "Þrymskviða, stanzas 31-32",
                "start": "31. The heart in the breast",
                "end": "33. And so his hammer",
            },
        ],
        "cards": [
            ("context", "The hammer is missing", "Thor wakes and discovers Mjollnir is gone. Thrym admits that he has hidden it and names the price he wants for returning it.", ["loss"], "concept"),
            ("source", "Thrym's condition", None, ["loss"], "concept"),
            ("context", "A disguise is proposed", "Thor objects to wearing a bridal veil. Loki argues that the giants may occupy Asgard if the hammer is not recovered; the gods then dress Thor for the journey.", ["disguise"], "concept"),
            ("source", "The return of Mjollnir", None, ["return"], "concept"),
            ("method", "Read the poem's comic reversal", "Bellows translates the bridal disguise as comedy. Treat this tone as a feature of Þrymskviða, not as a rule for every Thor story.", ["loss", "disguise", "return"], "source"),
        ],
        "questions": [
            ("What condition does Thrym set for returning Mjollnir?", "Freyja must marry him", ["Thor must give up Mjollnir permanently", "The gods must surrender Asgard"], "Thrym says no one will return the hammer unless he wins Freyja as his wife.", ["loss"], "concept"),
            ("What does Loki do when Thor resists the disguise?", "Warns that the giants may keep the hammer and threaten Asgard", ["Offers to fight Thrym alone while Thor waits", "Tells Thor to abandon the hammer"], "Loki argues that the hammer must be recovered to prevent the giants from entering Asgard.", ["disguise"], "source"),
        ],
    },
    {
        "slug": "loki-ambiguity",
        "title": "Loki: Cunning and Ambiguity",
        "subtitle": "An accusation at Aegir's feast",
        "objectives": [
            ("obj.loki-ambiguity.concept", "Describe how Lokasenna stages Loki's entrance and hostile speech."),
            ("obj.loki-ambiguity.source", "Keep Loki's role in this poem distinct from other Norse works."),
        ],
        "sources": [
            {
                "id": "lokasenna",
                "recordId": POETIC,
                "work": "Lokasenna (in the Poetic Edda)",
                "locator": "Lokasenna, stanzas 3-6",
                "start": "3. “In shall I go",
                "end": "7. “Why sit ye silent",
            },
        ],
        "cards": [
            ("context", "Loki approaches the feast", "In Lokasenna, Loki arrives at Aegir's hall after a warning from Eldir. His stated purpose is to provoke the assembled gods, not to mediate their dispute.", ["lokasenna"], "concept"),
            ("source", "Loki states his intent", None, ["lokasenna"], "concept"),
            ("synthesis", "Speech becomes the action", "The poem stages a contest of insults and accusations. Its Loki is a literary speaker in this feast scene, not a complete summary of the figure across Norse texts.", ["lokasenna"], "concept"),
            ("method", "Keep this poem's frame visible", "Lokasenna is an Eddic poem, translated and transmitted in a medieval manuscript. Read its hostile speech as a scene with a particular dramatic purpose.", ["lokasenna"], "source"),
            ("flavor", "An uneasy guest", "The poem's tension comes from Loki's position inside the feast and his choice to attack its hosts in words.", ["lokasenna"], "concept"),
        ],
        "questions": [
            ("What does Loki say he brings into Aegir's hall?", "Bale and hatred, and venom for the mead", ["A peace offering to settle the gods' quarrel", "A plan to return Thor's hammer"], "Loki announces hostile intent before he enters the hall.", ["lokasenna"], "concept"),
            ("How does Lokasenna present Loki in this scene?", "As a guest whose insults drive a feast-time verbal conflict", ["As a neutral compiler listing divine family lines", "As a narrator recounting Freyja's marriage"], "The poem stages a confrontation through speech; it is not a neutral biography.", ["lokasenna"], "source"),
        ],
    },
    {
        "slug": "freyja-power",
        "title": "Freyja: Desire, Magic, and Power",
        "subtitle": "Folkvang and the choice of the slain",
        "objectives": [
            ("obj.freyja-power.concept", "Explain what Snorri and Grímnismál say about Freyja and the slain."),
            ("obj.freyja-power.source", "Compare the prose account with its cited poetic passage."),
        ],
        "sources": [
            {
                "id": "prose",
                "recordId": PROSE,
                "work": "Gylfaginning (in the Prose Edda)",
                "locator": "Freyja and Folkvang in Gylfaginning",
                "start": "Freyja is the most famous of the goddesses.",
                "end": "The other half is Odin’s.",
            },
            {
                "id": "poem",
                "recordId": POETIC,
                "work": "Grímnismál (in the Poetic Edda)",
                "locator": "Grímnismál, stanza 14",
                "start": "14. The ninth is Folkvang",
                "end": "15. The tenth is Glitnir",
            },
        ],
        "cards": [
            ("context", "A share of the slain", "Snorri's Gylfaginning says Freyja chooses half of those slain in battle for seats in Folkvang; Odin receives the other half.", ["prose"], "concept"),
            ("source", "Snorri's prose account", None, ["prose"], "concept"),
            ("source", "The poetic stanza", None, ["poem"], "concept"),
            ("method", "Compare the witnesses carefully", "Anderson's edition identifies the verse as Grímnismál 14. Treat the prose and poem as related source testimony, not as two unrelated confirmations of a historical afterlife system.", ["prose", "poem"], "source"),
            ("synthesis", "Do not flatten the claim", "These passages describe a literary division of the battle-dead. They do not establish that every Norse community held one uniform belief about the afterlife.", ["prose", "poem"], "source"),
        ],
        "questions": [
            ("In Gylfaginning, who chooses half of those slain in battle?", "Freyja", ["Odin", "Frigg"], "Snorri assigns half to Freyja and half to Odin.", ["prose"], "concept"),
            ("What does Grímnismál 14 add to the prose description?", "A poetic stanza names Folkvang and says Freyja chooses half the dead", ["It says Thor chooses every fallen warrior", "It gives a complete account of all Norse burial customs"], "The stanza supports a source-specific comparison, not a universal account of practice.", ["poem", "prose"], "source"),
        ],
    },
    {
        "slug": "ragnarok-fate",
        "title": "Fate and Ragnarök",
        "subtitle": "Catastrophe and renewal in two tellings",
        "objectives": [
            ("obj.ragnarok-fate.concept", "Describe the renewed world in Völuspá 59 and Gylfaginning 58."),
            ("obj.ragnarok-fate.source", "Distinguish the poem from Snorri's prose retelling."),
        ],
        "sources": [
            {
                "id": "prose",
                "recordId": PROSE,
                "work": "Gylfaginning (in the Prose Edda)",
                "locator": "Gylfaginning 58, the renewed world",
                "start": "58. Then said Ganglere: Do any gods live then?",
                "end": "Vidar and Vale live.",
            },
            {
                "id": "poem",
                "recordId": POETIC,
                "work": "Völuspá (in the Poetic Edda)",
                "locator": "Völuspá, stanzas 59-61",
                "start": "59. Now do I see",
                "end": "62. Then fields unsowed",
            },
        ],
        "cards": [
            ("context", "The story continues after catastrophe", "Völuspá does not end its vision with the burning and sinking of the old world. Stanza 59 describes the earth rising green again from the waves.", ["poem"], "concept"),
            ("source", "The Völuspá stanza", None, ["poem"], "concept"),
            ("source", "Snorri's prose question and answer", None, ["prose"], "concept"),
            ("method", "Compare poem and retelling", "Völuspá speaks through a prophetic voice; Gylfaginning retells the events in a question-and-answer frame. Keep each work's wording and framing attached to the claim.", ["poem", "prose"], "source"),
            ("synthesis", "An ending with a sequel", "Both excerpts make renewal part of their account, but their narrative forms differ. Do not turn these two texts into a single timeless Norse canon.", ["poem", "prose"], "source"),
        ],
        "questions": [
            ("What does Völuspá 59 say happens to the earth?", "It rises green again from the waves", ["It remains sunk beneath the sea", "It is replaced by an untouched world with no prior catastrophe"], "The stanza names renewal after the preceding catastrophe.", ["poem"], "concept"),
            ("According to Gylfaginning 58, which gods survive to see the renewed world?", "Vidar and Vale", ["Thor and Loki", "Freyja and Frigg"], "Snorri names Vidar and Vale in this answer; compare it with the poem's own prophecy.", ["prose"], "source"),
        ],
    },
]


def make_reference(records, root, source):
    record = records[source["recordId"]]
    local_path = f"content/corpus/norse/{record['localPath']}"
    path = root / local_path
    segments = source_segments(path)
    segment = next((item for item in segments if item["evidenceType"] == "source-text"), None)
    if segment is None:
        raise ValueError(f"No source text: {local_path}")
    text = segment["text"]
    start = text.find(source["start"])
    end = text.find(source["end"], start + len(source["start"])) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {source['locator']}")
    excerpt = text[start:end].strip()
    if not excerpt or source["start"] not in excerpt:
        raise ValueError(f"Bad source excerpt: {source['locator']}")
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": source["work"],
        "author": ", ".join(record.get("ancientAuthors", [])),
        "translator": record["translator"],
        "locator": f"{source['locator']}; local text normalized characters {start}-{end}",
        "localPath": local_path,
        "excerpt": excerpt,
        "evidenceType": "quotation",
        "note": f"Verbatim {record['translator']} translation excerpt; whitespace normalized.",
    }


def build(root):
    manifest = json.loads((root / "content/corpus/norse/manifest.json").read_text(encoding="utf-8"))
    records = {item["id"]: item for item in manifest["records"]}
    changes = {}
    for item in PACK:
        path = root / f"content/lessons/norse/{'norse-gods' if item['slug'] == 'odin-wisdom' else 'gods'}/day-{1 if item['slug'] == 'odin-wisdom' else {'thor-protection': 2, 'loki-ambiguity': 3, 'freyja-power': 4, 'ragnarok-fate': 5}[item['slug']]:02d}-{item['slug']}.json"
        lesson = json.loads(path.read_text(encoding="utf-8"))
        lesson["version"] = 2
        lesson["estimatedMinutes"] = 3
        lesson["difficulty"] = 2
        lesson["learningObjectives"] = [{"id": obj_id, "text": text} for obj_id, text in item["objectives"]]
        lesson["sourceReferences"] = {source["id"]: make_reference(records, root, source) for source in item["sources"]}
        lesson["narrativeBlocks"] = [
            {
                "id": f"card-{index + 1:02d}",
                "kind": kind,
                "title": title,
                "body": body if body is not None else "Source quotation (translated; whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”",
                "sourceRefIds": refs,
                "objectiveIds": [objective_id],
            }
            for index, (kind, title, body, refs, objective_key) in enumerate(item["cards"])
            for objective_id in [next(obj_id for obj_id, _ in item["objectives"] if obj_id.endswith("source") == (objective_key == "source"))]
        ]
        # The generated ID is stable for the daily question index; choice order is authored below.
        lesson["quiz"] = []
        for index, (prompt, correct, wrong, explanation, refs, objective_key) in enumerate(item["questions"]):
            shift = (index + len(changes)) % 3
            options = [correct, *wrong]
            options = options[shift:] + options[:shift]
            choices = [{"id": chr(ord("a") + j), "text": text} for j, text in enumerate(options)]
            objective_id = next(obj_id for obj_id, _ in item["objectives"] if obj_id.endswith("source") == (objective_key == "source"))
            lesson["quiz"].append({
                "id": f"q{index + 1}",
                "type": "single-choice",
                "prompt": prompt,
                "choices": choices,
                "answerId": next(choice["id"] for choice in choices if choice["text"] == correct),
                "explanation": explanation,
                "sourceRefIds": refs,
                "objectiveIds": [objective_id],
                "deepDive": {
                    "prompt": "Explore the named source passage.",
                    "suggestedQuestions": ["What words in this excerpt support the answer?", "Which details belong to this source rather than another version?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft",
            "reviewedBy": None,
            "reviewedAt": None,
            "notes": "Source-specific editorial rewrite with locally matched quotations. Independent line-by-line scholarly, translation, and pedagogy review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/norse").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(
        json.loads(path.read_text(encoding="utf-8")).get("review", {}).get("status") == "reviewed"
        or json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 2
        for path in paths
    ):
        parser.error("Only unreviewed version-1/2 scaffolds may be migrated; refusing reviewed content.")
    changes = build(ROOT)
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} Norse lesson revisions; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        for path, document in changes.items():
            path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied the Norse source-specific lesson pass; future writes are disabled.")


if __name__ == "__main__":
    main()

"""One-time, digest-guarded source revision for the Gilgamesh starter lessons."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
CLAY = "content/corpus/mesopotamian/primary/gilgamesh-clay-jastrow-11000.txt"
LANGDON = "content/corpus/mesopotamian/primary/gilgamish-langdon-18897.txt"

PACK = [
    {
        "slug": "kingship-excess",
        "title": "Gilgamesh's Dream of a Companion",
        "subtitle": "A dream foreshadows the arrival of Enkidu",
        "refs": [
            ("dream", CLAY, "Pennsylvania Tablet · Column I", "My likeness I have seen in the streets", "Whom thou didst embrace like a woman]."),
        ],
        "cards": [
            ("context", "A second dream", "In the Pennsylvania Tablet translation, Gilgamesh describes a dream to his mother: he sees a likeness in Erech, an axe, and a figure he embraces as a brother.", ["dream"], "concept"),
            ("source", "Gilgamesh names the dream", None, ["dream"], "concept"),
            ("context", "A mother's interpretation", "The surviving lines show Gilgamesh's mother interpreting the dream as a man who will become his companion. The bracketed words signal editorial restorations in this translation.", ["dream"], "concept"),
            ("method", "A fragment, not a complete epic", "The Pennsylvania Tablet is an Old Babylonian fragment in a modern edited translation by Jastrow and Clay. Its missing or restored wording should remain visible.", ["dream"], "source"),
            ("synthesis", "The companion is anticipated", "The dream gives the relationship a narrative beginning before the two men meet. It is a scene in this tablet witness, not evidence that every version uses identical wording.", ["dream"], "source"),
        ],
        "questions": [
            ("What does Gilgamesh say he does with the figure in his second dream?", "He embraces the figure and regards him as a brother", ["He defeats the figure in a chariot race", "He follows the figure into the cedar forest"], "The quoted dream says Gilgamesh embraces the figure and takes him as a brother.", ["dream"], "concept"),
            ("What do square brackets in this edited translation often signal?", "Words restored or supplied by the editors", ["A new scene written by a later poet", "A line spoken by Gilgamesh's mother"], "The editors use brackets to mark readings or words supplied where the tablet is damaged.", ["dream"], "source"),
        ],
    },
    {
        "slug": "enkidu-wild",
        "title": "Enkidu: From the Herd to Erech",
        "subtitle": "Food, clothing, and a new social role",
        "refs": [
            ("change", CLAY, "Pennsylvania Tablet · Column III · part 1", "Enkidu had not known", "Enkidu was their protector."),
        ],
        "cards": [
            ("context", "A new kind of meal", "The Pennsylvania Tablet describes Enkidu learning to eat prepared food and drink wine with the woman who leads him away from the herds.", ["change"], "concept"),
            ("source", "Learning the customs of the land", None, ["change"], "concept"),
            ("context", "A changed role", "The passage says Enkidu is anointed, clothed, and becomes a protector of shepherds against lions. It presents a shift in social role, not a timeless claim about 'civilization.'", ["change"], "concept"),
            ("method", "Notice uncertain words", "This is Jastrow and Clay's translation of a damaged tablet. Even its phrase '[The barber(?)]' is uncertain; do not convert the translator's reconstruction into a secure detail.", ["change"], "source"),
            ("synthesis", "Transformation through relationships", "Enkidu's change is narrated through food, clothing, speech, and his work among shepherds.", ["change"], "concept"),
        ],
        "questions": [
            ("What does the Pennsylvania Tablet say Enkidu had not learned before?", "To eat prepared food or drink wine", ["To fight with an axe", "To interpret a dream"], "The text says Enkidu had not known food or been taught to drink wine.", ["change"], "concept"),
            ("What role does Enkidu take among the shepherds in this passage?", "He protects them from lions", ["He becomes king of Erech", "He guards the cedar forest for Enlil"], "The translation says Enkidu attacks lions so night shepherds can rest and becomes their protector.", ["change"], "source"),
        ],
    },
    {
        "slug": "friendship-grief",
        "title": "Gilgamesh and Enkidu: The First Contest",
        "subtitle": "A violent meeting ends with recognition",
        "refs": [
            ("meeting", CLAY, "Pennsylvania Tablet · Column VI · part 2", "They met in the plaza of the district.", "Kingship over men Enlil has decreed for thee."),
        ],
        "cards": [
            ("context", "Enkidu blocks the gate", "In this Pennsylvania Tablet witness, Enkidu prevents Gilgamesh from entering. They wrestle with the force of oxen and damage the threshold and wall.", ["meeting"], "concept"),
            ("source", "The contest changes direction", None, ["meeting"], "concept"),
            ("context", "The encounter eases", "After Gilgamesh's wrath is appeased, Enkidu speaks of Gilgamesh's mother Ninsun and the kingship Enlil decreed. This fragment presents a turn after their struggle.", ["meeting"], "concept"),
            ("method", "Keep witness and inference distinct", "The surviving translated lines show a fight followed by speech. Calling it a beginning of friendship is an interpretation of that sequence, not a separate line in this excerpt.", ["meeting"], "source"),
            ("synthesis", "Conflict becomes a relationship", "The scene moves from physical opposition toward recognition, but the lesson should not imply the fragment preserves every step of their relationship.", ["meeting"], "source"),
        ],
        "questions": [
            ("How does the Pennsylvania Tablet describe their first contest?", "They grapple like oxen and damage the threshold and wall", ["They compete in a chariot race", "They fight Huwawa in the cedar forest"], "The translated lines compare their struggle to oxen and describe damage to the threshold and wall.", ["meeting"], "concept"),
            ("What happens after Gilgamesh's breast is quieted?", "Enkidu speaks to him about Ninsun and kingship", ["Enkidu returns to the herds", "Gilgamesh interprets another dream"], "The excerpt follows the easing of Gilgamesh's anger with Enkidu's speech.", ["meeting"], "source"),
        ],
    },
    {
        "slug": "flood-mortality",
        "title": "The Cedar Forest: Huwawa's Terror",
        "subtitle": "Fear, fame, and a dangerous expedition",
        "refs": [
            ("terror", CLAY, "Yale Tablet · Column IV", "To keep safe [the cedar forest]", "[Weapons(?)] let them mould before us."),
        ],
        "cards": [
            ("context", "A guarded forest", "In the Yale Tablet fragment, Enkidu warns that Huwawa guards the cedar forest. The danger is described through a roar like a flood, a mouth of fire, and breath of death.", ["terror"], "concept"),
            ("source", "A sevenfold terror", None, ["terror"], "concept"),
            ("context", "Gilgamesh insists on going", "The translated fragment has Gilgamesh answer that if he falls, he will establish his name. The men then entrust work to artisans to make weapons.", ["terror"], "concept"),
            ("method", "The tablet is fragmentary", "The Yale Tablet translation includes gaps, question marks, and bracketed restorations. Treat the wording as an edited reading of a damaged witness, not an unbroken transcript.", ["terror"], "source"),
            ("synthesis", "Fear and fame", "This passage stages a tension between Enkidu's knowledge of danger and Gilgamesh's desire for lasting renown.", ["terror"], "concept"),
        ],
        "questions": [
            ("What does the Yale Tablet say Enlil decreed for the cedar forest?", "Sevenfold terror", ["A feast of seven goblets", "A wall around Erech"], "The translated fragment says Enlil decreed sevenfold terror to keep the cedar forest safe.", ["terror"], "concept"),
            ("Why does Gilgamesh say he will enter the forest even if he falls?", "To establish his name", ["To find a cure from Sabitum", "To recover an axe from Enkidu"], "The fragment has Gilgamesh say, 'If I fall, I will establish my name.'", ["terror"], "source"),
        ],
    },
    {
        "slug": "fragmented-source",
        "title": "Gilgamesh: Reading Across Fragments",
        "subtitle": "Separate tablets preserve different pieces",
        "refs": [
            ("pennsylvania", CLAY, "Pennsylvania Tablet · Column III · part 1", "Enkidu had not known", "Enkidu was their protector."),
            ("yale", CLAY, "Yale Tablet · Column IV", "To keep safe [the cedar forest]", "[Weapons(?)] let them mould before us."),
        ],
        "cards": [
            ("context", "Two named witnesses", "The local edition distinguishes a Pennsylvania Tablet from a Yale Tablet. These are separate fragmentary witnesses, and the edition presents different episodes from them.", ["pennsylvania", "yale"], "source"),
            ("source", "A passage from the Pennsylvania Tablet", None, ["pennsylvania"], "concept"),
            ("source", "A passage from the Yale Tablet", None, ["yale"], "concept"),
            ("method", "Do not silently join gaps", "The tablet texts contain breaks, restorations, and uncertain readings. A continuous classroom retelling can obscure what is present on each witness and what editors supply.", ["pennsylvania", "yale"], "source"),
            ("synthesis", "Read the edition as an edition", "Jastrow and Clay's book includes translated tablets alongside transliteration, introduction, and commentary. This lesson quotes only its labeled tablet translations.", ["pennsylvania", "yale"], "source"),
        ],
        "questions": [
            ("Which detail belongs to the Pennsylvania Tablet passage?", "Enkidu learns food and wine customs and protects shepherds", ["Enlil decrees sevenfold terror for the cedar forest", "Caesar's soul becomes a star"], "The Pennsylvania Tablet excerpt describes Enkidu's food, clothing, and protector role.", ["pennsylvania"], "concept"),
            ("Why should the Yale and Pennsylvania passages not be silently merged?", "They are distinct, fragmentary tablet witnesses with visible gaps and restorations", ["They are two names for the same complete modern novel", "One is a Greek poem and the other a Roman law code"], "The edition presents separate tablet texts and marks uncertainty and missing lines.", ["pennsylvania", "yale"], "source"),
        ],
    },
]


def make_reference(records, spec):
    ref_id, local_path, segment_locator, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / local_path)
         if item["locator"] == segment_locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Tablet translation segment not found: {segment_locator}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {segment_locator}")
    end += len(end_anchor)
    record = next(item for item in records if f"content/corpus/mesopotamian/{item['localPath']}" == local_path)
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": "Anonymous",
        "translator": record["translator"],
        "locator": f"{segment_locator}; {segment_locator}, normalized characters {start}-{end}",
        "localPath": local_path,
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim translation from the named Old Babylonian tablet witness in this edited edition. Brackets and question marks signal textual restoration or uncertainty.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/mesopotamian/manifest.json").read_text(encoding="utf-8"))
    records = manifest["records"]
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/mesopotamian").rglob("*.json")
    }
    changes = {}
    for spec in PACK:
        path = paths[spec["slug"]]
        lesson = json.loads(path.read_text(encoding="utf-8"))
        lesson["version"] = 2
        lesson["title"] = spec["title"]
        lesson["subtitle"] = spec["subtitle"]
        lesson["estimatedMinutes"] = 3
        lesson["difficulty"] = 2
        concept_id = lesson["learningObjectives"][0]["id"]
        source_id = lesson["learningObjectives"][-1]["id"]
        lesson["learningObjectives"] = [
            {"id": concept_id, "text": spec["questions"][0][0]},
            {"id": source_id, "text": spec["questions"][1][0]},
        ]
        lesson["sourceReferences"] = {item[0]: make_reference(records, item) for item in spec["refs"]}
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, refs, objective) in enumerate(spec["cards"], 1):
            if body is None:
                body = "Source quotation (Jastrow and Clay's tablet translation; whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
            lesson["narrativeBlocks"].append({
                "id": f"card-{index:02d}", "kind": kind, "title": title, "body": body,
                "sourceRefIds": refs,
                "objectiveIds": [concept_id if objective == "concept" else source_id],
            })
        lesson["quiz"] = []
        for index, (prompt, correct, wrong, explanation, refs, objective) in enumerate(spec["questions"]):
            choices = [correct, *wrong]
            shift = (index + len(changes)) % 3
            choices = choices[shift:] + choices[:shift]
            choice_objects = [{"id": chr(97 + i), "text": text} for i, text in enumerate(choices)]
            lesson["quiz"].append({
                "id": f"q{index + 1}", "type": "single-choice", "prompt": prompt,
                "choices": choice_objects,
                "answerId": next(choice["id"] for choice in choice_objects if choice["text"] == correct),
                "explanation": explanation, "sourceRefIds": refs,
                "objectiveIds": [concept_id if objective == "concept" else source_id],
                "deepDive": {
                    "prompt": "Read the labeled tablet passage and its edition notes.",
                    "suggestedQuestions": ["Which words support this answer?", "Which words are bracketed or uncertain?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Tablet-specific source rewrite; independent Assyriological and pedagogical review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/mesopotamian").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Mesopotamian starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} tablet-specific lessons; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        staged = []
        for path, lesson in changes.items():
            temporary = path.with_suffix(path.suffix + ".tmp")
            temporary.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            staged.append((temporary, path))
        for temporary, path in staged:
            temporary.replace(path)
        print("Applied once; future generated writes are disabled.")


if __name__ == "__main__":
    main()

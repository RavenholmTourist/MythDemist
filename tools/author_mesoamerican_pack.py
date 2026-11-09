"""One-time, digest-guarded source revision for a Mexica/Toltec starter set."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
SPENCE = "content/corpus/mesoamerican/primary/myths-mexico-peru-spence-53080.txt"

PACK = [
    {
        "slug": "five-suns",
        "title": "Nanahuatl: The Sun's Birth",
        "subtitle": "A creation episode in Spence's Mexican synthesis",
        "refs": [
            ("sun", "Chapter II · MEXICAN MYTHOLOGY", "The myth of Nanahuatl tells", "the sun rose above the horizon."),
        ],
        "cards": [
            ("context", "A world in darkness", "Spence's account says humanity lived in darkness before the sun appeared. Nanahuatl is led as a sacrifice and cast onto a funeral pyre.", ["sun"], "concept"),
            ("source", "The sun rises", None, ["sun"], "concept"),
            ("context", "The moon also enters the story", "In this version, Metztli also casts herself onto the flames, after which the sun rises. The lesson follows Spence's account rather than merging it with other creation narratives.", ["sun"], "concept"),
            ("method", "A twentieth-century synthesis", "Lewis Spence's early twentieth-century book summarizes Mexican, Maya, and Peruvian material. This passage is Spence's English account, not a direct translation from a named Nahuatl manuscript.", ["sun"], "source"),
            ("synthesis", "Name the tradition in view", "This episode is presented in Spence's Mexican mythology chapter; it is not evidence for every Mesoamerican people or every account of the sun's origin.", ["sun"], "source"),
        ],
        "questions": [
            ("What happens to Nanahuatl in Spence's account?", "He is cast onto a funeral pyre as a sacrifice", ["He escapes by raft to Tlapallan", "He hides the Sun and Moon in a mountain"], "Spence says Metztli leads Nanahuatl to the pyre, where he is consumed.", ["sun"], "concept"),
            ("What source is this lesson quoting?", "Lewis Spence's modern English synthesis", ["A direct translation of one named Nahuatl manuscript", "A contemporary eyewitness record"], "The local source is Spence's early twentieth-century synthesis, not a direct primary-text translation.", ["sun"], "source"),
        ],
    },
    {
        "slug": "quetzalcoatl",
        "title": "Quetzalcoatl: Departure from Tollan",
        "subtitle": "A Toltec episode as transmitted by Spence",
        "refs": [
            ("departure", "Chapter II · MEXICAN MYTHOLOGY", "On reaching the summit of Mount Poyauhtecatl", "the land of Tlapallan."),
        ],
        "cards": [
            ("context", "A journey away from Mexico", "Spence's account describes Quetzalcoatl leaving Mexico, reaching the shore, and departing on a raft of serpents toward Tlapallan.", ["departure"], "concept"),
            ("source", "The raft of serpents", None, ["departure"], "concept"),
            ("context", "A named transmission", "Spence says the legends are taken from Sahagun's Historia General de Nueva España and compared with accounts attributed to Ixtlilxochitl.", ["departure"], "source"),
            ("method", "Keep the Toltec setting", "Spence places this in a discussion of Toltec legends and the fall of Tollan. Do not collapse it into a single story shared identically by all Mesoamerican peoples.", ["departure"], "source"),
            ("synthesis", "Departure is not one fixed ending", "The passage records one written synthesis of a departure tradition. The text itself notes parallels and comparison, not a single uncontested version.", ["departure"], "source"),
        ],
        "questions": [
            ("What does Quetzalcoatl board at the sea-shore in this account?", "A raft of serpents", ["A canoe made by Ilmarinen", "A boat carrying the Sampo"], "Spence's passage says he embarked upon a raft of serpents and was wafted toward Tlapallan.", ["departure"], "concept"),
            ("Which source does Spence name for the legend?", "Sahagun's Historia General de Nueva España", ["Crawford's Kalevala", "Dutt's Ramayana"], "Spence states that the legends are taken from Sahagun's work and included for comparison.", ["departure"], "source"),
        ],
    },
    {
        "slug": "huitzilopochtli",
        "title": "Huitzilopochtli: Birth and Battle",
        "subtitle": "A Mexica divine birth in Spence's account",
        "refs": [
            ("birth", "Chapter II · MEXICAN MYTHOLOGY", "It recounts how, under the shadow of the mountain of Coatepec", "took counsel with one another to slay her."),
            ("battle", "Chapter II · MEXICAN MYTHOLOGY", "He shattered Coyolxauhqui with a flash of serpentine lightning", "All were slain save a few who escaped to a place called Uitzlampa"),
        ],
        "cards": [
            ("context", "A family prepares to attack", "Spence recounts Coatlicue's pregnancy, her daughter Coyolxauhqui's opposition, and the brothers' approach to kill their mother.", ["birth"], "concept"),
            ("source", "The child arrives armed", None, ["birth"], "concept"),
            ("context", "A battle on Coatepec", "In Spence's version, Huitzilopochtli is born when the attackers arrive, defeats Coyolxauhqui, and drives the brothers away.", ["battle"], "concept"),
            ("method", "Attribute the details to the edition", "This is Spence's English synthesis of a Mexica/Nahua story. Spellings such as Uitzlampa reflect his transliteration and should not be silently modernized.", ["birth", "battle"], "source"),
            ("synthesis", "A Mexica-specific account", "Keep Coatlicue, Coyolxauhqui, Huitzilopochtli, and Coatepec attached to this source's version rather than treating it as a generic Mesoamerican pantheon story.", ["birth", "battle"], "source"),
        ],
        "questions": [
            ("Who leads the attackers against Coatlicue in Spence's account?", "Coyolxauhqui", ["Louhi", "Sita"], "The passage says Coatlicue's daughter Coyolxauhqui incites the brothers.", ["birth"], "concept"),
            ("What does Spence say Huitzilopochtli does in the battle?", "He defeats Coyolxauhqui and pursues the brothers", ["He leaves on a raft of serpents", "He travels through Mictlan with a dog"], "The separate battle passage describes his attack on Coyolxauhqui and pursuit of the Centzonuitznaua.", ["battle"], "source"),
        ],
    },
    {
        "slug": "underworld-road",
        "title": "Mictlan: A Journey after Death",
        "subtitle": "A posthumous journey in Spence's Mexica chapter",
        "refs": [
            ("journey", "Chapter I · THE CIVILISATION OF MEXICO", "The dead person is given over to the tests", "the harassed ghost at length encounters"),
        ],
        "cards": [
            ("context", "A journey with dangers", "Spence describes a dead person being sent toward Mictlan and facing collapsing peaks, a serpent, an alligator, deserts, mountains, and a sharp whirlwind.", ["journey"], "concept"),
            ("source", "The road to Mictlan", None, ["journey"], "concept"),
            ("context", "A companion for the dead", "In this account, a favourite dog accompanies the ghost through the journey. This is Spence's summary of a source tradition, not a universal Mesoamerican afterlife map.", ["journey"], "concept"),
            ("method", "Do not generalize across peoples", "Spence's discussion is an early twentieth-century synthesis. The location and sequence should be attributed to the Mexican material as he presents it, not generalized to Maya, Peruvian, or all Indigenous traditions.", ["journey"], "source"),
            ("synthesis", "A source-specific afterlife account", "Read the route as one account within Spence's compilation; keep its monsters, tests, and companion attached to that written framing.", ["journey"], "source"),
        ],
        "questions": [
            ("What animal accompanies the dead person in Spence's account?", "A favourite dog", ["A nine-headed serpent", "An eagle carrying a cactus"], "Spence says the ghost is accompanied by the shade of a favourite dog.", ["journey"], "concept"),
            ("Which boundary matters when using this passage?", "It is Spence's account of Mexican material, not a universal Mesoamerican belief", ["It is a direct Maya inscription", "It is a Peruvian eyewitness report"], "The citation comes from Spence's broad synthesis and should not be generalized to distinct traditions.", ["journey"], "source"),
        ],
    },
    {
        "slug": "sacred-obligation",
        "title": "The Mexica Foundation Omen",
        "subtitle": "An origin tradition for the city of Mexico",
        "refs": [
            ("omen", "Chapter I · THE CIVILISATION OF MEXICO", "The most popular of these relates how the nomadic Nahua", "laid the foundation of the great city of Mexico."),
        ],
        "cards": [
            ("context", "A sign at a marshy site", "Spence recounts a migration legend in which the Nahua see an eagle on a cactus with a serpent in its talons and the rising sun behind it.", ["omen"], "concept"),
            ("source", "Reading the sign", None, ["omen"], "concept"),
            ("context", "A settlement follows", "In Spence's account, interpreters read the sight as a good omen and advise the people to settle there; they begin building on the marshy ground.", ["omen"], "concept"),
            ("method", "An origin narrative is not a site report", "Spence presents this as a popular legend about the foundation of Mexico. It is evidence for the written origin account, not independent proof that the event happened as described.", ["omen"], "source"),
            ("synthesis", "Name the people and source", "The passage concerns the Mexica/Nahua migration story as Spence records it; it should not be made representative of all Mesoamerican histories.", ["omen"], "source"),
        ],
        "questions": [
            ("What omen do the nomadic Nahua see in Spence's account?", "An eagle on a cactus holding a serpent", ["A white rabbit on a cold moon", "A raft of serpents carrying a smith"], "The passage describes an eagle on a cactus with a serpent in its talons.", ["omen"], "concept"),
            ("What do the interpreters advise after seeing the omen?", "Settle on the spot", ["Leave for Tlapallan", "Build a forge for the Sampo"], "Spence says the soothsayers advise the leaders to settle there.", ["omen"], "source"),
        ],
    },
]


def make_reference(record, spec):
    if len(spec) == 4:
        ref_id, segment_locator, start_anchor, end_anchor = spec
        source_locator = segment_locator
    else:
        ref_id, segment_locator, source_locator, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / "content/corpus/mesoamerican" / record["localPath"])
         if item["locator"] == segment_locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named Spence section not found: {segment_locator}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {source_locator}")
    end += len(end_anchor)
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": "Lewis Spence",
        "translator": "not applicable; authored in English",
        "locator": f"{source_locator}; {segment_locator}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/mesoamerican/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim prose from Lewis Spence's early twentieth-century synthesis, not a direct translation of the Indigenous source material he discusses. Preserve its dated, colonial framing.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/mesoamerican/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == "pg-53080")
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/mesoamerican").rglob("*.json")
    }
    changes = {}
    for spec in PACK:
        path = paths[spec["slug"]]
        lesson = json.loads(path.read_text(encoding="utf-8"))
        current_version = lesson.get("version", 1)
        lesson["version"] = current_version + 1 if current_version >= 2 else 2
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
        lesson["sourceReferences"] = {item[0]: make_reference(record, item) for item in spec["refs"]}
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, refs, objective) in enumerate(spec["cards"], 1):
            if body is None:
                body = "Quotation from Spence's English prose synthesis (whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the named chapter section in Spence's synthesis.",
                    "suggestedQuestions": ["Which words support this answer?", "Which community or source does this passage name?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Mexica and Toltec passages in Spence's dated synthesis; independent Indigenous, historical, translation, and pedagogical review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    parser.add_argument("--revise-v2", metavar="INPUT_SHA256")
    parser.add_argument("--revise-v3", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/mesoamerican").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    versions = {json.loads(path.read_text(encoding="utf-8")).get("version", 1) for path in paths}
    if args.apply and versions != {1}:
        parser.error("--apply only accepts the exact version-1 Mesoamerican starter lessons.")
    if args.revise_v2 and versions != {2}:
        parser.error("--revise-v2 only accepts the exact version-2 Mesoamerican starter lessons.")
    if args.revise_v3 and versions != {3}:
        parser.error("--revise-v3 only accepts the exact version-3 Mesoamerican starter lessons.")
    if versions - {1, 2, 3}:
        parser.error("Refusing to write beyond the reviewed one-time migrations for this pack.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} community-specific lessons; no files written.")
    expected_digest = args.apply or args.revise_v2 or args.revise_v3
    if expected_digest:
        if expected_digest != digest:
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

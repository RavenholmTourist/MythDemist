"""One-time, digest-guarded source revision for Chinese tradition starter lessons."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
WERNER = "content/corpus/chinese/primary/myths-legends-china-werner-15250.txt"
MACGOWAN = "content/corpus/chinese/primary/chinese-folk-lore-tales-macgowan-26070.txt"

PACK = [
    {
        "slug": "heaven-earth",
        "title": "P'an Ku: A Taoist Creation Account",
        "subtitle": "A later cosmogony and its editorial frame",
        "refs": [
            ("creation", WERNER, "Chapter III · Cosmogony-p'an Ku and the Creation Myth", "His task occupied eighteen thousand years", "insects creeping over his body human beings"),
            ("origin", WERNER, "Chapter III · Cosmogony-p'an Ku and the Creation Myth", "This account of P'an Ku and his achievements is of Taoist origin.", "must not be mistaken for Buddhist cosmogony proper."),
        ],
        "cards": [
            ("context", "P'an Ku shapes Chaos", "Werner's 1922 English synthesis describes P'an Ku as a figure who chisels the universe out of Chaos. In this account, his work lasts eighteen thousand years.", ["creation"], "concept"),
            ("source", "A world formed from a body", None, ["creation"], "concept"),
            ("context", "The body becomes the world", "Werner's account says P'an Ku's head becomes mountains, breath becomes wind and clouds, blood becomes rivers, and flesh becomes soil.", ["creation"], "concept"),
            ("method", "Do not call this timeless canon", "Werner identifies this as a Taoist-origin account and notes that he sees no evidence for P'an Ku before the surviving written account. This is a modern synthesis, not a translation of one ancient creation text.", ["origin"], "source"),
            ("synthesis", "The account has a history", "The story explains cosmic features through the transformation of P'an Ku's body, while Werner's discussion also records disagreement about the figure's historical development.", ["creation", "origin"], "source"),
        ],
        "questions": [
            ("How long does Werner's P'an Ku account say his cosmic work lasted?", "Eighteen thousand years", ["Seven days", "One hundred years"], "The passage says his task occupied eighteen thousand years.", ["creation"], "concept"),
            ("How does Werner classify this P'an Ku creation account?", "As Taoist in origin, with its history treated cautiously", ["As a direct translation of the earliest Chinese scripture", "As a story from Macgowan's collected folk tales"], "Werner explicitly calls the account Taoist in origin and discusses uncertainty about when it appeared.", ["creation"], "source"),
        ],
    },
    {
        "slug": "nuwa-repair",
        "title": "Nue Kua: Repairing the Heavens",
        "subtitle": "A tradition transmitted through Werner's synthesis",
        "refs": [
            ("repair", WERNER, "Chapter III · Cosmogony-p'an Ku and the Creation Myth", "The pillars of Heaven were broken", "the early seat of the Chinese sovereignty]."),
        ],
        "cards": [
            ("context", "A damaged cosmos", "Werner's 1922 synthesis attributes to Ssu-ma Cheng an account in which Kung Kung's rebellion ends with a mountain struck down and the cosmic supports broken.", ["repair"], "concept"),
            ("source", "Repair after the collapse", None, ["repair"], "concept"),
            ("context", "Stones, tortoise, and reeds", "In the account Werner quotes, Nue Kua melts five-coloured stones to repair heaven, uses a tortoise's feet to support earth, and stops floodwater with reed ashes.", ["repair"], "concept"),
            ("method", "Keep the transmission visible", "The lesson quotes Werner's English rendering of an account he attributes to Ssu-ma Cheng. It is not a direct translation made here from the Historical Records, and Werner's wording and framing should remain visible.", ["repair"], "source"),
            ("synthesis", "Restoration is the central action", "This version centers repair after damage rather than presenting Nue Kua as the sole maker of heaven and earth.", ["repair"], "concept"),
        ],
        "questions": [
            ("What does Werner's quoted account say Nue Kua melts to repair heaven?", "Stones of five colours", ["Iron from a celestial rod", "Nine arrows from a mountain"], "The passage says she melted stones of five colours to repair the heavens.", ["repair"], "concept"),
            ("What source boundary should readers keep in mind?", "This is Werner's English rendering of an account attributed to Ssu-ma Cheng", ["It is an eyewitness account by a modern folklorist", "It is a complete translation of a single oral performance"], "Werner introduces the words as an account by Ssu-ma Cheng; this lesson has not independently translated that source.", ["repair"], "source"),
        ],
    },
    {
        "slug": "yu-flood",
        "title": "Shen I: The Nine False Suns",
        "subtitle": "A modern synthesis links disaster and archery",
        "refs": [
            ("crisis", WERNER, "Chapter V · Myths of the Stars", "At this time terrible calamities began to lay waste the land.", "placing three hundred men at his service for that purpose."),
            ("suns", WERNER, "Chapter V · Myths of the Stars", "After this first victory Shen I led his troops", "the nine arrows stuck in nine red stones at the top of the mountain."),
        ],
        "cards": [
            ("context", "A land in crisis", "Werner's synthesis describes ten suns, storms, floods, a giant serpent, and destructive boars. Yao sends Shen I and a force of three hundred men to confront the calamities.", ["crisis"], "concept"),
            ("source", "The nine false suns", None, ["suns"], "concept"),
            ("context", "Arrows and red clouds", "In Werner's account, nine fiery birds create nine additional suns. Shen I shoots them; the false suns become red clouds and disappear.", ["suns"], "concept"),
            ("method", "An early twentieth-century synthesis", "This episode is Werner's English retelling and arrangement of Chinese myth material. It should not be mistaken for one consistent version or a direct translation from a named early text.", ["crisis", "suns"], "source"),
            ("synthesis", "Cosmic crisis and skilled action", "The story joins environmental disaster with a hero's task, but its details belong to Werner's compiled version.", ["crisis", "suns"], "source"),
        ],
        "questions": [
            ("What does Werner's account say produced the nine false suns?", "Nine extraordinary birds blowing out fire", ["A tortoise carrying burning stones", "The moon's rabbit scattering sparks"], "The passage says nine birds on nearby peaks blew fire to form the false suns.", ["suns"], "concept"),
            ("What happens after Shen I shoots the birds?", "The false suns become red clouds and melt away", ["They turn into the moon", "They flood the capital"], "Werner's passage says the false suns resolve into red clouds and melt away.", ["suns"], "source"),
        ],
    },
    {
        "slug": "change-moon",
        "title": "Heng O: Flight to the Moon",
        "subtitle": "An immortality pill in Werner's retelling",
        "refs": [
            ("flight", WERNER, "Chapter V · Myths of the Stars", "Heng O, during her husband's absence", "a blast of wind struck him to the ground like a dead leaf."),
            ("moon", WERNER, "Chapter V · Myths of the Stars", "Heng O continued her flight", "She took up her abode in this sphere."),
        ],
        "cards": [
            ("context", "The pill is found", "In Werner's version, Heng O finds and eats a pill of immortality while Shen I is away. When he returns, she opens a window and flies out.", ["flight"], "concept"),
            ("source", "A flight toward the moon", None, ["flight"], "concept"),
            ("context", "A rabbit on a cold sphere", "Werner describes Heng O reaching a cold, luminous sphere. She coughs up the pill's covering, which changes into a white rabbit, and stays there.", ["moon"], "concept"),
            ("method", "One version, not every telling", "The name here is Heng O, and the scene is Werner's early twentieth-century retelling. Do not treat its details as a universal or unchanging account of the moon story.", ["flight", "moon"], "source"),
            ("synthesis", "The moon story has variants", "Werner's episode links immortality, flight, and the rabbit; other retellings can vary in names, motives, and details.", ["flight", "moon"], "source"),
        ],
        "questions": [
            ("What does Heng O eat in Werner's retelling?", "A pill of immortality", ["A white jade rabbit", "A five-coloured stone"], "The passage says she finds the pill of immortality and eats it.", ["flight"], "concept"),
            ("What happens to the covering of the pill?", "It changes into a white rabbit", ["It becomes a red cloud", "It turns into a tortoise"], "Werner says she vomits the covering, which becomes a white rabbit.", ["moon"], "source"),
        ],
    },
    {
        "slug": "immortals-order",
        "title": "A Benevolent Life and the Coming Flood",
        "subtitle": "A twentieth-century English folklore collection",
        "refs": [
            ("warning", MACGOWAN, "THE REWARD OF A BENEVOLENT LIFE", "Before very long a great flood will take place in this district", "eyes of the stone lions in the East Street of the city shed tears of blood"),
            ("rescue", MACGOWAN, "THE REWARD OF A BENEVOLENT LIFE", "Chung replied that at such a time", "he was hauled into it and delivered from his peril."),
        ],
        "cards": [
            ("context", "A warning with a sign", "In Macgowan's collected literary tale, a priest warns Chung's household about a sudden flood and tells them to leave when the stone lions' eyes appear to shed blood.", ["warning"], "concept"),
            ("source", "The warning and the signal", None, ["warning"], "concept"),
            ("context", "Chung chooses to rescue", "When the flood arrives, Chung's wife recalls the warning not to rescue a man from the river. Chung decides that a person in immediate danger must still be saved.", ["rescue"], "concept"),
            ("method", "A collected tale, not a social survey", "Macgowan's Chinese Folk-Lore Tales is a literary collection in English. This episode supports claims about this written tale, not a universal Chinese belief or historical flood event.", ["warning", "rescue"], "source"),
            ("synthesis", "The title's moral is tested", "The story tests benevolence through a conflict between a supernatural warning and the immediate duty Chung feels toward a drowning stranger.", ["warning", "rescue"], "concept"),
        ],
        "questions": [
            ("What sign tells Chung's household to seek the boats?", "The stone lions' eyes appear to shed blood", ["A one-legged bird enters the palace", "The moon turns into a toad"], "The priest says the stained eyes will signal that the flood is close.", ["warning"], "concept"),
            ("Why does Chung order the boatmen to rescue the stranger?", "He says a person in immediate danger should not be left to drown", ["He recognizes the stranger as the River God", "The priest orders him to ignore the warning"], "Chung says personal interests should not outweigh saving a person from drowning.", ["rescue"], "source"),
        ],
    },
]


def make_reference(records, spec):
    ref_id, local_path, locator_name, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / local_path)
         if item["locator"] == locator_name and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named source section not found: {locator_name}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {locator_name}")
    end += len(end_anchor)
    relative = local_path.removeprefix("content/corpus/chinese/")
    record = next(item for item in records if item["localPath"] == relative)
    authors = ", ".join(record.get("ancientAuthors", []))
    translator = record.get("translator", "not applicable")
    note = (
        "Quotation from E. T. C. Werner's 1922 English synthesis; it is not a direct translation of the ancient source it discusses."
        if record["id"] == "pg-15250"
        else "Quotation from J. Macgowan's English literary collection of folktales; distinguish this written version from a community-wide canon."
    )
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": authors,
        "translator": translator,
        "locator": f"{locator_name}; {locator_name}, normalized characters {start}-{end}",
        "localPath": local_path,
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": note,
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/chinese/manifest.json").read_text(encoding="utf-8"))
    records = manifest["records"]
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/chinese").rglob("*.json")
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
        lesson["sourceReferences"] = {item[0]: make_reference(records, item) for item in spec["refs"]}
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, refs, objective) in enumerate(spec["cards"], 1):
            if body is None:
                body = "Quotation from the cited English edition (whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the cited passage in its named English edition.",
                    "suggestedQuestions": ["Which words support this answer?", "Is this a synthesis or a collected folktale?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Edition-specific Chinese myth and folklore revisions; independent review of source attribution, translation history, community variation, and pedagogy remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    parser.add_argument("--revise-v2", metavar="INPUT_SHA256", help="apply the checked editorial refinement to exact version-2 outputs")
    parser.add_argument("--revise-v3", metavar="INPUT_SHA256", help="apply the section-locator refinement to exact version-3 outputs")
    parser.add_argument("--revise-v4", metavar="INPUT_SHA256", help="apply the citation-anchor refinement to exact version-4 outputs")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/chinese").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    versions = {json.loads(path.read_text(encoding="utf-8")).get("version", 1) for path in paths}
    if args.apply and versions != {1}:
        parser.error("--apply only accepts the exact version-1 Chinese starter lessons.")
    if args.revise_v2 and versions != {2}:
        parser.error("--revise-v2 only accepts the exact version-2 Chinese starter lessons.")
    if args.revise_v3 and versions != {3}:
        parser.error("--revise-v3 only accepts the exact version-3 Chinese starter lessons.")
    if args.revise_v4 and versions != {4}:
        parser.error("--revise-v4 only accepts the exact version-4 Chinese starter lessons.")
    if versions - {1, 2, 3, 4}:
        parser.error("Refusing to write beyond the reviewed one-time migrations for this pack.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} edition-specific lessons; no files written.")
    expected_digest = args.apply or args.revise_v2 or args.revise_v3 or args.revise_v4
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

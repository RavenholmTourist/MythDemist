"""One-time, digest-guarded revision for Knud Rasmussen's Greenland story collection."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
RASMUSSEN = "content/corpus/inuit/primary/eskimo-folk-tales-28932.txt"

PACK = [
    {
        "slug": "the-sea-and-survival",
        "title": "The Coming of Men",
        "subtitle": "An origin narrative in a Greenland collection",
        "refs": [
            ("people", "The Coming Of Men, A Long, Long While Ago", "A long, long time ago, when the earth was to be made", "And in this way men grew to be many."),
            ("light", "The Coming Of Men, A Long, Long While Ago", "They knew nothing of death in those days", "become brightly shining things there."),
        ],
        "cards": [
            ("context", "A story about how people came", "This Greenland story says that earth, hills, and stones fell from the sky, and that children later came out of the earth among willow bushes.", ["people"], "concept"),
            ("source", "Light and death enter the story", None, ["light"], "concept"),
            ("context", "Two old women disagree", "When people crowd the earth, one old woman asks for a world without day if that will prevent death; another asks for both light and death. The story says the latter wish prevails.", ["light"], "concept"),
            ("method", "A collected Greenland story", "The text was collected by Knud Rasmussen in Greenland and edited into English by W. J. Alexander Worster. Keep this tale within that collection rather than treating it as a pan-Inuit origin account.", ["people", "light"], "source"),
            ("synthesis", "Keep the narrator's uncertainty", "The narrator says that parts of the first people's story are not clearly known. Preserve that uncertainty instead of filling gaps with a universal creation system.", ["people"], "source"),
        ],
        "questions": [
            ("How does the story say children first appeared?", "They came out of the earth among willow bushes", ["They were made from yellow and white maize", "They emerged from a wooden boat"], "The text says little children came out of the earth among willow bushes.", ["people"], "concept"),
            ("What do the two old women disagree about?", "Whether they should have light and death or avoid death by living without day", ["Whether Raven should marry a goose", "Whether the sea should be inside a mountain"], "One woman prefers no day if it means no death; the other wants both light and death.", ["light"], "source"),
        ],
    },
    {
        "slug": "animal-helpers",
        "title": "The Woman and Her Bear Foster-Son",
        "subtitle": "An animal becomes part of a household",
        "refs": [
            ("bear", "The Woman Who Had A Bear As A Foster-Son", "The old woman received a piece from the ribs", "remember to sheathe your claws when you play with them."),
        ],
        "cards": [
            ("context", "A cub comes into the house", "A hunter's household gives an old woman a bear cub. She warms it beside her lamp and feeds it blubber.", ["bear"], "concept"),
            ("source", "A rule for play", None, ["bear"], "concept"),
            ("context", "The cub learns restraint", "The story says the bear grows quickly and joins the children at play. The old woman reminds it to sheath its claws.", ["bear"], "concept"),
            ("method", "One named Greenland tale", "This passage comes from Rasmussen's collection and Worster's English version. Do not turn this single narrative into a universal statement about Inuit relationships with bears.", ["bear"], "source"),
            ("synthesis", "Kinship across species in this story", "The title calls the animal a foster-son; the narrative focuses on care, food, and limits during play.", ["bear"], "concept"),
        ],
        "questions": [
            ("What does the old woman feed the bear cub?", "Greaves and melted blubber", ["Berries and cinnamon", "Yams and peppers"], "The story says she feeds it greaves and melted blubber.", ["bear"], "concept"),
            ("What does the old woman tell the bear to remember when playing with children?", "To sheath its claws", ["To hide its food in a tree", "To leave the village before sunrise"], "She tells the cub to sheath its claws while playing with the children.", ["bear"], "source"),
        ],
    },
    {
        "slug": "moon-tides-and-danger",
        "title": "Kúnigseq Visits the Land of Shades",
        "subtitle": "A visitor must not eat the underworld berries",
        "refs": [
            ("visit", "Kúnigseq", "There was once a wizard whose name was Kúnigseq.", "If you eat of them, you will never return."),
        ],
        "cards": [
            ("context", "A journey below the floor", "Kúnigseq calls his helping spirits and travels down into the underworld, where he meets his dead mother.", ["visit"], "concept"),
            ("source", "A warning at the boundary", None, ["visit"], "concept"),
            ("context", "A visit has rules", "His spirit companion says that if Kúnigseq eats the berries, he will never return. The dead mother invites him to stay, but he says he will come back when he dies.", ["visit"], "concept"),
            ("method", "Do not infer one uniform afterlife", "This is one Greenland story in Rasmussen's collection, translated and edited by Worster. The title's historical spelling and the story's details belong to this edition and its source context.", ["visit"], "source"),
            ("synthesis", "A visit differs from a permanent journey", "The warning about eating marks a boundary between the living visitor and the dead community in this particular tale.", ["visit"], "concept"),
        ],
        "questions": [
            ("What warning does Kúnigseq's helping spirit give about the berries?", "If he eats them, he will never return", ["They will make the Sun move faster", "They will turn him into a raven"], "The spirit warns that eating the berries will prevent Kúnigseq from returning.", ["visit"], "concept"),
            ("What does Kúnigseq say after seeing his dead family?", "He will come again when he dies", ["He will stay forever in the underworld", "He will take the berries back to the village"], "The story quotes Kúnigseq saying he will come again when he dies.", ["visit"], "source"),
        ],
    },
    {
        "slug": "raven-and-daylight",
        "title": "The Raven and the Goose",
        "subtitle": "A short story about colour and stubbornness",
        "refs": [
            ("colours", "The Raven And The Goose", "It happened in the days when all the birds were getting their colours", "the goose, offended at all the fuss, simply splashed it black all over."),
        ],
        "cards": [
            ("context", "Two birds agree to paint", "In this story, Raven and Goose agree to paint each other's feathers while birds are receiving their colours and patterns.", ["colours"], "concept"),
            ("source", "The painting goes wrong", None, ["colours"], "concept"),
            ("context", "The source offers an explanation", "The story says Raven becomes angry about the pattern Goose paints, and Goose responds by splashing Raven all over with black.", ["colours"], "concept"),
            ("method", "Do not turn a story into natural history", "This is a narrative in Rasmussen's Greenland collection, not a zoological account or a claim that every Inuit group tells this exact bird story.", ["colours"], "source"),
            ("synthesis", "A just-so ending", "The final line links Raven's black colour to the quarrel in this tale.", ["colours"], "concept"),
        ],
        "questions": [
            ("What does Goose do after Raven complains about the pattern?", "She splashes Raven all over with black", ["She hides him in a mountain", "She turns into the Moon"], "The story ends by saying Goose splashes Raven black all over.", ["colours"], "concept"),
            ("What kind of story is this passage?", "A folk narrative that explains an animal feature", ["A scientific account of raven plumage", "A direct description of a historical hunt"], "The story uses a quarrel to explain why Raven is black.", ["colours"], "source"),
        ],
    },
    {
        "slug": "shamans-and-taboo",
        "title": "The Man Who Became a Star",
        "subtitle": "A violent story explains a low star in the west",
        "refs": [
            ("star", "The Man Who Became A Star", "There was once an old man who stood out on the ice", "he who stands and listens."),
        ],
        "cards": [
            ("context", "Children disturb a hunt", "An old hunter becomes angry when children repeatedly frighten seals away from his harpoon. He calls for the ravine to close over them.", ["star"], "concept"),
            ("source", "An ending among the stars", None, ["star"], "concept"),
            ("context", "A transformation after pursuit", "The story says the old man flees from the neighbours, becomes a bright star, and remains low in the western sky as the lights return after darkness.", ["star"], "concept"),
            ("method", "Treat the violence plainly", "This collection records a particular Greenland story with a violent outcome. Do not generalize it into a belief shared by all Inuit communities or soften the event into an abstract 'moral.'", ["star"], "source"),
            ("synthesis", "The story names a visible star", "The narrator gives the name N\u00e9laussartoq and glosses it as 'he who stands and listens'; keep that attribution within Rasmussen's collection.", ["star"], "source"),
        ],
        "questions": [
            ("Why does the hunter call for the ravine to close?", "Children keep frightening seals away from his hunt", ["They take his berries from the underworld", "They refuse to play with a bear cub"], "The story says the children repeatedly frighten a seal just as he is about to harpoon it.", ["star"], "concept"),
            ("How does the story end for the old man?", "He becomes a bright star low in the western sky", ["He becomes Raven's wife", "He returns as a bear cub"], "The final lines say he rises as a star and give its Greenlandic name.", ["star"], "source"),
        ],
    },
]


def make_reference(record, spec):
    ref_id, locator, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / "content/corpus/inuit" / record["localPath"])
         if item["locator"] == locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named Rasmussen story not found: {locator}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {locator}")
    end += len(end_anchor)
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": "Greenlandic storytellers, collected by Knud Rasmussen",
        "translator": "W. J. Alexander Worster",
        "locator": f"{locator}; {locator}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/inuit/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim English rendering by Worster from stories collected by Rasmussen in Greenland. The book title uses an outdated ethnonym; this lesson identifies the collection's Greenland scope.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/inuit/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == "pg-28932")
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/inuit").rglob("*.json")
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
        lesson["sourceReferences"] = {item[0]: make_reference(record, item) for item in spec["refs"]}
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, refs, objective) in enumerate(spec["cards"], 1):
            if body is None:
                body = "Quotation from the cited Worster translation (whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the named story in Rasmussen and Worster's Greenland collection.",
                    "suggestedQuestions": ["Which words support this answer?", "What Greenland-specific source label is given?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Greenland-specific tale revisions; independent community, translation, source-history, and pedagogical review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/inuit").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Inuit starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} Greenland-specific lessons; no files written.")
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

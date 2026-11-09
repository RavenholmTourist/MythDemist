"""One-time, digest-guarded revision of Pyle's Lithuanian-labeled folktale."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
PYLE = "content/corpus/baltic/primary/fairy-tales-far-near-66919.txt"

PACK = [
    {
        "slug": "baltic-folk-traditions",
        "title": "The Exiled Princes",
        "subtitle": "The opening scene of one Lithuanian-labeled tale",
        "refs": [
            ("exile", "Pyle retelling · The Princes And The Friendly Animals", "There was once a King who had three sons", "their stepsister with them."),
        ],
        "cards": [
            ("context", "A king loses his kingdom", "In Katherine Pyle's story labeled Lithuanian, an enemy kills the king, takes the kingdom, and drives the three princes and their stepsister into the world.", ["exile"], "concept"),
            ("source", "Four travelers leave together", None, ["exile"], "concept"),
            ("context", "A retold story begins", "The collection frames the text as a Lithuanian story, but does not identify a specific oral informant or an earlier source edition for this tale.", ["exile"], "source"),
            ("method", "A modern English retelling", "Katherine Pyle's 1922 Fairy Tales from Far and Near includes stories explicitly labeled by region. This is a children's literary retelling, not a direct translation of a named Lithuanian manuscript.", ["exile"], "source"),
            ("synthesis", "Limit the claim to this tale", "This lesson follows one Lithuanian-labeled story in Pyle's collection; it is not a complete survey of Baltic mythology or folklore.", ["exile"], "source"),
        ],
        "questions": [
            ("Who leaves the kingdom after the enemy takes it?", "The three princes and their stepsister", ["The Sun, Moon, and Raven", "The seven sons of Xibalba"], "Pyle's opening says the enemy drives the princes and their stepsister into the world.", ["exile"], "concept"),
            ("How is this tale identified in Pyle's book?", "As a Lithuanian story in a modern English collection", ["As an ancient eyewitness chronicle", "As a direct translation from a named runic manuscript"], "The title labels it 'A Lithuanian Story,' while the book is Pyle's 1922 English collection.", ["exile"], "source"),
        ],
    },
    {
        "slug": "lithuanian-heroes",
        "title": "The Animals Become Helpers",
        "subtitle": "Each prince spares a mother animal",
        "refs": [
            ("helpers", "Pyle retelling · The Princes And The Friendly Animals", "The eldest Prince was about to shoot at her", "now each Prince had a young fox, a young lion and a young bear to follow him."),
        ],
        "cards": [
            ("context", "A bear asks to be spared", "When the princes meet a mother bear and her cubs, she asks them not to kill her and offers one cub to each brother.", ["helpers"], "concept"),
            ("source", "The bargain repeats", None, ["helpers"], "concept"),
            ("context", "Lioness and fox follow", "The second prince spares a lioness, then the youngest spares a fox. By the end, each prince is followed by a bear, lion, and fox cub.", ["helpers"], "concept"),
            ("method", "Do not universalize animal meanings", "The tale gives these animals specific roles in Pyle's retelling. It does not establish a fixed Baltic symbolism for bears, lions, or foxes.", ["helpers"], "source"),
            ("synthesis", "The helpers follow acts of mercy", "The princes gain companions after sparing each mother animal in this story's sequence.", ["helpers"], "concept"),
        ],
        "questions": [
            ("What does the mother bear offer if the princes spare her?", "Her three cubs, one for each prince", ["A golden ring", "A magic stick"], "The bear offers a cub to each brother in exchange for being spared.", ["helpers"], "concept"),
            ("Which animals follow each prince by the end of the passage?", "A bear cub, a lion cub, and a fox cub", ["A raven, a goose, and a dog", "A dragon, a wolf, and a hare"], "The excerpt concludes that each prince has a young fox, lion, and bear following him.", ["helpers"], "source"),
        ],
    },
    {
        "slug": "sun-and-sacred-groves",
        "title": "Three Roads and a Tree's Warning",
        "subtitle": "Milk or blood marks the brothers' fortunes",
        "refs": [
            ("notches", "Pyle retelling · The Princes And The Friendly Animals", "The three brothers then asked their stepsister", "death or misfortune to that one."),
        ],
        "cards": [
            ("context", "The family parts at a crossroads", "The youngest prince chooses east, the second west, and the eldest chooses the road straight ahead. Their stepsister goes with the eldest.", ["notches"], "concept"),
            ("source", "A sign for each brother", None, ["notches"], "concept"),
            ("context", "The tree records their fortunes", "The eldest prince cuts a notch for each brother and explains the sign: milk means all is well; blood means death or misfortune.", ["notches"], "concept"),
            ("method", "A story device, not a ritual claim", "The notched tree is a plot device in Pyle's Lithuanian-labeled story. Do not present it as evidence of a documented Baltic divination practice.", ["notches"], "source"),
            ("synthesis", "The sign sets up the next event", "The brothers' separate roads and the tree's signal give the tale a way to reunite their stories later.", ["notches"], "concept"),
        ],
        "questions": [
            ("What does milk from a brother's notch mean?", "All is well with that brother", ["He has reached the dragon", "The prince must return to the crossroads"], "The eldest says milk means all is well, while blood means death or misfortune.", ["notches"], "concept"),
            ("Which direction does the eldest prince choose?", "Straight ahead, neither east nor west", ["East toward sunrise", "West toward sunset"], "The eldest says his road will go straight ahead.", ["notches"], "source"),
        ],
    },
    {
        "slug": "fate-and-helpers",
        "title": "The Dragon and the Youngest Prince",
        "subtitle": "Animal helpers join the fight",
        "refs": [
            ("dragon", "Pyle retelling · The Princes And The Friendly Animals", "The Prince hid himself behind a heap of rocks", "the life blood ran out from it into the sea, and it was dead."),
        ],
        "cards": [
            ("context", "A princess is offered as a reward", "The youngest prince hears that a dragon threatens the country and that the king promises his daughter's hand to whoever defeats it.", ["dragon"], "concept"),
            ("source", "The animals attack", None, ["dragon"], "concept"),
            ("context", "The prince delivers the final blow", "The fox splashes water into the dragon's eyes, the bear and boar attack, and the hare strikes its head; the prince's sword kills it.", ["dragon"], "concept"),
            ("method", "Keep the plot and source attribution distinct", "Pyle's story calls this a Lithuanian tale, but does not identify an informant or source-language text. Teach the episode as Pyle's retelling.", ["dragon"], "source"),
            ("synthesis", "Victory is collaborative", "The scene gives the animals active roles in the fight rather than making the prince succeed alone.", ["dragon"], "concept"),
        ],
        "questions": [
            ("How does the fox help fight the dragon?", "It splashes water into the dragon's eyes", ["It cuts the dragon's tongue", "It lures the dragon into the sea"], "The excerpt says the fox dips its tail in salty water and slashes it across the dragon's eyes.", ["dragon"], "concept"),
            ("Who delivers the final wound in this episode?", "The youngest prince", ["The princess", "The old woman by the fire"], "After the animals help, the prince plunges his sword into the dragon's heart.", ["dragon"], "source"),
        ],
    },
    {
        "slug": "european-variants",
        "title": "Betrayal, Healing, and Return",
        "subtitle": "The animals rescue the prince",
        "refs": [
            ("betrayal", "Pyle retelling · The Princes And The Friendly Animals", "But after they had driven on and left the Prince lying there", "he became quite well again and stronger than ever."),
        ],
        "cards": [
            ("context", "The prince is betrayed", "On the way to the palace, two nobles kill the prince and threaten the princess into silence so one of them can claim the reward.", ["betrayal"], "concept"),
            ("source", "The animals stay", None, ["betrayal"], "concept"),
            ("context", "Medicine brings him back", "The animals mourn beside the prince. The fox remembers healing supplies at the robbers' house; the hare fetches them, and the bear treats the wounds.", ["betrayal"], "concept"),
            ("method", "A tale's sequence, not historical testimony", "This is one written Lithuanian-labeled story in Pyle's children's collection. Its healing water and animal helpers support claims about this plot only.", ["betrayal"], "source"),
            ("synthesis", "A promise is finally fulfilled", "The rescued prince can continue to the palace, where the story's earlier rescue and betrayal are brought to light.", ["betrayal"], "concept"),
        ],
        "questions": [
            ("Who fetches the healing flasks for the wounded prince?", "The hare", ["The dragon", "The stepsister"], "The hare runs to the robbers' house and returns with the flasks.", ["betrayal"], "concept"),
            ("What does the bear do with the ointment?", "Rubs it on the prince's wounds", ["Uses it to turn the nobles to stone", "Pours it into the sea"], "The passage says the bear rubs the ointment on the prince's wounds.", ["betrayal"], "source"),
        ],
    },
]


def make_reference(record, spec):
    ref_id, locator, start_anchor, end_anchor = spec
    segment_locator = "Pyle retelling · The Princes And The Friendly Animals"
    segment = next(
        (item for item in source_segments(ROOT / "content/corpus/baltic" / record["localPath"])
         if item["locator"] == segment_locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named Pyle retelling section not found: {segment_locator}")
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
        "author": "Katherine Pyle",
        "translator": "not applicable; authored in English",
        "locator": f"{locator}; {segment_locator}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/baltic/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim text from Katherine Pyle's 1922 English children's retelling. The collection labels it Lithuanian but does not identify an oral informant or underlying source text.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/baltic/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == "pg-66919")
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/baltic").rglob("*.json")
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
                body = "Quotation from Pyle's English retelling (whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the named Lithuanian-labeled tale in Pyle's collection.",
                    "suggestedQuestions": ["Which words support this answer?", "What does the collection not tell us about the tale's original source?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "One Lithuanian-labeled tale as retold by Katherine Pyle; this is not a survey of Baltic traditions and the original source/informant is unspecified.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/baltic").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Baltic starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared five scenes from one Lithuanian-labeled tale; no files written.")
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

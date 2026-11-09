"""One-time, digest-guarded revision of Mooney's Cherokee story selections."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
MOONEY = "content/corpus/cherokee/primary/myths-cherokee-mooney-45634.txt"

PACK = [
    {
        "slug": "how-the-world-was-made",
        "title": "How the World Was Made",
        "subtitle": "A creation narrative in Mooney's field collection",
        "refs": [
            ("earth", "Myth 1 · HOW THE WORLD WAS MADE", "The earth is a great island floating in a sea of water", "it became the island which we call the earth."),
            ("buzzard", "Myth 1 · HOW THE WORLD WAS MADE", "When he reached the Cherokee country", "the Cherokee country remains full of mountains to this day."),
        ],
        "cards": [
            ("context", "Land begins in water", "Mooney's recorded narrative describes the earth as an island above water. The Water-beetle dives to the bottom and brings up soft mud.", ["earth"], "concept"),
            ("source", "A bird shapes the land", None, ["buzzard"], "concept"),
            ("context", "A Cherokee place enters the story", "The Great Buzzard's wings strike the soft earth; Mooney's version connects those impacts with valleys and mountains in Cherokee country.", ["buzzard"], "concept"),
            ("method", "Scope the record", "Mooney collected this work chiefly among Eastern Cherokee communities in North Carolina, with some additional material from western communities. It is not every Cherokee creation account.", ["earth", "buzzard"], "source"),
            ("synthesis", "Keep the story version visible", "The earth-making and mountain-making details here are from Mooney's printed English record; later readers should not silently merge other Cherokee versions.", ["earth", "buzzard"], "source"),
        ],
        "questions": [
            ("What brings up the mud that becomes land?", "The Water-beetle dives to the bottom and brings it up", ["The Great Buzzard carries it from the Sun", "The Uktena leaves it on a mountain"], "The opening says the Water-beetle dives and returns with soft mud.", ["earth"], "concept"),
            ("How are valleys and mountains formed in this version?", "The Great Buzzard's wings strike and turn up the soft earth", ["The Sun melts the ground with a crystal", "The Rabbit digs the animals' well"], "The story links the Buzzard's wing strokes with valleys and mountains.", ["buzzard"], "source"),
        ],
    },
    {
        "slug": "kanati-and-selu",
        "title": "Kana'ti and Selu: Game and Corn",
        "subtitle": "A family story explaining food and animal origins",
        "refs": [
            ("boy", "Myth 3 · KANA'TI AND SELU: THE ORIGIN OF GAME AND CORN", "Then they knew that the strange boy had sprung from the blood of the game", "at the river's edge."),
            ("corn", "Myth 3 · KANA'TI AND SELU: THE ORIGIN OF GAME AND CORN", "wherever her body was dragged corn would come up", "they must always save some for seed and plant every year."),
        ],
        "cards": [
            ("context", "A second child appears", "Kana'ti and Selu's son tells them that a playmate comes out of the water and calls himself his elder brother.", ["boy"], "concept"),
            ("source", "The story explains the brother's origin", None, ["boy"], "concept"),
            ("context", "A second origin follows", "Later in the same narrative, Selu says corn will grow wherever her body is dragged and tells the boys to save seed for planting.", ["corn"], "concept"),
            ("method", "Keep this account situated", "Mooney records this tale in his 1902 collection of Cherokee stories. It is a historical English record with an ethnographic frame, not a statement about every Cherokee community today.", ["boy", "corn"], "source"),
            ("synthesis", "One narrative links food and kinship", "The tale connects the origin of game with the origin and planting of corn; keep those events within this recorded story.", ["boy", "corn"], "source"),
        ],
        "questions": [
            ("What does the story say the other boy came from?", "The blood of game that Selu washed at the river", ["A crystal from Uktena's forehead", "A pine-gum figure by a well"], "Kana'ti and Selu infer the boy's origin from the game blood washed at the river.", ["boy"], "concept"),
            ("What instruction does Selu give about corn?", "Save some seed and plant it every year", ["Carry it to the Sun and never plant it", "Keep it hidden in the underworld"], "Selu tells the boys to save seed for yearly planting.", ["corn"], "source"),
        ],
    },
    {
        "slug": "uktena-and-danger",
        "title": "Agan-Unitsi's Search for the Uktena",
        "subtitle": "A dangerous hunt for the serpent's talisman",
        "refs": [
            ("search", "Myth 51 ·", "Other places he tried, going always southward", "at last on Gahû'ti mountain he found the Uktena asleep."),
            ("hunt", "Myth 51 ·", "The Uktena was still asleep", "the magician on the inside was untouched except by one small drop"),
            ("crystal", "Myth 50 ·", "The blazing diamond is called Ulûñsû'ti", "it is worth a man's life to attempt it"),
        ],
        "cards": [
            ("context", "A promise to find the Uktena", "Mooney's story says Agan-Unitsi is captured in war and promises to find the dangerous Uktena and its bright talisman.", ["search", "crystal"], "concept"),
            ("source", "The search reaches Gahû'ti", None, ["search"], "concept"),
            ("context", "A plan rather than a direct attack", "Agan-Unitsi makes a circle of pine cones, a trench, and fire before shooting the sleeping serpent beneath the seventh spot.", ["hunt"], "concept"),
            ("method", "Do not turn this into a safety guide", "This is a recorded Cherokee narrative about a dangerous being and a powerful object. It is not advice for approaching wildlife or a claim about present-day Cherokee practice.", ["hunt", "crystal"], "source"),
            ("synthesis", "The prize carries danger", "The narrative pairs the Uktena's crystal with danger to the hunter and his family; its power is not presented as consequence-free.", ["crystal"], "source"),
        ],
        "questions": [
            ("Where does Agan-Unitsi finally find the Uktena?", "Asleep on Gahû'ti mountain", ["At the edge of the Achaean ships", "Inside the labyrinth at Crete"], "The story says he finds the Uktena asleep on Gahû'ti mountain.", ["search"], "concept"),
            ("How does he keep the serpent's poison from reaching him?", "He hides inside a ring of fire and a trench", ["He uses Ariadne's clue", "He climbs onto a ship's mast"], "The account says the poison cannot pass the fire circle and trench.", ["hunt"], "source"),
        ],
    },
    {
        "slug": "animal-stories",
        "title": "The Rabbit and the Tar Wolf",
        "subtitle": "A printed Cherokee animal story about a stolen drink",
        "refs": [
            ("tarwolf", "Myth 21 · THE RABBIT AND THE TAR WOLF", "They noticed that the Rabbit kept sleek and lively", "there he stuck until the animals came for water in the morning."),
        ],
        "cards": [
            ("context", "A shared well runs low", "The animals dig a well during a drought. They suspect Rabbit is secretly drinking from it at night.", ["tarwolf"], "concept"),
            ("source", "A trap made from pine gum and tar", None, ["tarwolf"], "concept"),
            ("context", "Rabbit gets stuck", "The animals make a wolf figure from pine gum and tar. Rabbit strikes it, becomes stuck, and is found the next morning.", ["tarwolf"], "concept"),
            ("method", "Mooney identifies a printed source", "Mooney's note attributes this version to the Cherokee Advocate of December 18, 1845. Treat it as a story preserved in a Cherokee newspaper, not as a direct transcript of a named oral performance.", ["tarwolf"], "source"),
            ("synthesis", "Keep the source history attached", "The plot can be read as an animal trickster tale, while its cited newspaper source is part of the evidence.", ["tarwolf"], "source"),
        ],
        "questions": [
            ("What do the animals make to catch the water thief?", "A wolf figure made from pine gum and tar", ["A bear cub from blubber", "A golden ring"], "The story says the animals make a wolf of pine gum and tar.", ["tarwolf"], "concept"),
            ("How does Rabbit become stuck?", "He strikes the sticky figure with his paw", ["He eats a plant from the underworld", "He follows the Uktena into a cave"], "Rabbit strikes the tar figure and the gum holds his paw.", ["tarwolf"], "source"),
        ],
    },
    {
        "slug": "medicine-and-sacred-speech",
        "title": "Origin of Disease and Medicine",
        "subtitle": "A story about animals, plants, and human conduct",
        "refs": [
            ("animals", "Myth 4 · ORIGIN OF DISEASE AND MEDICINE", "This was bad enough, but to make it worse Man invented bows", "the animals resolved to consult upon measures for their common safety."),
            ("plants", "Myth 4 · ORIGIN OF DISEASE AND MEDICINE", "When the Plants, who were friendly to Man", "Thus came medicine"),
        ],
        "cards": [
            ("context", "Animals call a council", "In Mooney's recorded narrative, animals complain that people hunt and kill them, and decide to meet in council.", ["animals"], "concept"),
            ("source", "Plants respond after the animals", None, ["plants"], "concept"),
            ("context", "The story gives each plant a role", "The narrative says trees, shrubs, herbs, grasses, and mosses agree to provide remedies for diseases.", ["plants"], "concept"),
            ("method", "A historical narrative, not medical advice", "This is Mooney's 1902 English record of a Cherokee story. It does not validate treatments or describe all present-day Cherokee medicine.", ["animals", "plants"], "source"),
            ("synthesis", "The tale links human behavior and consequence", "The story frames disease as a response to harm done to animals and medicine as help offered by plants; keep that explanation inside this particular narrative.", ["animals", "plants"], "source"),
        ],
        "questions": [
            ("Why do the animals hold a council in the story?", "People hunt, kill, and use them without regard", ["The princes need help escaping a maze", "The Sun asks them to move the mountains"], "The opening says animals object to being killed for food and skins and to being carelessly harmed.", ["animals"], "concept"),
            ("What do the plants agree to provide?", "A cure for some of the diseases named", ["A new king for the Cherokee", "A magic spear for the Uktena"], "The story says each plant offers a remedy for one of the diseases.", ["plants"], "source"),
        ],
    },
]


def make_reference(record, spec):
    key, locator_prefix, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / "content/corpus/cherokee" / record["localPath"])
         if item["locator"].startswith(locator_prefix) and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named Mooney myth not found: {locator_prefix}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {locator_prefix}")
    end += len(end_anchor)
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": "James Mooney",
        "translator": "James Mooney (English rendering and editor)",
        "locator": f"{locator_prefix}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/cherokee/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim English text from Mooney's 1902 collection. Keep the specific numbered story and its East Cherokee/recorded-source context attached.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/cherokee/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == "pg-45634")
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/cherokee").rglob("*.json")
    }
    changes = {}
    for spec in PACK:
        path = paths[spec["slug"]]
        lesson = json.loads(path.read_text(encoding="utf-8"))
        lesson["version"] = lesson.get("version", 1) + 1
        lesson["title"] = spec["title"]
        lesson["subtitle"] = spec["subtitle"]
        lesson["estimatedMinutes"] = 3
        lesson["difficulty"] = 2
        objectives = [item["id"] for item in lesson["learningObjectives"]]
        lesson["learningObjectives"] = [
            {"id": objectives[0], "text": spec["questions"][0][0]},
            {"id": objectives[-1], "text": spec["questions"][1][0]},
        ]
        lesson["sourceReferences"] = {item[0]: make_reference(record, item) for item in spec["refs"]}
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, ref_ids, objective) in enumerate(spec["cards"], 1):
            if body is None:
                body = "Quotation from Mooney's English record (whitespace normalized): “" + lesson["sourceReferences"][ref_ids[0]]["excerpt"] + "”"
            lesson["narrativeBlocks"].append({
                "id": f"card-{index:02d}", "kind": kind, "title": title, "body": body,
                "sourceRefIds": ref_ids,
                "objectiveIds": [objectives[0] if objective == "concept" else objectives[-1]],
            })
        lesson["quiz"] = []
        for index, (prompt, correct, wrong, explanation, ref_ids, objective) in enumerate(spec["questions"]):
            choices = [correct, *wrong]
            shift = (index + len(changes)) % 3
            choices = choices[shift:] + choices[:shift]
            choice_docs = [{"id": chr(97 + i), "text": text} for i, text in enumerate(choices)]
            lesson["quiz"].append({
                "id": f"q{index + 1}", "type": "single-choice", "prompt": prompt,
                "choices": choice_docs,
                "answerId": next(c["id"] for c in choice_docs if c["text"] == correct),
                "explanation": explanation, "sourceRefIds": ref_ids,
                "objectiveIds": [objectives[0] if objective == "concept" else objectives[-1]],
                "deepDive": {
                    "prompt": "Read the numbered story in Mooney's Cherokee collection.",
                    "suggestedQuestions": ["Which words support this answer?", "What community or publication does Mooney identify?"],
                    "sourceRefIds": ref_ids,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Mooney's historical Cherokee collection; community and source type are identified, but independent community-led review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    parser.add_argument("--revise-v2", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/cherokee").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    versions = {json.loads(path.read_text(encoding="utf-8")).get("version", 1) for path in paths}
    if args.apply and versions != {1}:
        parser.error("--apply only accepts the exact version-1 Cherokee starter lessons.")
    if args.revise_v2 and versions != {2}:
        parser.error("--revise-v2 only accepts the exact version-2 Cherokee starter lessons.")
    if versions - {1, 2}:
        parser.error("Refusing to write beyond the reviewed one-time migrations for this pack.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} passage-specific Cherokee lessons; no files written.")
    expected_digest = args.apply or args.revise_v2
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

"""One-time, digest-guarded source revision for the five Slavic folklore lessons."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
RALSTON = "pg-22373"

PACK = [
    {
        "slug": "baba-yaga",
        "title": "Baba Yaga in Vasilissa the Fair",
        "subtitle": "A dangerous host in one Russian folktale",
        "refs": [
            ("scene", "Vasilissa the Fair, Baba Yaga's daily routine", "The Baba Yaga went out into the courtyard", "all her work was done already."),
        ],
        "objectives": [
            ("What does this tale show about Baba Yaga's power over Vasilissa?", "Her household tests Vasilissa with frightening tasks."),
            ("What does Ralston's source let us claim?", "It records one collected Russian tale, not a fixed Slavic canon."),
        ],
        "cards": [
            ("context", "At Baba Yaga's house", "In Ralston's Vasilissa the Fair, the witch leaves the girl with difficult work. The scene makes the household itself a test.", ["scene"], "concept"),
            ("source", "The task is tested at dawn", None, ["scene"], "concept"),
            ("synthesis", "Threat and help coexist", "Vasilissa is frightened by Baba Yaga, but an enchanted doll helps her meet the demands. Avoid reducing this tale's figure to a universal villain type.", ["scene"], "concept"),
            ("method", "Name the collector and tale", "Ralston's Russian Fairy Tales is a nineteenth-century collection and interpretation of stories; this scene is one recorded version, not a scripture or pan-Slavic canon.", ["scene"], "source"),
            ("flavor", "An uneasy helper", "The tale leaves Vasilissa with a dangerous household and help that depends on her following her mother's instructions.", ["scene"], "source"),
        ],
        "questions": [
            ("What does the doll do for Vasilissa while Baba Yaga is away?", "Completes the wheat-clearing task", ["Hides Baba Yaga's mortar", "Turns the house into a palace"], "The cited passage says Vasilissa finds the work completed and credits her doll.", ["scene"], "concept"),
            ("What kind of evidence is this episode?", "A Russian folktale recorded and translated by Ralston", ["A law code used by every Slavic community", "A contemporary eyewitness report"], "The source is a nineteenth-century folklore collection, not an eyewitness record or universal canon.", ["scene"], "source"),
        ],
    },
    {
        "slug": "koschei-hidden-death",
        "title": "Koschei: The Hidden Death",
        "subtitle": "A vulnerable life placed outside the body",
        "refs": [
            ("death", "Ralston's recorded Koschei tale, the external death", "There stands an oak, and under the oak is a casket", "in the egg is my death."),
            ("wolf", "Marya Morevna, Ivan spares the wolf", "Suddenly there appeared a young wolf", "Prince Ivan let the young wolf go."),
        ],
        "objectives": [
            ("What does Koschei say about the location of his death?", "It is hidden in a layered sequence outside his body."),
            ("What happens when Ivan first meets the wolf?", "He spares it after the wolf asks him not to kill its cub."),
        ],
        "cards": [
            ("context", "A strength that can be found", "In one tale Ralston records, Koschei locates his death outside his body: inside an egg, inside a duck, inside a hare, inside a casket beneath an oak.", ["death"], "concept"),
            ("source", "The nested hiding place", None, ["death"], "concept"),
            ("context", "A choice on the journey", "On his search, Ivan considers killing a young wolf. Its mother asks him to spare the cub and promises a good turn; Ivan lets it live.", ["wolf"], "concept"),
            ("method", "Do not flatten variants", "Ralston compares multiple reported versions of Koschei. The external death motif appears in a tale he quotes; details vary and do not define every Slavic story.", ["death", "wolf"], "source"),
            ("synthesis", "Discovery changes the contest", "The story makes knowledge of a hidden vulnerability more important than a direct contest of strength.", ["death"], "concept"),
        ],
        "questions": [
            ("Where does Koschei say his death is hidden in this version?", "In an egg nested inside a duck, hare, and casket under an oak", ["In a ring carried by Vasilissa", "In the Water King's bridge"], "The quoted tale gives a sequence of containers outside Koschei's body.", ["death"], "concept"),
            ("What does Ivan do when the wolf asks him to spare its cub?", "He spares it, and the wolf promises help", ["He kills the cub for food", "He asks Koschei to decide"], "Ivan lets the young wolf live; later the animal helps him.", ["wolf"], "source"),
        ],
    },
    {
        "slug": "vasilissa-wise",
        "title": "Vasilissa: The Doll and the Tasks",
        "subtitle": "Maternal advice in a Baba Yaga tale",
        "refs": [
            ("doll", "Vasilissa the Fair, her mother's instructions", "Listen, Vasilissa, dear;", "when it has fed, it will tell you a cure for your troubles."),
            ("task", "Vasilissa the Fair, the doll completes the work", "The doll had cleared the wheat to the very last grain.", "the Baba Yaga examined everything"),
        ],
        "objectives": [
            ("What instructions does Vasilissa's mother leave about the doll?", "Feed it and ask its advice when misfortune comes."),
            ("How does the doll help Vasilissa meet Baba Yaga's demand?", "It completes the wheat-clearing task while she sleeps."),
        ],
        "cards": [
            ("context", "A gift with instructions", "Before she dies, Vasilissa's mother gives her a doll and tells her to feed it and ask for counsel when trouble comes.", ["doll"], "concept"),
            ("source", "The mother's instructions", None, ["doll"], "concept"),
            ("context", "The work is done", "At Baba Yaga's house, Vasilissa fears she will fail. The doll clears the wheat while she rests, allowing her to face the morning inspection.", ["task"], "concept"),
            ("method", "Stay with this collected tale", "Ralston presents this as Vasilissa the Fair, a Russian folktale. Do not turn one tale's doll into evidence of a universal Slavic household ritual.", ["doll", "task"], "source"),
            ("synthesis", "Help is relational", "The doll's help follows Vasilissa's care and her mother's instruction; the tale connects survival with attention and trust.", ["doll", "task"], "concept"),
        ],
        "questions": [
            ("What does Vasilissa's mother tell her to do with the doll?", "Feed it and ask its advice when misfortune comes", ["Hide it from every family member and never use it", "Trade it to Baba Yaga for a horse"], "The mother's instruction explicitly links feeding the doll with asking its advice.", ["doll"], "concept"),
            ("What task does the doll complete at Baba Yaga's house?", "Clearing the wheat", ["Building the Water King's bridge", "Finding Koschei's hidden egg"], "The source says Vasilissa finds the wheat cleared after the doll helps her.", ["task"], "source"),
        ],
    },
    {
        "slug": "water-king-bargain",
        "title": "The Water King: Bargains and Impossible Tasks",
        "subtitle": "An eagle's debt leads to the Water King's test",
        "refs": [
            ("bridge", "The Water King and Vasilissa the Wise, the crystal bridge task", "The Water King saw him, and said", "If you don't build it--off goes your head!"),
            ("help", "The Water King and Vasilissa the Wise, Vasilissa summons help", "Vasilissa the Wise opened her window", "The Prince immediately snatched up a broom"),
        ],
        "objectives": [
            ("What does the Water King demand as the prince's first task?", "A crystal bridge built in one night."),
            ("How does Vasilissa help with the impossible task?", "She summons workers who build the bridge while the prince sleeps."),
        ],
        "cards": [
            ("context", "A favor becomes a debt", "In Ralston's tale, an eagle first asks the king to spare it and feed it. Years later, it carries him across the sea, where a promise leads the king's son into the Water King's service.", ["bridge"], "concept"),
            ("source", "The first task", None, ["bridge"], "concept"),
            ("context", "Vasilissa answers the problem", "The prince despairs over the deadline. Vasilissa tells him to sleep, summons builders with a whistle, and the bridge is ready by morning.", ["help"], "concept"),
            ("method", "A collected folktale, not a universal myth", "Ralston records a Russian folk tale with motifs that also occur elsewhere. The specific eagle, task, and Vasilissa episode belong to this version.", ["bridge", "help"], "source"),
            ("synthesis", "Bargains have consequences", "The tale connects a saved animal, a favor repaid, and an impossible task imposed on the king's son.", ["bridge", "help"], "concept"),
        ],
        "questions": [
            ("What is the Water King's first task for the prince?", "Build a crystal bridge in one night", ["Find Koschei's egg in the underworld", "Keep watch for the Firebird until dawn"], "The Water King sets a one-night deadline for the crystal bridge.", ["bridge"], "concept"),
            ("How does Vasilissa help the prince complete the task?", "She summons builders while he rests", ["She asks the eagle to carry the bridge", "She turns the Water King into a wolf"], "The source says Vasilissa calls workers who build the bridge overnight.", ["help"], "source"),
        ],
    },
    {
        "slug": "firebird-quest",
        "title": "The Firebird: A Chapbook Quest",
        "subtitle": "A collector's summary and its provenance caveat",
        "refs": [
            ("provenance", "Ralston's source note on the Zhar-Ptitsa tale", "it is a \"Chap-book\" story, and therefore of doubtful origin.", "King Vuislaf has an apple-tree"),
            ("story", "Ralston's summary of King Vuislaf and the Zhar-Ptitsa", "King Vuislaf has an apple-tree which bears golden fruits.", "secures one of its tail-feathers."),
        ],
        "objectives": [
            ("How does Ralston characterize the origin of this Firebird tale?", "As a chapbook story whose origin is doubtful."),
            ("What does Prince Ivan obtain when he fails to catch the bird?", "One feather from its tail."),
        ],
        "cards": [
            ("context", "A bird that starts a quest", "Ralston summarizes a tale in which a Zhar-Ptitsa steals golden fruit from King Vuislaf's tree. Ivan fails to catch the bird but secures a feather.", ["story"], "concept"),
            ("source", "The collector's caveat", None, ["provenance"], "source"),
            ("source", "The tale as summarized", None, ["story"], "concept"),
            ("method", "This is a summary, not the full folktale", "Ralston explicitly calls this a chapbook story and says its origin is doubtful. Attribute the outline to his discussion rather than presenting it as an ancient pan-Slavic myth.", ["provenance", "story"], "source"),
            ("synthesis", "Do not collapse the bird variants", "Ralston compares the Zhar-Ptitsa with the German Golden Bird and notes other variants. Similar motifs do not make every version the same story.", ["provenance", "story"], "concept"),
        ],
        "questions": [
            ("How does Ralston describe the source of this Zhar-Ptitsa tale?", "A chapbook story of doubtful origin", ["An eyewitness record of an ancient rite", "A fixed scripture used across all Slavic communities"], "The passage is Ralston's folkloristic summary and explicitly questions the chapbook's origin.", ["provenance"], "source"),
            ("What does Ivan secure when he cannot catch the Firebird?", "One feather from its tail", ["The bird's golden cage", "The entire apple tree"], "Ralston's summary says the youngest son gets a tail feather, then begins a quest.", ["story"], "concept"),
        ],
    },
]


def make_reference(record, spec):
    ref_id, locator, start_anchor, end_anchor = spec
    work = f"{record['title']} ({locator})"
    local_path = f"content/corpus/slavic/{record['localPath']}"
    text = source_segments(ROOT / local_path)[0]["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {locator}")
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": work,
        "author": "W. R. S. Ralston",
        "translator": "not applicable; Ralston writes in English",
        "locator": f"{locator}; local text normalized characters {start}-{end}",
        "localPath": local_path,
        "excerpt": text[start:end].strip(),
        "evidenceType": "quotation",
        "note": "Verbatim Ralston text; distinguish his collection, translation, or folkloristic summary from the tale traditions he discusses.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/slavic/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == RALSTON)
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/slavic").rglob("*.json")
    }
    changes = {}
    for spec in PACK:
        path = paths[spec["slug"]]
        lesson = json.loads(path.read_text(encoding="utf-8"))
        lesson["version"] = 2
        lesson["title"] = spec["title"]
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
                body = "Source quotation (Ralston's English text; whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the named folktale passage.",
                    "suggestedQuestions": ["Which words support this answer?", "Is this Ralston's translation, summary, or editorial comparison?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Source-specific editorial rewrite; independent claims, variants, and pedagogy still require review.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/slavic").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Slavic starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} source-specific lessons; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        for path, lesson in changes.items():
            path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied once; future generated writes are disabled.")


if __name__ == "__main__":
    main()

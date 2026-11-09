"""One-time, digest-guarded source revision for the K'iche' Popol Vuh starter set."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
POPOL_VUH = "content/corpus/maya/primary/popol-vuh-56550.txt"

PACK = [
    {
        "slug": "creation-and-first-people",
        "title": "Wooden People and the Flood",
        "subtitle": "A creation episode in Spence's K'iche' summary",
        "refs": [
            ("wood", "Spence summary · First Book", "To supply the deficiency the divine beings resolved", "lack of reverence, resolved to destroy them."),
            ("flood", "Spence summary · First Book", "Then by the will of Hurakan, the Heart of Heaven", "the little monkeys who live in the woods."),
        ],
        "cards": [
            ("context", "The first people do not satisfy the gods", "In Spence's summary of the Popol Vuh, the divine beings make wooden people, who fail to show reverence and are rejected.", ["wood"], "concept"),
            ("source", "A flood destroys the wooden people", None, ["flood"], "concept"),
            ("context", "The world responds to mistreatment", "The summary describes animals and household objects turning against the wooden people. Their descendants, it says, are the monkeys of the woods.", ["flood"], "concept"),
            ("method", "Spence is summarizing translations", "Lewis Spence's 1908 essay says it draws on Brasseur de Bourbourg's French translation and Ximénez's Spanish translation. This is Spence's English summary, not a direct translation of the K'iche' text.", ["wood", "flood"], "source"),
            ("synthesis", "Keep community and source visible", "This is a K'iche' narrative as transmitted through a colonial-era manuscript and Spence's early twentieth-century comparison. Do not present it as all Maya peoples' single creation account.", ["wood", "flood"], "source"),
        ],
        "questions": [
            ("What material are the unsuccessful people made from in Spence's summary?", "Wood", ["Gold and silver", "Yellow and white maize"], "The summary says the divine beings made mannikins carved out of wood.", ["wood"], "concept"),
            ("What happens to the wooden people?", "A flood destroys them, and animals and household objects turn against them", ["They become the rulers of Xibalba", "They leave for Tlapallan on a raft"], "Spence describes a flood and the animals and utensils abusing the wooden people.", ["flood"], "source"),
        ],
    },
    {
        "slug": "the-hero-twins",
        "title": "Vukub-Cakix and the Hero Twins",
        "subtitle": "Pride, a fruit tree, and a blowpipe",
        "refs": [
            ("pride", "Spence summary · Vukub-Cakix", "In his own opinion Vukub-Cakix's existence", "they resolved upon his overthrow."),
            ("attack", "Spence summary · Vukub-Cakix", "the hero-gods, who lay concealed within the foliage", "a severe wound in the jaw."),
        ],
        "cards": [
            ("context", "A being claims the light", "After the wooden people are destroyed, Spence's summary introduces Vukub-Cakix, whose brilliant ornaments make him boast that the Sun and Moon are unnecessary.", ["pride"], "concept"),
            ("source", "A fruit-tree encounter", None, ["attack"], "concept"),
            ("context", "The twins challenge the boast", "Hun-Ahpu and Xbalanque hide in a tree and strike Vukub-Cakix with a blowpipe dart. The shot knocks him down and wounds his jaw.", ["attack"], "concept"),
            ("method", "An editor's summary, not the source manuscript", "Spence summarizes a K'iche' narrative through earlier Spanish and French editions. His language, spelling, and framing are not a new translation from the K'iche' text.", ["pride", "attack"], "source"),
            ("synthesis", "The conflict begins with a claim", "The episode links Vukub-Cakix's boast about the Sun and Moon with the twins' first attack.", ["pride", "attack"], "concept"),
        ],
        "questions": [
            ("What does Vukub-Cakix claim about the Sun and Moon?", "His existence makes them unnecessary", ["He created them from a maize-stone", "He hides them in a mountain"], "Spence says Vukub-Cakix believes his brilliance makes the Sun and Moon unnecessary.", ["pride"], "concept"),
            ("How do the twins first strike Vukub-Cakix in this summary?", "They hit him with a blowpipe dart while he is in a tree", ["They defeat him in the ballcourt", "They trap him in the House of Cold"], "The account says the twins shoot him with a blowpipe while concealed in the foliage.", ["attack"], "source"),
        ],
    },
    {
        "slug": "xibalba-and-trials",
        "title": "The Hero Twins Receive a Call from Xibalba",
        "subtitle": "A ballgame leads to the underworld",
        "refs": [
            ("call", "Spence summary · Second Book", "It was not long, however, until Hun-Came and Vukub-Came", "they passed the river of blood and the river Papuhya."),
        ],
        "cards": [
            ("context", "The twins play ball", "In Spence's summary, the twins play in their fathers' ballcourt. The rulers of Xibalba hear them and send owls as messengers to summon them.", ["call"], "concept"),
            ("source", "The summons is carried by owls", None, ["call"], "concept"),
            ("context", "A message travels by animal helpers", "The grandmother sends a louse with the message; a toad, serpent, and bird help carry it. The twins return home before leaving for Xibalba.", ["call"], "concept"),
            ("method", "Keep the K'iche' frame specific", "The story belongs to the Popol Vuh material about the K'iche' Hero Twins as Spence summarizes it. It is not a generic Maya account or proof of one universal ballgame ritual.", ["call"], "source"),
            ("synthesis", "The ballgame has narrative stakes", "The twins' game prompts the summons, connecting play, family memory, and a journey to Xibalba.", ["call"], "concept"),
        ],
        "questions": [
            ("Why do the rulers of Xibalba summon the twins?", "They hear the twins playing ball and challenge them", ["The twins steal the Sampo", "Vukub-Cakix asks them to create the Sun"], "Spence says Hun-Came and Vukub-Came hear the ballgame and decide to lure the twins to the underworld.", ["call"], "concept"),
            ("Which creatures carry the grandmother's message in the summary?", "A louse, a toad, a serpent, and the bird Voc", ["A dog, a rabbit, and two owls", "An eagle, a tortoise, and a jaguar"], "The message is passed through the louse, toad, serpent, and bird Voc.", ["call"], "source"),
        ],
    },
    {
        "slug": "the-ballgame",
        "title": "Xibalba's Houses of Ordeal",
        "subtitle": "Cold, fire, tigers, and bats",
        "refs": [
            ("ordeals", "Spence summary · Second Book", "They even passed scatheless through the first ordeal", "who suddenly appeared from above."),
        ],
        "cards": [
            ("context", "The first test is a trap", "Spence describes the twins avoiding the red-hot seat and passing the House of Gloom before the rulers set further ordeals.", ["ordeals"], "concept"),
            ("source", "A series of dangerous houses", None, ["ordeals"], "concept"),
            ("context", "The House of Bats is different", "The twins survive the Houses of Cold, Tigers, and Fire, but in the House of Bats Hun-Ahpu is beheaded by Camazotz.", ["ordeals"], "concept"),
            ("method", "The summary admits uncertainty", "Spence says the account does not make clear how Hun-Ahpu recovers from the wound, because the text is unintelligible at that point. Do not fill that gap with invented certainty.", ["ordeals"], "source"),
            ("synthesis", "Survival does not erase the textual gap", "The episode names several ordeals and records a severe injury, while Spence explicitly marks the recovery sequence as unclear.", ["ordeals"], "source"),
        ],
        "questions": [
            ("In which House is Hun-Ahpu beheaded in Spence's summary?", "The House of Bats", ["The House of Cold", "The House of Fire"], "The passage says Camazotz appears in the House of Bats and cuts off Hun-Ahpu's head.", ["ordeals"], "concept"),
            ("What does Spence say about how Hun-Ahpu recovers?", "The text is unclear at that point", ["The twins use the Sampo to restore him", "The rulers of Xibalba return his head"], "Spence explicitly says the text is unintelligible about how the wound is cured.", ["ordeals"], "source"),
        ],
    },
    {
        "slug": "death-return-and-renewal",
        "title": "The Twins' Death and Return",
        "subtitle": "A staged death outwits Xibalba's rulers",
        "refs": [
            ("return", "Spence summary · Second Book", "they stretched themselves upon a funeral pile and died together", "where they sank, and were transformed into young men."),
            ("fate", "Spence summary · Second Book", "The monarchs of Xibalba, anxious to experience", "the brothers refrained from resuscitating their arch-enemies."),
        ],
        "cards": [
            ("context", "The twins plan a deception", "After surviving the ordeals, Hun-Ahpu and Xbalanque tell two sorcerers what to do with their bones, then die on a funeral pyre.", ["return"], "concept"),
            ("source", "Bones return to life", None, ["return"], "concept"),
            ("context", "The rulers ask for the same power", "The princes of Xibalba ask the twins to kill and revive them. The twins kill them but refuse to bring them back.", ["fate"], "concept"),
            ("method", "Do not confuse the different returns", "Spence's summary says the twins return to life, then later says their father and uncle rise to heaven and become the Sun and Moon. Those are distinct events in his account.", ["return", "fate"], "source"),
            ("synthesis", "Victory ends the rulers' authority", "After the princes die, the twins forbid them from playing ball and assign them menial tasks in Spence's version.", ["fate"], "concept"),
        ],
        "questions": [
            ("What happens to the twins' bones after their deaths?", "They are beaten to powder, thrown in the river, and the twins return in new forms", ["They are placed in the Sampo", "They are turned into the Sun and Moon immediately"], "Spence says the bones are powdered and thrown into the river, after which the twins reappear in other forms.", ["return"], "concept"),
            ("What do the twins do when Xibalba's rulers ask to be revived?", "They kill the rulers but do not bring them back", ["They let the rulers win a ballgame", "They send the rulers to the House of Bats"], "The summary says the twins refuse to resuscitate their arch-enemies.", ["fate"], "source"),
        ],
    },
]


def make_reference(record, spec):
    ref_id, segment_locator, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / "content/corpus/maya" / record["localPath"])
         if item["locator"] == segment_locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named Popol Vuh summary section not found: {segment_locator}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {segment_locator}")
    end += len(end_anchor)
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": "Lewis Spence",
        "translator": "not applicable; Spence authored this English summary",
        "locator": f"{segment_locator}; {segment_locator}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/maya/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim prose from Spence's 1908 English summary, which he says draws on Brasseur de Bourbourg's French and Ximénez's Spanish translations. This is not a direct translation of the K'iche' text.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/maya/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == "pg-56550")
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/maya").rglob("*.json")
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
                body = "Quotation from Spence's English summary (whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the named section of Spence's Popol Vuh summary.",
                    "suggestedQuestions": ["Which words support this answer?", "Is this Spence's summary or a direct translation?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "K'iche' Popol Vuh episodes as summarized by Lewis Spence; independent K'iche' community, source-text, translation, and pedagogical review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/maya").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Maya starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} K'iche' Popol Vuh lessons; no files written.")
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

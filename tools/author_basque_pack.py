"""One-time, digest-guarded revision for Basque stories collected by Webster."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "content/corpus/basque/primary/basque-legends-webster-34902.txt"

PACK = [
    {
        "slug": "mari-and-sacred-mountains",
        "title": "The Tartaro and the Talking Ring",
        "subtitle": "A short tale collected at Ahetze",
        "refs": [
            ("ring", "THE TARTARO.", "Once upon a time there was the son of a king", "there the Tartaro drowned himself."),
        ],
        "cards": [
            ("context", "A monster seeks a wife", "In one tale in Webster's Basque collection, a king's son becomes a Tartaro and can return to human form only by marrying.", ["ring"], "concept"),
            ("source", "A ring will not stay silent", None, ["ring"], "concept"),
            ("context", "The girl escapes pursuit", "The frightened girl throws away the ring, but it keeps calling to the Tartaro. She finally cuts it off with her finger and throws it into a pond.", ["ring"], "concept"),
            ("method", "A named local tale", "Webster says this version came from Estefanella Hirigaray of Ahetze in Labourd. It is one collected Basque story, not a universal account of every Basque community.", ["ring"], "source"),
            ("synthesis", "Keep the teller attached", "The unusual speaking ring and the ending belong to this reported Ahetze version. Other Tartaro stories in Webster's book have different plots.", ["ring"], "source"),
        ],
        "questions": [
            ("What must the Tartaro do to return to human form in this story?", "Marry", ["Win a ballgame", "Find a seven-headed serpent"], "The tale says the monster can become a man again only by marrying.", ["ring"], "concept"),
            ("How does the girl finally stop the ring's pursuit?", "She cuts off her finger and throws the ring into a pond", ["She hides it in a cave", "She asks Basa-Jaun to break it"], "The story ends with the girl cutting off her finger and throwing the ring into a pond.", ["ring"], "source"),
        ],
    },
    {
        "slug": "basa-jaun",
        "title": "Acheria the Fox",
        "subtitle": "A fox recruits a wolf to distract a shepherd",
        "refs": [
            ("fox", "ACHERIA, THE FOX.", "One day a fox was hungry.", "he eats all the contents of the jug."),
        ],
        "cards": [
            ("context", "A plan for milk and cheese", "Acheria, the fox, wants a meal from the shepherd. He asks a wolf to howl and draw the shepherd away while he steals the curdled milk.", ["fox"], "concept"),
            ("source", "The fox makes the division", None, ["fox"], "concept"),
            ("context", "A trick on a partner", "After eating the cream, Acheria fills the vessel with dirt and offers the wolf a choice between the top and bottom of the mixture.", ["fox"], "concept"),
            ("method", "A collected animal tale", "This is one named story in Webster's 1879 collection, collected chiefly in Labourd. It supports claims about this tale and its English telling, not a universal Basque rule about foxes.", ["fox"], "source"),
            ("synthesis", "The fox controls the bargain", "The story's humor depends on Acheria setting up the wolf's choice after secretly changing the contents.", ["fox"], "concept"),
        ],
        "questions": [
            ("What does Acheria ask the wolf to do?", "Howl to draw the shepherd away", ["Guard the cheese", "Carry the milk to the Tartaro"], "The fox asks the wolf to howl so the shepherd will leave the cheese-making behind.", ["fox"], "concept"),
            ("What does Acheria put into the vessel after eating the cream?", "Dirt", ["Water", "A ring"], "The passage says he fills it with dirt and puts the cream back on top.", ["fox"], "source"),
        ],
    },
    {
        "slug": "laminak-and-waters",
        "title": "The Grateful Tartaro and the Heren-Suge",
        "subtitle": "A ball-game bargain frees a prisoner",
        "refs": [
            ("ball", "THE GRATEFUL TARTARO AND THE HEREN-SUGE.", "The next day the two sons of the king were playing at ball", "When he was letting him go, he said to him:"),
        ],
        "cards": [
            ("context", "A ball enters the stable", "A king keeps a Tartaro in a stable. When a boy's ball rolls inside, the prisoner offers to return it if the boy will free him.", ["ball"], "concept"),
            ("source", "An exchange with consequences", None, ["ball"], "concept"),
            ("context", "The boy takes the key", "The Tartaro tells the boy how to take the key from his mother. He escapes and promises to help later.", ["ball"], "concept"),
            ("method", "A Basque collection with cross-tradition parallels", "Webster places this story among Basque Tartaro and serpent legends, while noting that the Heren-Suge cycle resembles wider European dragon-slayer motifs. Keep the local telling and the comparison distinct.", ["ball"], "source"),
            ("synthesis", "A small bargain launches the plot", "The returned ball is not a harmless ending: the boy's promise frees the Tartaro and creates a future debt.", ["ball"], "concept"),
        ],
        "questions": [
            ("What does the Tartaro ask for in exchange for the ball?", "The boy must deliver him from the stable", ["The boy must bring three cubs", "The boy must marry the princess"], "The prisoner says he will return the ball if the boy delivers him.", ["ball"], "concept"),
            ("How does the boy get the stable key?", "The Tartaro tells him a trick involving his mother's ear", ["He breaks the stable door", "The king gives it to him"], "The excerpt begins the Tartaro's instruction about where the key is hidden.", ["ball"], "source"),
        ],
    },
    {
        "slug": "tartaro-and-giants",
        "title": "Basa-Jauna and the Three Brothers",
        "subtitle": "A wild-man household in a Basque story",
        "refs": [
            ("wildman", "BASA-JAUNA, THE WILD MAN.", "The three brothers set out together.", "the Basa-Jaun, and if he catches you he will eat you; that's certain."),
        ],
        "cards": [
            ("context", "A trail of smoke", "Three brothers travel through a forest at night. The youngest sees a thin column of smoke in the distance and leads them toward a castle.", ["wildman"], "concept"),
            ("source", "A warning at the castle", None, ["wildman"], "concept"),
            ("context", "The Basa-Andre opens the door", "The brothers ask for shelter. The Basa-Andre warns them that her husband, the Basa-Jaun, may eat them, but lets them in.", ["wildman"], "concept"),
            ("method", "Name the collection's variant", "Basa-Jauna and Basa-Andre appear in Webster's collection of Labourd stories. Preserve these names and this written version rather than treating them as the same figure in every local account.", ["wildman"], "source"),
            ("synthesis", "Hospitality exists beside danger", "The story begins with shelter offered in a household that the visitors have reason to fear.", ["wildman"], "concept"),
        ],
        "questions": [
            ("What does the youngest brother see from the tree?", "A thin column of smoke far away", ["A moon hidden in a mountain", "A fox carrying a milk jug"], "The youngest brother says he sees a thin column of smoke and leads them toward it.", ["wildman"], "concept"),
            ("Who warns the brothers about the Basa-Jaun?", "The Basa-Andre", ["The Tartaro", "Acheria the fox"], "The Basa-Andre tells the brothers her husband may eat them.", ["wildman"], "source"),
        ],
    },
    {
        "slug": "witches-and-village-tales",
        "title": "The Servant at the Fairy's",
        "subtitle": "A dog corrects a servant's instructions",
        "refs": [
            ("fairy", "THE SERVANT AT THE FAIRY'S.", "She gave her her morning's work to do", "a sack of charcoal or of a bag of gold; of a beautiful star on your forehead, or of a donkey's tail hanging from it."),
        ],
        "cards": [
            ("context", "A new servant gets impossible instructions", "A young woman seeks work and is hired by a fairy. The mistress gives her a list of destructive tasks for the kitchen and children.", ["fairy"], "concept"),
            ("source", "The dog knows the real task", None, ["fairy"], "concept"),
            ("context", "Kindness changes the outcome", "After the servant feeds the little dog, it tells her the tasks she should actually do and what choices the fairy will offer.", ["fairy"], "concept"),
            ("method", "Do not overstate the supernatural label", "The title calls the being a fairy, within Webster's collected Basque tales. It is not evidence that all Basque communities used one uniform category called lamiñak.", ["fairy"], "source"),
            ("synthesis", "A familiar tale in a local collection", "This story appears in Webster's Basque collection, but the book also separates tales adapted directly from French. Its collection label alone does not prove an ancient or uniquely Basque origin.", ["fairy"], "source"),
        ],
        "questions": [
            ("What does the little dog tell the servant?", "The real tasks and the choices the fairy will offer", ["How to defeat Huitzilopochtli", "Where the Tartaro hides his ring"], "The dog tells her what the mistress actually instructed and how to answer the reward choices.", ["fairy"], "concept"),
            ("What should we avoid assuming from the title's word 'fairy'?", "That it names a single uniform Basque being in every community", ["That the tale is an English scientific report", "That the story comes from the Popol Vuh"], "Webster groups varied collected tales; a title label should not be generalized into a uniform belief system.", ["fairy"], "source"),
        ],
    },
]


def make_reference(record, spec):
    ref_id, locator, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / "content/corpus/basque" / record["localPath"])
         if item["locator"] == locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named Basque tale not found: {locator}")
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
        "author": "Basque storytellers; collected and translated by Wentworth Webster",
        "translator": "Wentworth Webster, with assistance from Julien Vinson and other local contributors",
        "locator": f"{locator}; {locator}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/basque/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim English text from Webster's second edition, collected chiefly in Labourd. The collection distinguishes local tales from French-derived contes des fées and compares some motifs with wider European stories.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/basque/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == "pg-34902")
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/basque").rglob("*.json")
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
                body = "Source quotation (Webster's English collection; whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the named tale in Webster's Basque collection.",
                    "suggestedQuestions": ["Which words support this answer?", "Does Webster identify the teller or compare this story with another tradition?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Collected Basque tales in Webster's Labourd-focused volume; independent source-history, community, and pedagogy review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/basque").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Basque starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} passage-specific Basque lessons; no files written.")
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

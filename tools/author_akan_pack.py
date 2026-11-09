"""One-time, digest-guarded revision of Gold Coast Anansi folktale lessons."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
DAYRELL = "content/corpus/akan/primary/west-african-folk-tales-66923.txt"

PACK = [
    {
        "slug": "anansi-the-spider",
        "title": "How Anansi Earned the Name Spider Tales",
        "subtitle": "A Gold Coast collection's own story about its genre",
        "refs": [
            ("name", "Story I · HOW WE GOT THE NAME ‘SPIDER TALES’", "In the olden days all the stories which men told", "gave him permission for the future to call all the old tales Anansi tales."),
        ],
        "cards": [
            ("context", "A request to Nyankupon", "In Barker and Sinclair's collection, Anansi asks Nyankupon to let future stories be called Anansi tales instead of Nyankupon stories.", ["name"], "concept"),
            ("source", "Three tasks", None, ["name"], "concept"),
            ("context", "Trickery fulfills the condition", "Nyankupon requires Anansi to bring bees, a boa-constrictor, and a tiger. Anansi tricks each one into going with him.", ["name"], "concept"),
            ("method", "A written collection, not a uniform canon", "The 1917 book was collected and arranged by Barker and Sinclair from Gold Coast storytellers. Its preface notes that versions vary and are retold; it does not name a specific community for every tale.", ["name"], "source"),
            ("synthesis", "The collection comments on itself", "This tale explains the collection's label 'Spider Tales' through an Anansi story. It is a story about storytelling, not proof that every West African tradition tells it the same way.", ["name"], "source"),
        ],
        "questions": [
            ("What does Nyankupon require Anansi to bring?", "Bees, a boa-constrictor, and a tiger", ["A tortoise, a fish, and a yam", "A drum, a pot, and a palm-tree"], "The tale lists three tasks: a jar of bees, a boa-constrictor, and a tiger.", ["name"], "concept"),
            ("What does Nyankupon allow after Anansi completes the tasks?", "The old tales may be called Anansi tales", ["Anansi becomes ruler of the Gold Coast", "All stories are translated into English"], "The ending says Nyankupon gives permission to call the old tales Anansi tales.", ["name"], "source"),
        ],
    },
    {
        "slug": "wisdom-becomes-human",
        "title": "Anansi and the Pot of Wisdom",
        "subtitle": "A tale explicitly set in Fanti-land",
        "refs": [
            ("pot", "Story II · HOW WISDOM BECAME THE PROPERTY OF THE HUMAN RACE", "There once lived, in Fanti-land", "the wisdom contained in it escaped and spread throughout the world."),
        ],
        "cards": [
            ("context", "Wisdom is gathered into a pot", "The story begins in Fanti-land. Father Anansi gathers wisdom into a pot and tries to hide it high in a tree.", ["pot"], "concept"),
            ("source", "A child's practical advice", None, ["pot"], "concept"),
            ("context", "The pot falls", "Anansi's son Kweku Tsin points out that the pot would be easier to carry on his back. Anansi admits that the boy knows something he did not.", ["pot"], "concept"),
            ("method", "Keep the story's place label", "The printed tale explicitly names Fanti-land. Barker and Sinclair's collection discusses Gold Coast peoples broadly, but not every tale has the same specific community attribution.", ["pot"], "source"),
            ("synthesis", "Knowledge cannot be monopolized", "In the story's ending, the pot breaks and its contents spread through the world, explaining why wisdom is no longer held by Anansi alone.", ["pot"], "concept"),
        ],
        "questions": [
            ("Where does the story say Father Anansi lived?", "Fanti-land", ["Jamaica", "Xibalba"], "The opening sentence places Anansi in Fanti-land.", ["pot"], "concept"),
            ("What advice does Kweku Tsin give his father?", "Hang the pot on his back to climb more easily", ["Throw the pot into the sea", "Give the pot to Nyankupon"], "Kweku Tsin says the pot would not swing in Anansi's way if it were on his back.", ["pot"], "source"),
        ],
    },
    {
        "slug": "diaspora-and-transformation",
        "title": "Anansi and Nothing: A Gold Coast Story",
        "subtitle": "Clothing, status, and a trickster's reversal",
        "refs": [
            ("nothing", "Story III · ANANSI AND NOTHING", "Near Anansi", "No one was waiting for Anansi."),
        ],
        "cards": [
            ("context", "Anansi borrows a fine cloth", "In Barker and Sinclair's story, Anansi and Nothing travel to seek wives. Anansi persuades Nothing to exchange a fine velvet cloth for his ragged cotton one.", ["nothing"], "concept"),
            ("source", "First impressions mislead", None, ["nothing"], "concept"),
            ("context", "The road home reveals the difference", "Anansi's fine clothes help him attract wives, but Nothing's home and servants reveal the status Anansi had misread.", ["nothing"], "concept"),
            ("method", "Do not make a Jamaican tale stand in for this one", "This passage is from the Gold Coast collection by Barker and Sinclair. The separate Jamaican Anansi collection is a diaspora source with its own field-recorded tellers and wording.", ["nothing"], "source"),
            ("synthesis", "A trick can reverse on its maker", "The episode contrasts the appearance of wealth with the actual household situation; Anansi's trick does not secure the better outcome.", ["nothing"], "concept"),
        ],
        "questions": [
            ("What does Anansi persuade Nothing to exchange?", "Their clothes", ["Their houses", "Their fishing nets"], "Anansi asks Nothing to exchange his velvet cloth for Anansi's ragged cotton one.", ["nothing"], "concept"),
            ("What does Anansi discover at the crossroads?", "Nothing's road is prepared and his servants await him", ["Nothing has moved into Anansi's hut", "The village has named Anansi its king"], "The tale contrasts the prepared road and servants at Nothing's home with Anansi's unprepared house.", ["nothing"], "source"),
        ],
    },
    {
        "slug": "tiger-and-dangerous-rivals",
        "title": "Thunder and Anansi: The Gifted Stick",
        "subtitle": "Repeated trouble follows repeated choices",
        "refs": [
            ("stick", "Story IV · THUNDER AND ANANSI", "This time, however, he presented Anansi with a fine stick", "wishing he had acted more wisely from the beginning."),
        ],
        "cards": [
            ("context", "A second gift", "In this Gold Coast story, Anansi returns to Thunder's cottage. Thunder gives him a stick and warns him of its magic.", ["stick"], "concept"),
            ("source", "An instruction ignored", None, ["stick"], "concept"),
            ("context", "The stick turns on Anansi", "Anansi tries to command the stick to do for him what it did for Thunder. It beats him until he jumps into the water and swims ashore.", ["stick"], "concept"),
            ("method", "A folktale's moral is not ethnography", "Barker and Sinclair retell this as one story in a Gold Coast collection. Its magical stick and comic punishment are narrative details, not evidence of a universal religious practice.", ["stick"], "source"),
            ("synthesis", "Repeated choices matter", "The episode frames Anansi's misfortune as a consequence of how he uses the gifts, not as a general account of Thunder worship.", ["stick"], "source"),
        ],
        "questions": [
            ("What does Thunder give Anansi on his second visit?", "A fine stick", ["A jar of live bees", "A pot of wisdom"], "The passage says Thunder presents Anansi with a fine stick.", ["stick"], "concept"),
            ("What happens when Anansi tells the stick to serve him?", "It beats him until he escapes into the water", ["It builds him a palace", "It turns into the Sampo"], "Anansi asks the stick to do for him what it did for its former master, and it beats him.", ["stick"], "source"),
        ],
    },
    {
        "slug": "stories-as-social-power",
        "title": "Anansi the Blind Fisherman",
        "subtitle": "Kind helpers meet an ungrateful response",
        "refs": [
            ("fisherman", "Story XI · ANANSI THE BLIND FISHERMAN", "When they told him where to spread his net", "was drowned."),
        ],
        "cards": [
            ("context", "Two helpers assist an old fisherman", "In Barker and Sinclair's tale, two men guide the blind Anansi into a canoe, help him fish, and lead him back to shore.", ["fisherman"], "concept"),
            ("source", "The final trip", None, ["fisherman"], "concept"),
            ("context", "Anansi refuses their help", "The men say the canoe has reached the beach. Anansi insists he knows where he is, jumps out, and finds himself in deep water.", ["fisherman"], "concept"),
            ("method", "A specific Gold Coast collection", "This tale is one of Barker and Sinclair's 1917 Gold Coast folk-story collection. The book's introduction explains that versions were collected and retold; it does not identify this story's exact community.", ["fisherman"], "source"),
            ("synthesis", "The story punishes ingratitude", "The tale links Anansi's insults to his helpers' decision to leave him; it is a literary moral, not a general statement about Akan or Gold Coast people.", ["fisherman"], "source"),
        ],
        "questions": [
            ("How do the two men help Anansi before the final trip?", "They guide him into the canoe and help him fish", ["They hide a pot in a tree", "They teach him to command a magic stick"], "The story says they lead him to the beach and help him with the net and canoe.", ["fisherman"], "concept"),
            ("Why does Anansi jump into deep water?", "He insists he knows they have reached shore", ["He tries to catch the Sampo", "He is ordered by Thunder"], "The men tell him they are at the beach; Anansi says he knows and jumps out.", ["fisherman"], "source"),
        ],
    },
]


def make_reference(record, spec):
    ref_id, locator, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / "content/corpus/akan" / record["localPath"])
         if item["locator"] == locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named Gold Coast tale not found: {locator}")
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
        "author": "W. H. Barker and Cecilia Sinclair",
        "translator": "not applicable; collected, arranged, and retold in English",
        "locator": f"{locator}; {locator}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/akan/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim text from Barker and Sinclair's 1917 English collection of Gold Coast stories. Attribute any specific community only where the collection does so.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/akan/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == "pg-66923")
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/akan").rglob("*.json")
    }
    changes = {}
    for spec in PACK:
        path = paths[spec["slug"]]
        lesson = json.loads(path.read_text(encoding="utf-8"))
        current_version = lesson.get("version", 1)
        lesson["version"] = 3 if current_version == 2 else 2
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
                body = "Quotation from Barker and Sinclair's English collection (whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the named Gold Coast story in the printed collection.",
                    "suggestedQuestions": ["Which words support this answer?", "What does the collection say about the teller or place?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Passage-specific stories from Barker and Sinclair's Gold Coast collection; community-specific and living-tradition review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    parser.add_argument("--revise-v2", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/akan").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    versions = {json.loads(path.read_text(encoding="utf-8")).get("version", 1) for path in paths}
    if args.apply and versions != {1}:
        parser.error("--apply only accepts the exact version-1 Akan starter lessons.")
    if args.revise_v2 and versions != {2}:
        parser.error("--revise-v2 only accepts the exact version-2 Akan starter lessons.")
    if versions - {1, 2}:
        parser.error("Refusing to write beyond the reviewed one-time migrations for this pack.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} Gold Coast folktale lessons; no files written.")
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

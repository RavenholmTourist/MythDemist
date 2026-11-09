"""One-time, digest-guarded source revision for the Roman Ovid starter lessons."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
BOOKS_1_7 = "content/corpus/roman/primary/ovid-metamorphoses-books-1-7-21765.txt"
BOOKS_8_15 = "content/corpus/roman/primary/ovid-metamorphoses-books-8-15-26073.txt"

PACK = [
    {
        "slug": "ovid-change",
        "title": "Ovid: Change as Story",
        "subtitle": "A Roman poem opens with transformation",
        "refs": [
            ("proem", BOOKS_1_7, "Book I · Proem [I.1-4]", "My design leads me to speak of forms changed into new bodies.", "to my own times.[3]"),
            ("daphne", BOOKS_1_7, "Book I · Fable XII [I.452-567]", "Her strength being {now} spent, she grows pale", "her elegance alone[84] remains in her."),
        ],
        "cards": [
            ("context", "The poem's opening promise", "Ovid's proem announces a poem about forms changed into new bodies, extending from the world's beginning to his own time.", ["proem"], "concept"),
            ("source", "The transformation theme", None, ["proem"], "concept"),
            ("context", "Daphne becomes a laurel", "In Book I, Daphne flees Apollo and calls for help. Her body changes into a tree; Apollo addresses the laurel as the tree he will wear.", ["daphne"], "concept"),
            ("method", "Roman literary reception", "This is Ovid's Roman epic in Henry T. Riley's nineteenth-century English translation, not neutral evidence for every Greek version or Roman cult practice.", ["proem", "daphne"], "source"),
            ("synthesis", "Follow the change in the scene", "The proem's promise becomes a concrete episode: pursuit ends in bodily transformation, while Apollo gives the laurel a continuing role in his own story.", ["proem", "daphne"], "concept"),
        ],
        "questions": [
            ("What subject does Ovid announce in the proem?", "Forms changed into new bodies", ["The founding laws of Rome", "The lives of historical emperors"], "The translated opening says the poem will speak of forms changed into new bodies.", ["proem"], "concept"),
            ("What does Daphne become in Ovid's Book I episode?", "A laurel tree", ["A constellation", "A wolf"], "After Daphne's prayer, her hair becomes leaves, her arms branches, and her feet roots.", ["daphne"], "source"),
        ],
    },
    {
        "slug": "jupiter-reception",
        "title": "Jupiter and Lycaon: Judgment and Change",
        "subtitle": "A test of divine power in Ovid's Book I",
        "refs": [
            ("lycaon", BOOKS_1_7, "Book I · Fable VII [I.216-243]", "In the first place, Lycaon derided their pious supplications.", "he becomes a wolf"),
        ],
        "cards": [
            ("context", "A guest is tested", "In Ovid's account, Jupiter tells the gods how he visited Arcadia. Lycaon mocks the worshippers and tests the visitor, preparing a murder and serving human flesh.", ["lycaon"], "concept"),
            ("source", "Lycaon's punishment", None, ["lycaon"], "concept"),
            ("synthesis", "Judgment becomes transformation", "Jupiter responds by changing Lycaon into a wolf. The episode is a poetic account of divine punishment, not a record of a historical trial.", ["lycaon"], "concept"),
            ("method", "Keep the Roman poem in view", "This is Ovid's literary portrayal of Jupiter in a Greek-myth setting. It cannot establish one universal Roman belief or a ritual practice.", ["lycaon"], "source"),
            ("flavor", "The wolf retains traces", "The translated passage says the wolf keeps marks of its former appearance as well as its ferocity.", ["lycaon"], "concept"),
        ],
        "questions": [
            ("What does Lycaon do to test the visitor in Ovid's account?", "He prepares a murder and serves human flesh", ["He locks the visitor in a labyrinth", "He challenges the visitor to a chariot race"], "Jupiter's narrated account describes Lycaon's attempted murder and the meal made from a captive.", ["lycaon"], "concept"),
            ("What happens to Lycaon?", "He becomes a wolf", ["He becomes a laurel", "He is placed among the stars"], "The passage describes his garments becoming hair and his arms becoming legs before he becomes a wolf.", ["lycaon"], "source"),
        ],
    },
    {
        "slug": "venus-desire",
        "title": "Venus and Adonis: Warning and Loss",
        "subtitle": "A warning, a hunt, and a flower",
        "refs": [
            ("warning", BOOKS_8_15, "Book X · Fable IX [X.519-707]", "Forbear, youth, to be rash at my hazard", "the {whole} race is odious to me."),
            ("flower", BOOKS_8_15, "Book X · Fable X [X.708-739]", "But thy blood shall be changed into a flower.", "a flower sprang up from the blood"),
        ],
        "cards": [
            ("context", "Venus warns Adonis", "Venus warns Adonis against attacking dangerous wild animals, especially boars and lions. Her warning is part of Ovid's narrative of their relationship.", ["warning"], "concept"),
            ("source", "The warning names the danger", None, ["warning"], "concept"),
            ("context", "The warning is not obeyed", "In the next episode, Adonis is killed by a boar while hunting. Venus says his blood will become a flower and marks his death with mourning.", ["flower"], "concept"),
            ("method", "A literary version, not a universal rite", "The lesson follows Ovid's Book X sequence in Riley's translation. The poem describes Venus's action; it does not prove that every community told the story or marked the death in the same way.", ["warning", "flower"], "source"),
            ("synthesis", "Advice and consequence", "The two passages connect Venus's warning with the later transformation of Adonis's blood into a flower.", ["warning", "flower"], "concept"),
        ],
        "questions": [
            ("What danger does Venus tell Adonis to avoid?", "Attacking wild animals armed by nature", ["Sailing during a storm", "Looking into a reflective pool"], "Venus specifically warns him not to attack wild animals such as boars and lions.", ["warning"], "concept"),
            ("What happens to Adonis's blood in the later episode?", "Venus changes it into a flower", ["It becomes a laurel tree", "It turns into a constellation"], "Venus says his blood will become a flower, and the narrator describes one springing up.", ["flower"], "source"),
        ],
    },
    {
        "slug": "mars-war-state",
        "title": "Mars, Romulus, and Roman Foundation",
        "subtitle": "Ovid's account of Romulus becoming Quirinus",
        "refs": [
            ("request", BOOKS_8_15, "Book XIV · Fable XII. AND XIII [XIV.698-851]", "The time is {now} come, O father", "admit him to heaven."),
            ("change", BOOKS_8_15, "Book XIV · Fable XII. AND XIII [XIV.698-851]", "Gradivus knew that this was a signal", "Quirinus arrayed in his regal robe."),
        ],
        "cards": [
            ("context", "Romulus after the conflict", "After the Romans and Sabines agree to share rule, Ovid turns to Romulus's divine future. Mars, named Mavors in Riley's translation, asks Jupiter to honor his grandson.", ["request"], "concept"),
            ("source", "Mars makes the request", None, ["request"], "concept"),
            ("context", "Romulus becomes Quirinus", "Jupiter assents, and Romulus is taken from earth to heaven. Ovid describes a new appearance and names the deified founder Quirinus.", ["change"], "concept"),
            ("method", "A Roman foundation narrative", "This is Ovid's epic account of Rome's legendary founder and divine status, not independent historical evidence that the events occurred.", ["request", "change"], "source"),
            ("synthesis", "Warrior ancestry and civic identity", "The poem links Mars, Romulus, and the Roman state through an act of literary apotheosis: a mortal founder becomes a deity in Ovid's narrative.", ["request", "change"], "concept"),
        ],
        "questions": [
            ("What does Mavors ask Jupiter to do for Romulus?", "Admit him to heaven as the promised reward", ["Make him king of the sea", "Turn him into the laurel sacred to Apollo"], "Mavors asks Jupiter to remove his grandson from earth and admit him to heaven.", ["request"], "concept"),
            ("What name is associated with Romulus after his transformation?", "Quirinus", ["Nisus", "Adonis"], "The passage describes Romulus in a form like Quirinus in regal robes.", ["change"], "source"),
        ],
    },
    {
        "slug": "metamorphosis-reception",
        "title": "Ovid, Caesar, and Poetic Apotheosis",
        "subtitle": "A poem's account of Caesar becoming a star",
        "refs": [
            ("plea", BOOKS_8_15, "Book XV · Fable VIII [XV.745-879]", "Behold, on how vast a scale treason is plotted", "extinguish the flames of Vesta."),
            ("star", BOOKS_8_15, "Book XV · Fable VIII [XV.745-879]", "Hardly had he uttered these words", "and, as a star, it glitters"),
        ],
        "cards": [
            ("context", "Venus sees danger", "In Ovid's Book XV, Venus fears the plot against Julius Caesar and pleads with the gods. The passage frames Caesar as her descendant through Aeneas.", ["plea"], "concept"),
            ("source", "A plea against the conspiracy", None, ["plea"], "concept"),
            ("context", "A soul becomes a star", "After a divine speaker asks that Caesar's soul become a beam of light, Venus carries it from the Senate-house and the poem describes it among the stars.", ["star"], "concept"),
            ("method", "Read apotheosis as poetic reception", "Ovid's episode is literary and politically situated praise. It is not eyewitness evidence for Caesar's death or proof that a literal transformation occurred.", ["plea", "star"], "source"),
            ("synthesis", "An ending with an audience", "The passage joins Venus's ancestry, Caesar's deification, and Augustus's public position in a poem that also turns toward Ovid's own hoped-for poetic survival.", ["star"], "concept"),
        ],
        "questions": [
            ("What does Venus ask the gods to prevent?", "The plot against Caesar's life", ["Adonis's hunt for a boar", "Romulus's agreement with the Sabines"], "Venus describes the conspiracy and asks the gods to avert it.", ["plea"], "concept"),
            ("How does Ovid's poem describe Caesar's soul after his death?", "Venus carries it among the stars, where it shines as a star", ["It becomes a laurel tree", "It is returned to the Senate-house"], "The passage says Venus carries the soul into the heavens and it glitters as a star.", ["star"], "source"),
        ],
    },
]


def make_reference(records, spec):
    ref_id, path, segment_locator, start_anchor, end_anchor = spec
    segments = source_segments(ROOT / path)
    segment = next((item for item in segments if item["locator"] == segment_locator and item["evidenceType"] == "source-text"), None)
    if not segment:
        raise ValueError(f"Primary passage segment not found: {segment_locator}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found in {segment_locator}: {label}")
    end += len(end_anchor)
    record = next(item for item in records if item["localPath"] == path.removeprefix("content/corpus/roman/"))
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": f"Metamorphoses, {segment_locator}",
        "author": "Ovid",
        "translator": "Henry T. Riley",
        "locator": f"{segment_locator}; {segment_locator}, normalized characters {start}-{end}",
        "localPath": path,
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim translated verse from Ovid. Riley's arguments, synopses, notes, and explanations are separately indexed and are not quoted as primary verse.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/roman/manifest.json").read_text(encoding="utf-8"))
    records = manifest["records"]
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/roman").rglob("*.json")
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
                body = "Source quotation (Riley's translation; whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the cited book and fable in Ovid's translated poem.",
                    "suggestedQuestions": ["Which words support this answer?", "Is this narrative evidence or a later editorial explanation?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Passage-specific Ovid revisions. Independent review of translation, political context, claims, and pedagogy remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/roman").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Roman starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} source-specific lessons; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        staged = []
        for path, lesson in changes.items():
            temporary = path.with_suffix(path.suffix + ".tmp")
            temporary.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            staged.append((temporary, path))
        # Stage the whole batch before replacing any authored lesson.
        for temporary, path in staged:
            temporary.replace(path)
        print("Applied once; future generated writes are disabled.")


if __name__ == "__main__":
    main()

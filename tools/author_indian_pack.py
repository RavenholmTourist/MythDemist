"""One-time, digest-guarded source revision for the Indian epic starter lessons."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
MAHABHARATA = "content/corpus/indian/primary/mahabharata-dutt-19630.txt"
RAMAYANA = "content/corpus/indian/primary/ramayana-vol1-dutt-57265.txt"

PACK = [
    {
        "slug": "dharma-duty",
        "title": "Krishna's Counsel: Peace Before War",
        "subtitle": "Duty is weighed against the cost of conflict",
        "refs": [
            ("duty", MAHABHARATA, "Book VII · UDYOGA", "Known to all, ye mighty monarchs!", "Thoughts of peace and not of anger still the good Yudhishthir move!"),
            ("counsel", MAHABHARATA, "Book VII · UDYOGA", "Seek not war and death of kinsmen", "preserve thy ancient race."),
        ],
        "cards": [
            ("context", "A kingdom is disputed", "In Dutt's condensed verse rendering of the Mahabharata, Krishna addresses a council while the Pandavas seek the return of their kingdom after exile.", ["duty", "counsel"], "concept"),
            ("source", "Krishna asks for counsel", None, ["counsel"], "concept"),
            ("context", "A claim without eager war", "Krishna describes Yudhishthira as preferring even a small settlement to empire if it can be gained without sin, and asks the assembled rulers how to proceed.", ["duty"], "concept"),
            ("method", "Do not turn one epic scene into a universal rule", "This is Romesh Chunder Dutt's nineteenth-century condensed verse rendering. It gives one literary portrayal of deliberation, not a complete account of dharma across Indian traditions.", ["duty", "counsel"], "source"),
            ("synthesis", "The choice is political and ethical", "The council scene connects a disputed inheritance with questions about peace, justice, and the cost of war.", ["duty", "counsel"], "concept"),
        ],
        "questions": [
            ("What does the poem say Yudhishthira prizes above empire?", "A hamlet, if his course can remain free from sin", ["A victory won by a loaded dice game", "A throne gained without the council's knowledge"], "Krishna says Yudhishthira prizes even a hamlet more than empire if his course is free from sin.", ["duty"], "concept"),
            ("What does Krishna ask Dhrita-rashtra to do?", "Avert slaughter and preserve his ancient race", ["Send Sita into exile", "Award the kingdom by another dice game"], "Krishna pleads with Dhrita-rashtra to avert slaughter and preserve the Kuru family.", ["counsel"], "source"),
        ],
    },
    {
        "slug": "rama-exile",
        "title": "Rama: Accepting the Exile",
        "subtitle": "A royal command, a kingdom, and a promise",
        "refs": [
            ("acceptance", RAMAYANA, "Ayodhyakandam · Section XIX", "What of the command of the king, my father", "my kingdom, Sita, wealth and even my life"),
            ("duration", RAMAYANA, "Ayodhyakandam · Section XIX", "I shall, not even judging the propriety of my father's words", "for fourteen years."),
        ],
        "cards": [
            ("context", "The command changes the succession", "In Manmatha Nath Dutt's prose translation of the Ayodhyakandam, Rama responds to the command that sends him to the forest for fourteen years while Bharata is to receive the kingdom.", ["acceptance", "duration"], "concept"),
            ("source", "Rama accepts the command", None, ["acceptance"], "concept"),
            ("context", "The promise is more than a throne", "Rama says he will give up kingdom, Sita, wealth, and even life at the command of his father and Kaikeyi. The words are part of this translation's literary scene.", ["acceptance"], "concept"),
            ("method", "A specific volume and translation", "This source is Volume 1 of Dutt's English prose translation, containing the Balakandam and Ayodhyakandam. It does not include every later Ramayana episode or regional retelling.", ["acceptance"], "source"),
            ("synthesis", "Exile begins with a decision", "The passage frames the exile through Rama's response to a royal promise and command, not through a single general definition of duty.", ["acceptance"], "concept"),
        ],
        "questions": [
            ("What does Rama say he will give up at his father's command?", "His kingdom, Sita, wealth, and even his life", ["Only his bow and chariot", "Bharata's claim to the throne"], "Rama's speech explicitly lists kingdom, Sita, wealth, and life.", ["acceptance"], "concept"),
            ("Which part of the Ramayana does this local volume contain?", "The Balakandam and Ayodhyakandam", ["The complete seven-kanda epic", "Only the Bhagavad Gita"], "The title page identifies this as Volume 1, Balakandam and Ayodhyakandam.", ["acceptance"], "source"),
        ],
    },
    {
        "slug": "sita-separation",
        "title": "Sita: Choosing the Forest",
        "subtitle": "A wife's argument against remaining in the palace",
        "refs": [
            ("choice", RAMAYANA, "Ayodhyakandam · Section XXVII", "I shall go before thee, Oh Raghava", "I shall not abide by any other counsel."),
        ],
        "cards": [
            ("context", "Sita answers the exile", "When Rama prepares to leave for the forest, Sita argues that she will go with him rather than remain in the palace.", ["choice"], "concept"),
            ("source", "Sita states her choice", None, ["choice"], "concept"),
            ("context", "A reasoned appeal", "Sita invokes the teaching she says she received from her parents and insists that she will follow Rama. The lesson stays with Dutt's translated speech rather than treating it as a rule for all women.", ["choice"], "concept"),
            ("method", "Read the text's own voice carefully", "This passage is Dutt's English prose translation of one Ayodhyakandam section. Its gendered language belongs to this scene and translation; it should not be made into a universal statement about Indian women or practice.", ["choice"], "source"),
            ("synthesis", "Sita is an active speaker", "In this episode, Sita argues for her own course and gives reasons rather than remaining a silent object in Rama's decision.", ["choice"], "concept"),
        ],
        "questions": [
            ("What does Sita decide when Rama prepares to go to the forest?", "She insists on accompanying him", ["She asks Bharata to go in her place", "She remains in the palace without objection"], "Sita says she will go before Rama and describes how she will live in the forest.", ["choice"], "concept"),
            ("Which source boundary is important when discussing this speech?", "It is one translated epic scene, not a universal rule for all women", ["It is a modern legal code", "It proves that every Ramayana version uses identical words"], "The cited lines are from one translated Ayodhyakandam passage, not a survey of all traditions or practice.", ["choice"], "source"),
        ],
    },
    {
        "slug": "dice-war",
        "title": "The Dice Game: Draupadi Questions the Wager",
        "subtitle": "A challenge to the claim made in the council hall",
        "refs": [
            ("wager", MAHABHARATA, "Book IV · DYUTA", "Doth a crowned king and husband stake his wife", "wedded wife to sacrifice!"),
        ],
        "cards": [
            ("context", "A messenger brings the claim", "In Dutt's condensed verse rendering, a menial tells Draupadi that Yudhishthira lost a dice game and that Duryodhana claims her as a stake.", ["wager"], "concept"),
            ("source", "Draupadi asks what was wagered", None, ["wager"], "concept"),
            ("context", "The question is about agency", "Draupadi asks whether a king who has lost himself can then stake his wife. The scene gives her a direct argument in the assembly.", ["wager"], "concept"),
            ("method", "Abridged verse, not a full critical text", "Dutt's Maha-bharata is explicitly condensed into English verse. The local edition notes that it translates selected portions of the Sanskrit epic.", ["wager"], "source"),
            ("synthesis", "The wager is contested", "The episode does not ask learners to accept the dice outcome as morally settled: Draupadi challenges the logic of the claim against her.", ["wager"], "concept"),
        ],
        "questions": [
            ("What does Draupadi question in the council hall?", "Whether Yudhishthira could stake her after losing himself", ["Whether Krishna should lead the exile", "Whether Rama should give Bharata the sandals"], "Draupadi asks if a king who is himself a bondsman can stake his wife.", ["wager"], "concept"),
            ("What kind of Mahabharata text is this?", "A condensed English verse rendering by Romesh Chunder Dutt", ["A complete Sanskrit critical edition", "A modern eyewitness account of a dice game"], "The book identifies itself as the epic condensed into English verse.", ["wager"], "source"),
        ],
    },
    {
        "slug": "krishna-counsel",
        "title": "Bharata: Governing in Rama's Name",
        "subtitle": "The sandals become a sign of delegated rule",
        "refs": [
            ("sandals", RAMAYANA, "Ayodhyakandam · Section CXII", "Thereupon taking off his sandals", "made over the task of government unto thy sandals."),
        ],
        "cards": [
            ("context", "Bharata refuses to replace Rama", "In Dutt's Ayodhyakandam, Bharata returns to Rama and asks him to take the throne. Rama's sandals become part of their agreement about who will govern.", ["sandals"], "concept"),
            ("source", "A symbol of delegated rule", None, ["sandals"], "concept"),
            ("context", "A vow with a time limit", "Bharata says he will remain outside the city in ascetic dress for fourteen years and assign the work of government to the sandals while awaiting Rama's return.", ["sandals"], "concept"),
            ("method", "Keep this within Volume 1", "Dutt's first volume contains the Balakandam and Ayodhyakandam. This episode is a literary account of a specific succession, not evidence that sandals universally signify kingship in Indian practice.", ["sandals"], "source"),
            ("synthesis", "Authority is represented in absence", "The passage shows Bharata acting as steward while treating Rama as the rightful ruler in this version.", ["sandals"], "concept"),
        ],
        "questions": [
            ("What does Bharata assign the work of government to?", "Rama's sandals", ["Krishna's chariot", "The council's dice"], "Bharata says he has made over the task of government to Rama's sandals.", ["sandals"], "concept"),
            ("How long does Bharata vow to wait for Rama?", "Fourteen years", ["Twelve years", "One year"], "Bharata says he will wait for four and ten years.", ["sandals"], "source"),
        ],
    },
]


def make_reference(records, spec):
    ref_id, local_path, segment_locator, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / local_path)
         if item["locator"] == segment_locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named epic passage not found: {segment_locator}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {segment_locator}")
    end += len(end_anchor)
    relative = local_path.removeprefix("content/corpus/indian/")
    record = next(item for item in records if item["localPath"] == relative)
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": ", ".join(record.get("ancientAuthors", [])),
        "translator": record["translator"],
        "locator": f"{segment_locator}; {segment_locator}, normalized characters {start}-{end}",
        "localPath": local_path,
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": (
            "Verbatim English translation from Dutt. The Mahabharata volume is a condensed verse rendering; the Ramayana volume contains only the Balakandam and Ayodhyakandam."
        ),
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/indian/manifest.json").read_text(encoding="utf-8"))
    records = manifest["records"]
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/indian").rglob("*.json")
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
                body = "Source quotation (Dutt's English rendering; whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the named book and section in Dutt's translation.",
                    "suggestedQuestions": ["Which words support this answer?", "Is this a translation, abridgment, or later retelling?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Passage-specific Dutt epic revisions; independent review of Sanskrit source, translation, abridgment, reception, and pedagogy remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    parser.add_argument("--revise-v2", metavar="INPUT_SHA256")
    parser.add_argument("--revise-v3", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/indian").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    versions = {json.loads(path.read_text(encoding="utf-8")).get("version", 1) for path in paths}
    if args.apply and versions != {1}:
        parser.error("--apply only accepts the exact version-1 Indian starter lessons.")
    if args.revise_v2 and versions != {2}:
        parser.error("--revise-v2 only accepts the exact version-2 Indian starter lessons.")
    if args.revise_v3 and versions != {3}:
        parser.error("--revise-v3 only accepts the exact version-3 Indian starter lessons.")
    if versions - {1, 2, 3}:
        parser.error("Refusing to write beyond the reviewed one-time migrations for this pack.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} passage-specific lessons; no files written.")
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

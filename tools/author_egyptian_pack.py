"""One-time, digest-guarded source revision for the five Egyptian starter lessons."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
LEGENDS = "pg-9411"
LITERATURE = "pg-15932"

PACK = [
    {
        "slug": "osiris-renewal",
        "title": "Osiris: Kingship and Renewal",
        "subtitle": "A funerary hymn addresses the dead king",
        "objectives": [
            ("obj.osiris-renewal.concept", "Explain what the Papyrus of Ani hymn says about Osiris and Horus."),
            ("obj.osiris-renewal.source", "Identify the hymn as funerary text rather than a full narrative of Osiris' death."),
        ],
        "refs": [
            ("ani", LITERATURE, "Hymn to Osiris in the Papyrus of Ani", "Glory be to Osiris Un-Nefer", "for thy son Horus is established on thy throne."),
        ],
        "scene": "The opening hymn in the Papyrus of Ani addresses Osiris as an enduring king and says Horus is established on his throne. This passage praises and invokes Osiris; it does not narrate the whole story of his death and restoration.",
        "quoteCard": "The hymn names Osiris and Horus",
        "why": "The passage links Osiris' kingship with Horus' succession. Treat it as a funerary hymn from one manuscript, not a single canonical timeline for all Egyptian traditions.",
        "method": "Budge's anthology translates and introduces the papyrus. Keep his edition and translation attached; distinguish the hymn's words from his notes about them.",
        "carry": "As you read other funerary texts, ask who is speaking, to whom, and what the text is meant to do.",
        "questions": [
            ("What does the Papyrus of Ani hymn say about Horus?", "Horus is established on Osiris' throne", ["Horus destroys the Papyrus of Ani", "Horus is named as the translator"], "The hymn explicitly places Horus on Osiris' throne.", ["ani"], "concept"),
            ("What kind of passage is this excerpt?", "An opening funerary hymn in the Papyrus of Ani", ["A complete chronological biography of Osiris", "A modern novel about Egyptian kings"], "The edition identifies the excerpt as an opening hymn; it is not a complete narrative of the Osiris cycle.", ["ani"], "source"),
        ],
    },
    {
        "slug": "ra-order",
        "title": "Ra and the Destruction of Mankind",
        "subtitle": "A rebellion, the divine Eye, and the beer ruse",
        "objectives": [
            ("obj.ra-order.concept", "Trace how this version moves from human complaint to Ra's decision."),
            ("obj.ra-order.source", "Explain how beer stops the destruction in Budge's translated legend."),
        ],
        "refs": [
            ("complaint", LEGENDS, "Legend of the Destruction of Mankind, Chapter I, human complaint", "Now men and women were speaking words of complaint", "His Majesty heard the words of complaint which men and women were uttering"),
            ("eye", LEGENDS, "Legend of the Destruction of Mankind, Ra consults the gods", "Then the Majesty of Nu, to son Ra, spake", "let thine Eye go against those who have uttered blasphemies against thee."),
            ("beer", LEGENDS, "Legend of the Destruction of Mankind, the beer plan", "Now when the Majesty of Re, the King of the South and North", "and she gave no further attention to men and women."),
        ],
        "scene": "In this translated legend, people complain that Ra has grown old. He consults the gods, and the divine Eye is sent against the rebels. Later, beer mixed with mandrake and blood makes the goddess drink and stop the slaughter.",
        "quoteCard": "Humans complain and Ra consults",
        "why": "The tale connects royal authority, rebellion, violence, and a ruse that ends the slaughter. Preserve the episode's sequence rather than simplifying it to 'Ra brings order.'",
        "method": "Budge presents this as a translated Egyptian legend with editorial framing. The passage is one literary account, not proof that every Egyptian community held a single creation or order doctrine.",
        "carry": "Compare the decision to release the Eye with the later beer plan. The story gives two different moments of divine action.",
        "questions": [
            ("What complaint prompts Ra to consult the gods in this version?", "People say Ra has grown old", ["People refuse to honor Osiris' throne", "Hathor asks to become ruler of the earth"], "The story opens with people complaining about Ra's age and appearance.", ["complaint"], "concept"),
            ("What happens after the beer is prepared and poured out?", "The goddess drinks, becomes intoxicated, and stops attacking people", ["The beer restores Ra's youth", "The people are turned into stars"], "The translated legend says the beer distracts and intoxicates the destructive goddess.", ["beer"], "source"),
        ],
    },
    {
        "slug": "isis-restoration",
        "title": "Isis and Ra's Secret Name",
        "subtitle": "Knowledge, magic, and a snakebite",
        "objectives": [
            ("obj.isis-restoration.concept", "Explain how Isis uses a serpent and a hidden name in this translated legend."),
            ("obj.isis-restoration.source", "Keep Budge's version of the Ra-and-Isis story distinct from other Isis traditions."),
        ],
        "refs": [
            ("serpent", LEGENDS, "Legend of Ra and Isis, the serpent and Ra's illness", "Soon after Isis had placed the serpent on the Path", "Then Isis said to him with guile"),
            ("name", LEGENDS, "Legend of Ra and Isis, the hidden name", "Then Isis said to him with guile", "Isis, however, was not deceived"),
            ("transfer", LEGENDS, "Legend of Ra and Isis, transfer of the hidden name", "Isis shall search in me", "Ra thus became to all intents and purposes a dead god."),
        ],
        "scene": "Budge's translation tells how Isis makes a serpent from Ra's saliva and dust. After it bites Ra, she asks for his hidden name, saying that speaking it will let him live.",
        "quoteCard": "Isis asks for the hidden name",
        "why": "The episode makes knowledge and speech powerful within this story. It is one translated legend, not a timeless summary of every Isis tradition.",
        "method": "The edition identifies this legend with a Turin papyrus and includes Budge's commentary. Keep the translated narrative distinct from his historical explanation.",
        "carry": "Track the chain of action: serpent, bite, request for the name, disclosure, and spell. Notice whose knowledge moves the plot.",
        "questions": [
            ("How does Isis first make Ra vulnerable in this story?", "She makes a poisonous serpent from his saliva and dust", ["She steals his sun boat", "She hides Osiris' throne"], "The legend says she mixes Ra's saliva with dust and leaves the serpent on his path.", ["serpent"], "concept"),
            ("What does Isis seek from Ra after the bite?", "His hidden name, which gives her power to speak a healing spell", ["His throne in Heliopolis", "A new name for the Nile"], "The narrative ties knowledge of Ra's hidden name to Isis' words of power.", ["name", "transfer"], "source"),
        ],
    },
    {
        "slug": "judgment-dead",
        "title": "Judgment of the Dead",
        "subtitle": "Declarations before the Forty-two Judges",
        "objectives": [
            ("obj.judgment-dead.concept", "Describe the declarations quoted from the Book of the Dead, Chapter 125."),
            ("obj.judgment-dead.source", "Limit conclusions to this funerary text and Budge's edition."),
        ],
        "refs": [
            ("confession", LITERATURE, "Book of the Dead, Chapter 125, declarations before the Forty-two Judges", "Hail, thou of the long strides", "Hail, Crusher of bones, who comest forth"),
        ],
        "scene": "In Budge's translation of Chapter 125, the deceased addresses named judges and declares that they have not committed particular wrongs. The text frames judgment as a speech act before divine assessors.",
        "quoteCard": "A few declarations from Chapter 125",
        "why": "These declarations belong to a particular funerary text and edition. Do not turn them into one uniform moral code for every Egyptian person or period.",
        "method": "The source is a translated collection with editorial explanations. A text about judgment is evidence for this ritual-literary tradition, not direct observation of every funeral practice.",
        "carry": "When a funerary text speaks in the first person, ask whether the speaker is the deceased, a ritual officiant, or a god.",
        "questions": [
            ("What kind of statements appear in the quoted declarations?", "The deceased denies specific wrongs before named judges", ["A list of Ra's military victories", "A record of how the pyramids were built"], "The excerpt lists declarations such as not committing sin, theft, or murder.", ["confession"], "concept"),
            ("What should this passage not be used to claim by itself?", "That every Egyptian community shared one identical judgment ritual", ["That this text names judges", "That the translation comes through Budge's edition"], "One funerary text cannot establish a uniform practice across all places and periods.", ["confession"], "source"),
        ],
    },
    {
        "slug": "thoth-knowledge",
        "title": "Thoth: Writing and Sacred Speech",
        "subtitle": "A funerary voice and a modern editor's account",
        "objectives": [
            ("obj.thoth-knowledge.concept", "Interpret the identification of the speaker as Thoth in the Papyrus of Hunefer hymn."),
            ("obj.thoth-knowledge.source", "Distinguish the translated ritual text from Budge's editorial claim about writing."),
        ],
        "refs": [
            ("hunefer", LITERATURE, "Hymn to Osiris in the Papyrus of Hunefer, the speaker's declaration", "I have not committed any kind of sin in the land", "what I abominate is sin."),
            ("budge", LITERATURE, "Budge, Chapter I, Thoth and writing", "Egyptian writing was believed to have been invented by the god Tehuti, or Thoth", "were held to be holy, or divine, or sacred."),
        ],
        "scene": "In a hymn that Budge attributes to the Papyrus of Hunefer, the speaker says, 'I am Thoth, the perfect scribe.' Budge's separate introductory chapter reports a belief that Thoth invented writing.",
        "quoteCard": "A ritual speaker identifies with Thoth",
        "why": "The words 'I am Thoth' occur in a funerary hymn's first-person declaration. They are not a biography of the god or proof that Thoth literally authored this manuscript.",
        "method": "Budge's Chapter I is modern editorial prose; the Hunefer hymn is a translated ancient text. Keep those evidence types and voices separate.",
        "carry": "Ask who is speaking before treating a divine identity formula as a literal statement about authorship.",
        "questions": [
            ("Who says 'I am Thoth, the perfect scribe' in the cited passage?", "The first-person speaker in a funerary hymn", ["Budge in his Chapter I essay", "A Greek historian describing Thoth"], "Budge introduces the words as part of a hymn in the Papyrus of Hunefer.", ["hunefer"], "concept"),
            ("How should Budge's statement that Thoth invented writing be treated?", "As a modern editor's report of an Egyptian religious belief", ["As Thoth's own surviving autobiography", "As a claim made in the Hunefer hymn"], "The statement appears in Budge's introductory essay, not as the Hunefer hymn's own voice.", ["budge", "hunefer"], "source"),
        ],
    },
]


def make_reference(records, root, spec):
    ref_id, record_id, work, start_anchor, end_anchor = spec
    record = records[record_id]
    local_path = f"content/corpus/egyptian/{record['localPath']}"
    text = source_segments(root / local_path)[0]["text"]
    start = text.find(start_anchor)
    end = text.find(end_anchor, start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {work}")
    editorial = work.startswith("Budge's Chapter")
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": work,
        "author": "E. A. Wallis Budge" if editorial else ", ".join(record.get("ancientAuthors", [])),
        "translator": record.get("translator", "not applicable"),
        "locator": f"{work}; local text normalized characters {start}-{end}",
        "localPath": local_path,
        "excerpt": text[start:end].strip(),
        "evidenceType": "quotation",
        "note": "Budge's 20th-century editorial prose, not ancient testimony." if editorial else "Verbatim translation excerpt; whitespace normalized. Keep the ancient text separate from Budge's editorial notes.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/egyptian/manifest.json").read_text(encoding="utf-8"))
    records = {item["id"]: item for item in manifest["records"]}
    lesson_paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/egyptian").rglob("*.json")
    }
    changes = {}
    for spec in PACK:
        path = lesson_paths[spec["slug"]]
        lesson = json.loads(path.read_text(encoding="utf-8"))
        lesson["version"] = 2
        lesson["estimatedMinutes"] = 3
        lesson["difficulty"] = 2
        concept_id = lesson["learningObjectives"][0]["id"]
        source_id = lesson["learningObjectives"][-1]["id"]
        lesson["learningObjectives"] = [
            {"id": concept_id, "text": spec["questions"][0][0]},
            {"id": source_id, "text": spec["questions"][1][0]},
        ]
        lesson["sourceReferences"] = {item[0]: make_reference(records, ROOT, item) for item in spec["refs"]}
        refs = list(lesson["sourceReferences"])
        cards = [
            ("context", "The scene", spec["scene"], refs, "concept"),
            ("source", spec["quoteCard"], None, refs[:1], "concept"),
            ("synthesis", "Why it matters", spec["why"], refs, "concept"),
            ("method", "Read the evidence carefully", spec["method"], refs, "source"),
            ("flavor", "Carry it forward", spec["carry"], refs, "source"),
        ]
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, card_refs, objective) in enumerate(cards, 1):
            if body is None:
                body = "Source quotation (Budge translation; whitespace normalized): “" + lesson["sourceReferences"][card_refs[0]]["excerpt"] + "”"
            lesson["narrativeBlocks"].append({
                "id": f"card-{index:02d}", "kind": kind, "title": title, "body": body,
                "sourceRefIds": card_refs,
                "objectiveIds": [concept_id if objective == "concept" else source_id],
            })
        lesson["quiz"] = []
        for index, (prompt, correct, wrong, explanation, question_refs, objective) in enumerate(spec["questions"]):
            options = [correct, *wrong]
            shift = (index + len(changes)) % 3
            options = options[shift:] + options[:shift]
            choices = [{"id": chr(97 + i), "text": text} for i, text in enumerate(options)]
            lesson["quiz"].append({
                "id": f"q{index + 1}", "type": "single-choice", "prompt": prompt,
                "choices": choices,
                "answerId": next(choice["id"] for choice in choices if choice["text"] == correct),
                "explanation": explanation, "sourceRefIds": question_refs,
                "objectiveIds": [concept_id if objective == "concept" else source_id],
                "deepDive": {
                    "prompt": "Read the cited local text.",
                    "suggestedQuestions": ["Which words support this answer?", "Is this the translated text or editorial context?"],
                    "sourceRefIds": question_refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Source-specific editorial rewrite; independent claim-by-claim scholarly and pedagogical review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/egyptian").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Egyptian starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} source-specific lesson revisions; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        for path, lesson in changes.items():
            path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied once; future generated writes are disabled.")


if __name__ == "__main__":
    main()

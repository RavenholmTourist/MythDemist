"""Synchronize reviewed Greek assessment evidence and improve generic explanations."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]

ASSESSMENT_REFS = {
    "grc.heroes.w02d02.briseis-and-withdrawal": ["main", "restraint", "aftermath"],
    "grc.heroes.w02d03.the-embassy-fails": ["offer", "main"],
    "grc.heroes.w02d04.patroclus-changes-everything": ["main", "armor"],
    "grc.heroes.w02d05.priam-and-achilles": ["main", "release"],
    "grc.heroes.w03d01.the-broken-house": ["main", "pressure"],
    "grc.heroes.w03d02.nobody-and-the-cyclops": ["main", "boast", "curse"],
    "grc.heroes.w04d02.aeetes-and-the-tasks": ["main", "aid"],
    "grc.heroes.w04d03.medea-chooses": ["main", "dilemma", "aid"],
    "grc.heroes.w04d04.flight-and-pursuit": ["main", "purification"],
    "grc.heroes.w05d02.the-nemean-lion": ["main", "combat"],
    "grc.heroes.w06d02.the-minotaur-and-ariadne": ["main", "escape"],
    "grc.heroes.w06d05.the-civic-hero": ["main", "heracles"],
    "grc.heroes.w07d01.agamemnon-returns": ["main", "murder", "odyssey"],
    "grc.heroes.w07d02.orestes-and-justice": ["main", "court"],
    "grc.heroes.w07d03.antigone-and-burial": ["main", "defense"],
    "grc.heroes.w07d04.oedipus-investigates": ["main", "revelation"],
    "grc.heroes.w08d01.persephone-descends": ["main", "agreement"],
    "grc.heroes.w08d03.ovid-transforms": ["main", "epitome"],
}


def add_epitome_reference(lesson):
    path = ROOT / "content/corpus/greek/primary/apollodorus-epitome-frazer-perseus-eng2.xml"
    segment = next(s for s in source_segments(path) if s["locator"] == "chapter 1 · section 9" and s["evidenceType"] == "source-text")
    start_anchor = "And at his suggestion she gave Theseus a clue"
    end_anchor = "drawing the clue after him made his way out again."
    start = segment["text"].casefold().find(start_anchor.casefold())
    end = segment["text"].casefold().find(end_anchor.casefold(), start + len(start_anchor)) + len(end_anchor)
    if start < 0 or end < len(end_anchor):
        raise ValueError("Could not anchor Epitome 1.9 clue passage")
    lesson["sourceReferences"]["epitome"] = {
        "recordId": "perseus-apollodorus-epitome-frazer",
        "sourceId": "grc.apollodorus.epitome",
        "work": "Bibliotheca (Epitome)",
        "author": "Pseudo-Apollodorus",
        "translator": "James George Frazer",
        "locator": f"Epitome 1.9, Ariadne's clue; chapter 1 · section 9, normalized characters {start}-{end}",
        "localPath": "content/corpus/greek/primary/apollodorus-epitome-frazer-perseus-eng2.xml",
        "excerpt": segment["text"][start:end],
        "evidenceType": "quotation",
        "note": "Verbatim text from the Epitome; this passage calls the aid a clue and does not specify a thread.",
    }
    lesson["narrativeBlocks"][-1]["sourceRefIds"] = ["main", "epitome"]


def explanation(answer, question_refs, lesson):
    refs = [lesson["sourceReferences"][ref_id] for ref_id in question_refs]
    cited = "; ".join(
        f"{ref['work']} ({ref['locator'].split(';')[0]})" for ref in refs
    )
    return f"{answer} is the passage-specific answer. Check {cited}, keeping each work and version distinct."


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    lesson_paths = sorted((ROOT / "content/lessons/greek").rglob("*.json"))
    week_paths = sorted((ROOT / "content/curriculum/greek").glob("*week*.json"))
    files = lesson_paths + week_paths
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in files)).hexdigest()
    lessons = {}
    originals = {}
    for path in lesson_paths:
        document = json.loads(path.read_text(encoding="utf-8"))
        lessons[document["id"]] = (path, document)
        originals[path] = json.dumps(document, ensure_ascii=False, sort_keys=True)
    lesson_changes = {}
    week_changes = {}

    target = lessons["grc.heroes.w08d03.ovid-transforms"][1]
    add_epitome_reference(target)
    lesson_changes[lessons["grc.heroes.w08d03.ovid-transforms"][0]] = target

    for path in week_paths:
        week = json.loads(path.read_text(encoding="utf-8"))
        if "assessment" not in week:
            continue
        for item in week["assessment"].get("questions", []):
            lesson_id = item["lessonId"]
            question = item["question"]
            lesson = lesson_changes.get(lessons[lesson_id][0], lessons[lesson_id][1])
            refs = ASSESSMENT_REFS.get(lesson_id, question.get("sourceRefIds", []))
            question["sourceRefIds"] = refs
            answer = next(choice["text"] for choice in question["choices"] if choice["id"] == question["answerId"])
            question["explanation"] = explanation(answer, refs, lesson)
        week_changes[path] = week

    # Daily explanations must explain the actual keyed answer and identify the
    # exact work rather than using the old generator's generic prompt.
    for path, lesson in lessons.values():
        lesson = lesson_changes.get(path, lesson)
        for question in lesson["quiz"]:
            answer = next(choice["text"] for choice in question["choices"] if choice["id"] == question["answerId"])
            if "Revisit the named passage" in question.get("explanation", ""):
                question["explanation"] = explanation(answer, question["sourceRefIds"], lesson)
        if json.dumps(lesson, ensure_ascii=False, sort_keys=True) != originals[path]:
            lesson_changes[path] = lesson

    print("Input SHA256:", digest)
    print(f"Prepared assessment/source alignment for {len(lesson_changes)} Greek lessons and {len(week_changes)} assessment banks; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Greek lesson or assessment inputs changed; refusing to overwrite.")
        for path, doc in {**lesson_changes, **week_changes}.items():
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied once.")


if __name__ == "__main__":
    main()

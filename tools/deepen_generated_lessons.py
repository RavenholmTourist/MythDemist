# Archived scaffolder: its unconditional writes would destroy later editorial work.
raise SystemExit('Retired generator: edit canonical JSON or implement a reviewed staging-only generator.')

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECOND_WAVE = {"chinese", "mesoamerican", "mesopotamian", "indian", "polynesian"}

def refs(lesson):
    return list(lesson["sourceReferences"].keys())

def upgrade(path):
    lesson = json.loads(path.read_text(encoding="utf-8"))
    cards = lesson["narrativeBlocks"]
    if len(cards) >= 5 or lesson["pantheon"] in SECOND_WAVE or lesson["pantheon"] == "greek":
        return False
    source_ids = refs(lesson)
    concept = lesson["learningObjectives"][0]["id"]
    source_obj = lesson["learningObjectives"][-1]["id"]
    synthesis = cards[-1]
    inserts = [
        {
            "id": "card-03", "kind": "source",
            "title": "What the second source adds",
            "body": "The additional corpus record gives a second lens on the same tradition. Compare it with the first source instead of treating either as a complete canon.",
            "sourceRefIds": source_ids,
            "objectiveIds": [source_obj]
        },
        {
            "id": "card-04", "kind": "method",
            "title": "How to read this evidence",
            "body": "Ask what kind of source this is, who translated or organized it, what it can actually prove, and whether another text preserves a different version.",
            "sourceRefIds": source_ids,
            "objectiveIds": [source_obj]
        }
    ]
    synthesis["id"] = "card-05"
    lesson["narrativeBlocks"] = cards[:2] + inserts + [synthesis]
    lesson["review"]["notes"] = (lesson["review"].get("notes", "") + " Deepened to the five-card lesson standard.").strip()
    path.write_text(json.dumps(lesson, indent=2) + "\n", encoding="utf-8")
    return True

changed = 0
for path in (ROOT / "content/lessons").rglob("*.json"):
    changed += upgrade(path)
print(f"deepened {changed} lessons")

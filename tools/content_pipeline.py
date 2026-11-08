#!/usr/bin/env python
"""Validate Mythos content and generate the shared content index."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator
from build_retrieval_index import main as build_retrieval_index
from source_evidence import check_reference

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def check_schema(doc_path, schema_path, errors):
    try:
        doc, schema = load(doc_path), load(schema_path)
    except Exception as exc:
        errors.append(f"{doc_path}: cannot load or schema load failed: {exc}")
        return None
    found = list(Draft202012Validator(schema).iter_errors(doc))
    errors.extend(f"{doc_path}: {error.message}" for error in found)
    return doc


def check_links(lesson, errors):
    refs = set(lesson['sourceReferences'])
    objectives = {item['id'] for item in lesson['learningObjectives']}
    review = lesson.get('review', {})
    if review.get('status') == 'reviewed':
        reviewer = (review.get('reviewedBy') or '').strip().lower()
        if not reviewer or reviewer in {'devin', 'assistant', 'ai', 'model'}:
            errors.append(f"{lesson['id']}: reviewed status needs an independent named reviewer")
        if not (review.get('notes') or '').strip():
            errors.append(f"{lesson['id']}: reviewed status needs a review note")
        untyped = [key for key, ref in lesson['sourceReferences'].items() if ref.get('evidenceType') not in {'quotation', 'paraphrase'}]
        if untyped:
            errors.append(f"{lesson['id']}: reviewed status contains untyped source references {untyped}")
    for item in [*lesson['narrativeBlocks'], *lesson['quiz']]:
        if not set(item['sourceRefIds']) <= refs or not set(item['objectiveIds']) <= objectives:
            errors.append(f"{lesson['id']}:{item['id']}: unknown source or objective")
    for question in lesson['quiz']:
        choices = [item['id'] for item in question['choices']]
        if len(set(choices)) != len(choices) or question['answerId'] not in choices:
            errors.append(f"{lesson['id']}:{question['id']}: invalid answer/duplicate choice")


def main(check_only=False):
    errors = []
    registry = check_schema("content/pantheons.json", "data/schemas/pantheon.schema.json", errors)
    art = check_schema("content/art/catalog.json", "data/schemas/art.schema.json", errors)
    shared_arcs = [
        check_schema(str(path.relative_to(ROOT)), "data/schemas/arc.schema.json", errors)
        for path in sorted((ROOT / "content/curriculum/arcs").glob("*.json"))
    ]
    programme_gates = load("content/curriculum/programme-gates.json")
    programme_manifests = load("content/curriculum/programmes.json") if (ROOT / "content/curriculum/programmes.json").exists() else {}

    all_weeks, all_lessons, all_topics, all_sources, all_arc_choices = [], [], [], [], []
    lesson_paths = {}
    pending_global_topic_checks = []
    pending_global_record_checks = []

    for pantheon_id, pantheon in registry["pantheons"].items():
        if pantheon["status"] != "active":
            continue
        paths = pantheon.get("paths", {})
        week_path, map_path, manifest_path = (
            paths.get("activeWeek"), paths.get("learningMap"), paths.get("corpusManifest")
        )
        if not all([week_path, map_path, manifest_path]):
            errors.append(f"{pantheon_id}: active pantheon is missing required content paths")
            continue

        learning_map = check_schema(map_path, "data/schemas/topic.schema.json", errors)
        manifest = load(manifest_path)
        manifest_by_id = {record["id"]: record for record in manifest["records"]}
        all_lesson_docs = []
        week_files = {week_path} | {str(path.relative_to(ROOT)).replace("\\", "/") for path in (ROOT / f"content/curriculum/{pantheon_id}").glob("*week*.json")}
        for current_week_path in sorted(week_files):
            current_week = check_schema(current_week_path, "data/schemas/week.schema.json", errors)
            lesson_docs = []
            for day in current_week["days"]:
                lesson_path = day.get("lessonPath")
                if day.get("status") == "available" and not lesson_path:
                    errors.append(f"{current_week_path}: day {day['day']} is available without lessonPath")
                    continue
                if not lesson_path:
                    continue
                if not (ROOT / lesson_path).exists():
                    errors.append(f"{lesson_path}: missing file")
                    continue
                lesson = check_schema(lesson_path, "data/schemas/lesson.schema.json", errors)
                if lesson:
                    if lesson["pantheon"] != pantheon_id:
                        errors.append(f"{lesson_path}: pantheon is {lesson['pantheon']}, expected {pantheon_id}")
                    if lesson['id'] != day.get('lessonId') or lesson['weekId'] != current_week['id']:
                        errors.append(f"{lesson_path}: lesson/week identity does not match its day entry")
                    check_links(lesson, errors)
                    lesson_paths[lesson['id']] = lesson_path
                    lesson_docs.append(lesson)
            all_lesson_docs.extend(lesson_docs)
            all_weeks.append({
                "id": current_week["id"], "title": current_week["title"], "pantheon": current_week["pantheon"],
                "path": current_week_path, "dayCount": len(current_week["days"]),
                "lessonIds": [day.get("lessonId") for day in current_week["days"] if day.get("lessonId")],
                "assessment": current_week.get("assessment"),
                "themes": sorted({tag for lesson in lesson_docs for tag in lesson.get("tags", [])})
            })
        week = check_schema(week_path, "data/schemas/week.schema.json", errors)
        lesson_docs = all_lesson_docs
        manifest_ids = set(manifest_by_id)
        for lesson in lesson_docs:
            for ref_id, source in lesson["sourceReferences"].items():
                record = manifest_by_id.get(source["recordId"])
                if not record:
                    errors.append(f"{lesson['id']}:{ref_id}: missing corpus record {source['recordId']}")
                    continue
                if record.get("accessScope") == "personal-local-only":
                    errors.append(f"{lesson['id']}:{ref_id}: personal-local-only sources cannot be lesson evidence")
                if source["sourceId"] not in record.get("sourceIds", []):
                    errors.append(f"{lesson['id']}:{ref_id}: sourceId {source['sourceId']} is not declared by record {record['id']}")
                expected = f"content/corpus/{pantheon_id}/{record['localPath']}"
                if source["localPath"] != expected:
                    errors.append(f"{lesson['id']}:{ref_id}: localPath expected {expected}, found {source['localPath']}")
        corpus_root = ROOT / "content/corpus" / pantheon_id
        for record in manifest["records"]:
            path = corpus_root / record["localPath"]
            available = path.exists()
            if not available and record.get("accessScope") != "personal-local-only":
                errors.append(f"missing corpus file: {path.relative_to(ROOT)}")
            all_sources.append({
                "id": record["id"], "pantheon": pantheon_id, "title": record["title"],
                "sourceType": record.get("sourceType"), "sourceIds": record.get("sourceIds", []),
                "localPath": f"content/corpus/{pantheon_id}/{record['localPath']}",
                "accessScope": record.get("accessScope", "shared"), "available": available
            })

        topics = learning_map["topics"]
        for topic_id, topic in topics.items():
            missing_topics = [item for item in topic["nextTopicIds"] if item not in topics]
            missing_records = [item for item in topic["recordIds"] if item not in manifest_ids]
            if missing_topics:
                pending_global_topic_checks.append((topic_id, missing_topics))
            if missing_records:
                errors.append(f"{topic_id}: missing corpus records {missing_records}")
            all_topics.append({
                "id": topic_id, "pantheon": pantheon_id, "title": topic["title"],
                "recordIds": topic["recordIds"], "nextTopicIds": topic["nextTopicIds"],
            "themes": topic.get("themes", []), "entities": topic.get("entities", [])
            })

        all_lessons.extend({
            "id": lesson["id"], "version": lesson['version'], "pantheon": lesson["pantheon"], "title": lesson["title"],
            "weekId": lesson["weekId"], "tags": lesson["tags"], "difficulty": lesson["difficulty"],
            "path": lesson_paths[lesson['id']],
            "objectiveIds": [item['id'] for item in lesson['learningObjectives']],
            "recordIds": sorted({ref['recordId'] for ref in lesson['sourceReferences'].values()}),
            "rewardArtId": lesson.get("rewardArtId"),
            "questionCount": len(lesson["quiz"]), "cardCount": len(lesson["narrativeBlocks"]),
            "themes": sorted(set(lesson.get("tags", []))),
            "entities": sorted(set(lesson.get("tags", [])))
        } for lesson in lesson_docs)
        all_arc_choices.extend(
            {**arc, "pantheon": pantheon_id, "scope": arc.get("scope", "pantheon")}
            for arc in learning_map["arcChoices"]
        )

    shared_map_path = ROOT / "content/curriculum/shared/learning-map.json"
    if shared_map_path.exists():
        shared_map = check_schema("content/curriculum/shared/learning-map.json", "data/schemas/topic.schema.json", errors)
        for topic_id, topic in shared_map["topics"].items():
            pending_global_topic_checks.append((topic_id, [item for item in topic["nextTopicIds"] if item not in shared_map["topics"]]))
            pending_global_record_checks.extend((topic_id, item) for item in topic["recordIds"])
            all_topics.append({"id": topic_id, "pantheon": "shared", "title": topic["title"], "recordIds": topic["recordIds"], "nextTopicIds": topic["nextTopicIds"]})
    for shared_week_path in sorted((ROOT / "content/curriculum/shared").glob("*week*.json")):
        shared_week = check_schema(str(shared_week_path.relative_to(ROOT)), "data/schemas/week.schema.json", errors)
        for day in shared_week["days"]:
            if day.get("lessonPath") and not (ROOT / day["lessonPath"]).exists():
                errors.append(f"{day['lessonPath']}: missing shared lesson file")
        all_weeks.append({"id": shared_week["id"], "title": shared_week["title"], "pantheon": shared_week["pantheon"], "path": str(shared_week_path.relative_to(ROOT)).replace("\\", "/"), "dayCount": len(shared_week["days"]), "lessonIds": [day.get("lessonId") for day in shared_week["days"] if day.get("lessonId")], "themes": sorted({day.get("theme", "") for day in shared_week["days"] if day.get("theme")})})

    gate_arc_ids = {item["id"] for item in all_arc_choices} | {item["id"] for item in shared_arcs}
    for arc_id, gate in programme_gates.items():
        if arc_id not in gate_arc_ids:
            errors.append(f"programme gate {arc_id}: unknown arc")
        missing = [item for item in gate.get("prerequisiteArcIds", []) if item not in gate_arc_ids]
        if missing:
            errors.append(f"programme gate {arc_id}: missing prerequisite arcs {missing}")
    weeks_by_id = {item["id"]: item for item in all_weeks}
    for arc_id, programme in programme_manifests.items():
        seen_week_ids = set()
        if len(programme.get("weeks", [])) != 8:
            errors.append(f"{arc_id}: programme must declare exactly 8 weeks")
        for module in programme.get("weeks", []):
            week_id = module.get("weekId")
            module_week = weeks_by_id.get(week_id)
            if not module_week:
                errors.append(f"{arc_id}: unknown programme week {week_id}")
                continue
            if week_id in seen_week_ids:
                errors.append(f"{arc_id}: duplicate programme week {week_id}")
            seen_week_ids.add(week_id)
            if module.get("weekPath") != module_week["path"]:
                errors.append(f"{arc_id}:{week_id}: expected path {module_week['path']}, found {module.get('weekPath')}")
            if module_week["dayCount"] != 5:
                errors.append(f"{arc_id}:{week_id}: programme week must have 5 days, found {module_week['dayCount']}")
            if module_week["lessonIds"] and (ROOT / module_week["path"]).exists():
                module_week_doc = load(module_week["path"])
                if module.get("assessment") and not module_week_doc.get("assessment"):
                    errors.append(f"{arc_id}:{week_id}: manifest declares assessment missing from week file")
                assessment = module_week_doc.get('assessment', {})
                questions = assessment.get('questions', [])
                if len(questions) != 5:
                    errors.append(f"{week_id}: five authored assessment questions required")
                for item in questions:
                    day = next((day for day in module_week_doc['days'] if day.get('lessonId') == item.get('lessonId')), None)
                    if not day:
                        errors.append(f"{week_id}: assessment references unknown lesson")
                        continue
                    doc = load(day['lessonPath'])
                    question = item['question']
                    check_links({**doc, 'quiz': [question], 'narrativeBlocks': []}, errors)
                    validation = Draft202012Validator(load('data/schemas/lesson.schema.json')['properties']['quiz']['items'])
                    errors.extend(f"{week_id}: {issue.message}" for issue in validation.iter_errors(question))
                    if any(question['prompt'] == old['prompt'] for old in doc['quiz']):
                        errors.append(f"{week_id}: assessment must not reuse a daily prompt")
                for lesson_id in module_week["lessonIds"]:
                    lesson = next((item for item in all_lessons if item["id"] == lesson_id), None)
                    lesson_path = next((day['lessonPath'] for day in module_week_doc['days'] if day.get('lessonId') == lesson_id), None)
                    if lesson_path:
                        lesson_doc = load(lesson_path)
                        for ref in lesson_doc['sourceReferences'].values():
                            errors.extend(f"{lesson_id}: {issue}" for issue in check_reference(ref, ROOT))
                    if not lesson:
                        errors.append(f"{arc_id}:{week_id}: unindexed lesson {lesson_id}")
                    if lesson and (lesson["cardCount"] < 5 or lesson["questionCount"] < 2 or not lesson.get("themes")):
                        errors.append(f"{arc_id}:{week_id}:{lesson_id}: dedicated programme lesson needs at least 5 cards, 2 questions, and themes")
    for collection in (all_arc_choices, shared_arcs):
        for arc in collection:
            arc.update(programme_gates.get(arc["id"], {}))
            if arc["id"] in programme_manifests:
                # Lesson plans own their question banks; do not propagate a stale duplicate from the arc manifest.
                arc["programmeWeeks"] = [
                    {
                        **entry,
                        "assessment": weeks_by_id[entry["weekId"]].get("assessment"),
                    }
                    for entry in programme_manifests[arc["id"]]["weeks"]
                    if entry["weekId"] in weeks_by_id
                ]

    global_record_ids = {item["id"] for item in all_sources}
    for topic_id, record_id in pending_global_record_checks:
        if record_id not in global_record_ids:
            errors.append(f"{topic_id}: missing corpus record {record_id}")

    known_topic_ids = {item["id"] for item in all_topics}
    for topic_id, missing in pending_global_topic_checks:
        unresolved = [item for item in missing if item not in known_topic_ids]
        if unresolved:
            errors.append(f"{topic_id}: missing next topics {unresolved}")

    for record in art["records"]:
        if not (ROOT / record["localPath"]).exists():
            errors.append(f"missing art file: {record['localPath']}")

    index = {
        "version": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "pantheons": {key: {"id": item["id"], "name": item["name"], "status": item["status"], "visual": item["visual"], "coverageType": item.get("coverageType", "tradition")} for key, item in registry["pantheons"].items()},
        "weeks": all_weeks,
        "lessons": all_lessons,
        "topics": all_topics,
        "arcChoices": all_arc_choices,
        "arcs": shared_arcs,
        "sources": all_sources,
        "art": [{
            "id": record["id"], "title": record["title"], "localPath": record["localPath"],
            "subjects": record["subjects"], "usage": record.get("usage", ["reward"])
        } for record in art["records"]]
    }
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    # Invalid content must never replace a previously working index. --check is read-only.
    if check_only:
        print(f"Content checks passed: {len(all_lessons)} lessons (no files written)")
        return
    build_retrieval_index()
    destination = ROOT / 'content/index.json'
    temporary = destination.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(index, indent=2) + '\n', encoding='utf-8')
    temporary.replace(destination)
    print(f"Validated {len(all_lessons)} lessons, {len(all_sources)} sources, {len(art['records'])} art records, {len(shared_arcs)} shared arcs")
    print("Wrote content/index.json")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Validate without changing any indexes')
    main(check_only=parser.parse_args().check)

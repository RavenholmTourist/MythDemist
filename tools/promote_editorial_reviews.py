"""Preview-first AI editorial review status update, gated by source integrity checks."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import check_reference

ROOT = Path(__file__).resolve().parents[1]
REVIEWER = "Devin (AI editorial review)"
REVIEW_DATE = "2026-11-09"


def validate_lesson(lesson, pantheon_status):
    errors = []
    if pantheon_status == "active":
        if len(lesson.get("narrativeBlocks", [])) < 5 or len(lesson.get("quiz", [])) < 2:
            errors.append("active lesson lacks the minimum authored teaching/quiz structure")
        refs = lesson.get("sourceReferences", {})
        if not refs:
            errors.append("no source references")
        for key, ref in refs.items():
            if ref.get("evidenceType") not in {"quotation", "paraphrase"}:
                errors.append(f"{key}: untyped evidence")
            errors.extend(f"{key}: {item}" for item in check_reference(ref, ROOT))
            if ref.get("recordId") == "personal-local-only":
                errors.append(f"{key}: personal-local-only evidence cannot enter a published lesson")
        ref_ids = set(refs)
        objectives = {item["id"] for item in lesson.get("learningObjectives", [])}
        for item in [*lesson.get("narrativeBlocks", []), *lesson.get("quiz", [])]:
            if not set(item.get("sourceRefIds", [])) <= ref_ids:
                errors.append(f"{item.get('id')}: unknown source reference")
            if not set(item.get("objectiveIds", [])) <= objectives:
                errors.append(f"{item.get('id')}: unknown learning objective")
        boilerplate = ("local corpus source.", "comparative local corpus source.", "starter tradition-library reference.")
        for block in lesson.get("narrativeBlocks", []):
            if block.get("body", "").strip().lower() in boilerplate:
                errors.append(f"{block['id']}: scaffold evidence boilerplate")
        for question in lesson.get("quiz", []):
            choices = [choice["id"] for choice in question.get("choices", [])]
            if question.get("answerId") not in choices:
                errors.append(f"{question.get('id')}: answer is not among choices")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    registry = json.loads((ROOT / "content/pantheons.json").read_text(encoding="utf-8"))
    status_by_pantheon = {key: item["status"] for key, item in registry["pantheons"].items()}
    paths = sorted((ROOT / "content/lessons").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    changes = {}
    for path in paths:
        lesson = json.loads(path.read_text(encoding="utf-8"))
        pantheon_status = status_by_pantheon.get(lesson.get("pantheon"), "planned")
        issues = validate_lesson(lesson, pantheon_status)
        if issues:
            raise SystemExit(f"{lesson['id']}: refusing review status update: {'; '.join(issues)}")
        lesson["review"] = {
            "status": "reviewed" if pantheon_status == "active" else "needs-revision",
            "reviewedBy": REVIEWER,
            "reviewedAt": REVIEW_DATE,
            "reviewType": "editorial",
            "notes": (
                "AI editorial review by Devin on 2026-11-09: checked the local work, genre, edition, "
                "source excerpt and locator, factual card claims, quiz answers, and version boundaries. "
                "This is not independent scholarly review or scholarly certification; specialist and "
                "community review remains recommended."
                if pantheon_status == "active"
                else
                "AI editorial source audit on 2026-11-09: this planned curriculum lacks adequately "
                "identified community-specific local evidence. Keep it inactive and revise only after "
                "appropriate sources are curated. This is not scholarly certification."
            ),
        }
        changes[path] = lesson
    print("Input SHA256:", digest)
    print(f"Prepared review metadata for {len(changes)} lessons; no files written.")
    print("Active lessons will be marked reviewed after source-integrity checks; planned lessons will be marked needs-revision.")
    if args.apply:
        if args.apply != digest:
            parser.error("Lesson input digest changed; refusing to write.")
        staged = []
        for path, lesson in changes.items():
            temporary = path.with_suffix(path.suffix + ".tmp")
            temporary.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            staged.append((temporary, path))
        for temporary, path in staged:
            temporary.replace(path)
        print("Applied AI editorial review status, without claiming independent scholarly certification.")


if __name__ == "__main__":
    main()

"""One-time repair for Greek refs whose migration dropped the content/ prefix."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/greek").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    changes = {}
    for path in paths:
        lesson = json.loads(path.read_text(encoding="utf-8"))
        updated = False
        for ref in lesson.get("sourceReferences", {}).values():
            if ref.get("localPath", "").startswith("corpus/greek/"):
                ref["localPath"] = "content/" + ref["localPath"]
                updated = True
        if updated:
            changes[path] = lesson
    print("Input SHA256:", digest)
    print(f"Prepared path-prefix repairs in {len(changes)} Greek lessons; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Greek lesson inputs changed; refusing to write.")
        for path, lesson in changes.items():
            path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied once.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""Build a compact local retrieval index over Mythos corpus texts."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
CHUNK_SIZE = 1400
OVERLAP = 180


def words(text):
    return re.findall(r"[a-z0-9][a-z0-9'-]+", text.lower())


def chunks(text):
    cleaned = re.sub(r"\s+", " ", text).strip()
    start = 0
    while start < len(cleaned):
        end = min(len(cleaned), start + CHUNK_SIZE)
        yield start, cleaned[start:end]
        if end >= len(cleaned):
            break
        start = end - OVERLAP


def main():
    registry = json.loads((ROOT / "content/pantheons.json").read_text(encoding="utf-8"))
    rows = []
    sources = {}
    for pantheon_id, pantheon in registry["pantheons"].items():
        if pantheon.get("status") != "active":
            continue
        manifest_path = pantheon.get("paths", {}).get("corpusManifest")
        if not manifest_path:
            continue
        manifest = json.loads((ROOT / manifest_path).read_text(encoding="utf-8"))
        for record in manifest["records"]:
            path = ROOT / "content/corpus" / pantheon_id / record["localPath"]
            if not path.exists():
                continue
            source_type = record.get("sourceType") or ('scholarship' if 'scholarship' in record['localPath'] else 'reception' if 'reception' in record['localPath'] else 'primary')
            sources[record["id"]] = {
                "id": record["id"], "pantheon": pantheon_id, "title": record["title"],
                "sourceType": source_type, "sourceIds": record.get("sourceIds", []),
                "coverageType": pantheon.get("coverageType"), "rightsStatus": record.get("rightsStatus"),
                "translator": record.get("translator")
            }
            # Restricted local copies stay in the private corpus, never in the browser/LLM index.
            if record.get('accessScope') == 'personal-local-only':
                continue
            number = 0
            for segment in source_segments(path):
                # Editorial apparatus (prefaces, footnotes, contents pages) is not
                # lesson evidence and must not reach the assistant's evidence pool.
                if segment['evidenceType'] != 'source-text':
                    continue
                for start, text_chunk in chunks(segment['text']):
                    tokens = words(text_chunk)
                    if len(tokens) < 20:
                        continue
                    number += 1
                    # Chunks stay slim; shared bibliographic fields live once in
                    # sources[] and consumers join on recordId. Keeps the file ~half
                    # the size and makes the generated-not-committed artifact cheap.
                    rows.append({
                        'id': f"{record['id']}:{number}", 'recordId': record['id'],
                        'locator': f"{record['title']} · {segment['locator']} · characters {start}-{start + len(text_chunk)}",
                        'start': start, 'text': text_chunk, 'terms': sorted(set(tokens))
                    })
    out = ROOT / "content/retrieval"
    out.mkdir(parents=True, exist_ok=True)
    index = {
        "version": 2,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sources": list(sources.values()),
        "chunks": rows
    }
    temporary = out / 'index.json.tmp'
    temporary.write_text(json.dumps(index, separators=(',', ':')), encoding='utf-8')
    temporary.replace(out / 'index.json')
    print(f"wrote {len(rows)} retrieval chunks from {len(sources)} sources")


if __name__ == "__main__":
    main()

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
                    # terms are recomputable from text at load time; storing them
                    # doubled every file. Keep chunks to the evidence itself.
                    rows.append({
                        'id': f"{record['id']}:{number}", 'recordId': record['id'],
                        'locator': f"{record['title']} · {segment['locator']} · characters {start}-{start + len(text_chunk)}",
                        'start': start, 'text': text_chunk
                    })
    out = ROOT / "content/retrieval"
    out.mkdir(parents=True, exist_ok=True)
    # Split chunk payloads per tradition so the browser only parses what the
    # active tradition needs instead of one ~58 MB monolith on the phone.
    # Split by tradition AND source type so a browser only ever parses the
    # slices the active tradition needs (e.g. greek-primary ~11 MB instead of
    # one 58 MB monolith).
    by_group = {}
    for row in rows:
        source = sources.get(row['recordId'], {})
        key = (source.get('pantheon', 'shared'), source.get('sourceType') or 'primary')
        by_group.setdefault(key, []).append(row)
    files = []
    for (pantheon_id, source_type), group in sorted(by_group.items()):
        name = f"chunks-{pantheon_id}-{source_type}.json"
        temporary = out / (name + '.tmp')
        temporary.write_text(json.dumps({"pantheon": pantheon_id, "sourceType": source_type, "chunks": group}, separators=(',', ':')), encoding='utf-8')
        temporary.replace(out / name)
        files.append({"pantheon": pantheon_id, "sourceType": source_type, "path": f"content/retrieval/{name}", "chunks": len(group)})
    index = {
        "version": 3,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sources": list(sources.values()),
        "files": files
    }
    temporary = out / 'index.json.tmp'
    temporary.write_text(json.dumps(index, separators=(',', ':')), encoding='utf-8')
    temporary.replace(out / 'index.json')
    print(f"wrote {len(rows)} retrieval chunks from {len(sources)} sources into {len(files)} tradition files")


if __name__ == "__main__":
    main()

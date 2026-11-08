#!/usr/bin/env python
"""Normalize and locally store rights-cleared artwork records for Mythos."""
import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "content/art/catalog.json"


def fetch_json(url):
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def download(url, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    with urllib.request.urlopen(url, timeout=60) as response:
        path.write_bytes(response.read())


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def normalize_met(object_id, subjects, entities, usage, source_ids, output_dir):
    api_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    item = fetch_json(api_url)
    if not item.get("isPublicDomain") or not item.get("primaryImage"):
        raise ValueError(f"Met object {object_id} is not a rights-cleared image candidate")
    title = item.get("title") or f"Met object {object_id}"
    filename = f"met-{object_id}-{slug(title)}.jpg"
    local_path = ROOT / output_dir / filename
    download(item["primaryImage"], local_path)
    return {
        "id": f"art.met.{object_id}",
        "provider": "met",
        "title": title,
        "creator": item.get("artistDisplayName") or "Unknown",
        "date": item.get("objectDate") or "Undated",
        "culture": item.get("culture") or item.get("period") or "Uncategorized",
        "medium": item.get("medium"),
        "collection": "The Metropolitan Museum of Art",
        "objectNumber": item.get("accessionNumber") or str(object_id),
        "sourceUrl": item.get("objectURL") or f"https://www.metmuseum.org/art/collection/search/{object_id}",
        "apiUrl": api_url,
        "localPath": str(local_path.relative_to(ROOT)).replace("\\", "/"),
        "remoteImageUrl": item["primaryImage"],
        "license": "Public domain / The Met Open Access CC0",
        "licenseUrl": "https://www.metmuseum.org/policies/image-resources",
        "attribution": f"{item.get('artistDisplayName') or 'Unknown'}, {title}, {item.get('objectDate') or 'Undated'}. The Metropolitan Museum of Art.",
        "alt": item.get("title") or "Public-domain artwork from The Met Open Access collection.",
        "usage": usage,
        "subjects": subjects,
        "entities": entities,
        "sourceIds": source_ids,
        "verifiedAt": datetime.now(timezone.utc).date().isoformat()
    }


def normalize_aic(object_id, subjects, entities, usage, source_ids, output_dir):
    api_url = f"https://api.artic.edu/api/v1/artworks/{object_id}?fields=id,title,artist_display,date_display,image_id,thumbnail,department_title,medium_display,main_reference_number,is_public_domain"
    item = fetch_json(api_url)["data"]
    if not item.get("is_public_domain") or not item.get("image_id"):
        raise ValueError(f"AIC object {object_id} is not a rights-cleared image candidate")
    image_url = f"https://www.artic.edu/iiif/2/{item['image_id']}/full/843,/0/default.jpg"
    title = item.get("title") or f"AIC object {object_id}"
    filename = f"aic-{object_id}-{slug(title)}.jpg"
    local_path = ROOT / output_dir / filename
    download(image_url, local_path)
    return {
        "id": f"art.aic.{object_id}",
        "provider": "aic",
        "title": title,
        "creator": item.get("artist_display") or "Unknown",
        "date": item.get("date_display") or "Undated",
        "culture": item.get("department_title") or "Uncategorized",
        "medium": item.get("medium_display"),
        "collection": "Art Institute of Chicago",
        "objectNumber": str(item.get("main_reference_number") or object_id),
        "sourceUrl": f"https://www.artic.edu/artworks/{object_id}",
        "apiUrl": api_url,
        "localPath": str(local_path.relative_to(ROOT)).replace("\\", "/"),
        "remoteImageUrl": image_url,
        "license": "CC0 / Art Institute of Chicago Open Access",
        "licenseUrl": "https://api.artic.edu/docs/",
        "attribution": f"{item.get('artist_display') or 'Unknown'}, {title}, {item.get('date_display') or 'Undated'}. Art Institute of Chicago.",
        "alt": item.get("thumbnail", {}).get("alt_text") or title,
        "usage": usage,
        "subjects": subjects,
        "entities": entities,
        "sourceIds": source_ids,
        "verifiedAt": datetime.now(timezone.utc).date().isoformat()
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=["met", "aic"], required=True)
    parser.add_argument("--object-id", required=True)
    parser.add_argument("--subjects", required=True, help="Comma-separated topic tags")
    parser.add_argument("--entities", default="", help="Comma-separated named figures")
    parser.add_argument("--usage", default="reward", help="Comma-separated roles: reward,evidence,flavor,thumbnail")
    parser.add_argument("--source-ids", default="", help="Comma-separated source IDs")
    parser.add_argument("--output-dir", default="content/art/provider", help="Relative local art directory")
    args = parser.parse_args()

    subjects = [item.strip() for item in args.subjects.split(",") if item.strip()]
    entities = [item.strip() for item in args.entities.split(",") if item.strip()]
    usage = [item.strip() for item in args.usage.split(",") if item.strip()]
    source_ids = [item.strip() for item in args.source_ids.split(",") if item.strip()]
    normalizer = {"met": normalize_met, "aic": normalize_aic}[args.provider]
    record = normalizer(args.object_id, subjects, entities, usage, source_ids, args.output_dir)

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    catalog["records"] = [item for item in catalog["records"] if item["id"] != record["id"]]
    catalog["records"].append(record)
    catalog["records"].sort(key=lambda item: item["id"])
    CATALOG.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Upserted {record['id']} -> {record['localPath']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

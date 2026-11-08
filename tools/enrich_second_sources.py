# Archived scaffolder: its unconditional writes would destroy later editorial work.
raise SystemExit('Retired generator: edit canonical JSON or implement a reviewed staging-only generator.')

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCES = {
    "norse": {
        "id": "pg-73533", "title": "The Poetic Edda", "sourceType": "primary-text-translation",
        "ancientAuthors": ["Anonymous Old Norse poets"], "translator": "Henry Adams Bellows",
        "sourceIds": ["nor.poetic-edda"], "sourceUrl": "https://www.gutenberg.org/ebooks/73533",
        "localPath": "primary/poetic-edda-bellows-73533.txt",
        "rightsStatus": "Project Gutenberg public-domain edition; preserve attribution and review UK reuse before redistribution.",
        "notes": "Mythological and heroic lays in English translation; complements the Prose Edda by preserving poetic versions and variant emphases."},
    "egyptian": {
        "id": "pg-15932", "title": "The Literature of the Ancient Egyptians", "sourceType": "translated-anthology",
        "ancientAuthors": ["various Egyptian authors"], "translator": "E. A. Wallis Budge",
        "sourceIds": ["egy.literature-ancient-egyptians"], "sourceUrl": "https://www.gutenberg.org/ebooks/15932",
        "localPath": "primary/literature-ancient-egyptians-budge-15932.txt",
        "rightsStatus": "Project Gutenberg public-domain edition; preserve attribution and review UK reuse before redistribution.",
        "notes": "Broad translated anthology including Pyramid Texts, funerary material, magical stories, hymns, and moral writing."},
    "celtic": {
        "id": "pg-16464", "title": "The Ancient Irish Epic Tale Táin Bó Cúalnge", "sourceType": "primary-text-translation",
        "ancientAuthors": ["Anonymous Irish traditions"], "translator": "Joseph Dunn",
        "sourceIds": ["cel.tain-bo-cualnge"], "sourceUrl": "https://www.gutenberg.org/ebooks/16464",
        "localPath": "primary/tain-bo-cualnge-dunn-16464.txt",
        "rightsStatus": "Project Gutenberg public-domain edition; preserve attribution and review UK reuse before redistribution.",
        "notes": "Irish epic material centered on the cattle raid and Cú Chulainn; complements the Welsh Mabinogion rather than treating Celtic myth as one canon."},
    "slavic": {
        "id": "pg-48761", "title": "Sixty Folk-Tales from Exclusively Slavonic Sources", "sourceType": "folklore-collection-translation",
        "ancientAuthors": ["various collectors and storytellers"], "translator": "A. H. Wratislaw",
        "sourceIds": ["sla.folklore.sixty-slavonic-tales"], "sourceUrl": "https://www.gutenberg.org/ebooks/48761",
        "localPath": "primary/sixty-slavonic-folk-tales-48761.txt",
        "rightsStatus": "Project Gutenberg public-domain edition; preserve attribution and review UK reuse before redistribution.",
        "notes": "Additional Slavonic folk-tale corpus from multiple traditions and languages; useful for variants and comparisons."},
    "japanese": {
        "id": "pg-4018", "title": "Japanese Fairy Tales", "sourceType": "folklore-retelling-collection",
        "ancientAuthors": ["traditional tales; collected by Yei Theodora Ozaki"], "translator": "Yei Theodora Ozaki",
        "sourceIds": ["jpn.folklore.japanese-fairy-tales"], "sourceUrl": "https://www.gutenberg.org/ebooks/4018",
        "localPath": "primary/japanese-fairy-tales-ozaki-4018.txt",
        "rightsStatus": "Project Gutenberg public-domain edition; preserve attribution and review UK reuse before redistribution.",
        "notes": "Popular story collection with moral, supernatural, and heroic episodes; complements the Kojiki-derived myth retellings."},
    "roman": {
        "id": "roman-pg-26073", "title": "The Metamorphoses of Ovid, Books VIII–XV", "sourceType": "primary-text-translation",
        "ancientAuthors": ["Ovid"], "translator": "Henry T. Riley",
        "sourceIds": ["rom.ovid.metamorphoses-8-15"], "sourceUrl": "https://www.gutenberg.org/ebooks/26073",
        "localPath": "primary/ovid-metamorphoses-books-8-15-26073.txt",
        "rightsStatus": "Project Gutenberg public-domain edition; preserve attribution and review UK reuse before redistribution.",
        "notes": "Completes the local Ovid scaffold and deepens Roman reception across the second half of the Metamorphoses."}
}

SOURCE_NOTES = {
    "norse": "Use the Poetic Edda alongside the Prose Edda to compare poetic and prose forms rather than assuming one uniform Norse canon.",
    "egyptian": "Use the anthology alongside Legends of the Gods to connect divine stories with funerary, magical, hymnic, and moral literature.",
    "celtic": "Use the Táin alongside the Mabinogion to compare Irish epic and Welsh medieval traditions without flattening them into one Celtic canon.",
    "slavic": "Use the second folk-tale collection to compare variants across Slavonic sources and avoid treating folklore as fixed scripture.",
    "japanese": "Use Ozaki’s tales alongside Rinder’s retelling to distinguish myth-period traditions from popular folklore and literary retelling.",
    "roman": "Use Books VIII–XV alongside Books I–VII to deepen Ovid’s Roman reception and transformation themes."
}

for pantheon, record in SOURCES.items():
    manifest_path = ROOT / f"content/corpus/{pantheon}/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not any(item["id"] == record["id"] for item in manifest["records"]):
        manifest["records"].append(record)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    map_path = ROOT / f"content/curriculum/{pantheon}/learning-map.json"
    learning_map = json.loads(map_path.read_text(encoding="utf-8"))
    for topic in learning_map["topics"].values():
        if record["id"] not in topic["recordIds"]:
            topic["recordIds"].append(record["id"])
        for card in topic.get("cards", []):
            if record["id"] not in card["recordIds"]:
                card["recordIds"].append(record["id"])
    map_path.write_text(json.dumps(learning_map, indent=2) + "\n", encoding="utf-8")

    for lesson_path in (ROOT / "content/lessons" / pantheon).rglob("*.json"):
        lesson = json.loads(lesson_path.read_text(encoding="utf-8"))
        if "ref-secondary" not in lesson["sourceReferences"]:
            lesson["sourceReferences"]["ref-secondary"] = {
                "recordId": record["id"], "sourceId": record["sourceIds"][0], "work": record["title"],
                "author": ", ".join(record["ancientAuthors"]), "translator": record["translator"],
                "locator": "Secondary enrichment source", "localPath": f"content/corpus/{pantheon}/{record['localPath']}",
                "excerpt": record["notes"], "note": SOURCE_NOTES[pantheon]
            }
        for card in lesson["narrativeBlocks"]:
            if "ref-secondary" not in card["sourceRefIds"]:
                card["sourceRefIds"].append("ref-secondary")
        for question in lesson["quiz"]:
            if "ref-secondary" not in question["sourceRefIds"]:
                question["sourceRefIds"].append("ref-secondary")
            if question.get("deepDive") and "ref-secondary" not in question["deepDive"]["sourceRefIds"]:
                question["deepDive"]["sourceRefIds"].append("ref-secondary")
        lesson_path.write_text(json.dumps(lesson, indent=2) + "\n", encoding="utf-8")
    print(f"{pantheon}: added {record['id']} and enriched lessons/topics")

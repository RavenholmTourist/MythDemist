"""One-time, digest-guarded revision for Westervelt's Maui and Hina selections."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
MAUI = "content/corpus/polynesian/primary/legends-ma-ui-westervelt-32601.txt"

PACK = [
    {
        "slug": "maui-trickster",
        "title": "Maui's Family Across Island Accounts",
        "subtitle": "Names and kinship vary across the collected versions",
        "refs": [
            ("family", "Chapter I · MAUI'S HOME", "In the Hawaiian chant, Akalana was the name of his father.", "Elsewhere Ina, or Hina, was the grandmother, from whom he secured fire."),
        ],
        "cards": [
            ("context", "One hero, different genealogies", "Westervelt's collection notes that accounts vary: in the Hawaiian chant Akalana is Maui's father, while other versions give the name to his mother or connect Hina with his grandmother.", ["family"], "concept"),
            ("source", "Kinship depends on the island version", None, ["family"], "concept"),
            ("context", "The compiler compares traditions", "Westervelt's 1910s volume brings together material identified with Hawaii, New Zealand, Hervey, Tahiti, and other islands. The compiler's comparison is not one single Polynesian canon.", ["family"], "source"),
            ("method", "A modern compilation", "W. D. Westervelt wrote in English and collated island accounts and chants. This source is not a direct translation of one ancient manuscript or one unmediated oral performance.", ["family"], "source"),
            ("synthesis", "Keep the variant label", "When retelling Maui's family story, name the Hawaiian chant or the other island account rather than merging their genealogies.", ["family"], "concept"),
        ],
        "questions": [
            ("What does the Hawaiian chant name as Maui's father's name?", "Akalana", ["Kullervo", "Vukub-Cakix"], "Westervelt says the Hawaiian chant gives Akalana as Maui's father.", ["family"], "concept"),
            ("What does Westervelt say varies among the island accounts?", "Whether a name such as Akalana or Hina refers to the father, mother, or grandmother", ["Whether the Sampo makes flour or salt", "Whether Xibalba has six or seven houses"], "The passage explicitly contrasts the Hawaiian genealogy with other island versions.", ["family"], "source"),
        ],
    },
    {
        "slug": "fishing-islands",
        "title": "Hawaiian Maui and the Fishing Hook",
        "subtitle": "A chant of Kualii describes land drawn from the sea",
        "refs": [
            ("chant", "Chapter II · MAUI THE FISHERMAN", "Oh the great fish hook of Maui!", "The Ulua of the deep muddy places."),
        ],
        "cards": [
            ("context", "A hook with a name", "Westervelt prints a chant attributed to Kualii, about 1700, in which Maui's hook is named Manai-i-ka-lani, 'Made fast to the heavens.'", ["chant"], "concept"),
            ("source", "The land rises", None, ["chant"], "concept"),
            ("context", "A Hawaiian setting", "The chant names Kauiki, Hawaii, and Hina. Westervelt's surrounding account locates one version near Kauiki in the Hawaiian Islands.", ["chant"], "source"),
            ("method", "Attribute the chant as printed", "The quotation is Westervelt's English presentation of a chant he attributes to Kualii. Its date and wording are transmitted through his compilation and should not be treated as an independently verified original.", ["chant"], "source"),
            ("synthesis", "A named island version", "The episode gives one Hawaiian account of Maui fishing up land; other islands preserve related but not identical Maui stories.", ["chant"], "concept"),
        ],
        "questions": [
            ("What does the chant say Maui's hook catches?", "Land beneath the water, which floats to the surface", ["The Sun's legs", "A golden bride from a furnace"], "The chant says the hook catches land under the water and floats it up.", ["chant"], "concept"),
            ("Which chant does Westervelt identify in this section?", "A chant of Kualii, about A.D. 1700", ["A K'iche' chant from the Popol Vuh", "A Jamaican recording by Martha Beckwith"], "Westervelt attributes the quoted chant to Kualii and gives an approximate date.", ["chant"], "source"),
        ],
    },
    {
        "slug": "snaring-sun",
        "title": "Maui: The Sun-Snaring Variant",
        "subtitle": "A shared motif and a Hawaiian telling",
        "refs": [
            ("range", "Chapter IV · MAUI SNARING THE SUN.", "A very unique legend is found among the widely-scattered Polynesians.", "They say that the snare was cast by a child of the sun itself."),
            ("hawaii", "Chapter IV · MAUI SNARING THE SUN.", "The Hawaiian legend says Maui was taunted", "the sun quickly promised to be more thoughtful of the needs of men and go at a more reasonable pace across the sky."),
        ],
        "cards": [
            ("context", "A motif told in more than one place", "Westervelt reports a sun-snaring story among Maori, Hervey and Society Island, and Hawaiian accounts; he says a Samoan version names a child of the Sun instead of Maui.", ["range"], "concept"),
            ("source", "The Hawaiian version", None, ["hawaii"], "concept"),
            ("context", "A challenge and a changed pace", "In the Hawaiian version, Maui's mother sends him to his grandmother, who helps him prepare a snare. He captures the Sun, and the story gives a reason for its slower course.", ["hawaii"], "concept"),
            ("method", "Do not collapse versions", "The source explicitly contrasts island versions and even notes differences in who catches the Sun. These are not interchangeable transcripts of one pan-Polynesian story.", ["range", "hawaii"], "source"),
            ("synthesis", "Compare only what the source supports", "Westervelt's compilation supports a comparison of related motifs; each version still needs its own island label and source history.", ["range", "hawaii"], "source"),
        ],
        "questions": [
            ("Which island version names a child of the Sun as the snarer?", "The Samoan version described by Westervelt", ["The Hawaiian version", "The New Zealand version of Hina and the Moon"], "Westervelt says Samoans tell a similar story but name a child of the Sun rather than Maui.", ["range"], "concept"),
            ("What does Maui's Hawaiian snare do to the Sun in this account?", "It catches him, after which he promises to move more slowly", ["It turns him into the Moon", "It carries him to the underworld"], "The passage says the Sun promises a more reasonable pace after Maui catches him.", ["hawaii"], "source"),
        ],
    },
    {
        "slug": "finding-fire",
        "title": "Hawaiian Maui: Finding Fire",
        "subtitle": "A Maui and Hina story set near Kaupo",
        "refs": [
            ("place", "Chapter V · MAUI FINDING FIRE.", "The Hawaiian story of fire finding is one of the least marvelous", "This was at Kaupo on the island of Maui."),
            ("fire", "Chapter V · MAUI FINDING FIRE.", "The bird told the demi-god to rub the stalks of water plants together.", "the Hawaiians have had the secret of fire making."),
        ],
        "cards": [
            ("context", "A fire on the mountain", "In the Hawaiian story presented by Westervelt, Maui sees a fire while fishing with his brothers near Kaupo on Maui and leaves to discover who kindled it.", ["place"], "concept"),
            ("source", "The mud-hen's secret", None, ["fire"], "concept"),
            ("context", "Repeated attempts", "Maui tests different plants and woods after the mud-hen reveals that fire is hidden in a green stick. The account links the legend to rubbing wood to make fire.", ["fire"], "concept"),
            ("method", "This is one Hawaiian version", "Westervelt distinguishes the Hawaiian story from other versions in which Hina may be a grandmother or the fire-giver's role differs. Do not treat the compilation as a uniform Polynesian practice.", ["place", "fire"], "source"),
            ("synthesis", "A practical art in narrative form", "The episode explains fire-making through Maui's struggle with the mud-hen, in a story Westervelt specifically labels Hawaiian.", ["fire"], "source"),
        ],
        "questions": [
            ("Where does Westervelt locate this Hawaiian Maui story?", "Near Kaupo on the island of Maui", ["In Xibalba", "At the foot of Mount Coatepec"], "The passage says the fishing trip was at Kaupo on the island of Maui.", ["place"], "concept"),
            ("What does the mud-hen finally tell Maui about fire?", "It is hidden in a green stick", ["It comes from a Sampo", "It is inside a pill of immortality"], "The bird says it has hidden fire in a green stick.", ["fire"], "source"),
        ],
    },
    {
        "slug": "pele-volcano",
        "title": "Hina: A Hawaiian Ascent to the Moon",
        "subtitle": "One Hawaiian version among several island accounts",
        "refs": [
            ("hawaiian", "Chapter XV · HINA, THE WOMAN IN THE MOON.", "The Sun was very bright and Hina said", "found her abiding home."),
            ("variant", "Chapter XV · HINA, THE WOMAN IN THE MOON.", "The New Zealand legend says that the woman", "they can all be traced when the nights are clear."),
        ],
        "cards": [
            ("context", "Hina seeks a place in the sky", "In one Hawaiian account summarized by Westervelt, Hina tries the Sun, finds the heat unbearable, and then climbs toward the Moon.", ["hawaiian"], "concept"),
            ("source", "The Hawaiian ascent", None, ["hawaiian"], "concept"),
            ("context", "A different New Zealand account", "Westervelt separately describes a New Zealand woman who spills water, curses the Moon, and is carried into the sky with a tree and calabash.", ["variant"], "concept"),
            ("method", "Keep Hina's island versions distinct", "The chapter notes that stories about Hina's ascent vary across Hawaiian, New Zealand, Tongan, Hervey, Nauru, and other island traditions. This lesson does not merge them into one account.", ["hawaiian", "variant"], "source"),
            ("synthesis", "The compiler records variation", "The two passages show different motives and outcomes; the useful comparison depends on retaining their regional labels.", ["hawaiian", "variant"], "source"),
        ],
        "questions": [
            ("Why does Hina leave the Sun in the Hawaiian version?", "Its heat is too great", ["The Moon orders her away", "She loses a ballgame to Xibalba"], "The passage says the Sun's heat weakens and torments her, so she returns to earth before trying the Moon.", ["hawaiian"], "concept"),
            ("What accompanies the woman in the New Zealand version described here?", "A tree and a calabash", ["A golden Sampo and an iron rod", "A canoe and a fire-stick"], "The New Zealand account says she is pulled up with the tree and calabash.", ["variant"], "source"),
        ],
    },
]


def make_reference(record, spec):
    ref_id, segment_locator, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / "content/corpus/polynesian" / record["localPath"])
         if item["locator"] == segment_locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named Westervelt chapter not found: {segment_locator}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {segment_locator}")
    end += len(end_anchor)
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": "W. D. Westervelt",
        "translator": "not applicable; authored in English",
        "locator": f"{segment_locator}; {segment_locator}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/polynesian/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim prose from Westervelt's early twentieth-century English compilation. Retain the named island/version; this is not a direct transcription of one oral performance.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/polynesian/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == "pg-32601")
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/polynesian").rglob("*.json")
    }
    changes = {}
    for spec in PACK:
        path = paths[spec["slug"]]
        lesson = json.loads(path.read_text(encoding="utf-8"))
        lesson["version"] = 2
        lesson["title"] = spec["title"]
        lesson["subtitle"] = spec["subtitle"]
        lesson["estimatedMinutes"] = 3
        lesson["difficulty"] = 2
        concept_id = lesson["learningObjectives"][0]["id"]
        source_id = lesson["learningObjectives"][-1]["id"]
        lesson["learningObjectives"] = [
            {"id": concept_id, "text": spec["questions"][0][0]},
            {"id": source_id, "text": spec["questions"][1][0]},
        ]
        lesson["sourceReferences"] = {item[0]: make_reference(record, item) for item in spec["refs"]}
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, refs, objective) in enumerate(spec["cards"], 1):
            if body is None:
                body = "Quotation from Westervelt's English compilation (whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
            lesson["narrativeBlocks"].append({
                "id": f"card-{index:02d}", "kind": kind, "title": title, "body": body,
                "sourceRefIds": refs,
                "objectiveIds": [concept_id if objective == "concept" else source_id],
            })
        lesson["quiz"] = []
        for index, (prompt, correct, wrong, explanation, refs, objective) in enumerate(spec["questions"]):
            choices = [correct, *wrong]
            shift = (index + len(changes)) % 3
            choices = choices[shift:] + choices[:shift]
            choice_objects = [{"id": chr(97 + i), "text": text} for i, text in enumerate(choices)]
            lesson["quiz"].append({
                "id": f"q{index + 1}", "type": "single-choice", "prompt": prompt,
                "choices": choice_objects,
                "answerId": next(choice["id"] for choice in choice_objects if choice["text"] == correct),
                "explanation": explanation, "sourceRefIds": refs,
                "objectiveIds": [concept_id if objective == "concept" else source_id],
                "deepDive": {
                    "prompt": "Read the island-labeled chapter in Westervelt's compilation.",
                    "suggestedQuestions": ["Which words support this answer?", "Which island version is being described?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Island-specific Westervelt passages; independent community, source-history, translation, and pedagogy review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/polynesian").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Polynesian starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} island-specific Maui and Hina lessons; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        staged = []
        for path, lesson in changes.items():
            temporary = path.with_suffix(path.suffix + ".tmp")
            temporary.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            staged.append((temporary, path))
        for temporary, path in staged:
            temporary.replace(path)
        print("Applied once; future generated writes are disabled.")


if __name__ == "__main__":
    main()

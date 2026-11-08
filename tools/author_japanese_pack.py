"""One-time, digest-guarded source revision for the Japanese starter lessons."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
RINDER = "pg-46863"
OZAKI = "pg-4018"

PACK = [
    {
        "slug": "creation",
        "title": "Izanagi and Izanami",
        "subtitle": "A creation retelling and its source frame",
        "refs": [
            ("main", RINDER, "The creation episode in Old-World Japan", "Now Izanagi and Izanami wandered on the Floating Bridge of Heaven.", "Thereupon the Earth-Makers descended"),
        ],
        "scene": "Rinder's retelling opens with Izanagi and Izanami above an unformed world. Izanagi stirs the waters with a jeweled spear; drops from its point congeal as the island of Onogoro.",
        "quoteCard": "The spear stirs the unformed world",
        "why": "The source gives a literary creation scene, not a direct quotation from an ancient Japanese chronicle. Name Rinder's retelling when describing its details.",
        "method": "This local record is a modern English compilation by Frank Rinder, not a direct Kojiki translation. Use it for the story as retold in this book; seek the Kojiki text for claims about its wording.",
        "carry": "Track the sequence: divine pair, jeweled spear, drops, island. Do not turn this one retelling into the whole of Japanese creation tradition.",
        "questions": [
            ("What forms Onogoro in Rinder's retelling?", "Drops falling from Izanagi's jeweled spear", ["A mirror thrown by Amaterasu", "A box carried home by Urashima"], "The passage says the drops from the spear congeal into Onogoro.", ["main"], "concept"),
            ("What kind of source is Old-World Japan?", "A modern compilation and retelling", ["A direct English translation of the Kojiki", "A contemporary witness to the creation story"], "The local record is Rinder's early-modern English-language retelling, not a translation presented as the Kojiki itself.", ["main"], "source"),
        ],
    },
    {
        "slug": "amaterasu-light",
        "title": "Amaterasu: Light and Withdrawal",
        "subtitle": "An offense, a cave, and a staged return",
        "refs": [
            ("offense", RINDER, "Old-World Japan, Susa-no-o's actions before Amaterasu withdraws", "Susa-no-o, the brother of Ama-terasu, who had resigned his ocean sceptre", "Ama-terasu, trembling at the horrible sight"),
            ("cave", RINDER, "Old-World Japan, the Heavenly Rock Dwelling", "Ama-terasu, trembling at the horrible sight", "The universe was plunged in darkness."),
            ("festival", RINDER, "Old-World Japan, Uzume's dance and Amaterasu's return", "The great festival began.", "Darkness fled from the Central Land of Reed-Plains, and there was light."),
        ],
        "scene": "Rinder's retelling says Susa-no-o's destructive behavior culminates in a flayed colt frightening Amaterasu while she weaves. She withdraws into the Heavenly Rock Dwelling, and the world grows dark.",
        "quoteCard": "The retreat darkens the world",
        "why": "The account links an offense in the heavenly household to darkness beyond it. It then describes the gods using music, dance, and a mirror to draw Amaterasu out.",
        "method": "Keep the sequence attached to Rinder's modern retelling. Do not claim that every Japanese version gives the same details or the same ritual practice.",
        "carry": "Notice how the cave episode makes light depend on a social response by the assembled deities, not on force alone.",
        "questions": [
            ("What immediately precedes Amaterasu's withdrawal in this retelling?", "Susa-no-o's violent act in the weaving hall", ["Urashima opening a forbidden box", "Izanagi plunging the spear into the sea"], "Rinder says the sight of the flayed colt shocks Amaterasu, who retreats into the cave.", ["offense"], "concept"),
            ("How do the assembled gods draw Amaterasu out?", "They hold a noisy festival, and she looks toward the mirror", ["They break down the cave by force", "They ask Urashima to carry a message"], "The passage describes Uzume's dance and a mirror whose reflection catches Amaterasu's attention.", ["festival"], "source"),
        ],
    },
    {
        "slug": "susanoo-storm",
        "title": "Susanoo: Disruption and Consequence",
        "subtitle": "A disruptive brother and the cave episode",
        "refs": [
            ("disruption", RINDER, "Old-World Japan, Susanoo's destructive conduct", "Susa-no-o, the brother of Ama-terasu, who had resigned his ocean sceptre", "Ama-terasu, trembling at the horrible sight"),
            ("withdrawal", RINDER, "Old-World Japan, Amaterasu withdraws", "Ama-terasu, trembling at the horrible sight", "The universe was plunged in darkness."),
        ],
        "scene": "In Rinder's retelling, Susanoo's actions damage the fields and culminate in violence at Amaterasu's weaving hall. She withdraws into the cave, and darkness spreads.",
        "quoteCard": "Susanoo's conduct has consequences",
        "why": "This passage makes a family conflict matter beyond the family: Amaterasu's withdrawal changes the world's light. Keep it distinct from other Susanoo episodes and later retellings.",
        "method": "The citation is Rinder's modern compilation of Japanese mythic traditions. It supports claims about this retelling, not every account of Susanoo or all Japanese religious practice.",
        "carry": "Follow the consequence chain from the damaged fields to the weaving-hall offense and Amaterasu's withdrawal.",
        "questions": [
            ("What happens to the fields as Susanoo weeps in this retelling?", "The grass withers, flowers are blighted, and crops are damaged", ["They become a sea of rice overnight", "They turn into a palace for Amaterasu"], "Rinder describes the grass withering, flowers blighting, and rice crops being destroyed.", ["disruption"], "concept"),
            ("What wider consequence follows Amaterasu's withdrawal?", "The world is plunged into darkness", ["The Dragon King's palace sinks into the sea", "The island of Onogoro disappears"], "The cited passage says darkness spreads after she closes the cave.", ["withdrawal"], "source"),
        ],
    },
    {
        "slug": "kami-boundaries",
        "title": "Urashima Taro: A Return Across Time",
        "subtitle": "A folktale boundary and a forbidden box",
        "refs": [
            ("warning", OZAKI, "Urashima Taro, the box and promise", "you will never open this box", "Then bidding good-by to Otohime Sama"),
            ("return", OZAKI, "Urashima Taro returns to his village", "When Urashima heard these strange words", "“I am no spirit!"),
        ],
        "scene": "In Ozaki's literary retelling of the Urashima folktale, the fisherman returns from the Sea King's palace and finds that three hundred years have passed. Otohime had warned him not to open a box.",
        "quoteCard": "The warning about the box",
        "why": "This is a popular folktale retelling, not a primary source for the kami myths in the Kojiki. Its otherworld and time boundary belong to this story's version.",
        "method": "Keep genre and source visible: Ozaki's Japanese Fairy Tales is a collected literary retelling. Do not use Urashima as evidence for the Amaterasu myth or a universal Japanese belief about the afterlife.",
        "carry": "Track the promise, the return, and the changed time-scale before interpreting the box as a symbol.",
        "questions": [
            ("What does Otohime tell Urashima not to do?", "Open the box she gives him", ["Return to his village", "Speak to the Sea King"], "She asks him to promise never to open the box.", ["warning"], "concept"),
            ("What does Urashima learn when he returns home?", "The village accounts say he has been gone for three hundred years", ["He has returned to the same evening", "The Sea King has taken his place as fisherman"], "In Ozaki's retelling, people in the village say Urashima lived three hundred years earlier.", ["return"], "source"),
        ],
    },
    {
        "slug": "izanami-boundary",
        "title": "Izanami: Death and Separation",
        "subtitle": "A return from the underworld is refused",
        "refs": [
            ("yomi", RINDER, "Old-World Japan, Izanagi finds Izanami in the underworld", "he gazed intently into her eyes ere he could recognise her.", "All hope of our reunion is now at an end."),
        ],
        "scene": "Rinder's retelling has Izanagi find Izanami in the underworld, changed and unable to return without the ruler's sanction. He flees, distracting the guardians with grapes and bamboo; then he declares their separation eternal.",
        "quoteCard": "The failed return",
        "why": "The story sets a boundary between the living and the dead through a failed attempt at reunion. This is Rinder's retelling, not a transcript of one fixed Japanese doctrine.",
        "method": "Read the underworld episode as a narrative in a modern compilation. Keep the translator's choices, names, and story sequence attached to it.",
        "carry": "Compare this attempted return with Urashima's return: distinct stories, distinct source genres, and different consequences.",
        "questions": [
            ("Why does Izanami say she cannot return to earth?", "She has not received the underworld ruler's consent", ["Izanagi has opened Urashima's box", "The heavenly bridge has disappeared"], "The retelling says Izanami tried in vain to obtain the ruler's sanction.", ["yomi"], "concept"),
            ("How does Izanagi escape the underworld guardians?", "He throws grapes and bamboo behind him, distracting them", ["He bargains with the Dragon King", "He asks Susanoo to carry him"], "The passage says the guardians chase him while he scatters food and plants behind him.", ["yomi"], "source"),
        ],
    },
]


def make_reference(records, source):
    ref_id, record_id, locator, start_anchor, end_anchor = source
    record = records[record_id]
    local_path = f"content/corpus/japanese/{record['localPath']}"
    text = source_segments(ROOT / local_path)[0]["text"]
    start = text.find(start_anchor)
    end = text.find(end_anchor, start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {locator}")
    end += len(end_anchor)
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": f"{record['title']}: {locator}",
        "author": ", ".join(record.get("ancientAuthors", [])),
        "translator": record.get("translator", "not applicable"),
        "locator": f"{locator}; local text normalized characters {start}-{end}",
        "localPath": local_path,
        "excerpt": text[start:end].strip(),
        "evidenceType": "quotation",
        "note": "Rinder's modern retelling, not a direct Kojiki translation." if record_id == RINDER else "Ozaki's literary retelling of a traditional story, not a primary mythographic text.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/japanese/manifest.json").read_text(encoding="utf-8"))
    records = {item["id"]: item for item in manifest["records"]}
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/japanese").rglob("*.json")
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
        lesson["sourceReferences"] = {
            item[0]: make_reference(records, item) for item in spec["refs"]
        }
        ref_ids = list(lesson["sourceReferences"])
        cards = [
            ("context", "The scene", spec["scene"], [ref_ids[0]], "concept"),
            ("source", spec["quoteCard"], None, [ref_ids[0]], "concept"),
            ("synthesis", "Why it matters", spec["why"], ref_ids, "concept"),
            ("method", "Read the source boundary", spec["method"], ref_ids, "source"),
            ("flavor", "Carry it forward", spec["carry"], ref_ids, "source"),
        ]
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, refs, objective) in enumerate(cards, 1):
            if body is None:
                body = "Source quotation (local English retelling; whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
            lesson["narrativeBlocks"].append({
                "id": f"card-{index:02d}", "kind": kind, "title": title, "body": body,
                "sourceRefIds": refs,
                "objectiveIds": [concept_id if objective == "concept" else source_id],
            })
        lesson["quiz"] = []
        for index, (prompt, correct, wrong, explanation, refs, objective) in enumerate(spec["questions"]):
            options = [correct, *wrong]
            shift = (index + len(changes)) % 3
            options = options[shift:] + options[:shift]
            choices = [{"id": chr(97 + i), "text": text} for i, text in enumerate(options)]
            lesson["quiz"].append({
                "id": f"q{index + 1}", "type": "single-choice", "prompt": prompt,
                "choices": choices,
                "answerId": next(choice["id"] for choice in choices if choice["text"] == correct),
                "explanation": explanation, "sourceRefIds": refs,
                "objectiveIds": [concept_id if objective == "concept" else source_id],
                "deepDive": {
                    "prompt": "Read the cited local version.",
                    "suggestedQuestions": ["Which words support this answer?", "What does this retelling not establish?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Source-specific rewrite with verbatim local retellings. Independent source, community, and pedagogy review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/japanese").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Japanese starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} source-specific lessons; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        for path, lesson in changes.items():
            path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied once; future generated writes are disabled.")


if __name__ == "__main__":
    main()

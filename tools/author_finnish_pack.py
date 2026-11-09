"""One-time, digest-guarded passage revision for the Kalevala starter lessons."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
KALEVALA = "content/corpus/finnish/primary/kalevala-crawford-5186.txt"

PACK = [
    {
        "slug": "vainamoinen-and-song",
        "title": "Väinämöinen: Birth and Song",
        "subtitle": "A Kalevala episode in Crawford's English rendering",
        "refs": [
            ("birth", "Rune I · Birth of Wainamoinen", "Seven hundred years she labored", "Ere her first-born was delivered."),
        ],
        "cards": [
            ("context", "A birth across generations", "Rune I describes Ilmatar carrying her child for seven hundred years before Väinämöinen is delivered.", ["birth"], "concept"),
            ("source", "The long birth", None, ["birth"], "concept"),
            ("context", "A compiled epic speaks", "This is John Martin Crawford's English translation of Elias Lönnrot's nineteenth-century Kalevala, an edited compilation of Finnish and Karelian oral poetry.", ["birth"], "source"),
            ("method", "Not a single ancient manuscript", "The Kalevala is a modern national epic compiled from oral materials, not one unchanged ancient text or a record of every Finnish or Karelian performance.", ["birth"], "source"),
            ("synthesis", "Name the actual witness", "For this lesson, the witness is Rune I in Crawford's English translation of Lönnrot's compilation. Keep its edition and sequence visible.", ["birth"], "source"),
        ],
        "questions": [
            ("How long does Ilmatar labor in this Rune I passage?", "Seven hundred years", ["Seven days", "Three generations"], "The translated passage says she labored seven hundred years before her first-born was delivered.", ["birth"], "concept"),
            ("What kind of book is Crawford's Kalevala?", "An English translation of Lönnrot's nineteenth-century compilation", ["A single ancient manuscript copied unchanged", "A modern field recording of one singer"], "Lönnrot compiled and edited oral poetry; Crawford translated the resulting epic into English.", ["birth"], "source"),
        ],
    },
    {
        "slug": "the-sampo",
        "title": "The Sampo: A Threefold Mill",
        "subtitle": "Ilmarinen's forge produces an extraordinary object",
        "refs": [
            ("mill", "Rune X · Ilmarinen forges the Sampo", "On one side the flour is grinding", "Grinds a third one for the store-house."),
        ],
        "cards": [
            ("context", "A smith makes the Sampo", "In Rune X, Ilmarinen forges the Sampo for Louhi of Pohjola. The translated song describes its three outputs after the smithing.", ["mill"], "concept"),
            ("source", "What the Sampo produces", None, ["mill"], "concept"),
            ("context", "Three kinds of abundance", "The passage says the Sampo produces flour, salt, and money, with portions for eating, market, and storehouse.", ["mill"], "concept"),
            ("method", "Keep the poem's edition visible", "This scene is Crawford's English translation of Rune X in Lönnrot's compiled epic. It is not a verbatim transcript of one identifiable ancient performance.", ["mill"], "source"),
            ("synthesis", "The object's value is practical", "The Sampo's importance in this passage comes from repeated production of food, salt, and money.", ["mill"], "concept"),
        ],
        "questions": [
            ("What three things does the Sampo produce in this passage?", "Flour, salt, and money", ["Iron, fire, and water", "Gold, silver, and copper"], "The poem names flour on one side, salt on another, and money on a third.", ["mill"], "concept"),
            ("Where does this Sampo episode appear in Crawford's edition?", "Rune X", ["Rune I", "Rune XXXIII"], "The translated section is labeled Rune X, 'Ilmarinen forges the Sampo.'", ["mill"], "source"),
        ],
    },
    {
        "slug": "ilmarinen-the-smith",
        "title": "Ilmarinen: The Bride of Gold",
        "subtitle": "A crafted image is not a living partner",
        "refs": [
            ("bride", "Rune XXXVII · Ilmarinen’s Bride of Gold", "I desire a bride of beauty", "One side warm, the other lifeless"),
        ],
        "cards": [
            ("context", "A bride made in the forge", "After the death of the Maiden of the Rainbow, Ilmarinen says he wants a bride made of gold and silver and puts the metals into the furnace.", ["bride"], "concept"),
            ("source", "The crafted bride", None, ["bride"], "concept"),
            ("context", "The image lacks life", "Ilmarinen takes the golden image to bed. The poem describes him as warm beneath his furs while the side next to the metal bride grows cold.", ["bride"], "concept"),
            ("method", "Read the episode as poetic narrative", "This is a scene in Rune XXXVII of Lönnrot's compiled Kalevala, translated by Crawford. Avoid turning one episode into a universal statement about Finnish marriage or belief.", ["bride"], "source"),
            ("synthesis", "Craft cannot supply reciprocity", "The episode contrasts Ilmarinen's crafted image with a living companion; the image remains cold and lifeless in this version.", ["bride"], "concept"),
        ],
        "questions": [
            ("What does Ilmarinen put into the furnace to make the bride?", "Gold and silver", ["A tortoise shell and five-coloured stones", "Flour, salt, and money"], "The passage says he adds gold and silver and works the metals in the furnace.", ["bride"], "concept"),
            ("What happens when Ilmarinen lies beside the golden bride?", "The side beside her turns cold; she is lifeless", ["She sings and wakes him", "She becomes a living maiden"], "The poem contrasts his warm side with the cold side beside the metal bride.", ["bride"], "source"),
        ],
    },
    {
        "slug": "louhi-and-pohjola",
        "title": "Louhi: The Sun and Moon Hidden",
        "subtitle": "A night without the familiar lights",
        "refs": [
            ("hiding", "Rune XLVII · Louhi steals Sun, Moon, and Fire", "Louhi, hostess of Pohyola,", "Sable coursers of one mother!"),
        ],
        "cards": [
            ("context", "Louhi hides the luminaries", "In Rune XLVII, Louhi of Pohjola hides the Sun and Moon in a mountain cavern and says they will not shine until she frees them.", ["hiding"], "concept"),
            ("source", "The command to hide", None, ["hiding"], "concept"),
            ("context", "Northland loses its light", "The poem then describes the Sun and Moon vanishing and darkness covering Kalevala and the home of Ukko.", ["hiding"], "concept"),
            ("method", "Do not flatten the Kalevala", "Louhi's episode belongs to Crawford's translation of Lönnrot's compiled epic. Keep Pohjola, Northland, and this poem's sequence attached to the claim.", ["hiding"], "source"),
            ("synthesis", "A disruption calls for response", "The disappearance changes daily life in the poem: the houses become dark and the inhabitants seek a remedy.", ["hiding"], "concept"),
        ],
        "questions": [
            ("Where does Louhi hide the Sun and Moon?", "In the caverns of Pohjola's mountain", ["Under the sea in a tortoise shell", "Inside Ilmarinen's forge"], "Louhi orders the Sun and Moon to hide in the caverns of Pohjola's mountain.", ["hiding"], "concept"),
            ("What follows when the Sun and Moon disappear?", "Darkness rules in Kalevala and the home of Ukko", ["The Sampo begins producing fire", "Ilmarinen becomes the new Sun"], "The next lines describe darkness in Northland and in Ukko's home.", ["hiding"], "source"),
        ],
    },
    {
        "slug": "kullervo-and-consequence",
        "title": "Kullervo: The Cheat-Cake",
        "subtitle": "An insult to a knife sparks retaliation",
        "refs": [
            ("knife", "Rune XXXIII · Kullervo and the Cheat-cake", "This, the blade that I hold sacred", "What the wages for deception?"),
        ],
        "cards": [
            ("context", "A broken knife", "In Rune XXXIII, Kullervo cuts into his oat-loaf and breaks the knife he values. He discovers a stone hidden inside the cake.", ["knife"], "concept"),
            ("source", "Kullervo names the insult", None, ["knife"], "concept"),
            ("context", "Anger turns toward revenge", "Kullervo calls the loaf a cheat-cake and asks what the wages for deception should be. The next lines carry his retaliation into the herd.", ["knife"], "concept"),
            ("method", "A named rune in a compiled epic", "The episode is from Lönnrot's Kalevala as translated by Crawford, not a direct transcript of a single oral performance. Kullervo's story must stay inside this version and sequence.", ["knife"], "source"),
            ("synthesis", "A small object carries history", "Kullervo calls the knife a relic of his mother's people; the broken blade makes the meal an insult with personal and family meaning.", ["knife"], "concept"),
        ],
        "questions": [
            ("What breaks Kullervo's knife?", "A stone hidden inside the oat-loaf", ["The Sampo's lid", "A piece of iron from Louhi's mountain"], "Kullervo says his knife broke on a stone embedded in the loaf.", ["knife"], "concept"),
            ("What does Kullervo call the loaf after finding the stone?", "A cheat-cake", ["A wedding-cake", "A bread of life"], "The excerpt calls the oat-loaf a cheat-cake and asks how to repay the deception.", ["knife"], "source"),
        ],
    },
]


def make_reference(records, spec):
    ref_id, segment_locator, start_anchor, end_anchor = spec
    segment = next(
        (item for item in source_segments(ROOT / KALEVALA)
         if item["locator"] == segment_locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named Kalevala rune not found: {segment_locator}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {segment_locator}")
    end += len(end_anchor)
    record = next(item for item in records if item["id"] == "pg-5186")
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": "Elias Lönnrot, compiler and editor",
        "translator": record["translator"],
        "locator": f"{segment_locator}; {segment_locator}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/finnish/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": "Verbatim English verse translated by John Martin Crawford from Lönnrot's nineteenth-century compilation of oral poetry; not a transcript of one ancient or single oral witness.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/finnish/manifest.json").read_text(encoding="utf-8"))
    records = manifest["records"]
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/finnish").rglob("*.json")
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
        lesson["sourceReferences"] = {item[0]: make_reference(records, item) for item in spec["refs"]}
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, refs, objective) in enumerate(spec["cards"], 1):
            if body is None:
                body = "Source quotation (Crawford's English translation; whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
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
                    "prompt": "Read the named rune in Crawford's translation.",
                    "suggestedQuestions": ["Which words support this answer?", "How does Lönnrot's compiled epic frame this episode?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Passage-specific Kalevala revisions; independent review of oral source traditions, Lönnrot's compilation, translation, and pedagogy remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/finnish").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Finnish starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} rune-specific lessons; no files written.")
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

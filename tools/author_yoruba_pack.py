"""One-time, digest-guarded authoring pass for the Yoruba starter pack.

Replaces the generic needs-revision scaffolds with lessons bounded to two
Yoruba-specific local sources: Ellis's 1894 colonial-era ethnographic survey
and Ogumefu's 1929 Yoruba-authored legend collection. Preview by default;
--apply requires the exact input digest and refuses non-scaffold lessons.
"""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
RECORD_FILES = {
    "ellis": "primary/yoruba-speaking-peoples-ellis-1894.txt",
    "ogumefu": "primary/yoruba-legends-ogumefu-1929.txt",
}
AUTHOR_BY_RECORD = {
    "ellis": "A. B. Ellis",
    "ogumefu": "Yoruba storytellers; collected and published in English by M. I. Ogumefu",
}
TRANSLATOR_BY_RECORD = {
    "ellis": "not applicable; authored in English by A. B. Ellis",
    "ogumefu": "not applicable; authored in English by M. I. Ogumefu",
}
NOTE_BY_RECORD = {
    "ellis": (
        "Verbatim English text from Ellis's 1894 survey of the Yoruba-speaking peoples. "
        "It is colonial-era ethnography: claims belong to Ellis's report, and his "
        "comparative and evolutionary framing is commentary, not community testimony."
    ),
    "ogumefu": (
        "Verbatim English text from M. I. Ogumefu's 1929 collection, which his preface "
        "describes as belonging to the Yoruba country of Southern Nigeria. It is a "
        "Yoruba-authored retelling for readers, not an ethnographic record of practice."
    ),
}

PACK = [
    {
        "slug": "orishas-and-living-religion",
        "title": "Shango, the King Who Became a Storm",
        "subtitle": "A legend and an ethnographer hear the same royal cry",
        "refs": [
            ("sango", "ogumefu", "Legend VI · WHY PEOPLE CRY \u201cLONG LIVE THE KING!\u201d WHEN THUNDER FOLLOWS LIGHTNING",
             "worshipped as the god of thunder and lightning",
             "Long live the King!\u201d"),
            ("chant", "ellis", "Chapter II · CHIEF GODS",
             "A chant of the Oni-Shango very commonly heard is",
             "is a very common imprecation."),
            ("orisha", "ellis", "Chapter II · CHIEF GODS",
             "The term used by the Yoruba tribes to express a superhuman being",
             "One who sees the cult.\""),
        ],
        "cards": [
            ("context", "A king's terrible charm", "In Ogumefu's legend, King Sango finds a charm that calls down lightning. He tries it on his own palace; the storm kills his family, his followers desert him, and he ends his life in despair.", ["sango"], "concept"),
            ("source", "The people remember a king", None, ["sango"], "concept"),
            ("context", "An ethnographer hears the same cry", "Writing in 1894, Ellis reports that Shango's worshippers run into the streets during thunderstorms crying \"Shango, Shango, Great King!\" A legend explains the cry; the survey records it happening.", ["chant"], "source"),
            ("method", "Two kinds of book, one custom", "Ogumefu was a Yoruba author publishing legends in 1929; Ellis was a British colonial officer describing religion in 1894. Keep the legend's explanation and the ethnographer's report distinct, and remember Yoruba religion is still practised today.", ["sango", "chant"], "source"),
            ("synthesis", "What orisha means", "Ellis reports that the Yoruba word for a superhuman being or god is orisha, a word also used for sacred images and objects and as an adjective meaning holy. Shango is one orisha among many in his survey.", ["orisha"], "source"),
        ],
        "questions": [
            ("In Ogumefu's legend, what happens after lightning destroys Sango's palace?",
             "His friends desert him and he ends his life in despair",
             ["He marries the river goddess Oya", "He hides in a cave and becomes a soothsayer"],
             "After the palace burns, Sango's followers desert him one by one until, alone, he puts an end to his life; his people then give him an honourable funeral and worship him as god of thunder.",
             ["sango"], "concept"),
            ("What do people cry when thunder follows lightning, in both Ogumefu's legend and Ellis's report?",
             "\u201cLong live the King!\u201d",
             ["\u201cOro has spoken!\u201d", "\u201cEgungun walks tonight!\u201d"],
             "Ogumefu ends the legend with people crying \u201cLong live the King!\u201d; Ellis independently records worshippers crying \u201cShango, Shango, Great King!\u201d in storms.",
             ["sango", "chant"], "source"),
        ],
    },
    {
        "slug": "divination-and-destiny",
        "title": "Ifa and the Secret-Keeper",
        "subtitle": "Divination in Ellis's survey, beside a legend of a soothsayer",
        "refs": [
            ("ifa", "ellis", "Chapter II · CHIEF GODS",
             "Ifa, god of divination, who is usually termed the God of Palm Nuts",
             "it being considered a disgrace not to bear children."),
            ("babalawo", "ellis", "Chapter V · PRIESTS AND WORSHIP",
             "The reason of the Babalawo taking the highest place",
             "to make the gods propitious."),
            ("orisa-oko", "ogumefu", "Legend IX · ORISA OKO",
             "He earned a meagre living by trapping in his nets guinea-fowls",
             "managed to live very comfortably."),
        ],
        "cards": [
            ("context", "A god of palm nuts", "In Ellis's 1894 survey, Ifa is the god of divination, usually called the God of Palm Nuts because sixteen palm-nuts are used in the divination process.", ["ifa"], "concept"),
            ("source", "The highest priesthood", None, ["babalawo"], "source"),
            ("context", "Why the Babalawo outrank", "Ellis says the Babalawo, priests of Ifa, hold the highest place in the priesthood because through Ifa people learn what must be done to please the other gods. Other priests divine too, but without Ifa's palm-nuts and board.", ["babalawo"], "concept"),
            ("method", "A legend about a soothsayer", "Ogumefu retells how Orisa Oko, a solitary hunter, gained fame when people mistook his silence for secret knowledge. It is a story about a reputation for seeing the future, not a description of Ifa practice.", ["orisa-oko"], "source"),
            ("synthesis", "Report versus legend", "Ellis describes an institution: priests, palm-nuts, a board, ranks. Ogumefu tells a tale about one man credited with foresight. Both involve divination; they are different kinds of evidence.", ["ifa", "orisa-oko"], "source"),
        ],
        "questions": [
            ("According to Ellis, why is Ifa called the God of Palm Nuts?",
             "Because sixteen palm-nuts are used in the divination process",
             ["Because his priests are paid in palm nuts", "Because palm-nut oil is poured on his images"],
             "Ellis writes that Ifa is usually termed the God of Palm Nuts \u201cbecause sixteen palm-nuts are used in the process of divination.\u201d",
             ["ifa"], "source"),
            ("In Ogumefu's legend, why do people begin seeking Orisa Oko's advice?",
             "His solitary, silent life made people think he held secret knowledge",
             ["The king appointed him court diviner", "He trained as a Babalawo priest of Ifa"],
             "The legend says his solitary habits made people credit him with secret knowledge he did not divulge; it never mentions Ifa, the Babalawo, or palm-nut divination.",
             ["orisa-oko"], "concept"),
        ],
    },
    {
        "slug": "ancestors-and-community",
        "title": "Egungun and the Voice of Oro",
        "subtitle": "Ancestors and community in a colonial-era report",
        "refs": [
            ("egungun", "ellis", "Chapter VI · EGUNGUN, ORO, ABIKU, AND VARIOUS SUPERSTITIONS",
             "EGUNGUN really means",
             "causes death."),
            ("oro", "ellis", "Chapter VI · EGUNGUN, ORO, ABIKU, AND VARIOUS SUPERSTITIONS",
             "The word Oro means fierceness",
             "fastened to a stick by a long string."),
        ],
        "cards": [
            ("context", "A figure named for bone", "Ellis reports that Egungun means \u201cbone,\u201d hence \u201cskeleton\u201d: a performer in a long grass robe and wooden mask plays a man risen from the dead.", ["egungun"], "concept"),
            ("source", "The dead inspect the living", None, ["egungun"], "concept"),
            ("context", "Everyone knows, and still steps back", "Ellis notes it is \u201cvery well known\u201d that Egungun is only a disguised man, yet people believe even an accidental touch causes death, and crowds scatter when he rushes toward them.", ["egungun"], "concept"),
            ("method", "An outside reporter's apparatus", "Ellis openly describes the costume, the performer, and the crowd's reaction. That is an 1894 observer explaining how the figure is made, not testimony from inside the institution.", ["egungun"], "source"),
            ("synthesis", "Oro's hidden voice", "In the same chapter Ellis describes Oro as \u201cpersonified executive power.\u201d Its voice is the whirring roar of a slat of wood spun on a string, a bull-roarer, and women were required to stay indoors when it sounded. Two figures, two different relationships between the community and the unseen.", ["oro"], "source"),
        ],
        "questions": [
            ("What does Ellis say the word Egungun means?",
             "Bone, and so skeleton",
             ["Thunder-clap", "Lord of the White Cloth"],
             "Ellis glosses Egungun as \u201cbone,\u201d hence \u201cskeleton,\u201d suiting a figure \u201csupposed to be a man risen from the dead.\u201d",
             ["egungun"], "concept"),
            ("In Ellis's account, what produces the voice of Oro?",
             "A thin strip of wood whirled on a string, a bull-roarer",
             ["A drum beaten inside a cave", "The chant of the Oni-Shango priests"],
             "Ellis says Oro's whirring, roaring voice is made by whirling a tapering strip of wood on a long string, the instrument he calls a bull-roarer.",
             ["oro"], "source"),
        ],
    },
    {
        "slug": "tortoise-tales",
        "title": "Tortoise the Boaster",
        "subtitle": "Ogumefu's tortoise cycle and Ellis's name for it",
        "refs": [
            ("tortoise-crab", "ogumefu", "Legend XXXVII · TORTOISE AND CRAB",
             "EVERYONE knows that Tortoise and Crab are enemies",
             "always shun one another."),
            ("tortoise-stories", "ellis", "Chapter XIV · FOLK-LORE TALES",
             "We now come to those tales which may be called",
             "Spider Stories.\""),
            ("rascal", "ogumefu", "Preface",
             "We may weep at the death of rascally Tortoise",
             "he deserves his fate!"),
        ],
        "cards": [
            ("context", "Two suits of armour", "In Ogumefu's tale, Tortoise and Crab fight to prove which is stronger, agree their shells make them unbeatable, and boast that nothing can harm them.", ["tortoise-crab"], "concept"),
            ("source", "The pot answers the boast", None, ["tortoise-crab"], "concept"),
            ("context", "A shame that explains a habit", "A passing boy picks them both up: Tortoise is boiled and Crab is stewed. The tale ends etiologically: their ashamed descendants still shun one another.", ["tortoise-crab"], "concept"),
            ("method", "Ellis names the type", "Ellis's 1894 survey calls these \u201cTortoise Stories\u201d because the tortoise (awon, also called ajapa) always plays the leading, crafty part, and says the tortoise fills the role the spider Anansi plays in Gold Coast tales.", ["tortoise-stories"], "source"),
            ("synthesis", "The collector's verdict", "Ogumefu, a Yoruba author, calls Tortoise \u201crascally\u201d in his own preface and says readers feel he deserves his fate. The trickster is loved and judged at once, and Ellis's Anansi comparison shows the same trickster slot holding a different animal on a neighbouring coast.", ["rascal", "tortoise-stories"], "source"),
        ],
        "questions": [
            ("In Ogumefu's \u201cTortoise and Crab,\u201d what ends the two friends' boasting?",
             "A boy picks them up; Tortoise is boiled and Crab is stewed",
             ["They drown each other in the river", "The king confiscates their shells"],
             "At the height of their boasting a boy carries them both off for dinner, and the tale says their descendants still shun one another out of shame.",
             ["tortoise-crab"], "concept"),
            ("What role does Ellis say the tortoise fills in Slave Coast tales?",
             "The leading, crafty part that the spider Anansi plays in Gold Coast tales",
             ["The wise judge who settles every dispute", "The creator who moulds the first humans"],
             "Ellis writes that the tortoise \u201cfills in the folk-lore tales of the Slave Coast the place of the spider (anansi) in the tales of the Gold Coast.\u201d",
             ["tortoise-stories"], "source"),
        ],
    },
    {
        "slug": "animals-and-moral-lessons",
        "title": "Why the Bat Hides by Day",
        "subtitle": "Why-stories and morals in Ogumefu's collection",
        "refs": [
            ("bat", "ogumefu", "Legend XI · THE BAT",
             "THE Bat is half a bird and half a rodent",
             "when his enemies cannot see him."),
            ("leopard", "ogumefu", "Legend XIX · HOW LEOPARD GOT HIS SPOTS",
             "But where each arrow struck him, there appeared a dark mark",
             "the mingling of the sun and shadow."),
            ("explain", "ogumefu", "Preface",
             "They relate the adventures of men and animals",
             "and so forth."),
        ],
        "cards": [
            ("context", "A deserter in mid-battle", "In Ogumefu's tale, the Bat fights beside his cousins the rats, but when the birds begin to win he flies up and joins their side instead.", ["bat"], "concept"),
            ("source", "Both armies turn on him", None, ["bat"], "concept"),
            ("context", "A story that explains a habit", "Disgusted by his disloyalty, rats and birds unite against the Bat, who must now hide in dark places all day and only come out in the evening. The moral punishes a traitor; the ending explains a real animal's behaviour.", ["bat"], "concept"),
            ("method", "The collector's own description", "Ogumefu writes in his 1929 preface that these legends \u201crelate the adventures of men and animals, and try to explain the mysteries of Nature\u201d, naming the leopard's spots and women's long hair as examples. The Bat's nights fit his description exactly.", ["explain", "leopard"], "source"),
            ("synthesis", "Two jobs at once", "These tales explain an animal's feature (spots, night-flying) and judge a character's conduct (cowardice, greed) at the same time. Reading only the moral or only the explanation misses half the design.", ["bat", "leopard"], "source"),
        ],
        "questions": [
            ("Why do the rats and the birds unite against the Bat?",
             "He abandoned the rats mid-battle to join the winning side",
             ["He stole their food stores during the fight", "He refused to take any side at all"],
             "The Bat fought with the rats but flew to the birds when they seemed to be winning; both armies, disgusted, joined to attack him.",
             ["bat"], "concept"),
            ("In Ogumefu's telling, where do the Leopard's spots come from?",
             "The dark marks left where Akiti's arrows struck him",
             ["He painted himself to hide in the forest", "They are burn marks from a forest fire"],
             "Each of the hunter Akiti's arrows left a dark mark on the Leopard, so his coat now looks like the mingling of sun and shadow.",
             ["leopard"], "concept"),
        ],
    },
]


def make_reference(manifest, spec):
    ref_id, record_key, locator, start_anchor, end_anchor = spec
    record = next(item for item in manifest["records"] if item["localPath"] == RECORD_FILES[record_key])
    segment = next(
        (item for item in source_segments(ROOT / "content/corpus/yoruba" / record["localPath"])
         if item["locator"] == locator and item["evidenceType"] == "source-text"),
        None,
    )
    if not segment:
        raise ValueError(f"Named passage not found: {locator}")
    text = segment["text"]
    start = text.casefold().find(start_anchor.casefold())
    end = text.casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found in {locator}: {start_anchor!r} / {end_anchor!r}")
    end += len(end_anchor)
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": record["title"],
        "author": AUTHOR_BY_RECORD[record_key],
        "translator": TRANSLATOR_BY_RECORD[record_key],
        "locator": f"{locator}; {locator}, normalized characters {start}-{end}",
        "localPath": f"content/corpus/yoruba/{record['localPath']}",
        "excerpt": text[start:end],
        "evidenceType": "quotation",
        "note": NOTE_BY_RECORD[record_key],
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/yoruba/manifest.json").read_text(encoding="utf-8"))
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/yoruba").rglob("*.json")
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
        lesson["sourceReferences"] = {item[0]: make_reference(manifest, item) for item in spec["refs"]}
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, refs, objective) in enumerate(spec["cards"], 1):
            if body is None:
                ref = lesson["sourceReferences"][refs[0]]
                body = ("Source quotation (" + ref["work"] + "; whitespace normalized): \u201c"
                        + ref["excerpt"] + "\u201d")
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
                    "prompt": "Read the named passage in the cited local source.",
                    "suggestedQuestions": [
                        "Which words support this answer?",
                        "Is this passage a legend retold by Ogumefu or a report written by Ellis, and how does that change what it can prove?",
                    ],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Bounded to Ellis's 1894 colonial-era survey and Ogumefu's 1929 Yoruba-authored legends; independent scholarly and community review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/yoruba").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Yoruba scaffolds.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} source-bounded Yoruba lessons; no files written.")
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

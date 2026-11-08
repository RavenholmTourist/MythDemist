"""One-time, digest-guarded source and lesson rewrite for the five Welsh tale modules."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
RECORD = "pg-5160"

PACK = [
    {
        "slug": "pwyll-otherworld",
        "title": "Pwyll and the Otherworld",
        "subtitle": "A pact, a borrowed shape, and one required blow",
        "refs": [
            ("main", "The First Branch, Arawn asks Pwyll to defeat Hafgan", "One year from this night", "“Verily,” said Pwyll"),
        ],
        "scene": "Arawn, king of Annwvyn, asks Pwyll to fight Hafgan at the Ford after a year. Pwyll must take Arawn’s shape and give Hafgan only one blow; a second blow would let him recover.",
        "quoteCard": "Arawn's terms",
        "why": "The test is not just whether Pwyll can win a fight. He must keep the agreement's exact limit, even when his opponent asks for another blow.",
        "method": "This is the Mabinogion's Welsh tale of Pwyll and Arawn. Keep the otherworld setting and the tale's rule about a single blow attached to this version.",
        "carry": "Track the promise through the exchange: what Pwyll owes Arawn, what he is forbidden to do, and how restraint changes the result.",
        "questions": [
            ("What does Arawn ask Pwyll to do?", "Take Arawn's shape and defeat Hafgan with one blow at the Ford after a year", ["Defeat Arawn in a contest for Dyved", "Marry Hafgan's daughter and surrender Annwvyn"], "Arawn offers friendship if Pwyll takes his form, meets Hafgan at the Ford, and gives only one blow.", ["main"], "concept"),
            ("Why does Arawn forbid a second blow?", "Hafgan would recover and fight again the next day", ["A second blow would break Pwyll's disguise", "The Ford can be crossed only once"], "Arawn explains that Hafgan fought as well as before after receiving a second blow.", ["main"], "source"),
        ],
    },
    {
        "slug": "branwen-sovereignty",
        "title": "Branwen: Hospitality and Consequence",
        "subtitle": "An insult, a letter, and a widening conflict",
        "refs": [
            ("insult", "The Second Branch, Evnissyen injures Matholwch's horses", "And behold one day, Evnissyen", "rendered them useless."),
            ("message", "The Second Branch, Branwen sends word to her brother", "And Branwen reared a starling", "the tidings of Branwen’s woes."),
        ],
        "scene": "When Efnissien learns that Branwen was married to Matholwch without his consent, he mutilates the Irish king's horses. The insult helps turn an alliance into a conflict that reaches Branwen.",
        "quoteCard": "Branwen sends her letter",
        "why": "Branwen's starling carries a letter across the sea after she has been mistreated and isolated. The tale makes communication a turning point in a political crisis.",
        "method": "This is a Welsh tale in the Mabinogion, translated by Lady Charlotte Guest. Do not merge it with the Irish Táin Bó Cúailnge just because both are medieval Celtic-language narratives.",
        "carry": "Follow the chain from the wedding alliance to the insult, Branwen's message, and Bran's response; keep each step tied to the tale.",
        "questions": [
            ("What starts the insult to Matholwch?", "Efnissien mutilates his horses because the marriage was made without consulting him", ["Branwen refuses to send her brother a message", "Matholwch takes the throne of Dyved"], "The tale says Efnissien objects that his sister was married without his consent, then injures Matholwch's horses.", ["insult"], "concept"),
            ("How does Branwen get her message to Britain?", "She trains a starling and ties her letter to its wing", ["She sends it through a merchant at the Ford", "She asks Matholwch to carry it to her brother"], "The narrative describes Branwen teaching the bird to speak and attaching her letter to its wing.", ["message"], "source"),
        ],
    },
    {
        "slug": "manawydan-patience",
        "title": "Manawydan: Patience and Enchantment",
        "subtitle": "A mouse, a missing harvest, and a hidden cause",
        "refs": [
            ("mouse", "The Third Branch, Manawydan catches the last mouse", "he caught it and put it in his glove", "that I found robbing me."),
            ("reveal", "The Third Branch, Llwyd explains the enchantment", "I will know who the mouse may be.", "which he did unadvisedly in the Court of Heveydd Hên."),
        ],
        "scene": "After the harvest has been stripped, Manawydan catches the slowest mouse and keeps it in his glove. His questioning reveals that it is part of a deliberate enchantment, not an ordinary pest.",
        "quoteCard": "The mouse is not an ordinary thief",
        "why": "The tale delays the explanation. Manawydan observes what happened, preserves the evidence, and questions the mouse rather than answering magical trouble with immediate violence.",
        "method": "The story explains Llwyd's act as revenge for an earlier episode in Pwyll's tale. Keep that narrative connection explicit; do not make it a generic claim about all Welsh enchantment stories.",
        "carry": "Follow the evidence from the ruined harvest to the captured mouse, then to Llwyd's account of the revenge behind the spell.",
        "questions": [
            ("What does Manawydan do with the last mouse he catches?", "Keeps it in his glove and questions it", ["Turns it loose as a harvest offering", "Takes it to Math for a wrestling contest"], "The source says he catches the mouse, ties the glove, and asks what kind of thief it is.", ["mouse"], "concept"),
            ("Who does the mouse turn out to be?", "Llwyd's wife, part of his revenge enchantment", ["Rhiannon in disguise", "A messenger sent by Arawn"], "Llwyd tells Manawydan that the mouse is his wife and explains the spell as revenge.", ["reveal"], "source"),
        ],
    },
    {
        "slug": "math-sovereignty",
        "title": "Math: Law, Magic, and Sovereignty",
        "subtitle": "A ruler's condition and Goewin's testimony",
        "refs": [
            ("rule", "The Fourth Branch, Math's rule and Goewin", "Math the son of Mathonwy could not exist", "except only when he was prevented by the tumult of war."),
            ("testimony", "The Fourth Branch, Goewin reports the assault", "An attack, lord, was made unawares upon me;", "unto me they did wrong, and unto thee dishonour."),
        ],
        "scene": "The Fourth Branch says Math normally must rest his feet in a maiden's lap, except when war prevents it. Goewin later tells Math that his nephews attacked her while he was away and names them.",
        "quoteCard": "Goewin speaks to Math",
        "why": "The tale links a court custom with the harm done under its protection. Keep Goewin's testimony visible; do not turn the assault into a romantic subplot or erase her account.",
        "method": "This is one medieval Welsh branch in the Mabinogion collection, not a universal account of Celtic law or kingship.",
        "carry": "Compare the rule described at the opening with Goewin's own report of how it was violated.",
        "questions": [
            ("When can Math be without a maiden holding his feet?", "When war prevents the custom", ["Whenever he is judging a legal dispute", "Only while he is travelling to Annwvyn"], "The branch states the condition and gives war as the exception.", ["rule"], "concept"),
            ("Whom does Goewin identify in her report to Math?", "Gwydion and Gilvaethwy, Math's nephews", ["Pwyll and Arawn", "Bran and Matholwch"], "Goewin names the two nephews and says they wronged her and dishonoured Math.", ["testimony"], "source"),
        ],
    },
    {
        "slug": "taliesin-change",
        "title": "Taliesin: Poetry and Transformation",
        "subtitle": "Three drops, foresight, and a shape-changing chase",
        "refs": [
            ("cauldron", "The Tale of Taliesin, Gwion drinks the cauldron drops", "three blessed drops were obtained of the grace of Inspiration.", "he foresaw everything that was to come"),
            ("chase", "The Tale of Taliesin, Gwion and Ceridwen transform", "he saw her, and changed himself into a hare", "She, as a hawk, followed him and gave him no rest in the sky."),
        ],
        "scene": "Ceridwen keeps a cauldron boiling to create three drops of inspiration for her son. Gwion receives the drops by accident, gains foresight, and flees; the tale then turns his flight into a sequence of transformations.",
        "quoteCard": "The drops change Gwion's knowledge",
        "why": "The source links poetic inspiration to a specific magical episode. Keep this account in the Mabinogion's Taliesin tale rather than treating it as the origin story of every Welsh bard.",
        "method": "The Mabinogion is a later translated collection of Welsh tales. This passage is evidence for the tale as transmitted in Guest's edition, not an eyewitness record of an ancient poet's life.",
        "carry": "Track what the drops change first—Gwion's knowledge—and then notice how the chase changes bodies and forms.",
        "questions": [
            ("What happens after the cauldron drops reach Gwion?", "He gains foresight and realizes he must escape Ceridwen", ["He becomes king of Dyved", "He immediately forgets every poem he knows"], "The tale says he foresaw what was to come and fled in fear of Ceridwen.", ["cauldron"], "concept"),
            ("Which sequence describes the chase?", "Gwion becomes a hare, then a fish, then a bird; Ceridwen follows in other forms", ["Gwion sails to Ireland while Ceridwen remains at court", "Ceridwen turns into a horse and Gwion hides in a cave"], "The passage presents a series of transformations as Ceridwen pursues Gwion.", ["chase"], "source"),
        ],
    },
]


def make_reference(record, source):
    ref_id, locator, start_anchor, end_anchor = source
    work = locator.split(",")[0]
    local_path = f"content/corpus/celtic/{record['localPath']}"
    text = source_segments(ROOT / local_path)[0]["text"]
    start = text.find(start_anchor)
    end = text.find(end_anchor, start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Source anchor not found: {locator}")
    excerpt = text[start:end].strip()
    if not excerpt:
        raise ValueError(f"Empty source excerpt: {locator}")
    return {
        "recordId": record["id"],
        "sourceId": record["sourceIds"][0],
        "work": f"{work} (in The Mabinogion)",
        "author": ", ".join(record["ancientAuthors"]),
        "translator": record["translator"],
        "locator": f"{locator}; local text normalized characters {start}-{end}",
        "localPath": local_path,
        "excerpt": excerpt,
        "evidenceType": "quotation",
        "note": "Verbatim Guest translation excerpt; whitespace normalized. Lesson interpretation is separate.",
    }


def build():
    manifest = json.loads((ROOT / "content/corpus/celtic/manifest.json").read_text(encoding="utf-8"))
    record = next(item for item in manifest["records"] if item["id"] == "pg-5160")
    paths = {
        json.loads(path.read_text(encoding="utf-8"))["id"].rsplit(".", 1)[-1]: path
        for path in (ROOT / "content/lessons/celtic").rglob("*.json")
    }
    changes = {}
    for spec in PACK:
        path = paths[spec["slug"]]
        lesson = json.loads(path.read_text(encoding="utf-8"))
        lesson["version"] = 2
        lesson["estimatedMinutes"] = 3
        lesson["difficulty"] = 2
        concept_id = lesson["learningObjectives"][0]["id"]
        source_id = lesson["learningObjectives"][-1]["id"]
        lesson["learningObjectives"] = [
            {"id": concept_id, "text": spec["questions"][0][0]},
            {"id": source_id, "text": spec["questions"][1][0]},
        ]
        lesson["sourceReferences"] = {item[0]: make_reference(record, item) for item in spec["refs"]}
        ref_ids = [item[0] for item in spec["refs"]]
        cards = [
            ("context", "The scene", spec["scene"], [ref_ids[0]], "concept"),
            ("source", spec["quoteCard"], None, [ref_ids[0]], "concept"),
            ("synthesis", "Why it matters", spec["why"], ref_ids, "concept"),
            ("method", "Read it carefully", spec["method"], ref_ids, "source"),
            ("flavor", "Carry it forward", spec["carry"], ref_ids, "source"),
        ]
        lesson["narrativeBlocks"] = []
        for index, (kind, title, body, refs, objective_kind) in enumerate(cards, start=1):
            if body is None:
                body = "Source quotation (Guest translation; whitespace normalized): “" + lesson["sourceReferences"][refs[0]]["excerpt"] + "”"
            lesson["narrativeBlocks"].append({
                "id": f"card-{index:02d}", "kind": kind, "title": title, "body": body,
                "sourceRefIds": refs, "objectiveIds": [concept_id if objective_kind == "concept" else source_id],
            })
        lesson["quiz"] = []
        for index, (prompt, correct, wrong, explanation, refs, objective_kind) in enumerate(spec["questions"]):
            options = [correct, *wrong]
            shift = (index + len(changes)) % 3
            options = options[shift:] + options[:shift]
            choices = [{"id": chr(97 + i), "text": text} for i, text in enumerate(options)]
            lesson["quiz"].append({
                "id": f"q{index + 1}", "type": "single-choice", "prompt": prompt,
                "choices": choices,
                "answerId": next(choice["id"] for choice in choices if choice["text"] == correct),
                "explanation": explanation, "sourceRefIds": refs,
                "objectiveIds": [concept_id if objective_kind == "concept" else source_id],
                "deepDive": {
                    "prompt": "Read the cited passage closely.",
                    "suggestedQuestions": ["Which words support the answer?", "What does this one text not establish?"],
                    "sourceRefIds": refs,
                },
            })
        lesson["review"] = {
            "status": "draft", "reviewedBy": None, "reviewedAt": None,
            "notes": "Source-specific rewrite with verbatim local quotations. Independent scholarly and pedagogical review remains pending.",
        }
        changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/celtic").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding="utf-8")).get("version", 1) > 1 for path in paths):
        parser.error("This one-time migration only accepts the exact version-1 Celtic starter lessons.")
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} source-grounded lessons; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        for path, lesson in changes.items():
            path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied once; further generated writes are disabled.")


if __name__ == "__main__":
    main()

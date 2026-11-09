"""One-time, digest-guarded repair of Greek weekly assessment evidence."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PATCHES = {
    1: {
        1: {
            "prompt": "How do the two openings differ in what they foreground?",
            "answer": "The Iliad names anger and loss; the Odyssey names travel, suffering, and return.",
            "wrong": ["Both openings describe the same battle scene.", "The Iliad begins with the Argo while the Odyssey begins with Theseus."],
            "explanation": "The Iliad's invocation foregrounds Achilles' anger; the Odyssey's invocation foregrounds a journey and its costs.",
            "refs": ["ref-iliad-1-opening", "ref-odyssey-1-opening"],
        },
        2: {
            "prompt": "After the heralds take Briseis, where does Achilles go and whom does he call?",
            "answer": "He goes to the seashore and calls on Thetis.",
            "wrong": ["He sails to Crete and calls on Ariadne.", "He goes to Mount Oeta and calls on Zeus."],
            "explanation": "Book 1 says Achilles goes alone to the sea and prays to his mother Thetis.",
            "refs": ["aftermath"],
        },
        3: {
            "prompt": "What does the Odyssey say Odysseus suffers while trying to save his men?",
            "answer": "Much suffering by sea, and he cannot save his crew.",
            "wrong": ["He loses his armor in the Nemean cave.", "He is trapped by the suitors in Ithaca."],
            "explanation": "Butler's invocation says Odysseus suffers by sea and cannot save his men.",
            "refs": ["odyssey"],
        },
    },
    2: {
        2: {
            "prompt": "Which sequence does Butler's Book 1 narrate?",
            "answer": "Agamemnon threatens to take Briseis, Athena restrains Achilles, and Achilles appeals to Thetis.",
            "wrong": ["Achilles kills Agamemnon, then sails to Crete.", "Priam ransoms Hector, then Athena stops the war."],
            "explanation": "The Book 1 sequence runs from the threat to Athena's intervention and Achilles' appeal.",
            "refs": ["main", "restraint", "aftermath"],
        },
        4: {
            "prompt": "What does the report of Patroclus' death add to the story of Achilles' borrowed armour?",
            "answer": "Hector now holds the armour that Patroclus wore.",
            "wrong": ["The armour is returned to Chryses.", "Patroclus gives it to Priam as a ransom."],
            "explanation": "Antilochus says Patroclus has fallen and Hector holds his armour.",
            "refs": ["main"],
        },
        5: {
            "refs": ["main", "release"],
        },
    },
    3: {
        1: {
            "prompt": "What do the suitors do in Odysseus' home while he is absent?",
            "answer": "They consume his resources and press Penelope about remarriage.",
            "wrong": ["They guard the house for Telemachus.", "They return the estate to Odysseus."],
            "explanation": "Telemachus says the suitors eat up his house and press his mother about marriage.",
            "refs": ["main", "pressure"],
        },
        2: {
            "prompt": "What does Odysseus' boast reveal, and what does Polyphemus do next?",
            "answer": "His name; Polyphemus prays to Poseidon to prevent his return.",
            "wrong": ["His ship's location; Polyphemus gives him a safe passage.", "His father's name; Polyphemus returns his crew."],
            "explanation": "Odysseus reveals his name, and Polyphemus invokes Poseidon against his return.",
            "refs": ["boast", "curse"],
        },
    },
    4: {
        2: {
            "prompt": "What does Medea's charm protect Jason from during Aeetes' task?",
            "answer": "The bulls' fire and the earthborn men's weapons.",
            "wrong": ["The Sirens' song and the whirlpool.", "The cold of the House of Cold."],
            "explanation": "Medea instructs Jason to use the charm against the spearpoints and the bulls' flame.",
            "refs": ["aid"],
        },
        4: {
            "prompt": "What does Apollonius say follows Apsyrtus' killing?",
            "answer": "Zeus orders the Argonauts to seek purification from Circe.",
            "wrong": ["Athena gives Jason the throne of Athens.", "Aeetes welcomes the Argonauts home."],
            "explanation": "The Book 4 passage connects the bloodshed with Zeus' purification order.",
            "refs": ["purification"],
        },
        5: {
            "prompt": "Which contrast between Apollonius and Euripides is supported?",
            "answer": "Apollonius frames the fleece quest; Euripides begins with its later consequences for Medea.",
            "wrong": ["Both texts are eyewitness diaries of Jason's voyage.", "Euripides' play is a catalogue of the Argonauts."],
            "explanation": "Apollonius' proem frames the quest; Euripides' Nurse speaks from the later crisis in Corinth.",
            "refs": ["argo", "main"],
        },
    },
    5: {
        2: {
            "prompt": "What method defeats the lion after arrows fail?",
            "answer": "Heracles blocks one cave entrance and chokes the lion through the other.",
            "wrong": ["Iolaus helps cauterize the Hydra's neck.", "He distracts it with a singing contest."],
            "explanation": "The Library says Heracles changes tactics and strangles the lion inside its cave.",
            "refs": ["main", "combat"],
        },
    },
    6: {
        2: {
            "prompt": "What does Ariadne's clue let Theseus do in the Epitome?",
            "answer": "Find his way out after killing the Minotaur.",
            "wrong": ["Capture the Nemean lion.", "Escape from Polyphemus."],
            "explanation": "The Epitome says Theseus draws the clue after him as he leaves the labyrinth.",
            "refs": ["escape"],
        },
    },
    7: {
        1: {
            "prompt": "Which contrast between the returns is supported by these works?",
            "answer": "Agamemnon faces household murder; Odysseus is recognized by Penelope.",
            "wrong": ["Both kings are welcomed without conflict.", "Neither work includes a household after the war."],
            "explanation": "Aeschylus stages Agamemnon's murder; Butler's Odyssey passage shows Penelope recognizing Odysseus.",
            "refs": ["main", "murder", "odyssey"],
        },
        2: {"refs": ["main", "court"]},
        3: {"refs": ["main", "defense"]},
        4: {"refs": ["main", "revelation"]},
        5: {
            "prompt": "What does the cited Trojan Women passage foreground after Troy's fall?",
            "answer": "Captive women being assigned to Greek masters.",
            "wrong": ["A Greek council choosing a new king.", "Odysseus explaining the construction of his marriage bed."],
            "explanation": "The passage describes captive women at the Scamander being assigned by lot.",
            "refs": ["main"],
        },
    },
    8: {
        1: {"refs": ["main", "agreement"]},
        3: {
            "prompt": "What does Ovid say Liber does after Theseus abandons Ariadne?",
            "answer": "He embraces her and places her crown among the stars.",
            "wrong": ["He gives Theseus a clue to leave the labyrinth.", "He orders Medea to return to Colchis."],
            "explanation": "Ovid names Liber as Ariadne's helper and describes the crown's celestial afterlife.",
            "refs": ["main"],
        },
        5: {"refs": ["main", "heracles", "odysseus", "theseus"]},
    },
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/curriculum/greek").glob("*week*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    changes = {}
    lesson_docs = {}
    for lesson_path in (ROOT / "content/lessons/greek").rglob("*.json"):
        lesson = json.loads(lesson_path.read_text(encoding="utf-8"))
        lesson_docs[lesson["id"]] = lesson

    def evidence_explanation(answer, ref_ids, lesson):
        refs = [lesson["sourceReferences"][ref_id] for ref_id in ref_ids]
        locators = [f"{ref['work']} ({ref['locator'].split(';')[0]})" for ref in refs]
        if len(locators) == 1:
            return f"{answer} is supported by {locators[0]}; the other choices are not stated in this passage."
        return f"{answer} follows from reading the cited passages together: {'; '.join(locators)}. Keep their versions distinct."

    for week_number, patches in PATCHES.items():
        path = ROOT / f"content/curriculum/greek/greek-heroes-week-{week_number:02d}.json"
        week = json.loads(path.read_text(encoding="utf-8"))
        for question in week.get("assessment", {}).get("questions", []):
            q = question["question"]
            update = patches.get(int(q["id"][1:]))
            lesson_id = question["lessonId"]
            lesson = lesson_docs[lesson_id]
            if update and "prompt" in update:
                q["prompt"] = update["prompt"]
            if update and "answer" in update:
                wrong = update["wrong"]
                texts = [update["answer"], *wrong]
                rotate = (int(q["id"][1:]) + week_number) % len(texts)
                texts = texts[rotate:] + texts[:rotate]
                q["choices"] = [{"id": chr(97 + i), "text": text} for i, text in enumerate(texts)]
                q["answerId"] = next(c["id"] for c in q["choices"] if c["text"] == update["answer"])
            if update and "explanation" in update:
                q["explanation"] = update["explanation"]
            if update and "refs" in update:
                q["sourceRefIds"] = update["refs"]
            answer = next(c["text"] for c in q["choices"] if c["id"] == q["answerId"])
            if "Revisit the named passage" in q.get("explanation", "") or ".. Revisit" in q.get("explanation", ""):
                q["explanation"] = evidence_explanation(answer, q["sourceRefIds"], lesson)
        changes[path] = week

    for lesson_path, lesson in [(path, json.loads(path.read_text(encoding="utf-8"))) for path in sorted((ROOT / "content/lessons/greek").rglob("*.json"))]:
        changed = False
        for q in lesson.get("quiz", []):
            answer = next(c["text"] for c in q["choices"] if c["id"] == q["answerId"])
            if "Revisit the named passage" in q.get("explanation", "") or ".. Revisit" in q.get("explanation", ""):
                q["explanation"] = evidence_explanation(answer, q["sourceRefIds"], lesson)
                changed = True
        if changed:
            changes[lesson_path] = lesson

    print("Input SHA256:", digest)
    print(f"Prepared assessment alignment and source-specific explanations in {len(changes)} Greek files; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Assessment files changed; refusing to overwrite.")
        for path, week in changes.items():
            path.write_text(json.dumps(week, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied once.")


if __name__ == "__main__":
    main()

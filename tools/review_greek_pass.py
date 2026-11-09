"""Guarded editorial repair of the Greek foundation lessons and Homer citations."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]


def path_for(lesson_id):
    for path in (ROOT / "content/lessons/greek").rglob("*.json"):
        if json.loads(path.read_text(encoding="utf-8"))["id"] == lesson_id:
            return path
    raise KeyError(lesson_id)


def quote_ref(base, segment_path, segment_locator, start_anchor, end_anchor, human_locator=None):
    segment = next(
        item for item in source_segments(segment_path)
        if item["locator"] == segment_locator and item["evidenceType"] == "source-text"
    )
    start = segment["text"].casefold().find(start_anchor.casefold())
    end = segment["text"].casefold().find(end_anchor.casefold(), start + len(start_anchor)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Unable to anchor {segment_locator}: {start_anchor!r} ... {end_anchor!r}")
    end += len(end_anchor)
    quote = segment["text"][start:end]
    base.update({
        "locator": f"{human_locator or segment_locator}; {segment_locator}, normalized characters {start}-{end}",
        "excerpt": quote,
        "evidenceType": "quotation",
        "note": f"Verbatim passage from the named work/translation; the locator selects this exact local source segment.",
    })
    return base


def homer_ref(lesson, key, segment_locator, start, end, label):
    ref = lesson["sourceReferences"][key]
    return quote_ref(ref, ROOT / ref["localPath"].replace("content/", "content/"), segment_locator, start, end, label)


def make_question(qid, prompt, correct, distractors, explanation, ref_ids, objective_id, shift):
    texts = [correct, *distractors]
    shift %= len(texts)
    texts = texts[shift:] + texts[:shift]
    choices = [{"id": chr(97 + index), "text": text} for index, text in enumerate(texts)]
    return {
        "id": qid,
        "type": "single-choice",
        "prompt": prompt,
        "choices": choices,
        "answerId": next(item["id"] for item in choices if item["text"] == correct),
        "explanation": explanation,
        "sourceRefIds": ref_ids,
        "objectiveIds": [objective_id],
        "deepDive": {
            "prompt": "Read the named passage in its work and translation.",
            "suggestedQuestions": ["Which words support the answer?", "What does this passage not establish?"],
            "sourceRefIds": ref_ids,
        },
    }


def rewrite_lesson(lesson, title, subtitle, refs, cards, questions):
    lesson["version"] += 1
    lesson["title"] = title
    lesson["subtitle"] = subtitle
    objective_ids = [item["id"] for item in lesson["learningObjectives"]]
    lesson["learningObjectives"] = [
        {"id": objective_ids[0], "text": questions[0][0]},
        {"id": objective_ids[-1], "text": questions[1][0]},
    ]
    lesson["sourceReferences"] = refs
    lesson["narrativeBlocks"] = []
    for index, (kind, heading, body, ref_ids, objective_index) in enumerate(cards, 1):
        lesson["narrativeBlocks"].append({
            "id": f"card-{index:02d}",
            "kind": kind,
            "title": heading,
            "body": body,
            "sourceRefIds": ref_ids,
            "objectiveIds": [objective_ids[objective_index]],
        })
    lesson["quiz"] = [
        make_question(
            f"q{index + 1}", prompt, correct, wrong, explanation, ref_ids,
            objective_ids[objective_index], index + 1,
        )
        for index, (prompt, correct, wrong, explanation, ref_ids, objective_index) in enumerate(questions)
    ]


def build():
    originals = {}
    changes = {}
    il = ROOT / "content/corpus/greek/primary/homer-iliad-2199.txt"
    od = ROOT / "content/corpus/greek/primary/homer-odyssey-1727.txt"
    arg = ROOT / "content/corpus/greek/primary/apollonius-argonautica-0830.txt"
    buckley = ROOT / "content/corpus/greek/primary/euripides-buckley-volume-i-15081.txt"
    iliad_open = quote_ref(
        {
            "recordId": "pg-02199", "sourceId": "grc.homer.iliad",
            "work": "The Iliad", "author": "Homer", "translator": "Samuel Butler",
            "localPath": "content/corpus/greek/primary/homer-iliad-2199.txt",
        }, il, "Book 1", "Sing, O goddess, the anger of Achilles",
        "first fell out with one another.",
        "Iliad 1, proem",
    )
    odyssey_open = quote_ref(
        {
            "recordId": "pg-01727", "sourceId": "grc.homer.odyssey",
            "work": "The Odyssey", "author": "Homer", "translator": "Samuel Butler",
            "localPath": "content/corpus/greek/primary/homer-odyssey-1727.txt",
        }, od, "Book 1", "Tell me, O Muse, of that ingenious hero",
        "they perished through their own sheer folly in eating the cattle of the Sun-god Hyperion;",
        "Odyssey 1, invocation and proem",
    )

    lesson = json.loads(path_for("grc.heroes.day01.heroic-excellence").read_text(encoding="utf-8"))
    refs = {"ref-iliad-1-opening": iliad_open, "ref-odyssey-1-opening": odyssey_open}
    claim, source_objective = [item["id"] for item in lesson["learningObjectives"]]
    rewrite_lesson(
        lesson, "Heroes Are Not Moral Certificates",
        "Two epic openings, two different pressures",
        refs,
        [
            ("context", "The Iliad names a costly anger", "The invocation names Achilles' anger and connects it to loss among the Achaeans. It begins with a conflict, not a complete biography of the hero.", "ref-iliad-1-opening".split(), 0),
            ("source", "The Odyssey names an ingenious wanderer", "Verbatim opening from Samuel Butler's translation: “" + odyssey_open["excerpt"] + "”", ["ref-odyssey-1-opening"], 1),
            ("context", "One proem, a different emphasis", "The Odyssey's opening describes travel, suffering at sea, and the crew's failure to return. The Iliad's opening foregrounds anger and its consequences.", ["ref-iliad-1-opening", "ref-odyssey-1-opening"], 0),
            ("method", "Translations are evidence, not the Greek wording", "These quotations are Samuel Butler's English translations. Keep the work and book locator attached, and do not treat either opening as a universal definition of Greek heroism.", ["ref-iliad-1-opening", "ref-odyssey-1-opening"], 1),
            ("synthesis", "Compare the poems, not a single canon", "The two openings present different narrative problems. Comparison is useful precisely because the poems remain distinct.", ["ref-iliad-1-opening", "ref-odyssey-1-opening"], 0),
        ],
        [
            ("What consequence does the Iliad's invocation connect with Achilles' anger?", "Countless ills for the Achaeans and the deaths of heroes", ["A safe return for every crew member", "The founding of a unified Athens"], "The Iliad's opening directly links Achilles' anger with ills for the Achaeans and dead heroes.", ["ref-iliad-1-opening"], 0),
            ("How does the Odyssey's invocation describe its hero?", "As an ingenious traveler who suffers while trying to return", ["As a king who never leaves Ithaca", "As a warrior whose anger ends the Trojan War"], "Butler's invocation calls him ingenious, widely travelled, and struggling to save his men and return home.", ["ref-odyssey-1-opening"], 1),
        ],
    )
    changes[path_for(lesson["id"])] = lesson

    lesson = json.loads(path_for("grc.heroes.day02.achilles-anger").read_text(encoding="utf-8"))
    existing = lesson["sourceReferences"]["iliad"]
    threat = quote_ref(
        dict(existing), il, "Book 1", "since Phoebus Apollo is taking Chryseis from me",
        "fear to set himself up as equal or comparable with me.",
        "Iliad 1, Agamemnon threatens to take Briseis",
    )
    restraint = quote_ref(
        dict(existing), il, "Book 1", "The son of Peleus was furious",
        "Cease, then, this brawling, and do not draw your sword",
        "Iliad 1, Athena restrains Achilles",
    )
    aftermath = quote_ref(
        dict(existing), il, "Book 1", "Then Achilles went all alone by the side of the hoar sea",
        "and his mother heard him",
        "Iliad 1, Achilles appeals to Thetis",
    )
    refs = {"iliad": threat, "restraint": restraint, "aftermath": aftermath}
    q_ids = [item["id"] for item in lesson["learningObjectives"]]
    rewrite_lesson(
        lesson, "Achilles: Anger, Honor, and Restraint",
        "A public quarrel changes what the army can do",
        refs,
        [
            ("context", "Agamemnon threatens a second seizure", "Agamemnon says he will return Chryseis but take Briseis from Achilles as compensation. His speech makes the quarrel about public rank and control of captives.", ["iliad"], 0),
            ("source", "Achilles considers violence", "The passage says Achilles is divided between drawing his sword against Agamemnon and restraining his anger.", ["restraint"], 0),
            ("context", "Athena intervenes", "Athena tells Achilles not to draw his sword. The conflict continues through speech and a seizure of Briseis rather than becoming a duel.", ["restraint"], 0),
            ("source", "Achilles turns to the sea", "After Briseis is taken, Achilles goes alone to the shore, weeps, and calls on his mother Thetis.", ["aftermath"], 1),
            ("synthesis", "Honor has a public cost", "The poem frames a dispute between leaders as a danger to the larger Achaean host. Preserve the sequence: threat, restraint, seizure, grief.", ["iliad", "restraint", "aftermath"], 0),
        ],
        [
            ("What does Agamemnon threaten to take from Achilles?", "Briseis", ["Chryses' priestly sceptre", "The wooden horse"], "Agamemnon says he will take Achilles' prize Briseis.", ["iliad"], 0),
            ("What does Athena tell Achilles to do?", "Restrain his anger and not draw his sword", ["Leave for Crete immediately", "Return Briseis to Chryses"], "Athena intervenes as Achilles is considering killing Agamemnon and tells him not to draw his sword.", ["restraint"], 1),
        ],
    )
    changes[path_for(lesson["id"])] = lesson

    lesson = json.loads(path_for("grc.heroes.day03.odysseus-cunning").read_text(encoding="utf-8"))
    refs = {"odyssey": odyssey_open}
    rewrite_lesson(
        lesson, "Odysseus: Journey and Loss",
        "The Odyssey's opening names a difficult return",
        refs,
        [
            ("context", "A hero is introduced through travel", "The opening calls Odysseus ingenious and says he has visited many cities and learned their customs.", ["odyssey"], 0),
            ("source", "The journey costs lives", "Verbatim opening from Butler's translation: “" + odyssey_open["excerpt"] + "”", ["odyssey"], 1),
            ("context", "The crew's fate is not hidden", "The proem says Odysseus cannot save his men because they eat the cattle of the Sun-god Hyperion.", ["odyssey"], 0),
            ("method", "An invocation sets a frame", "This is the Odyssey's opening in Butler's translation. It previews the poem; it does not replace the later episodes that show how each event unfolds.", ["odyssey"], 1),
            ("synthesis", "Return is not a simple victory", "The hero longs for home, but the opening also remembers crew members who never reach it.", ["odyssey"], 0),
        ],
        [
            ("What adjective does Butler's invocation use for Odysseus?", "Ingenious", ["Invulnerable", "Untroubled"], "The opening directly calls him an ingenious hero.", ["odyssey"], 0),
            ("According to the invocation, why do Odysseus' men fail to return?", "They eat the Sun-god's cattle and are destroyed", ["They follow Achilles to the shore", "They are captured by the Minotaur"], "The proem says they perish through their own folly in eating Hyperion's cattle.", ["odyssey"], 1),
        ],
    )
    changes[path_for(lesson["id"])] = lesson

    lesson = json.loads(path_for("grc.heroes.day04.jason-medea").read_text(encoding="utf-8"))
    refs = lesson["sourceReferences"]
    refs["argo"] = quote_ref(
        dict(refs["argo"]), arg, "Book 3",
        "And forth from her fragrant girdle ungrudgingly she brought out the charm",
        "and he at once received it in his hands with joy.",
        "Argonautica 3, Medea gives Jason the charm",
    )
    refs["medea"] = quote_ref(
        dict(refs["medea"]), buckley, "local text",
        "But now every thing is at variance",
        "having married the daughter of Creon, who is prince of this land.",
        "Medea, Nurse's prologue",
    )
    rewrite_lesson(
        lesson, "Jason and Medea: Help and Aftermath",
        "Apollonius' epic and Euripides' tragedy ask different questions",
        refs,
        [
            ("context", "Medea supplies essential help", "In Apollonius' Argonautica, Medea gives Jason a protective charm for the dangerous task. The epic connects his success to her knowledge.", ["argo"], 0),
            ("source", "The charm changes the contest", "Verbatim from Seaton's translation: “" + refs["argo"]["excerpt"] + "”", ["argo"], 1),
            ("context", "Euripides begins later", "The Nurse in Medea remembers the Argo's voyage, then says Jason has married Creon's daughter while Medea is dishonored.", ["medea"], 0),
            ("method", "Do not merge epic and tragedy", "Apollonius narrates a quest and Medea's aid; Euripides stages the consequences of Jason's later marriage. These works preserve different moments and genres.", ["argo", "medea"], 1),
            ("synthesis", "The same names carry different claims", "A successful voyage does not settle the obligations that the tragedy brings forward.", ["argo", "medea"], 0),
        ],
        [
            ("What does Medea give Jason in Apollonius' account?", "A charm that protects him for the contest", ["Ariadne's thread", "A golden fleece"], "The passage says Medea gives Jason the charm and he receives it.", ["argo"], 0),
            ("What does the Nurse say Jason has done in Euripides' Medea?", "Married Creon's daughter while Medea is dishonored", ["Returned the fleece to Pelias", "Founded Athens with Theseus"], "The Nurse says Jason has married Creon's daughter and Medea is dishonored.", ["medea"], 1),
        ],
    )
    changes[path_for(lesson["id"])] = lesson

    lesson = json.loads(path_for("grc.heroes.day05.theseus-heracles").read_text(encoding="utf-8"))
    refs = lesson["sourceReferences"]
    library = ROOT / "content/corpus/greek/primary/apollodorus-library-frazer-perseus-eng2.xml"
    refs["apollo"] = quote_ref(
        dict(refs["apollo"]), library, "book 2 · chapter 4 · section 12",
        "The Pythian priestess then first called him Hercules",
        "perform the ten labours imposed on him",
        "Library 2.4.12, oracle assigns service",
    )
    pl_path = ROOT / "content/corpus/greek/primary/plutarch-lives-00674.txt"
    refs["plutarch"] = quote_ref(
        dict(refs["plutarch"]), pl_path, "local text",
        "together all the inhabitants of Attica into one town",
        "which he by his persuasions appeased",
        "Life of Theseus, civic unification",
    )
    rewrite_lesson(
        lesson, "Theseus and Heracles: Two Later Accounts",
        "A civic biography beside a mythographic catalogue",
        refs,
        [
            ("context", "Plutarch's Theseus unites Attica", "Plutarch credits Theseus with bringing dispersed inhabitants into one civic community and calming disputes.", ["plutarch"], 0),
            ("source", "The Library's Heracles receives an order", "The Pythian priestess directs Heracles to serve Eurystheus and perform the first ten labours.", ["apollo"], 1),
            ("context", "The works have different purposes", "Plutarch shapes a Life around civic and moral action; the Library organizes myths into genealogies and episodes.", ["plutarch", "apollo"], 0),
            ("method", "A comparison needs both passages", "The Theseus claim comes from Plutarch; the Heracles service comes from Pseudo-Apollodorus' Library. Neither passage defines every version of either hero.", ["plutarch", "apollo"], 1),
            ("synthesis", "Do not turn order into a canon", "These selected accounts show how later authors used heroes for different narrative and political purposes.", ["plutarch", "apollo"], 0),
        ],
        [
            ("Which civic achievement does Plutarch attribute to Theseus?", "Uniting Attica into one political community", ["Serving Eurystheus for twelve years", "Sailing with the Argo"], "Plutarch's passage says Theseus brought Attica's inhabitants together into one city and people.", ["plutarch"], 0),
            ("Who directs Heracles to serve Eurystheus in the Library?", "The Pythian priestess", ["Penelope", "Medea"], "The Library says the Pythian priestess sends Heracles to Tiryns to serve Eurystheus.", ["apollo"], 1),
        ],
    )
    changes[path_for(lesson["id"])] = lesson

    # Recompute local anchors for existing Homer quotations that remain exact.
    for path in sorted((ROOT / "content/lessons/greek").rglob("*.json")):
        lesson = changes.get(path) or json.loads(path.read_text(encoding="utf-8"))
        touched = False
        for ref in lesson["sourceReferences"].values():
            local = ref.get("localPath", "")
            if not (local.endswith("homer-iliad-2199.txt") or local.endswith("homer-odyssey-1727.txt")):
                continue
            segment_match = re.search(r";\s*(Book \d+), normalized characters \d+-\d+$", ref["locator"])
            if not segment_match:
                continue
            segment_name = segment_match.group(1)
            src = ROOT / local
            segment = next(s for s in source_segments(src) if s["locator"] == segment_name and s["evidenceType"] == "source-text")
            start = segment["text"].find(ref["excerpt"])
            if start < 0:
                continue
            end = start + len(ref["excerpt"])
            old_prefix = ref["locator"].split(";")[0]
            ref["locator"] = f"{old_prefix}; {segment_name}, normalized characters {start}-{end}"
            touched = True
        if touched:
            changes[path] = lesson
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/greek").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared {len(changes)} Greek lessons for source and pedagogy repair; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Greek lesson inputs changed; refusing to overwrite.")
        for path, lesson in changes.items():
            path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied the focused editorial repair.")


if __name__ == "__main__":
    main()

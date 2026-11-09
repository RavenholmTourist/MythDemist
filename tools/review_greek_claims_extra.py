"""Guarded claim-to-source repairs found during the Greek lesson editorial audit."""
import argparse
import hashlib
import json
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "content/corpus/greek"
IL = CORPUS / "primary/homer-iliad-2199.txt"
OD = CORPUS / "primary/homer-odyssey-1727.txt"
ARG = CORPUS / "primary/apollonius-argonautica-0830.txt"
LIB = CORPUS / "primary/apollodorus-library-frazer-perseus-eng2.xml"
EPI = CORPUS / "primary/apollodorus-epitome-frazer-perseus-eng2.xml"
AES = CORPUS / "primary/aeschylus-house-of-atreus-8604.txt"
SOP = CORPUS / "primary/sophocles-theban-plays-0031.txt"
HYMNS = CORPUS / "primary/hesiod-homeric-hymns-homerica-0348.txt"
BUCKLEY = CORPUS / "primary/euripides-buckley-volume-i-15081.txt"
FRAZER = CORPUS / "scholarship/frazer-greek-scenery-legend-history-56002.txt"


def lesson_path(lesson_id):
    return next(
        path for path in (ROOT / "content/lessons/greek").rglob("*.json")
        if json.loads(path.read_text(encoding="utf-8"))["id"] == lesson_id
    )


def set_quote(lesson, key, base_key, source_path, segment_name, first, last, label, metadata=None):
    segments = source_segments(source_path)
    segment = next(
        item for item in segments
        if item["locator"] == segment_name and item["evidenceType"] == "source-text"
    )
    start = segment["text"].casefold().find(first.casefold())
    end = segment["text"].casefold().find(last.casefold(), start + len(first)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Could not anchor {lesson['id']}:{key}: {first!r} ... {last!r}")
    end += len(last)
    if base_key in lesson["sourceReferences"]:
        ref = dict(lesson["sourceReferences"][base_key])
    elif metadata:
        ref = dict(metadata)
    else:
        raise KeyError(f"{lesson['id']} has no reference template {base_key}")
    ref.update({
        "localPath": "content/" + str(source_path.relative_to(ROOT / "content")).replace("\\", "/"),
        "locator": f"{label}; {segment_name}, normalized characters {start}-{end}",
        "excerpt": segment["text"][start:end],
        "evidenceType": "quotation",
        "note": "Verbatim passage from the named work and translation; this locator selects the exact local narrative passage.",
    })
    lesson["sourceReferences"][key] = ref


def quote_ref(base, source_path, segment_name, first, last, label):
    segment = next(
        item for item in source_segments(source_path)
        if item["locator"] == segment_name and item["evidenceType"] == "source-text"
    )
    start = segment["text"].casefold().find(first.casefold())
    end = segment["text"].casefold().find(last.casefold(), start + len(first)) if start >= 0 else -1
    if start < 0 or end < 0:
        raise ValueError(f"Could not anchor {label}: {first!r} ... {last!r}")
    end += len(last)
    ref = dict(base)
    ref.update({
        "localPath": str(source_path.relative_to(ROOT / "content")).replace("\\", "/"),
        "locator": f"{label}; {segment_name}, normalized characters {start}-{end}",
        "excerpt": segment["text"][start:end],
        "evidenceType": "quotation",
        "note": "Verbatim passage from the named work and translation; this locator selects the exact local narrative passage.",
    })
    return ref


def set_card(lesson, card_id, *, body=None, refs=None, title=None):
    card = next(item for item in lesson["narrativeBlocks"] if item["id"] == card_id)
    if body is not None:
        card["body"] = body
    if refs is not None:
        card["sourceRefIds"] = refs
    if title is not None:
        card["title"] = title


def set_question(lesson, qid, *, prompt=None, correct=None, wrong=None, explanation=None, refs=None):
    q = next(item for item in lesson["quiz"] if item["id"] == qid)
    if prompt is not None:
        q["prompt"] = prompt
    if correct is not None:
        choices = [correct, *(wrong or [])]
        shift = 1 if qid == "q1" else 2
        choices = choices[shift:] + choices[:shift]
        q["choices"] = [{"id": chr(97 + i), "text": text} for i, text in enumerate(choices)]
        q["answerId"] = next(c["id"] for c in q["choices"] if c["text"] == correct)
    if explanation is not None:
        q["explanation"] = explanation
    if refs is not None:
        q["sourceRefIds"] = refs
        if "deepDive" in q:
            q["deepDive"]["sourceRefIds"] = refs


def touch(changes, lesson):
    lesson["version"] += 1
    changes[lesson_path(lesson["id"])] = lesson


def build():
    changes = {}

    lid = "grc.heroes.w02d01.the-quarrel-and-the-ransom"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "main", "main", IL, "Book 1",
              "It was the son of Jove and Leto", "I will not free her.",
              "Iliad 1, Chryses petitions and Agamemnon refuses")
    set_card(lesson, "card-02", body="Source quotation from Butler's translation (whitespace normalized): “" + lesson["sourceReferences"]["main"]["excerpt"] + "”")
    touch(changes, lesson)

    lid = "grc.heroes.w02d02.briseis-and-withdrawal"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    lesson["sourceReferences"].pop("iliad", None)
    set_quote(lesson, "main", "main", IL, "Book 1",
              "since Phoebus Apollo is taking Chryseis from me",
              "fear to set himself up as equal or comparable with me.",
              "Iliad 1, Agamemnon threatens to take Briseis")
    set_quote(lesson, "restraint", "main", IL, "Book 1",
              "The son of Peleus was furious",
              "Cease, then, this brawling, and do not draw your sword",
              "Iliad 1, Athena restrains Achilles")
    set_quote(lesson, "aftermath", "main", IL, "Book 1",
              "Then Achilles went all alone by the side of the hoar sea",
              "and his mother heard him",
              "Iliad 1, Achilles appeals to Thetis")
    set_card(lesson, "card-03", refs=["restraint"])
    set_card(lesson, "card-04", body="After the heralds take Briseis, Achilles goes alone to the seashore, weeps, and calls on Thetis.", refs=["aftermath"])
    set_question(lesson, "q2", prompt="What does Achilles do after Briseis is taken?",
                 correct="He goes to the seashore and calls on Thetis",
                 wrong=["He accepts Agamemnon's offer and returns to battle", "He sails at once to Crete"],
                 explanation="The poem says Achilles goes alone to the sea and prays to his mother after the seizure.",
                 refs=["aftermath"])
    touch(changes, lesson)

    lid = "grc.heroes.w02d03.the-embassy-fails"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "offer", "main", IL, "Book 9",
              "will make amends, and will give him great gifts by way of atonement",
              "I will give him these, and with them her whom I erewhile took from him, the daughter of Briseus;",
              "Iliad 9, Agamemnon lists gifts for Achilles")
    set_card(lesson, "card-01", refs=["offer", "main"])
    set_question(lesson, "q1", prompt="What does Agamemnon offer Achilles through the embassy?",
                 correct="Gifts, including Briseis, if he returns to battle",
                 wrong=["The throne of Ithaca", "A place among the gods"],
                 explanation="Agamemnon's speech lists material gifts and Briseis as part of his offer.",
                 refs=["offer"])
    set_question(lesson, "q2", prompt="How does Achilles answer the embassy?",
                 correct="He says Agamemnon and the Danaans will not appease him",
                 wrong=["He accepts the gifts immediately", "He asks Odysseus to lead the Myrmidons"],
                 explanation="Achilles says he will not be appeased by Agamemnon or the other Danaans.",
                 refs=["main"])
    touch(changes, lesson)

    lid = "grc.heroes.w02d05.priam-and-achilles"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "release", "main", IL, "Book 24",
              "O king, bid me not be seated",
              "I am of myself minded to give up the body of Hector.",
              "Iliad 24, Priam asks for Hector and Achilles agrees")
    set_card(lesson, "card-01", refs=["main", "release"])
    set_card(lesson, "card-03", body="Priam asks Achilles to accept a ransom and return Hector's body. Achilles says he is already minded to give it up.", refs=["release"])
    set_question(lesson, "q1", prompt="What does Priam ask Achilles to return?",
                 correct="Hector's body",
                 wrong=["Briseis", "The armor of Patroclus"],
                 explanation="Priam asks Achilles to give him Hector's body in exchange for ransom.",
                 refs=["release"])
    touch(changes, lesson)

    lid = "grc.heroes.w03d01.the-broken-house"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "pressure", "main", OD, "Book 1",
              "the chiefs from all our islands",
              "before long will do so also with myself.",
              "Odyssey 1, Telemachus describes the suitors' pressure")
    set_card(lesson, "card-01", body="Odysseus is absent while suitors eat his household's food and court Penelope, who has not agreed to marry one of them.", refs=["main", "pressure"])
    set_question(lesson, "q1", prompt="What do the suitors do in Odysseus' hall?",
                 correct="They sit down and eat the household's food",
                 wrong=["They escort Odysseus home", "They guard the house from the Trojans"],
                 explanation="The passage describes the suitors taking their places and eating the household's food.",
                 refs=["main"])
    set_question(lesson, "q2", prompt="Why does Telemachus call the suitors a threat to his household?",
                 correct="They consume his property while pressuring his mother to marry",
                 wrong=["They have taken the household to Troy", "They are protecting the estate for Odysseus"],
                 explanation="Telemachus says the suitors eat up his house, press his mother, and make havoc of his estate.",
                 refs=["pressure"])
    touch(changes, lesson)

    lid = "grc.heroes.w03d02.nobody-and-the-cyclops"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "boast", "main", OD, "Book 9",
              "Cyclops, if any one asks you who it was that put your eye out",
              "who lives in Ithaca.",
              "Odyssey 9, Odysseus reveals his name to Polyphemus")
    set_quote(lesson, "curse", "main", OD, "Book 9",
              "On this he lifted up his hands to the firmament of heaven and prayed",
              "grant that Ulysses may never reach his home alive",
              "Odyssey 9, Polyphemus prays to Poseidon")
    set_card(lesson, "card-04", refs=["boast", "curse"])
    set_question(lesson, "q2", prompt="What follows Odysseus' boast of his real name?",
                 correct="Polyphemus prays to Poseidon to keep him from reaching home",
                 wrong=["The Cyclops agrees to guide the ship", "Athena immediately brings the crew to Ithaca"],
                 explanation="After Odysseus names himself, Polyphemus raises his hands and prays to Poseidon.",
                 refs=["boast", "curse"])
    touch(changes, lesson)

    lid = "grc.heroes.w03d03.circe-and-the-sirens"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_question(lesson, "q2", prompt="What must the crew do if Odysseus begs to be released?",
                 correct="Bind him more tightly to the mast",
                 wrong=["Let him steer toward the Sirens", "Remove the wax from their ears"],
                 explanation="Circe anticipates his plea and tells the crew to bind him faster.",
                 refs=["main"])
    touch(changes, lesson)

    lid = "grc.heroes.w04d01.the-political-quest"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "main", "main", ARG, "Book 1",
              "who, at the behest of King Pelias",
              "devised for him the toil of a troublous voyage, in order that on the sea or among strangers he might lose his home-return.",
              "Argonautica 1, Pelias' commission and Jason's sign")
    set_card(lesson, "card-01", body="The Argonautica says the voyage begins at Pelias' behest. When Jason arrives with one sandal, Pelias devises a dangerous voyage to keep him from returning.", refs=["main"])
    set_question(lesson, "q1", prompt="What does Pelias do after Jason arrives with one sandal?",
                 correct="He devises a dangerous voyage that may keep Jason from returning",
                 wrong=["He appoints Jason king of Iolcus", "He sends Medea to Athens"],
                 explanation="The passage links the one-sandal prophecy with Pelias devising a dangerous voyage for Jason.",
                 refs=["main"])
    touch(changes, lesson)

    lid = "grc.heroes.w04d02.aeetes-and-the-tasks"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "main", "main", ARG, "Book 3",
              "Two bulls with feet of bronze I have",
              "I will not give it, expect it not.",
              "Argonautica 3, Aeetes sets the trial")
    set_quote(lesson, "aid", "main", ARG, "Book 3",
              "And at dawn steep this charm in water",
              "nor the flame of the deadly bulls as it rushes forth resistless.",
              "Argonautica 3, Medea explains the charm")
    set_card(lesson, "card-01", body="Aeetes orders Jason to yoke bronze bulls, plough four fields, and sow serpent's teeth before he will give up the fleece.", refs=["main"])
    set_card(lesson, "card-03", body="Medea explains how to use a charm that gives Jason strength and protects him from the bronze spearpoints and the bulls' fire.", refs=["aid"])
    set_question(lesson, "q2", prompt="What protection does Medea instruct Jason to use?",
                 correct="A charm to anoint his body and sprinkle on his weapons",
                 wrong=["A clue for the labyrinth", "A shield made by Daedalus"],
                 explanation="Medea tells him to steep the charm in water, anoint himself, and sprinkle his weapons.",
                 refs=["aid"])
    touch(changes, lesson)

    lid = "grc.heroes.w04d03.medea-chooses"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "main", "main", ARG, "Book 3",
              "the bolt burnt deep down",
              "her heart panted fast through anguish",
              "Argonautica 3, Eros' arrow strikes Medea")
    set_quote(lesson, "dilemma", "main", ARG, "Book 3",
              "And she thought now that she would give him the charms",
              "yielding to a mad passion.",
              "Argonautica 3, Medea debates helping Jason")
    set_quote(lesson, "aid", "main", ARG, "Book 3",
              "And forth from her fragrant girdle ungrudgingly she brought out the charm",
              "he at once received it in his hands with joy",
              "Argonautica 3, Medea gives Jason the charm")
    set_card(lesson, "card-01", body="Apollonius describes Eros' arrow striking Medea, then narrates her conflict about aiding Jason without her parents' knowledge.", refs=["main", "dilemma"])
    set_card(lesson, "card-03", body="Medea fears shame and her parents' reaction, yet she resolves to provide the charms that can help Jason.", refs=["dilemma"])
    set_card(lesson, "card-04", body="The episode holds together divine pressure, Medea's deliberation, and her later action; it is not a simple picture of either total freedom or total passivity.", refs=["main", "dilemma", "aid"])
    set_question(lesson, "q1", prompt="What does Medea debate doing in her inner speech?",
                 correct="Giving Jason the charms or refusing to help him",
                 wrong=["Returning the fleece to Pelias", "Asking Athena to take her to Ithaca"],
                 explanation="Medea explicitly considers giving the charms and then not giving them.",
                 refs=["dilemma"])
    set_question(lesson, "q2", prompt="What reputational risk does Medea fear?",
                 correct="That people will say she disgraced her home for a stranger",
                 wrong=["That she will lose a contest for the throne of Athens", "That the crew will forget the route to Colchis"],
                 explanation="Her speech imagines being mocked for disgracing her home and parents while helping a stranger.",
                 refs=["dilemma"])
    touch(changes, lesson)

    lid = "grc.heroes.w04d04.flight-and-pursuit"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "main", "main", ARG, "Book 4",
              "And Jason went to the ambush to lie in wait for Apsyrtus",
              "Jason marked him and struck him down",
              "Argonautica 4, Jason kills Apsyrtus")
    set_quote(lesson, "purification", "main", ARG, "Book 4",
              "When Apsyrtus had fallen in mighty overthrow",
              "cleanse themselves from the terrible stain of blood",
              "Argonautica 4, Zeus orders purification")
    set_card(lesson, "card-01", body="In Apollonius' version, Medea and Jason plan an ambush; when Apsyrtus arrives, Jason strikes him down.", refs=["main"])
    set_card(lesson, "card-03", body="After the killing, the poem says Zeus orders the Argonauts to seek purification from Circe for the bloodshed.", refs=["purification"])
    set_question(lesson, "q2", prompt="Why does the return remain morally troubled in Apollonius?",
                 correct="Zeus orders purification after the killing of Apsyrtus",
                 wrong=["The Argonauts lose the Sampo", "The Trojans refuse to bury Hector"],
                 explanation="The poem connects the killing with Zeus' order that Circe purify the travelers.",
                 refs=["purification"])
    touch(changes, lesson)

    lid = "grc.heroes.w04d05.medea-on-stage"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "main", "main", BUCKLEY, "local text",
              "But now every thing is at variance",
              "having married the daughter of Creon, who is prince of this land.",
              "Medea, Nurse's opening account of Jason's new marriage")
    set_card(lesson, "card-01", body="Euripides begins in Corinth after the Argonautic voyage. The Nurse says Jason has married Creon's daughter while Medea is dishonored.", refs=["main"])
    set_card(lesson, "card-02", body="The Nurse's speech recalls the Argo and Medea's earlier help, then turns to the new marriage and Jason's broken obligations.", refs=["main"])
    touch(changes, lesson)

    lid = "grc.heroes.w05d02.the-nemean-lion"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "combat", "main", LIB, "book 2 · chapter 5 · section 1",
              "And having come to Nemea and tracked the lion",
              "held it tight till he had choked it",
              "Library 2.5.1, Heracles changes method")
    set_card(lesson, "card-01", body="The Library says arrows fail against the invulnerable lion; Heracles then controls the cave and fights at close range.", refs=["main", "combat"])
    set_card(lesson, "card-03", body="He blocks one cave entrance, enters through the other, and strangles the lion. The narrative stresses a change of method.", refs=["combat"])
    set_question(lesson, "q1", prompt="How does Heracles kill the Nemean lion in the Library?",
                 correct="He strangles it after controlling the cave",
                 wrong=["He poisons it with a pomegranate seed", "He tricks it into a ballgame"],
                 explanation="The source says Heracles blocks one entrance, enters through the other, and chokes the lion.",
                 refs=["combat"])
    set_question(lesson, "q2", prompt="Why does the cave matter to his method?",
                 correct="Blocking one entrance lets him approach through the other",
                 wrong=["It supplies a clue for the labyrinth", "It is where Eurystheus hides"],
                 explanation="The cave has two mouths; Heracles blocks one and enters through the other.",
                 refs=["combat"])
    touch(changes, lesson)

    lid = "grc.heroes.w06d01.the-road-to-athens"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_card(lesson, "card-01", body="Plutarch recounts a road encounter at Epidaurus: Periphetes carries a club and tries to stop Theseus from continuing.", refs=["main"])
    set_card(lesson, "card-03", body="Plutarch says Theseus defeats Periphetes and takes the club as his own weapon; this is one episode in a later biography.", refs=["main"])
    set_card(lesson, "card-04", body="This passage supports a claim about Plutarch's account, not eyewitness documentation of a historical journey.", refs=["main"])
    set_question(lesson, "q1", prompt="What weapon is associated with Periphetes in Plutarch's account?",
                 correct="A club",
                 wrong=["A bow made by Hephaestus", "A clue from Ariadne"],
                 explanation="Plutarch calls Periphetes the club-bearer because he uses a club.",
                 refs=["main"])
    set_question(lesson, "q2", prompt="What does Theseus do with Periphetes' club?",
                 correct="He takes it and carries it as his own weapon",
                 wrong=["He gives it to the Minotaur", "He buries it under the olive bed"],
                 explanation="Plutarch says Theseus takes the club and afterward carries it as his own weapon.",
                 refs=["main"])
    touch(changes, lesson)

    lid = "grc.heroes.w06d02.the-minotaur-and-ariadne"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "escape", "main", EPI, "chapter 1 · section 9",
              "And at his suggestion she gave Theseus a clue",
              "drawing the clue after him made his way out again.",
              "Epitome 1.9, Ariadne's clue and Theseus' escape")
    set_card(lesson, "card-01", body="In the Epitome, Ariadne asks Daedalus how Theseus can leave the labyrinth and gives him a clue to follow.", refs=["main", "escape"])
    set_card(lesson, "card-03", body="The Epitome says Theseus kills the Minotaur and draws the clue after him to find his way out; it does not specify 'thread' in this passage.", refs=["escape"])
    set_question(lesson, "q1", prompt="What does Ariadne give Theseus in the Epitome?",
                 correct="A clue to help him find the way out",
                 wrong=["A magic sword", "A golden apple"],
                 explanation="The Epitome calls it a clue and says Theseus draws it after him to escape.",
                 refs=["escape"])
    touch(changes, lesson)

    lid = "grc.heroes.w06d05.the-civic-hero"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "heracles", "heracles", LIB, "book 2 · chapter 4 · section 12",
              "The Pythian priestess then first called him Hercules",
              "perform the ten labours imposed on him",
              "Library 2.4.12, oracle assigns service")
    set_card(lesson, "card-03", body="The Library says the Pythian priestess directs Heracles to serve Eurystheus for twelve years and perform ten labours; Plutarch separately credits Theseus with unifying Attica.", refs=["main", "heracles"])
    set_question(lesson, "q1", prompt="Which pairing fits the cited works?",
                 correct="Plutarch's Theseus unites Attica; the Library's Heracles serves Eurystheus",
                 wrong=["The Iliad's Achilles founds Athens; Pindar's Theron fights the Hydra", "Ovid's Theseus kills the Minotaur; Plutarch's Heracles becomes king of Crete"],
                 explanation="Plutarch describes Theseus' civic role; the Library gives Heracles' service and labours.",
                 refs=["main", "heracles"])
    touch(changes, lesson)

    lid = "grc.heroes.w07d01.agamemnon-returns"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "main", "main", AES, "local text",
              "I pray the gods to quit me of my toils",
              "such fiery message gleams",
              "Agamemnon, the Watchman waits for the beacon")
    set_quote(lesson, "murder", "main", AES, "local text",
              "By me he fell, by me he died",
              "And now his burial rites be mine!",
              "Agamemnon, Clytemnestra confesses")
    # The Odyssey comparison is cited separately rather than being inferred
    # from the Aeschylus passage alone.
    lesson["sourceReferences"]["odyssey"] = quote_ref(
        {
            "recordId": "pg-01727", "sourceId": "grc.homer.odyssey",
            "work": "The Odyssey", "author": "Homer", "translator": "Samuel Butler",
            "localPath": "content/corpus/greek/primary/homer-odyssey-1727.txt",
        }, OD, "Book 23", "When she heard the sure proofs Ulysses now gave her",
        "you have convinced me by showing that you know all about our bed",
        "Odyssey 23, Odysseus and Penelope reunite",
    )
    set_card(lesson, "card-01", body="The Watchman awaits a beacon announcing Troy's fall. Aeschylus later gives Clytemnestra's account of killing Agamemnon.", refs=["main", "murder"])
    set_card(lesson, "card-02", refs=["main"])
    set_card(lesson, "card-03", refs=["murder", "odyssey"])
    set_question(lesson, "q1", prompt="What signal does the Watchman await?",
                 correct="A beacon announcing Troy's fall",
                 wrong=["A raven carrying news from Ithaca", "A messenger returning the Golden Fleece"],
                 explanation="The Watchman says the beacon will announce Ilion's fall.",
                 refs=["main"])
    set_question(lesson, "q2", prompt="Who claims responsibility for Agamemnon's death in the play?",
                 correct="Clytemnestra",
                 wrong=["The Watchman", "The Trojan women"],
                 explanation="Clytemnestra says, 'By me he fell, by me he died.'",
                 refs=["murder"])
    touch(changes, lesson)

    lid = "grc.heroes.w07d02.orestes-and-justice"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "court", "main", AES, "local text",
              "Here to all time for Aegeus",
              "Here the tribunal, set on Ares",
              "Eumenides, Athena establishes the court")
    set_card(lesson, "card-01", refs=["main", "court"])
    set_card(lesson, "card-03", body="Athena establishes a council-court for future cases. The Erinyes remain part of the settlement, so the play does not simply remove divine claims from justice.", refs=["court"])
    set_question(lesson, "q2", prompt="What changes in the handling of Orestes' conflict?",
                 correct="Athena establishes a court to hear claims instead of another killing",
                 wrong=["The Erinyes leave before judgment", "Orestes is sent to fight Hector"],
                 explanation="Athena announces a council-court on Ares' Hill while the divine figures remain part of the play's outcome.",
                 refs=["court"])
    touch(changes, lesson)

    lid = "grc.heroes.w07d03.antigone-and-burial"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "defense", "main", SOP, "local text",
              "Nor did I deem that thou, a mortal man",
              "They die not; and none knoweth whence they sprang.",
              "Antigone, defense of divine laws")
    set_card(lesson, "card-01", refs=["main", "defense"])
    set_card(lesson, "card-03", body="Antigone says she follows unwritten divine laws rather than a mortal decree; the play stages the conflict and its consequences.", refs=["defense"])
    set_question(lesson, "q2", prompt="What reason does Antigone give for burying Polyneices?",
                 correct="She follows unwritten divine laws that a mortal decree cannot erase",
                 wrong=["Creon secretly ordered her to bury him", "She wants to claim the throne of Thebes"],
                 explanation="Antigone says a mortal man's decree cannot override the unwritten laws of heaven.",
                 refs=["defense"])
    touch(changes, lesson)

    lid = "grc.heroes.w07d04.oedipus-investigates"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "revelation", "main", SOP, "local text",
              "Friend, he that stands before thee was that child.",
              "I did; and would that I had died that day!",
              "Oedipus the King, the herdsman confirms the foundling")
    set_card(lesson, "card-01", refs=["main", "revelation"])
    set_card(lesson, "card-03", body="The messenger connects Oedipus with the infant given away by Laius' household; the herdsman confirms he passed the child on.", refs=["revelation"])
    set_question(lesson, "q2", prompt="What does the herdsman's testimony confirm?",
                 correct="Oedipus was the child passed from Laius' household to the messenger",
                 wrong=["Oedipus commanded the Trojan army", "Oedipus founded the Argo"],
                 explanation="The messenger identifies Oedipus as the child, and the herdsman confirms giving him away.",
                 refs=["revelation"])
    touch(changes, lesson)

    lid = "grc.heroes.w08d01.persephone-descends"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "agreement", "main", HYMNS, "local text",
              "has agreed that for a third part of the circling year",
              "with you and the other deathless gods",
              "Homeric Hymn to Demeter, return agreement")
    set_card(lesson, "card-01", refs=["main", "agreement"])
    set_card(lesson, "card-03", body="The hymn's settlement says Persephone spends a third of the year below and two thirds with Demeter and the other gods.", refs=["agreement"])
    set_question(lesson, "q2", prompt="Why is Persephone's return not unconditional?",
                 correct="The hymn assigns her part of the year below and the rest with Demeter",
                 wrong=["She refuses to eat any pomegranate", "Hermes takes her to Crete"],
                 explanation="The settlement gives Persephone one third of the year below and two thirds above.",
                 refs=["agreement"])
    touch(changes, lesson)

    lid = "grc.heroes.w08d04.heroes-in-landscape"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "main", "main", FRAZER, "local text",
              "This is nearly a direct affirmation that the region about Mount Sipylus in Lydia was his native land.",
              "the bereaved Niobe weeping for her children.",
              "Frazer's discussion of Pausanias and Mount Sipylus")
    set_card(lesson, "card-01", refs=["main"])
    set_question(lesson, "q1", prompt="Whose observations does Frazer discuss in this passage?",
                 correct="Pausanias' accounts of Mount Sipylus and its monuments",
                 wrong=["Homer's description of Achilles' armour", "Ovid's account of the Argo"],
                 explanation="Frazer's passage explicitly discusses Pausanias' descriptions of monuments and scenery near Sipylus.",
                 refs=["main"])
    touch(changes, lesson)

    lid = "grc.heroes.w08d05.four-heroic-models"
    lesson = json.loads(lesson_path(lid).read_text(encoding="utf-8"))
    set_quote(lesson, "heracles", "heracles", LIB, "book 2 · chapter 4 · section 12",
              "The Pythian priestess then first called him Hercules",
              "perform the ten labours imposed on him",
              "Library 2.4.12, oracle assigns service")
    set_card(lesson, "card-01", refs=["main", "heracles", "odysseus", "theseus"])
    set_card(lesson, "card-03", refs=["main", "heracles", "odysseus", "theseus"])
    set_card(lesson, "card-04", refs=["main", "heracles", "odysseus", "theseus"])
    set_question(lesson, "q1", prompt="Which pairing fits the cited works?",
                 correct="Achilles receives Priam; Heracles receives an oracle assigning service",
                 wrong=["Odysseus creates Attic democracy; Theseus kills the Nemean lion", "Achilles receives the Sampo; Heracles wins the Argo"],
                 explanation="The Iliad depicts Priam's appeal; the Library gives Heracles the oracle's service and labour instructions.",
                 refs=["main", "heracles"])
    touch(changes, lesson)

    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", metavar="INPUT_SHA256")
    args = parser.parse_args()
    paths = sorted((ROOT / "content/lessons/greek").rglob("*.json"))
    digest = hashlib.sha256(b"".join(path.read_bytes() for path in paths)).hexdigest()
    changes = build()
    print("Input SHA256:", digest)
    print(f"Prepared source-relevance repairs for {len(changes)} Greek lessons; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        for path, lesson in changes.items():
            path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied once.")


if __name__ == "__main__":
    main()

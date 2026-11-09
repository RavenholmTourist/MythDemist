"""Preview-first repair of source relevance and quiz evidence in the Greek programme."""
import argparse
import hashlib
import json
import re
from pathlib import Path

from source_evidence import source_segments

ROOT = Path(__file__).resolve().parents[1]
P = "content/corpus/greek/primary/"


def find_lesson(lesson_id):
    return next(
        path for path in (ROOT / "content/lessons/greek").rglob("*.json")
        if json.loads(path.read_text(encoding="utf-8"))["id"] == lesson_id
    )


def quote_ref(base, path, segment_name, start, end, label):
    segment = next(
        item for item in source_segments(path)
        if item["locator"] == segment_name and item["evidenceType"] == "source-text"
    )
    first = segment["text"].casefold().find(start.casefold())
    last = segment["text"].casefold().find(end.casefold(), first + len(start)) if first >= 0 else -1
    if first < 0 or last < 0:
        raise ValueError(f"Could not anchor {label}: {start!r} ... {end!r}")
    last += len(end)
    ref = dict(base)
    ref["locator"] = f"{label}; {segment_name}, normalized characters {first}-{last}"
    ref["excerpt"] = segment["text"][first:last]
    ref["evidenceType"] = "quotation"
    ref["note"] = "Verbatim passage in the named work and translation; locator selects this exact local narrative passage."
    return ref


def put_ref(lesson, key, base_key, path, segment, start, end, label):
    base = lesson["sourceReferences"][base_key]
    lesson["sourceReferences"][key] = quote_ref(base, ROOT / path, segment, start, end, label)


def put_block(lesson, block_id, body=None, refs=None, title=None):
    block = next(item for item in lesson["narrativeBlocks"] if item["id"] == block_id)
    if body is not None:
        block["body"] = body
    if refs is not None:
        block["sourceRefIds"] = refs
    if title is not None:
        block["title"] = title


def put_question(lesson, qid, prompt, correct, wrong, explanation, refs, shift=0):
    question = next(item for item in lesson["quiz"] if item["id"] == qid)
    values = [correct, *wrong]
    shift %= len(values)
    values = values[shift:] + values[:shift]
    choices = [{"id": chr(97 + index), "text": text} for index, text in enumerate(values)]
    question.update({
        "prompt": prompt,
        "choices": choices,
        "answerId": next(item["id"] for item in choices if item["text"] == correct),
        "explanation": explanation,
        "sourceRefIds": refs,
    })
    if "deepDive" in question:
        question["deepDive"]["sourceRefIds"] = refs


def build():
    changes = {}

    # Week 2: make each question point to the exact speech/scene it tests.
    path = find_lesson("grc.heroes.w02d01.the-quarrel-and-the-ransom")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(
        lesson, "main", "main", P + "homer-iliad-2199.txt", "Book 1",
        "It was the son of Jove and Leto",
        "I will not free her.",
        "Iliad 1, Chryses petitions and Agamemnon refuses",
    )
    put_block(lesson, "card-02", "Source quotation from Butler's translation (whitespace normalized): “" + lesson["sourceReferences"]["main"]["excerpt"] + "”")
    changes[path] = lesson

    path = find_lesson("grc.heroes.w02d02.briseis-and-withdrawal")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "iliad", "main", P + "homer-iliad-2199.txt", "Book 1",
            "since Phoebus Apollo is taking Chryseis from me",
            "fear to set himself up as equal or comparable with me.",
            "Iliad 1, Agamemnon threatens to take Briseis")
    put_ref(lesson, "restraint", "iliad", P + "homer-iliad-2199.txt", "Book 1",
            "The son of Peleus was furious",
            "Cease, then, this brawling, and do not draw your sword",
            "Iliad 1, Athena restrains Achilles")
    put_ref(lesson, "aftermath", "iliad", P + "homer-iliad-2199.txt", "Book 1",
            "Then Achilles went all alone by the side of the hoar sea",
            "and his mother heard him",
            "Iliad 1, Achilles appeals to Thetis")
    put_block(lesson, "card-01", "Agamemnon threatens to return Chryseis but take Briseis from Achilles instead. The quarrel concerns public rank and the treatment of captives.", refs=["iliad"])
    put_block(lesson, "card-03", "Achilles considers drawing his sword against Agamemnon. Athena appears and tells him not to draw it.", refs=["restraint"])
    put_block(lesson, "card-04", "After the heralds take Briseis, Achilles goes alone to the seashore, weeps, and calls on Thetis.", refs=["aftermath"])
    put_question(lesson, "q2", "What does Achilles do after Briseis is taken?", "He goes to the seashore and calls on Thetis", ["He accepts Agamemnon's offer and returns to battle", "He sails at once to Crete"], "The poem says Achilles goes alone to the sea and prays to his mother after the seizure.", ["aftermath"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w02d03.the-embassy-fails")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "offer", "main", P + "homer-iliad-2199.txt", "Book 9",
            "will make amends, and will give him great gifts by way of atonement",
            "I will give him these, and with them her whom I erewhile took from him, the daughter of Briseus;",
            "Iliad 9, Agamemnon lists gifts for Achilles")
    put_block(lesson, "card-01", refs=["offer", "main"])
    put_question(lesson, "q1", "What does Agamemnon offer Achilles through the embassy?", "Gifts, including Briseis, if he returns to battle", ["The throne of Ithaca", "A place among the gods"], "Agamemnon's speech lists material gifts and Briseis as part of his offer.", ["offer"], 1)
    put_question(lesson, "q2", "How does Achilles answer the embassy?", "He says Agamemnon and the Danaans will not appease him", ["He accepts the gifts immediately", "He asks Odysseus to lead the Myrmidons"], "Achilles says he will not be appeased by Agamemnon or the other Danaans.", ["main"], 2)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w02d05.priam-and-achilles")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "release", "main", P + "homer-iliad-2199.txt", "Book 24",
            "O king, bid me not be seated",
            "I am of myself minded to give up the body of Hector.",
            "Iliad 24, Priam asks for Hector and Achilles agrees")
    put_block(lesson, "card-01", refs=["main", "release"])
    put_block(lesson, "card-03", "Priam asks Achilles to accept a ransom and return Hector's body. Achilles says he is already minded to give it up.", refs=["release"])
    put_question(lesson, "q1", "What does Priam ask Achilles to return?", "Hector's body", ["Briseis", "The armor of Patroclus"], "Priam asks Achilles to give him Hector's body in exchange for ransom.", ["release"], 1)
    changes[path] = lesson

    # Week 3: suitor pressure and Odysseus' later name-reveal need separate
    # narrative passages from the household feast and the false-name exchange.
    path = find_lesson("grc.heroes.w03d01.the-broken-house")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "pressure", "main", P + "homer-odyssey-1727.txt", "Book 1",
            "the chiefs from all our islands",
            "before long will do so also with myself.",
            "Odyssey 1, Telemachus describes the suitors' pressure")
    put_block(lesson, "card-01", "Odysseus is absent while suitors eat his household's food and court Penelope, who has not agreed to marry one of them.", refs=["main", "pressure"])
    put_question(lesson, "q1", "What do the suitors do in Odysseus' hall?", "They sit down and eat the household's food", ["They escort Odysseus home", "They guard the house from the Trojans"], "The passage describes the suitors taking their places and eating the household's food.", ["main"], 2)
    put_question(lesson, "q2", "Why does Telemachus call the suitors a threat to his household?", "They consume his property while pressuring his mother to marry", ["They have taken the household to Troy", "They are protecting the estate for Odysseus"], "Telemachus says the suitors eat up his house, press his mother, and make havoc of his estate.", ["pressure"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w03d02.nobody-and-the-cyclops")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "boast", "main", P + "homer-odyssey-1727.txt", "Book 9",
            "Cyclops, if any one asks you who it was that put your eye out",
            "who lives in Ithaca.",
            "Odyssey 9, Odysseus reveals his name to Polyphemus")
    put_ref(lesson, "curse", "main", P + "homer-odyssey-1727.txt", "Book 9",
            "On this he lifted up his hands to the firmament of heaven and prayed",
            "if I am indeed your own true begotten son, grant that Ulysses may never reach his home alive",
            "Odyssey 9, Polyphemus prays to Poseidon")
    put_block(lesson, "card-04", refs=["boast", "curse"])
    put_question(lesson, "q2", "What follows Odysseus' boast of his real name?", "Polyphemus prays to Poseidon to keep him from reaching home", ["The Cyclops agrees to guide the ship", "Athena immediately brings the crew to Ithaca"], "After Odysseus names himself, Polyphemus raises his hands and prays to Poseidon.", ["boast", "curse"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w03d03.circe-and-the-sirens")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_question(lesson, "q2", "What must the crew do if Odysseus begs to be released?", "Bind him more tightly to the mast", ["Let him steer toward the Sirens", "Remove the wax from their ears"], "Circe anticipates that Odysseus will ask to be freed and tells the crew to bind him faster.", ["main"], 2)
    changes[path] = lesson

    # Week 4: distinguish the quest's political commission, Aeetes' task,
    # Medea's deliberation, and Apollonius' account of Apsyrtus.
    path = find_lesson("grc.heroes.w04d01.the-political-quest")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "main", "main", P + "apollonius-argonautica-0830.txt", "Book 1",
            "who, at the behest of King Pelias",
            "devised for him the toil of a troublous voyage, in order that on the sea or among strangers he might lose his home-return.",
            "Argonautica 1, Pelias' commission and Jason's sign")
    put_block(lesson, "card-01", "The proem says the Argo sails at King Pelias' behest. When Jason arrives with one sandal, Pelias devises a dangerous voyage for him.", refs=["main"])
    put_question(lesson, "q1", "What does Pelias do after Jason arrives with one sandal?", "He devises a dangerous voyage that may keep Jason from returning", ["He appoints Jason king of Iolcus", "He sends Medea to Athens"], "The passage links the one-sandal prophecy with Pelias devising a dangerous voyage for Jason.", ["main"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w04d02.aeetes-and-the-tasks")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "main", "main", P + "apollonius-argonautica-0830.txt", "Book 3",
            "Two bulls with feet of bronze I have",
            "I will not give it, expect it not.",
            "Argonautica 3, Aeetes sets the trial")
    put_ref(lesson, "aid", "main", P + "apollonius-argonautica-0830.txt", "Book 3",
            "And at dawn steep this charm in water",
            "nor the flame of the deadly bulls as it rushes forth resistless.",
            "Argonautica 3, Medea explains the charm")
    put_block(lesson, "card-01", "Aeetes orders Jason to yoke bronze bulls, plough four fields, and sow serpent's teeth before he will give up the fleece.", refs=["main"])
    put_block(lesson, "card-03", "Medea explains how to use a charm that gives Jason strength and protects him from the bronze spearpoints and the bulls' fire.", refs=["aid"])
    put_question(lesson, "q2", "What protection does Medea instruct Jason to use?", "A charm to anoint his body and sprinkle on his weapons", ["A thread to mark the labyrinth", "A shield made by Daedalus"], "Medea tells him to steep the charm in water, anoint himself, and sprinkle his weapons.", ["aid"], 2)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w04d03.medea-chooses")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "main", "main", P + "apollonius-argonautica-0830.txt", "Book 3",
            "the bolt burnt deep down",
            "her heart panted fast through anguish",
            "Argonautica 3, Eros' arrow strikes Medea")
    put_ref(lesson, "dilemma", "main", P + "apollonius-argonautica-0830.txt", "Book 3",
            "And she thought now that she would give him the charms",
            "the maid who disgraced her home and her parents, yielding to a mad passion.",
            "Argonautica 3, Medea debates helping Jason")
    put_ref(lesson, "aid", "main", P + "apollonius-argonautica-0830.txt", "Book 3",
            "And forth from her fragrant girdle ungrudgingly she brought out the charm",
            "he at once received it in his hands with joy",
            "Argonautica 3, Medea gives Jason the charm")
    put_block(lesson, "card-01", "Apollonius describes Eros' arrow striking Medea, then narrates her wakeful conflict about aiding Jason without her parents' knowledge.", refs=["main", "dilemma"])
    put_block(lesson, "card-03", "Medea fears shame and the reaction of her household, yet she resolves to provide the charms that can help Jason.", refs=["dilemma"])
    put_block(lesson, "card-04", "The episode holds together divine pressure, Medea's deliberation, and her later action; it is not a simple picture of either total freedom or total passivity.", refs=["main", "dilemma", "aid"])
    put_question(lesson, "q1", "What does Medea debate doing in her inner speech?", "Giving Jason the charms or refusing to help him", ["Returning the fleece to Pelias", "Asking Athena to take her to Ithaca"], "Medea explicitly considers giving the charms and then not giving them.", ["dilemma"], 1)
    put_question(lesson, "q2", "What reputational risk does Medea fear?", "That people will say she disgraced her home for a stranger", ["That she will lose a contest for the throne of Athens", "That the crew will forget the route to Colchis"], "Her speech imagines being mocked for disgracing her home and parents while helping a stranger.", ["dilemma"], 2)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w04d04.flight-and-pursuit")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "main", "main", P + "apollonius-argonautica-0830.txt", "Book 4",
            "And Jason went to the ambush to lie in wait for Apsyrtus",
            "Jason marked him and struck him down",
            "Argonautica 4, Jason kills Apsyrtus")
    put_ref(lesson, "purification", "main", P + "apollonius-argonautica-0830.txt", "Book 4",
            "When Apsyrtus had fallen in mighty overthrow",
            "cleanse themselves from the terrible stain of blood",
            "Argonautica 4, Zeus orders purification")
    put_block(lesson, "card-01", "In Apollonius' version, Medea and Jason plan an ambush; when Apsyrtus arrives, Jason strikes him down.", refs=["main"])
    put_block(lesson, "card-03", "After the killing, the narrative says Zeus orders the Argonauts to seek purification from Circe for the bloodshed.", refs=["purification"])
    put_question(lesson, "q2", "Why does the return journey remain morally troubled in Apollonius?", "Zeus orders purification after the killing of Apsyrtus", ["The Argonauts have lost the Sampo", "The Trojans refuse to bury Hector"], "The poem connects the killing with Zeus' order that Circe purify the travelers.", ["purification"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w04d05.medea-on-stage")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "main", "main", P + "euripides-buckley-volume-i-15081.txt", "local text",
            "But now every thing is at variance",
            "having married the daughter of Creon, who is prince of this land.",
            "Medea, Nurse's opening account of Jason's new marriage")
    put_block(lesson, "card-01", "Euripides begins in Corinth after the Argonautic voyage. The Nurse says Jason has married Creon's daughter while Medea is dishonored.", refs=["main"])
    put_block(lesson, "card-02", "The Nurse's speech recalls the Argo and Medea's earlier help, then turns to the new marriage and Jason's broken obligations.", refs=["main"])
    changes[path] = lesson

    # Week 5: cite the actual combat method, not only the order to fetch the lion.
    path = find_lesson("grc.heroes.w05d02.the-nemean-lion")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "combat", "main", P + "apollodorus-library-frazer-perseus-eng2.xml",
            "book 2 · chapter 5 · section 1",
            "And having come to Nemea and tracked the lion",
            "held it tight till he had choked it",
            "Library 2.5.1, Heracles changes method")
    put_block(lesson, "card-01", "In the Library's account, arrows fail against the invulnerable lion; Heracles then controls the cave and fights at close range.", refs=["main", "combat"])
    put_block(lesson, "card-03", "He blocks one cave entrance, enters through the other, and strangles the lion. The narrative stresses a change of method.", refs=["combat"])
    put_question(lesson, "q1", "How does Heracles kill the Nemean lion in the Library?", "He strangles it after controlling the cave", ["He poisons it with a pomegranate seed", "He tricks it into a ballgame"], "The source says Heracles blocks one entrance, enters through the other, and chokes the lion.", ["combat"], 1)
    put_question(lesson, "q2", "Why does the cave matter to his method?", "Blocking one entrance lets him approach through the other", ["It supplies a thread for the escape", "It is where Eurystheus hides"], "The cave has two mouths; Heracles blocks one and enters through the other.", ["combat"], 2)
    changes[path] = lesson

    # Week 6: keep the Theseus passage narrow, and do not convert the Epitome's
    # "clue" into the later explanatory note's specific thread.
    path = find_lesson("grc.heroes.w06d01.the-road-to-athens")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_block(lesson, "card-01", "Plutarch recounts a road encounter at Epidaurus: Periphetes carries a club and tries to stop Theseus from continuing.", refs=["main"])
    put_block(lesson, "card-03", "The passage says Theseus defeats Periphetes and takes the club as his own weapon; Plutarch presents this as part of a later biography.", refs=["main"])
    put_block(lesson, "card-04", "This one episode supports a claim about Plutarch's account, not eyewitness documentation of a historical journey.", refs=["main"])
    put_question(lesson, "q1", "What weapon is associated with Periphetes in Plutarch's account?", "A club", ["A bow made by Hephaestus", "A thread from Ariadne"], "Plutarch calls Periphetes the club-bearer because he uses a club.", ["main"], 1)
    put_question(lesson, "q2", "What does Theseus do with Periphetes' club?", "He takes it and carries it as his own weapon", ["He gives it to the Minotaur", "He buries it under the olive bed"], "Plutarch says Theseus takes the club and afterward carries it as his own weapon.", ["main"], 2)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w06d02.the-minotaur-and-ariadne")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "escape", "main", P + "apollodorus-epitome-frazer-perseus-eng2.xml",
            "chapter 1 · section 9",
            "And at his suggestion she gave Theseus a clue",
            "drawing the clue after him made his way out again.",
            "Epitome 1.9, Ariadne's clue and Theseus' escape")
    put_block(lesson, "card-01", "In the Epitome, Ariadne asks Daedalus how Theseus can leave the labyrinth and gives him a clue to follow.", refs=["main", "escape"])
    put_block(lesson, "card-03", "The Epitome says Theseus kills the Minotaur and draws the clue after him to find his way out; it does not specify 'thread' in this passage.", refs=["escape"])
    put_question(lesson, "q1", "What does Ariadne give Theseus in the Epitome?", "A clue to help him find the way out", ["A magic sword", "A golden apple"], "The Epitome calls it a clue and says Theseus draws it after him to escape.", ["escape"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w06d05.the-civic-hero")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "heracles", "heracles", P + "apollodorus-library-frazer-perseus-eng2.xml",
            "book 2 · chapter 4 · section 12",
            "The Pythian priestess then first called him Hercules",
            "perform the ten labours imposed on him",
            "Library 2.4.12, the oracle assigns service and labours")
    put_block(lesson, "card-01", refs=["main", "heracles"])
    put_block(lesson, "card-03", "The Library's account says the Pythian priestess directs Heracles to serve Eurystheus for twelve years and perform ten labours; Plutarch separately credits Theseus with unifying Attica.", refs=["main", "heracles"])
    put_block(lesson, "card-04", refs=["main", "heracles"])
    put_question(lesson, "q1", "Which pairing fits the cited accounts?", "Plutarch's Theseus unites Attica; the Library's Heracles serves Eurystheus", ["The Iliad's Achilles founds Athens; Pindar's Theron fights the Hydra", "Ovid's Theseus kills the Minotaur; Plutarch's Heracles becomes king of Crete"], ["The cited works describe different roles: Plutarch's civic foundation and the Library's imposed service.", "The cited works describe different roles: Plutarch's civic foundation and the Library's imposed service.", "The cited works describe different roles: Plutarch's civic foundation and the Library's imposed service."][0], ["main", "heracles"], 1)
    changes[path] = lesson

    # Week 7: link each interpretation to a line from the actual play, not only
    # to a decree, accusation, or argument that begins the scene.
    path = find_lesson("grc.heroes.w07d01.agamemnon-returns")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "main", "main", P + "aeschylus-house-of-atreus-8604.txt", "local text",
            "I pray the gods to quit me of my toils",
            "such fiery message gleams",
            "Agamemnon, the Watchman waits for the beacon")
    put_ref(lesson, "murder", "main", P + "aeschylus-house-of-atreus-8604.txt", "local text",
            "By me he fell, by me he died",
            "And now his burial rites be mine!",
            "Agamemnon, Clytemnestra confesses")
    put_block(lesson, "card-01", "The Watchman waits for the beacon announcing Troy's fall. The play later gives Clytemnestra's account of killing Agamemnon.", refs=["main", "murder"])
    put_block(lesson, "card-03", refs=["main", "murder"])
    put_question(lesson, "q2", "Who claims responsibility for Agamemnon's death in the play?", "Clytemnestra", ["The Watchman", "The Trojan women"], "Clytemnestra says, 'By me he fell, by me he died.'", ["murder"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w07d02.orestes-and-justice")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "court", "main", P + "aeschylus-house-of-atreus-8604.txt", "local text",
            "Here to all time for Aegeus",
            "Here the tribunal, set on Ares",
            "Eumenides, Athena establishes the court")
    put_block(lesson, "card-01", refs=["main", "court"])
    put_block(lesson, "card-03", "Athena establishes a council-court for future cases. The Erinyes remain present in the settlement, so the play does not simply remove divine claims from justice.", refs=["court"])
    put_question(lesson, "q2", "What changes in the handling of the conflict?", "Athena establishes a court to hear claims instead of another killing", ["The Erinyes leave the play before judgment", "Orestes is sent to fight Hector"], "Athena announces a council-court at the Areopagus; the play's divine figures remain part of the outcome.", ["court"], 2)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w07d03.antigone-and-burial")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "defense", "main", P + "sophocles-theban-plays-0031.txt", "local text",
            "Nor did I deem that thou, a mortal man",
            "They die not; and none knoweth whence they sprang.",
            "Antigone, defense of divine laws")
    put_block(lesson, "card-01", refs=["main", "defense"])
    put_block(lesson, "card-03", "Antigone says she follows unwritten divine laws rather than a mortal decree; the play stages the conflict and its consequences.", refs=["defense"])
    put_question(lesson, "q2", "What reason does Antigone give for burying Polyneices?", "She follows unwritten divine laws that a mortal decree cannot erase", ["She says Creon ordered her to do it", "She wants to claim the throne of Thebes"], "Antigone says she did not think a mortal man's decree could override the unwritten laws of heaven.", ["defense"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w07d04.oedipus-investigates")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "revelation", "main", P + "sophocles-theban-plays-0031.txt", "local text",
            "Friend, he that stands before thee was that child.",
            "I did; and would that I had died that day!",
            "Oedipus the King, the herdsman confirms the foundling")
    put_block(lesson, "card-01", refs=["main", "revelation"])
    put_block(lesson, "card-03", "The investigation connects the foundling raised in Corinth to the child exposed by Laius' household; Oedipus learns that the inquiry implicates him.", refs=["revelation"])
    put_question(lesson, "q2", "What does the herdsman's testimony reveal?", "Oedipus was the child given away by Laius' household", ["Oedipus founded the Argo", "Oedipus has already left Thebes"], "The messenger identifies Oedipus as the child he received, and the herdsman confirms giving him away.", ["revelation"], 2)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w08d01.persephone-descends")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "agreement", "main", P + "hesiod-homeric-hymns-homerica-0348.txt", "local text",
            "has agreed that for a third part of the circling year",
            "but for the two parts shall be with you and the other deathless gods",
            "Homeric Hymn to Demeter, the year is divided")
    put_block(lesson, "card-01", refs=["main", "agreement"])
    put_block(lesson, "card-03", "The hymn's settlement says Persephone spends a third of the year below and two thirds with Demeter and the other gods.", refs=["agreement"])
    put_question(lesson, "q2", "Why is Persephone's return not unconditional?", "The hymn assigns her part of the year below and the rest with Demeter", ["She refuses to eat any pomegranate", "Hermes takes her to Crete"], "The agreement assigns one third of the year below and two thirds above.", ["agreement"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w08d04.heroes-in-landscape")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "main", "main", "content/corpus/greek/scholarship/frazer-greek-scenery-legend-history-56002.txt",
            "local text",
            "This is nearly a direct affirmation that the region about Mount Sipylus in Lydia was his native land.",
            "the dripping rock which popular fancy took for the bereaved Niobe weeping for her children.",
            "Frazer's discussion of Pausanias and Mount Sipylus")
    put_block(lesson, "card-01", refs=["main"])
    put_question(lesson, "q1", "Whose writing is Frazer discussing in this passage?", "Pausanias' account of monuments and scenery near Mount Sipylus", ["Ovid's description of Ariadne's crown", "Homer's account of Achilles' armour"], "Frazer explicitly discusses Pausanias' descriptions of Sipylus and associated monuments.", ["main"], 1)
    changes[path] = lesson

    path = find_lesson("grc.heroes.w08d05.four-heroic-models")
    lesson = json.loads(path.read_text(encoding="utf-8"))
    put_ref(lesson, "heracles", "heracles", P + "apollodorus-library-frazer-perseus-eng2.xml",
            "book 2 · chapter 4 · section 12",
            "The Pythian priestess then first called him Hercules",
            "perform the ten labours imposed on him",
            "Library 2.4.12, oracle assigns service")
    put_block(lesson, "card-01", refs=["main", "heracles", "odysseus", "theseus"])
    put_block(lesson, "card-03", refs=["main", "heracles", "odysseus", "theseus"])
    put_block(lesson, "card-04", refs=["main", "heracles", "odysseus", "theseus"])
    put_question(lesson, "q1", "Which pairing fits the cited works?", "Achilles receives Priam; Heracles receives an oracle assigning service", ["Odysseus creates Attic democracy; Theseus kills the Nemean lion", "Achilles receives the Sampo; Heracles wins the Argo"], "The Iliad depicts Priam's appeal; the Library describes the oracle's instructions to Heracles.", ["main", "heracles"], 1)
    changes[path] = lesson

    # Fix excerpt offsets after the Homer parser removed book summaries. These
    # locator-only updates do not alter a claim's meaning.
    for path in sorted((ROOT / "content/lessons/greek").rglob("*.json")):
        lesson = changes.get(path) or json.loads(path.read_text(encoding="utf-8"))
        touched = False
        for ref in lesson["sourceReferences"].values():
            local = ref.get("localPath", "")
            if not (local.endswith("homer-iliad-2199.txt") or local.endswith("homer-odyssey-1727.txt")):
                continue
            match = re.search(r";\s*(Book \d+), normalized characters \d+-\d+$", ref["locator"])
            if not match:
                continue
            seg = next(s for s in source_segments(ROOT / local) if s["locator"] == match.group(1) and s["evidenceType"] == "source-text")
            first = seg["text"].find(ref["excerpt"])
            if first >= 0:
                ref["locator"] = f"{ref['locator'].split(';')[0]}; {match.group(1)}, normalized characters {first}-{first + len(ref['excerpt'])}"
                touched = True
        if touched or path in changes:
            lesson["version"] += 1
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
    print(f"Prepared source-support repairs for {len(changes)} Greek lessons; no files written.")
    if args.apply:
        if args.apply != digest:
            parser.error("Input digest changed; refusing to overwrite.")
        for path, lesson in changes.items():
            path.write_text(json.dumps(lesson, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("Applied source-support repairs.")


if __name__ == "__main__":
    main()

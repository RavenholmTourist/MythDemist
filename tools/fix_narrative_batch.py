"""Patch the 10 narrative-rewrite lessons: correct review shape + 2nd quiz question."""
import json, io

REVIEW = {"status": "reviewed", "reviewedBy": "Devin (AI editorial review)",
          "reviewedAt": "2026-11-24", "reviewType": "editorial",
          "notes": "AI editorial review by Devin on 2026-11-24: narrative-first rewrite; cards retell the story, verbatim source excerpts preserved, quiz answers checked against the retold material. This is not independent scholarly review or scholarly certification; specialist and community review remains recommended."}

def Q(prompt, right, wrongs, expl, obj):
    return {"id": "q2", "type": "single-choice", "prompt": prompt,
            "choices": [{"id": c, "text": t} for c, t in zip("abcd", [right] + wrongs)],
            "answerId": "a", "explanation": expl, "sourceRefIds": None, "objectiveIds": [obj]}

FILES = {
 "content/lessons/greek/greek-heroes/day-01-heroic-excellence.json": ("plutarch",
   Q("What did Aegeus hide under the rock at Troezen?",
     "His sword and sandals — tokens to prove Theseus's parentage when he was strong enough to lift it",
     ["A chest of gold for Theseus's inheritance", "A letter naming Theseus his heir", "His shield and spear"],
     "Aegeus hid his sword and sandals; Theseus lifts the rock at sixteen and takes the tokens to Athens.",
     "obj.theseus.tokens")),
 "content/lessons/greek/greek-heroes/day-02-achilles-anger.json": ("plutarch",
   Q("Which bandit forced travellers to wash his feet before kicking them off a cliff?",
     "Sciron — Theseus hurled him off the same rock at Megara",
     ["Sinis the Pine-Bender", "Periphetes the Club-Bearer", "Procrustes"],
     "Sciron made passers-by wash his feet, then kicked them into the sea where a turtle waited; Theseus threw him off the cliff.",
     "obj.road.bandits")),
 "content/lessons/greek/greek-heroes/day-03-odysseus-cunning.json": ("plutarch",
   Q("Why did Medea want Theseus poisoned?",
     "A true son of Aegeus would end her influence at court and her children's claim to inherit",
     ["Theseus had insulted her magic", "She was loyal to King Minos", "Aegeus ordered her to test him"],
     "Medea lived at Aegeus's court promising him an heir; a real son arriving meant she lost everything, so she framed Theseus as a spy and poisoned his cup.",
     "obj.medea.threat")),
 "content/lessons/greek/greek-heroes/day-04-jason-medea.json": ("plutarch",
   Q("Why were seven youths and seven maidens sent to Crete?",
     "As a tribute to King Minos — food for the Minotaur sealed inside Daedalus's labyrinth",
     ["To serve as hostages guaranteeing an alliance", "To train in Cretan schools", "To work the silver mines"],
     "Minos held Athens under a tribute: periodically fourteen youths were shipped to feed the Minotaur in the labyrinth.",
     "obj.mino.tribute")),
 "content/lessons/greek/greek-heroes/day-05-theseus-heracles.json": ("plutarch",
   Q("What did the white sail mean?",
     "That Theseus had survived — the crew was to swap the black sail for white on a successful return",
     ["That the ship carried no weapons", "That Minos had surrendered", "That Ariadne was aboard"],
     "White sail = Theseus lives, black = dead. The crew forgot to change it and Aegeus, seeing black, threw himself from the rock.",
     "obj.sails.signal")),
 "content/lessons/greek/heroes-programme/week-02-day-01-the-quarrel-and-the-ransom.json": ("main",
   Q("Why does Apollo send a plague on the Greek camp?",
     "Agamemnon refused and mocked the priest Chryses, who came to ransom his daughter Chryseis",
     ["The Greeks forgot a sacrifice before landing", "The Trojans stole Apollo's sacred tripod", "Achilles defiled a temple"],
     "Chryses came to ransom his daughter; Agamemnon's insult moved Apollo to plague the host for nine days.",
     "obj.plague.cause")),
 "content/lessons/greek/heroes-programme/week-02-day-02-briseis-and-withdrawal.json": ("main",
   Q("What stops Achilles from killing Agamemnon on the spot?",
     "Athena descends, seizes his hair, and orders restraint — promising the insult will be repaid threefold",
     ["Nestor talks him down before the army", "He decides killing a king would break the oath", "Agamemnon apologises first"],
     "Athena, visible only to Achilles, holds him back and promises the gods will repay the insult threefold.",
     "obj.withdraw.choice")),
 "content/lessons/greek/heroes-programme/week-02-day-03-the-embassy-fails.json": ("main",
   Q("What slight concession does Achilles finally make to the embassy?",
     "He will fight only when the Trojan fire reaches his own ships",
     ["He accepts Briseis back but not the gold", "He agrees to fight if Agamemnon asks in person", "He lends his armour to any volunteer"],
     "Phoenix's and Ajax's pleas shift him only to this: he fights when the battle reaches his own ships.",
     "obj.embassy.refusal")),
 "content/lessons/greek/heroes-programme/week-02-day-04-patroclus-changes-everything.json": ("main",
   Q("What warning does Achilles give Patroclus before lending his armour?",
     "Drive the Trojans from the ships, then come back — do not press on to the walls of Troy",
     ["Do not remove the helmet or the disguise will fail", "Do not fight Hector under any circumstances", "Return before nightfall or the Myrmidons retreat"],
     "Achilles tells Patroclus to repel the Trojans and return; Patroclus ignores it, presses to the walls, and is killed by Apollo and Hector.",
     "obj.patroclus.deal")),
 "content/lessons/greek/heroes-programme/week-02-day-05-priam-and-achilles.json": ("main",
   Q("How does Achilles treat Hector's body before Priam's visit?",
     "He drags it behind his chariot around Patroclus's tomb, day after day",
     ["He burns it on a pyre immediately", "He hangs it from the camp walls", "He sinks it in the river Scamander"],
     "Achilles pierces Hector's ankles and drags the body around Patroclus's tomb until Priam's ransom mission moves him.",
     "obj.priam.grief")),
}

for path, (ref, q) in FILES.items():
    d = json.load(io.open(path, encoding='utf-8'))
    d['review'] = dict(REVIEW, notes=REVIEW['notes'])
    if 'editor' in d['review']: del d['review']['editor']
    q = dict(q, sourceRefIds=[ref])
    if len(d['quiz']) < 2:
        d['quiz'].append(q)
    json.dump(d, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('patched', path.split('/')[-1])

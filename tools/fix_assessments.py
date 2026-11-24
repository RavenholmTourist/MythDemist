"""Rewrite week-01 and week-02 assessment banks to match the narrative lessons."""
import json, io

def Q(qid, lid, prompt, right, wrongs, expl, refs, obj):
    choices = [{"id": "a", "text": right}] + [{"id": c, "text": t} for c, t in zip("bcd", wrongs)]
    return {"lessonId": lid, "question": {"id": qid, "type": "single-choice", "prompt": prompt,
            "choices": choices, "answerId": "a", "explanation": expl,
            "sourceRefIds": refs, "objectiveIds": [obj]}}

W1 = [
 Q("q1", "grc.heroes.day01.heroic-excellence",
   "Why does Theseus choose the bandit-ridden land road to Athens instead of the safe sea voyage?",
   "He wants to win renown through deeds, imitating Heracles — arriving having done something worth remembering",
   ["He cannot pay for a ship", "The sea route is blocked by storms", "He wants to avoid recognition"],
   "Theseus refuses the safer way deliberately: a hero should earn his arrival, as Heracles cleared monsters.",
   ["plutarch"], "obj.theseus.road"),
 Q("q2", "grc.heroes.day02.achilles-anger",
   "What pattern unites Theseus's victories over the road bandits?",
   "He turns each bandit's own cruelty back on them — club, bent pines, cliff, and bed",
   ["He spares each bandit after winning surrender", "He traps each bandit in a labyrinth", "Each duel is won by divine intervention"],
   "Plutarch notes Theseus imitated Heracles by returning on assailants the same violence they dealt.",
   ["plutarch"], "obj.road.mirror"),
 Q("q3", "grc.heroes.day03.odysseus-cunning",
   "How does Aegeus save Theseus from Medea's poisoned cup?",
   "He recognizes the sword Theseus draws at dinner — the token he left under the rock — and knocks the cup away",
   ["Medea confesses before Theseus drinks", "A servant switches the cups", "An oracle warns him at the table"],
   "Theseus draws his sword 'as if he designed to cut with it'; Aegeus recognizes the token and throws down the cup.",
   ["plutarch"], "obj.medea.recognition"),
 Q("q4", "grc.heroes.day04.jason-medea",
   "How does Theseus escape the labyrinth after killing the Minotaur?",
   "He follows Ariadne's thread — tied at the entrance and unwound through the maze — back out",
   ["He memorizes Daedalus's floor plan", "The Minotaur's dying cry opens the walls", "Ariadne leads him out by hand"],
   "Ariadne gives him a clue (ball) of thread; he unwinds it through the windings and follows it out.",
   ["plutarch"], "obj.mino.thread"),
 Q("q5", "grc.heroes.day05.theseus-heracles",
   "Why does King Aegeus die at Theseus's homecoming?",
   "The crew forgets to raise the white sail; seeing black sails, Aegeus believes his son dead and throws himself down",
   ["Medea poisons him before fleeing Athens", "The Minotaur's curse reaches him", "He dies of old age while Theseus is at sea"],
   "The forgotten sail signal costs Aegeus his life — and names the Aegean Sea.",
   ["plutarch"], "obj.sails.signal"),
]

W2 = [
 Q("q1", "grc.heroes.w02d01.the-quarrel-and-the-ransom",
   "What triggers Apollo's plague on the Greek camp at the Iliad's opening?",
   "Agamemnon refuses and mocks the priest Chryses, who came to ransom his daughter Chryseis",
   ["Achilles refuses to fight the Trojans", "The Greeks steal Apollo's golden tripod", "Chryses poisons the wells"],
   "Chryses came to ransom his daughter; the king's insult brought Apollo's arrows on the host.",
   ["main"], "obj.plague.cause"),
 Q("q2", "grc.heroes.w02d02.briseis-and-withdrawal",
   "After Briseis is taken, what does Achilles ask his mother Thetis to win from Zeus?",
   "That the Trojans prevail — so the Greeks suffer until they learn what Achilles was worth",
   ["That Agamemnon be struck by lightning", "That he be made king of the army", "That his ships be spared for the voyage home"],
   "Achilles asks Zeus to favour the Trojans; the army's suffering will prove his worth — and nearly destroys it.",
   ["main"], "obj.withdraw.ask"),
 Q("q3", "grc.heroes.w02d03.the-embassy-fails",
   "Why does Achilles reject Agamemnon's enormous offer of gifts in Iliad 9?",
   "The stripped honour is beyond material compensation — he will fight only when fire reaches his own ships",
   ["The offer arrives too late; he has already sailed", "He demands the kingship, not gifts", "He has sworn an oath to Hector"],
   "Achilles refuses everything; no list of tripods and gold can repair the public insult to his honour.",
   ["main"], "obj.embassy.refusal"),
 Q("q4", "grc.heroes.w02d04.patroclus-changes-everything",
   "How does Patroclus die?",
   "Wearing Achilles's armour, he presses past the warning to Troy's walls, where Apollo and Hector kill him",
   ["Defending the ships as they burn", "In single combat with Aeneas", "Caught in an ambush returning to camp"],
   "Patroclus ignores the warning, chases to the walls, and dies to Apollo and Hector — redirecting Achilles's rage.",
   ["main"], "obj.patroclus.turn"),
 Q("q5", "grc.heroes.w02d05.priam-and-achilles",
   "What finally moves Achilles to return Hector's body?",
   "Priam kneels and asks him to think of his own father, Peleus — the two enemies weep together",
   ["Zeus orders it directly", "The ransom gold outweighs his rage", "The Greek commanders demand it"],
   "Shared grief breaks the rage: Priam's plea for his son's body recalls Achilles's own father.",
   ["main"], "obj.priam.release"),
]

for path, qs in [("content/curriculum/greek/greek-heroes-week-01.json", W1),
                 ("content/curriculum/greek/greek-heroes-week-02.json", W2)]:
    d = json.load(io.open(path, encoding='utf-8'))
    d['assessment']['questions'] = qs
    json.dump(d, io.open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('assessment rewritten:', path)

"""One-off narrative rewrite for Greek Heroes week 2 (Iliad arc).
Loads each existing lesson, preserves its verbatim sourceReferences,
replaces cards/quiz/objectives with story-first content.
"""
import json, glob, os

DIR = 'content/lessons/greek/heroes-programme/'

def C(i, k, t, b, o):
    return {"id": f"card-{i:02d}", "kind": k, "title": t, "body": b,
            "sourceRefIds": ["main"], "objectiveIds": [o]}

def W(idx, title, sub, tags, objs, cards, q, notes):
    f = glob.glob(DIR + f'week-02-day-{idx:02d}-*.json')[0]
    d = json.load(open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub,
             estimatedMinutes=3, tags=tags, learningObjectives=objs,
             narrativeBlocks=cards, quiz=[q],
             review={"status": "reviewed", "reviewType": "editorial",
                     "editor": "Devin (AI)", "notes": notes})
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', os.path.basename(f))

W(1, "The Iliad: Apollo's Plague",
  "A priest, a ransom, and a king's insult that starts it all",
  ["achilles", "agamemnon", "apollo", "iliad"],
  [{"id": "obj.plague.cause", "text": "Why does Apollo send the plague on the Greek camp?"},
   {"id": "obj.plague.price", "text": "What does Agamemnon demand for returning Chryseis?"}],
  [C(1, "story", "A priest comes begging",
    "For nine days the Greek camp has been dying. Apollo's arrows — the plague itself — fell because Agamemnon refused a ransom: the priest Chryses came to buy back his daughter Chryseis, taken as a war-prize, and the king mocked and dismissed him.", "obj.plague.cause"),
   C(2, "story", "Achilles calls the assembly",
    "It is Achilles, not the king, who calls the army together and demands they ask a prophet why the god is angry. Calchas speaks: the plague will not lift until Chryseis goes home — unpaid, unransomed.", "obj.plague.cause"),
   C(3, "story", "The king's counter-demand",
    "Agamemnon gives way with a snarl: he will return the girl, but only if the army makes good his loss. 'I shall come to your tent and take your own prize' — someone's honour-prize will pay for his pride.", "obj.plague.price"),
   C(4, "story", "Why a girl is a war-prize",
    "Chryseis is not a character with choices here; she is time — honour made physical. In the Greek camp, prizes measure a man's standing. Take one and you have not stolen property, you have publicly degraded a warrior.", "obj.plague.price"),
   C(5, "flavor", "The quarrel that launches the epic",
    "The Iliad does not start with the war — it starts with this argument over honour. Everything that follows, every death including Patroclus and Hector, flows from this moment of wounded pride.", "obj.plague.price")],
  {"question": "What does Agamemnon demand in exchange for releasing Chryseis?",
   "answers": [
    {"text": "He will take another man's honour-prize to replace his — which means seizing Achilles's prize, Briseis", "correct": True},
    {"text": "A ransom of seven tripods from the whole army", "correct": False},
    {"text": "Achilles must publicly apologise to the priest", "correct": False},
    {"text": "Immediate sacrifice of a hundred oxen to Apollo", "correct": False}],
   "explanation": "Agamemnon agrees to return Chryseis but declares he will come to someone's tent and take their prize — the insult that provokes Achilles's withdrawal.",
   "objectiveIds": ["obj.plague.price"]},
  "Narrative rewrite: Iliad book 1's plague and quarrel retold as story; verbatim refs preserved. AI editorial review, not scholarly certification.")

W(2, "The Iliad: Achilles Withdraws",
  "The sword half-drawn, the sea prayed to, the war abandoned",
  ["achilles", "briseis", "thetis", "iliad"],
  [{"id": "obj.withdraw.choice", "text": "What stops Achilles from killing Agamemnon?"},
   {"id": "obj.withdraw.ask", "text": "What does Achilles ask his mother to win from Zeus?"}],
  [C(1, "story", "Briseis is taken",
    "Agamemnon sends heralds to Achilles's tent and they lead away Briseis — his honour-prize, publicly stripped. Achilles does not stop them; his rage is beyond the point where stopping anyone would satisfy it.", "obj.withdraw.choice"),
   C(2, "story", "The half-drawn sword",
    "His heart is divided — draw the sword and kill the king on the spot, or swallow the insult. Athena herself descends, visible to him alone, seizes his hair and holds him back: restrain yourself, and the gods will repay this insult threefold.", "obj.withdraw.choice"),
   C(3, "story", "Weeping by the grey sea",
    "Achilles walks alone to the shore and weeps over the boundless water. He is the greatest fighter alive, and the army's commander has just shamed him before everyone — this is not pique, it is a broken compact between leader and warrior.", "obj.withdraw.ask"),
   C(4, "story", "Thetis carries the request",
    "His goddess mother rises from the sea to comfort him, and he asks the unthinkable: go to Zeus and beg him to let the TROJANS win. Let the Greeks bleed until they understand what Achilles was worth to them.", "obj.withdraw.ask"),
   C(5, "context", "Rage as the epic's engine",
    "The Iliad's first word is 'anger' — menin, a word for divine rage. Achilles's withdrawal is not sulking; it is a god-backed curse on his own side, and Zeus will grant it.", "obj.withdraw.ask")],
  {"question": "What does Achilles ask Thetis to beg of Zeus?",
   "answers": [
    {"text": "That the Trojans prevail in battle — so the Greeks suffer until they feel his worth", "correct": True},
    {"text": "That Agamemnon be struck dead in the night", "correct": False},
    {"text": "That Briseis be returned by divine command", "correct": False},
    {"text": "That he be allowed to sail home to Phthia immediately", "correct": False}],
   "explanation": "Achilles asks Zeus to favour the Trojans — the Greeks' own suffering will prove how much they needed him, and it nearly destroys their army.",
   "objectiveIds": ["obj.withdraw.ask"]},
  "Narrative rewrite: Briseis's seizure, Athena's restraint, and the prayer to Thetis (Iliad 1). AI editorial review, not scholarly certification.")

W(3, "The Iliad: The Embassy Fails",
  "The Greeks' best offer meets Achilles's immovable no",
  ["achilles", "embassy", "phoenix", "ajax", "iliad"],
  [{"id": "obj.embassy.offer", "text": "What does Agamemnon offer Achilles to return?"},
   {"id": "obj.embassy.refusal", "text": "Why does Achilles refuse?"}],
  [C(1, "story", "Defeat forces humility",
    "With Achilles out, the war turns. Hector drives the Greeks back to their ships, and Agamemnon — desperate — finally admits the quarrel was madness. He sends an embassy to Achilles's tent.", "obj.embassy.offer"),
   C(2, "story", "The shopping-list of amends",
    "The offer is staggering: seven tripods, ten talents of gold, twenty cauldrons, twelve prize horses, seven skilled women, Briseis returned untouched — and his daughter's hand in marriage after the war.", "obj.embassy.offer"),
   C(3, "story", "Achilles's answer",
    "He hates 'even as the gates of hell' the man who says one thing and hides another. He will not fight. Gifts cannot buy back the honour that was stripped — and tomorrow, he says, he may simply sail home.", "obj.embassy.refusal"),
   C(4, "story", "Phoenix's last plea",
    "Old Phoenix, who raised Achilles as a child, begs him by their bond. Ajax is blunter: this stubbornness is destroying your friends. Achilles softens just slightly — he will fight only when fire reaches his own ships.", "obj.embassy.refusal"),
   C(5, "context", "The loneliest 'no' in literature",
    "The embassy fails because Achilles's grievance has outgrown any compensation. Honour cannot be repaid in tripods — only the coming catastrophe will move him.", "obj.embassy.refusal")],
  {"question": "How does Achilles respond to Agamemnon's enormous offer of gifts?",
   "answers": [
    {"text": "He refuses — no compensation can repair the stripped honour; he will fight only when fire reaches his own ships", "correct": True},
    {"text": "He accepts the gifts but refuses to forgive Agamemnon", "correct": False},
    {"text": "He doubles the demand and keeps negotiating", "correct": False},
    {"text": "He sails home to Phthia that night", "correct": False}],
   "explanation": "Achilles rejects the whole offer — the insult is beyond material repair — and sets one condition: he fights when the battle reaches his own ships.",
   "objectiveIds": ["obj.embassy.refusal"]},
  "Narrative rewrite: the failed embassy of Iliad 9. AI editorial review, not scholarly certification.")

W(4, "The Iliad: Patroclus Changes Everything",
  "Borrowed armour, a friend's death, and rage redirected",
  ["achilles", "patroclus", "hector", "iliad"],
  [{"id": "obj.patroclus.deal", "text": "Why does Achilles let Patroclus fight in his place?"},
   {"id": "obj.patroclus.turn", "text": "What does Patroclus's death do to Achilles's anger?"}],
  [C(1, "story", "The compromise",
    "The battle reaches the ships — the exact point Achilles said he would fight. But he still will not yield his pride: instead Patroclus begs to borrow his armour so the Trojans, thinking Achilles returned, will panic. Achilles agrees — with a warning: drive them off, then come back. Do not chase glory to the walls.", "obj.patroclus.deal"),
   C(2, "story", "The disguise works — then fails",
    "The Trojans see the armour and break. But Patroclus, drunk on his own rampage, ignores the warning and presses toward Troy itself — where Apollo strikes him from behind, and Hector finishes him.", "obj.patroclus.turn"),
   C(3, "story", "The news",
    "'Patroclus has fallen, and a fight is raging about his naked body.' Achilles's grief is volcanic — he pours dust over his head, and the sound of his crying reaches Thetis under the sea.", "obj.patroclus.turn"),
   C(4, "story", "Rage finds its true target",
    "The quarrel with Agamemnon now means nothing to him. He reconciles instantly — the gifts, Briseis, all irrelevant. His rage has a new name: Hector. He will return to battle knowing his own death follows, because the Fates have already promised it.", "obj.patroclus.turn"),
   C(5, "context", "The price of pride",
    "Every death at Troy traces back to that first quarrel — but Patroclus's death is the one Achilles caused himself, by staying out and letting another man wear his armour.", "obj.patroclus.turn")],
  {"question": "How does Patroclus die?",
   "answers": [
    {"text": "Wearing Achilles's armour, he presses past the warning and attacks Troy itself, where Apollo and Hector kill him", "correct": True},
    {"text": "He is killed guarding the ships when the Trojans burn them", "correct": False},
    {"text": "Achilles kills him in a quarrel over Briseis", "correct": False},
    {"text": "He is struck by a stray arrow during a truce", "correct": False}],
   "explanation": "Patroclus goes beyond his mission — chasing to Troy's walls, Apollo strikes him, Hector kills him. His death turns Achilles's rage from Agamemnon to Hector.",
   "objectiveIds": ["obj.patroclus.turn"]},
  "Narrative rewrite: Patroclus's sortie and death (Iliad 16-18). AI editorial review, not scholarly certification.")

W(5, "The Iliad: Priam and Achilles",
  "A father kneels in the killer's tent",
  ["achilles", "priam", "hector", "ransom", "iliad"],
  [{"id": "obj.priam.grief", "text": "What does Achilles do to Hector's body before Priam comes?"},
   {"id": "obj.priam.release", "text": "Why does Achilles finally release the body?"}],
  [C(1, "story", "After the duel",
    "Achilles kills Hector before the walls of Troy — and it is not enough. He pierces the ankles, lashes the body to his chariot, and drags it through the dust around Patroclus's tomb, day after day.", "obj.priam.grief"),
   C(2, "story", "A father's impossible errand",
    "Priam, king of Troy and father of the dead man, crosses the enemy lines alone at night with a wagon of ransom — into the tent of his son's killer. He kneels and kisses the hands that killed his children.", "obj.priam.release"),
   C(3, "story", "'Think of your father'",
    "Priam does not argue — he asks Achilles to remember Peleus, his own aged father far away who will never see his son return. The two enemies weep together: one for his father and friend, one for his sons.", "obj.priam.release"),
   C(4, "story", "The body goes home",
    "Moved by the shared grief, Achilles lifts the old man up, accepts the ransom, and grants twelve days of truce for Hector's funeral. The Iliad ends not with Troy's fall but with a burial.", "obj.priam.release"),
   C(5, "context", "Why the epic ends here",
    "The Iliad's final movement is not conquest but compassion — two men bound by loss. The rage that opened the poem dissolves into the recognition that enemies grieve alike.", "obj.priam.release")],
  {"question": "What finally moves Achilles to return Hector's body?",
   "answers": [
    {"text": "Priam kneels before him and asks him to think of his own father — shared grief breaks through the rage", "correct": True},
    {"text": "The gods threaten him with divine punishment", "correct": False},
    {"text": "The ransom of gold outweighs his anger", "correct": False},
    {"text": "The Greeks order him to release the body", "correct": False}],
   "explanation": "Priam asks Achilles to think of Peleus, his own father; the two weep together and Achilles releases the body and grants a funeral truce.",
   "objectiveIds": ["obj.priam.release"]},
  "Narrative rewrite: Hector's death, Priam's ransom, the epic's close (Iliad 22-24). AI editorial review, not scholarly certification.")

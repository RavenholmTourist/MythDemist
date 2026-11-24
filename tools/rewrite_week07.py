"""Narrative rewrite for Greek Heroes week 7 (house of Atreus / Oedipus / Trojan Women)."""
import json, io, glob

DIR = 'content/lessons/greek/heroes-programme/'
REVIEW = {"status": "reviewed", "reviewedBy": "Devin (AI editorial review)", "reviewedAt": "2026-11-24",
          "reviewType": "editorial",
          "notes": "AI editorial review by Devin on 2026-11-24: narrative-first rewrite; cards retell the story, verbatim source excerpts preserved, quiz answers checked against the retold material. This is not independent scholarly review or scholarly certification; specialist and community review remains recommended."}

def C(i, k, t, b, r, o):
    return {"id": f"card-{i:02d}", "kind": k, "title": t, "body": b,
            "sourceRefIds": r, "objectiveIds": [o]}

def Q(qid, prompt, right, wrongs, expl, r, o):
    return {"id": qid, "type": "single-choice", "prompt": prompt,
            "choices": [{"id": "a", "text": right}] + [{"id": c, "text": t} for c, t in zip("bcd", wrongs)],
            "answerId": "a", "explanation": expl, "sourceRefIds": r, "objectiveIds": [o]}

def W(idx, title, sub, tags, objs, cards, quiz):
    f = glob.glob(DIR + f'week-07-day-{idx:02d}-*.json')[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub,
             estimatedMinutes=3, tags=tags, learningObjectives=objs,
             narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W(1, "Agamemnon: The Homecoming",
  "Ten years at Troy, one bath at Mycenae — the king's return is the murder scene",
  ["agamemnon", "clytemnestra", "aegisthus", "orestia"],
  [{"id": "obj.agem.motive", "text": "Why does Clytemnestra kill Agamemnon?"},
   {"id": "obj.agem.scene", "text": "How is the murder staged?"}],
  [C(1, "story", "The king who paid in blood", "To sail for Troy, Agamemnon sacrificed his daughter Iphigenia — the fleet would not move until the gods had their price. Ten years later he returns a victor; his wife Clytemnestra has never stopped counting.", ["main"], "obj.agem.motive"),
   C(2, "story", "A war won, a house lost", "While he was gone, Clytemnestra took his cousin Aegisthus — whose family Agamemnon's father once fed his own sons to — as lover and co-ruler. The palace has already moved on.", ["main"], "obj.agem.motive"),
   C(3, "story", "The purple carpet", "She greets him in triumph and spreads crimson tapestries across the threshold — an honour fit for gods, which a king should refuse. Agamemnon steps onto the carpet: the audience has just watched him walk into his own pride.", ["main"], "obj.agem.scene"),
   C(4, "story", "In the bath", "The murder happens offstage and by firelight: Clytemnestra and Aegisthus kill him in his bath — entangled in a robe, defenceless. Then she opens the palace doors and shows the bodies, declaring justice done.", ["murder"], "obj.agem.scene"),
   C(5, "story", "Cassandra's bonus horror", "Agamemnon brought home a Trojan princess-prophetess as a war-prize — Cassandra, fated to be believed by no one. She foresees the murder and is killed with him, screaming the truth to a city that cannot hear it.", ["odyssey"], "obj.agem.motive")],
  [Q("q1", "Why does Clytemnestra kill Agamemnon?",
     "He sacrificed their daughter Iphigenia to launch the fleet — she has been counting the years since",
     ["He refused to share the spoils of Troy", "Aegisthus forced her hand", "She wanted his throne for herself"],
     "Iphigenia's sacrifice is the wound at the story's heart; Aegisthus adds his own family grievance.",
     ["main"], "obj.agem.motive"),
   Q("q2", "What is the significance of the purple carpet scene?",
     "Spreading honours fit for gods across his threshold is the trap — Agamemnon walks into his own pride moments before the murder",
     ["It marks his official coronation", "It is a peace offering to the gods", "It hides the murder weapon"],
     "The carpet makes him complicit: he knows the gesture is excessive, and steps onto it anyway.",
     ["main"], "obj.agem.scene")])

W(2, "Orestes: Vengeance and the Court",
  "A son must kill his mother — and the gods argue about justice",
  ["orestes", "electra", "furies", "athena"],
  [{"id": "obj.ore.stasis", "text": "What impossible duty is Orestes given?"},
   {"id": "obj.ore.court", "text": "How does the cycle of blood end?"}],
  [C(1, "story", "The son returns", "Orestes, smuggled out as a baby when his father was murdered, comes home grown — to a mother who is both the wronged wife of Agamemnon and the killer of his father. Every obligation pulls in opposite directions.", ["main"], "obj.ore.stasis"),
   C(2, "story", "Apollo's command", "The god of Delphi himself orders the revenge: kill Clytemnestra and Aegisthus. Matricide is the deepest pollution — and refusing vengeance is betrayal of the father. There is no clean act left in this family.", ["main"], "obj.ore.stasis"),
   C(3, "story", "The deed and the Furies", "Orestes kills both his mother and her lover — and immediately the Furies arrive: ancient earth-goddesses who pursue blood-kin killers. He is hounded across Greece, purified yet never free.", ["main"], "obj.ore.stasis"),
   C(4, "story", "Trial at Athens", "At the Areopagus, Athena convenes the first murder trial in myth: Apollo argues duty, the Furies argue blood. The jury of Athenians splits evenly — and Athena casts the deciding vote for acquittal.", ["court"], "obj.ore.court"),
   C(5, "story", "The court replaces the feud", "The play's real ending: blood-for-blood is replaced by legal process. The Furies are not defeated but honoured — renamed 'the Kindly Ones' and given a shrine. Vengeance doesn't end; it is institutionalised.", ["court"], "obj.ore.court")],
  [Q("q1", "What makes Orestes's duty impossible?",
     "Apollo commands him to avenge his father by killing his mother — whichever way he acts, he violates a sacred bond",
     ["He must choose between two wives", "He is asked to betray his ally Pylades", "He must surrender the throne to Aegisthus"],
     "Duty to father and horror of matricide collide — the play's engine is that no act is clean.",
     ["main"], "obj.ore.stasis"),
   Q("q2", "How is Orestes finally cleared?",
     "Athena's court at the Areopagus — a jury splits evenly and her casting vote acquits him, ending the feud with law instead of blood",
     ["Apollo pardons him at Delphi", "The Furies are killed by Heracles", "He exiles himself forever"],
     "Aeschylus's answer to the vendetta: an institution — the court — replaces endless retaliation.",
     ["court"], "obj.ore.court")])

W(3, "Antigone: The Burial",
  "A king's edict against a sister's duty — and no one bends",
  ["antigone", "creon", "polynices", "thebes"],
  [{"id": "obj.anti.conflict", "text": "What do Antigone and Creon each defend?"},
   {"id": "obj.anti.cost", "text": "What does the standoff cost?"}],
  [C(1, "story", "Two brothers, one throne", "Oedipus's sons killed each other in civil war: Eteocles defending Thebes, Polynices attacking it. Creon, the new king, honours the defender with full burial — and leaves the attacker's body to rot, a warning to traitors.", ["main"], "obj.anti.conflict"),
   C(2, "story", "Antigone's answer", "Their sister Antigone defies the edict: divine law and family duty outrank a king's decree. She walks out and buries her brother — scattering dust on the corpse herself when the guards undo her work.", ["main"], "obj.anti.conflict"),
   C(3, "story", "Creon cannot bend", "Caught, she does not apologise — she argues. Creon cannot back down without weakening the new throne. So he sentences her to be walled alive in a cave: the state versus the family, neither willing to break first.", ["defense"], "obj.anti.conflict"),
   C(4, "story", "The cascade", "Too late, the prophet Tiresias warns Creon that the unburied corpse pollutes the city. Creon relents — but the cave is already empty: Antigone has hanged herself. His son Haemon (her betrothed) kills himself beside her; his mother follows. The 'stable' city loses its ruling family in an afternoon.", ["main"], "obj.anti.cost"),
   C(5, "context", "The argument that never resolves", "Antigone is the foundational text of conscientious objection — every generation re-fights her case. Sophocles gives both sides real arguments; the tragedy is that both are right.", ["main"], "obj.anti.conflict")],
  [Q("q1", "What does Antigone defend in burying Polynices?",
     "Divine law and family duty — burial rites owed to the dead, above the king's decree",
     ["Polynices's claim to the throne", "Thebes's treaty obligations", "Her own right to rule"],
     "Her argument is with unwritten divine law, not with Creon's politics — which is why the conflict can't be resolved by compromise.",
     ["main"], "obj.anti.conflict"),
   Q("q2", "How does the standoff end?",
     "Creon relents too late — Antigone is already dead, and his son and wife follow her",
     ["Antigone is exiled to Argos", "The chorus persuades Creon in time", "Haemon rescues Antigone alive"],
     "The tragedy isn't the wrong choice — it's the delayed right one.",
     ["main"], "obj.anti.cost")])

W(4, "Oedipus: The Investigation",
  "The king who hunts the murderer — and finds himself",
  ["oedipus", "tiresias", "jocasta", "sphinx"],
  [{"id": "obj.oed.method", "text": "How does Oedipus investigate the plague's cause?"},
   {"id": "obj.oed.truth", "text": "What does the investigation reveal?"}],
  [C(1, "story", "The plague and the promise", "Thebes is dying — crops fail, women miscarry, the city begs its king. Oedipus, who saved Thebes once by answering the Sphinx's riddle, sends to Delphi: the oracle says the plague lives because the city shelters the murderer of old King Laius, unpunished.", ["main"], "obj.oed.method"),
   C(2, "story", "The detective-king", "Oedipus does not hesitate: he curses the killer, orders a city-wide inquiry, questions the prophet Tiresias (who hints at the truth and is called a fraud for it), summons witnesses — and slowly unravels the case like a detective who never suspects the murderer is himself.", ["main"], "obj.oed.method"),
   C(3, "story", "The accumulating truth", "The pieces converge: Laius was killed at a crossroads where Oedipus once killed a rude stranger. A survivor's description of the attacker is one man, not bandits. A messenger brings news that his 'father' in Corinth died naturally — he was adopted. A shepherd confesses he once handed over a baby with pierced ankles.", ["revelation"], "obj.oed.truth"),
   C(4, "story", "The answer: himself", "The investigation concludes that Oedipus is Laius's killer — and worse: Laius's son, exposed at birth to prevent a prophecy that he would kill his father and marry his mother. Every precaution Laius and Oedipus took produced exactly what it feared. Jocasta hangs herself; Oedipus blinds himself with her brooch-pins.", ["revelation"], "obj.oed.truth"),
   C(5, "context", "Why the play endures", "Oedipus Rex is the first detective story — and its inversion: the detective is the criminal. Every generation re-reads the question of what self-knowledge costs.", ["main"], "obj.oed.truth")],
  [Q("q1", "What triggers Oedipus's investigation?",
     "A plague on Thebes — the oracle says the city shelters Laius's unpunished murderer",
     ["Tiresias's prophecy about the crown", "Jocasta's nightmare", "The Sphinx's return"],
     "The plague makes the murder a civic emergency — Oedipus must find the killer to save the city.",
     ["main"], "obj.oed.method"),
   Q("q2", "What does the investigation finally prove?",
     "Oedipus himself killed Laius at the crossroads — and the man he killed was his father, whose son he is",
     ["Tiresias killed Laius for the throne", "The bandits were Polynices's men", "Laius died of natural causes at the pass"],
     "The detective finds himself — the play's inversion of every mystery since.",
     ["revelation"], "obj.oed.truth")])

W(5, "The Trojan Women",
  "The morning after Troy — what victory costs the losers",
  ["trojan-women", "hecuba", "cassandra", "andromache"],
  [{"id": "obj.tro.cost", "text": "What does the play show about the cost of victory?"},
   {"id": "obj.tro.women", "text": "What happens to Troy's royal women?"}],
  [C(1, "story", "The city already fallen", "The Trojan Women opens after the sack — the Greeks have won, the heroes are dead, and the city is ash. The play has no war left: only the division of the spoils.", ["main"], "obj.tro.cost"),
   C(2, "story", "Hecuba's ledger", "Queen Hecuba, who watched her husband and sons die, is now counted as property. The Greeks parcel out the royal women as slaves and concubines: Cassandra to Agamemnon, Andromache to Achilles's son, Hecuba to Odysseus — the man she once helped deceive.", ["main"], "obj.tro.women"),
   C(3, "story", "The last child of Troy", "The play's unbearable centre: Astyanax, Hector's infant son, is taken from Andromache's arms and thrown from the walls — the Greeks will not let a Trojan prince grow up. Hecuba buries the future of Troy.", ["main"], "obj.tro.cost"),
   C(4, "story", "A warning to the audience", "The Athenian audience watching this was itself an empire that had just destroyed a neutral island's men and enslaved its women. Euripides makes them watch what that looks like from below.", ["main"], "obj.tro.cost"),
   C(5, "flavor", "Victors write, but survivors remember", "Everything the Greeks 'won' at Troy sits on a pile of widows and orphans — the plays keep both the victory and the bill visible. The same war the Iliad made glorious, Euripides prices in the same coin.", ["main"], "obj.tro.cost")],
  [Q("q1", "What does The Trojan Women focus on that the Iliad does not?",
     "The aftermath for the defeated — the enslaved women and murdered heir of a sacked city, not the victors' glory",
     ["The gods' quarrels over the war", "Achilles's battle rage", "The siege strategies of the Greeks"],
     "Euripides deliberately shows the cost side of the same war the Iliad epicises.",
     ["main"], "obj.tro.cost"),
   Q("q2", "What happens to Astyanax?",
     "He is thrown from the walls by the Greeks — no Trojan prince will be allowed to grow up",
     ["He is adopted by Agamemnon", "He escapes to found Rome", "He dies in the siege already"],
     "The killing of Hector's infant son is the play's moral bottom line: victory that requires this is not clean.",
     ["main"], "obj.tro.women")])

ASSESSMENT = [
 ("grc.heroes.w07d01.agamemnon-returns", "What is the deepest motive behind Agamemnon's murder?",
  "Clytemnestra's revenge for Iphigenia — the daughter sacrificed to launch the fleet",
  ["Aegisthus's ambition for the throne", "A quarrel over Trojan spoils", "Apollo's command for justice"],
  "The sacrifice at Aulis is the wound; the carpet and the bath are only the staging.", ["main", "murder"], "obj.agem.motive"),
 ("grc.heroes.w07d02.orestes-and-justice", "How does the Oresteia resolve the blood-feud?",
  "Athena establishes a court at the Areopagus — law replaces vendetta, and the Furies are honoured, not defeated",
  ["Orestes is purified at Delphi and pardoned", "The Furies are destroyed by Zeus", "Orestes kills himself to end the cycle"],
  "Aeschylus's answer to endless retaliation is an institution.", ["main", "court"], "obj.ore.court"),
 ("grc.heroes.w07d03.antigone-and-burial", "What is Antigone's core argument against Creon?",
  "Divine law and burial duty outrank a king's decree — the unwritten laws of the gods are older than the state",
  ["Polynices was the rightful king", "Creon has no legal right to rule", "The burial was ordered by the oracle"],
  "She appeals above the state to the gods — which is why the conflict cannot be settled politically.", ["main", "defense"], "obj.anti.conflict"),
 ("grc.heroes.w07d04.oedipus-investigates", "What is the twist at the heart of Oedipus Rex?",
  "The detective is the murderer — the king who hunts Laius's killer finds himself",
  ["Tiresias is the murderer", "Laius faked his death", "The Sphinx set a trap for Oedipus"],
  "The play inverts every mystery: self-discovery is the catastrophe.", ["main", "revelation"], "obj.oed.truth"),
 ("grc.heroes.w07d05.the-trojan-women", "What does The Trojan Women show that the Iliad does not?",
  "The defeated side's price — enslaved queens and a murdered child, the cost side of the same victory",
  ["The gods' political manoeuvres", "Achilles's heroism", "The siege tactics of Troy"],
  "Euripides prices the same war the Iliad glorifies — for an audience that was itself an empire.", ["main"], "obj.tro.cost")]

wpath = 'content/curriculum/greek/greek-heroes-week-07.json'
w = json.load(io.open(wpath, encoding='utf-8'))
for day in w['days']:
    les = json.load(io.open(day['lessonPath'], encoding='utf-8'))
    day['title'] = les['title']
w['assessment']['questions'] = [
    {"lessonId": lid, "question": {"id": f"q{i+1}", "type": "single-choice", "prompt": p,
        "choices": [{"id": "a", "text": r}] + [{"id": c, "text": t} for c, t in zip("bcd", ws)],
        "answerId": "a", "explanation": e, "sourceRefIds": rf, "objectiveIds": [o]}}
    for i, (lid, p, r, ws, e, rf, o) in enumerate(ASSESSMENT)]
json.dump(w, io.open(wpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('week 7 rewritten')

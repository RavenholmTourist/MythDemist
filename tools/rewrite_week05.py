"""Narrative rewrite for Greek Heroes week 5 (Heracles arc)."""
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
    f = glob.glob(DIR + f'week-05-day-{idx:02d}-*.json')[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub,
             estimatedMinutes=3, tags=tags, learningObjectives=objs,
             narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W(1, "Heracles: The Twelve Labours",
  "A debt of service measured in monsters",
  ["heracles", "labours", "eurystheus"],
  [{"id": "obj.labours.list", "text": "What are the twelve labours?"},
   {"id": "obj.labours.reason", "text": "Why does Heracles owe them?"}],
  [C(1, "story", "The sentence", "Heracles does not labour for glory at first — he labours for a sentence. In a fit of god-sent madness he kills his own children; the oracle at Delphi orders him to serve King Eurystheus and perform the tasks set him. The labours are penance, not ambition.", ["main"], "obj.labours.reason"),
   C(2, "story", "The famous twelve", "The canonical list: the Nemean lion, the Lernaean hydra, the Ceryneian hind, the Erymanthian boar, the Augean stables, the Stymphalian birds, the Cretan bull, the man-eating mares of Diomedes, the Amazons' girdle, the cattle of Geryon, the apples of the Hesperides, and Cerberus dragged up from the underworld.", ["main"], "obj.labours.list"),
   C(3, "story", "Not always clean strength", "The labours are not all fights. The Hydra needs a cauterising ally; the Augean stables are cleaned in a day by diverting two rivers — labour as engineering, not muscles. Several 'labours' are errands or tricks, which is part of their interest.", ["hydra", "augeas"], "obj.labours.list"),
   C(4, "story", "Eurystheus's moving goalposts", "The cowardly king hides in a bronze jar when Heracles returns, and disqualifies labours on technicalities — helped with the Hydra? doesn't count. Cleaned the stables for payment? doesn't count. Ten becomes twelve.", ["main"], "obj.labours.list"),
   C(5, "context", "Why a catalogue endures", "The list is the story: each labour is a self-contained trial a listener can hold in memory. Together they map a hero who conquers not just monsters but geography — the labours literally walk him across the known world and below it.", ["main"], "obj.labours.list")],
  [Q("q1", "Why does Heracles owe the labours?",
     "He killed his own children in a fit of god-sent madness; the oracle sentences him to serve Eurystheus as penance",
     ["He volunteered to prove Zeus wrong", "Eurystheus is his rival for the throne", "The labours are a bride-price for Deianira"],
     "The labours are penance for kin-killing under madness — the darkest possible origin for the hero.",
     ["main"], "obj.labours.reason"),
   Q("q2", "Which labour shows the list isn't all fighting?",
     "The Augean stables — cleaned by diverting two rivers through them, a feat of engineering not strength",
     ["The Nemean lion — wrestled barehanded", "The Amazons' girdle — taken by force", "Cerberus — carried bodily from the underworld"],
     "Several labours are errands or tricks; the stables are the clearest case of brains over brawn.",
     ["augeas"], "obj.labours.list")])

W(2, "Heracles: The Nemean Lion",
  "An unbreakable hide, bare hands, and the skin he wears forever",
  ["heracles", "nemean", "lion"],
  [{"id": "obj.lion.fight", "text": "How does Heracles kill the lion?"},
   {"id": "obj.lion.skin", "text": "Why does he keep the skin?"}],
  [C(1, "story", "The first labour", "The Nemean lion is no ordinary beast — offspring of monsters, hide proof against every weapon. It has been terrorising Nemea; no arrow or blade can touch it.", ["main"], "obj.lion.fight"),
   C(2, "story", "When weapons fail", "Heracles looses arrows at the beast — they bounce off its hide like rain. He chases it into its cave, blocks the exits, and does the only thing left: strangles it barehanded.", ["combat"], "obj.lion.fight"),
   C(3, "story", "The trophy that dresses him", "He can't skin the invulnerable hide with a knife — so he uses the lion's own claws, the only things sharp enough to cut it. The pelt becomes his signature: the lionskin and club you see in every image of Heracles start here.", ["main"], "obj.lion.skin"),
   C(4, "story", "Eurystheus's terror", "When Heracles returns wearing the beast that was supposed to kill him, Eurystheus forbids him from entering the city again — the labours must be reported at the gates. The king is so afraid he keeps a bronze jar buried as a hiding place.", ["main"], "obj.lion.fight"),
   C(5, "context", "The signature image", "Everything in the iconic Heracles — the club, the lionskin, the wrestling — comes from this single story. It is the pattern for every strength-labour after it: when the tool fails, the body doesn't.", ["main"], "obj.lion.fight")],
  [Q("q1", "How does Heracles kill the Nemean lion?",
     "He strangles it barehanded — its hide is proof against every weapon",
     ["He shoots it with poisoned arrows", "He traps it in a bronze jar", "He blinds it and it starves"],
     "Arrows bounce off the monster's hide; Heracles corners it in its cave and chokes it to death.",
     ["combat"], "obj.lion.fight"),
   Q("q2", "Why does Heracles wear the lion's skin?",
     "As the trophy of his first labour — he skins it with the beast's own claws and it becomes his signature garb",
     ["As armour against the remaining labours", "As a gift to Eurystheus", "As a disguise to enter Nemea"],
     "The lionskin (with club) becomes the universal identifier of Heracles in art and story.",
     ["main"], "obj.lion.skin")])

W(3, "Heracles: Madness and Service",
  "The hero who killed his family — and the sentence that made him",
  ["heracles", "hera", "eurystheus", "madness"],
  [{"id": "obj.mad.cause", "text": "What drives Heracles to his worst act?"},
   {"id": "obj.mad.hate", "text": "Why does Hera persecute him?"}],
  [C(1, "story", "Born under a curse", "Heracles is Zeus's son by the mortal Alcmene — and Hera's hatred begins at his conception. She sends serpents to his cradle (he strangles them) and spends his life hounding the child her husband fathered.", ["main"], "obj.mad.hate"),
   C(2, "story", "The madness sent by Hera", "At his height — a wife, children, a city — Hera strikes him with madness. In the fog of it he kills his own sons (and in some accounts his wife Megara). When the fog lifts, the man under the hero's skin is a child-killer.", ["main"], "obj.mad.cause"),
   C(3, "story", "The oracle's sentence", "He seeks purification at Delphi and the answer is service: twelve years under his cousin Eurystheus, a man far beneath him in courage. The greatest hero in Greece takes orders from a coward — that is the price of absolution.", ["main"], "obj.mad.cause"),
   C(4, "story", "Why this story matters", "Heracles is not a clean hero: he breaks things he loves as often as he saves them. The labours are redemptive precisely because he is not innocent — the Greeks kept both halves, the monster-killer and the man who must be cleansed.", ["main"], "obj.mad.cause"),
   C(5, "context", "The pattern: service as penance", "Greek heroes repeatedly pay for blood with service (Orestes, Apollo after Python, Heracles). The rule seems to be: the gods don't forgive bloodguilt — they commute it into labour.", ["main"], "obj.mad.cause")],
  [Q("q1", "What drives Heracles to kill his own children?",
     "Hera sends a fit of madness on him — the persecution begun at his birth as Zeus's illegitimate son",
     ["Eurystheus bewitches him", "A poisoned wound drives him to frenzy", "He does it knowingly in anger"],
     "Hera's madness produces the crime — and the labours are the sentence that follows.",
     ["main"], "obj.mad.cause"),
   Q("q2", "Why does Hera persecute Heracles?",
     "He is Zeus's son by a mortal woman — her hatred of the child starts at his conception",
     ["He killed her sacred serpent", "He refused to worship at her temple", "He stole the golden apples from her garden"],
     "The enmity is dynastic jealousy: every labour he survives is another insult to her pride.",
     ["main"], "obj.mad.hate")])

W(4, "Heracles: Death and Apotheosis",
  "A centaur's revenge, a burning robe, and a seat among the gods",
  ["heracles", "deianira", "nessus", "apotheosis"],
  [{"id": "obj.apo.death", "text": "How does Heracles die?"},
   {"id": "obj.apo.god", "text": "What happens to him after death?"}],
  [C(1, "story", "The centaur's dying gift", "Years before, the centaur Nessus tried to assault Heracles's wife Deianira; Heracles shot him. Dying, Nessus told Deianira his blood was a love charm — keep it, and Heracles will never stray. She kept it.", ["main"], "obj.apo.death"),
   C(2, "story", "The robe of fire", "When Deianira fears a rival, she soaks a robe in the centaur's blood and sends it to Heracles. It is poisoned: the fabric burns into his skin and cannot be torn off without tearing his flesh with it. The greatest body in the world dies by his wife's desperate gift.", ["main"], "obj.apo.death"),
   C(3, "story", "The pyre on Oeta", "In agony beyond bearing, Heracles builds his own pyre on Mount Oeta and lies on it. No one will light the fire until a passing stranger does — the strongest man in creation begging for a mercy burn.", ["main"], "obj.apo.death"),
   C(4, "story", "Up, not down", "The flames take the mortal part — and the immortal part ascends to Olympus. Hera finally relents; Heracles marries Hebe, goddess of youth, and feasts with the gods. He is the only hero in the whole cycle who becomes a god.", ["main"], "obj.apo.god"),
   C(5, "context", "A hero's strange ending", "The apotheosis is earned the hard way — no other hero buys divinity with a life this painful. The Greeks meant it as the final verdict: the labours were redemption enough to lift him above mortals.", ["main"], "obj.apo.god")],
  [Q("q1", "How does Heracles die?",
     "Deianira sends him a robe soaked in the centaur Nessus's poisoned blood — it burns into his flesh and he asks to be burned on a pyre",
     ["He is killed by Achilles in a duel", "Hera strikes him down at last", "He drowns crossing the river Styx"],
     "The dying centaur's 'love charm' is actually his revenge — Heracles's own wife delivers the blow.",
     ["main"], "obj.apo.death"),
   Q("q2", "What happens to Heracles after death?",
     "He becomes a god — the only hero in the cycle to be received on Olympus, reconciled to Hera and married to Hebe",
     ["He judges the dead in the underworld", "He is reborn as a constellation", "He remains a shade like all mortals"],
     "His apotheosis is unique: mortality consumed on the pyre, divinity ascending to Olympus.",
     ["main"], "obj.apo.god")])

W(5, "Heracles: Strong Man or Problem?",
  "The hero who also wrecks things — weighing the ledger",
  ["heracles", "violence", "contradictions"],
  [{"id": "obj.prob.balance", "text": "Why is Heracles both saviour and problem?"},
   {"id": "obj.prob.use", "text": "What is he actually FOR in the myths?"}],
  [C(1, "story", "The civilizing strong man", "On one side: he clears the world of monsters, frees Prometheus, kills bandits on every road, breaks the death-god's hold on Alcestis. He is the great remover — whatever is too dangerous for everyone else, he does.", ["main"], "obj.prob.use"),
   C(2, "story", "And the wrecker", "On the other side: he sacks cities on slight provocation, kills a guest-friend (Iphitus) in a rage, fights the god Apollo for a tripod, nearly breaks hospitality rules everywhere he goes. The same body that saves also smashes.", ["main"], "obj.prob.balance"),
   C(3, "story", "A god's appetite", "Heracles eats like a force of nature and loves like a disaster — dozens of liaisons, a trail of sons across the Greek world. He is civilization's patron AND its problem, depending on which side of him you land.", ["main"], "obj.prob.balance"),
   C(4, "story", "Why keep both halves?", "The myths don't reconcile the contradiction — they preserve it. Heracles is the honest hero: the strength that protects is the same strength that harms, and you don't get one without the other.", ["main"], "obj.prob.balance"),
   C(5, "flavor", "The ancestor of the strong hero", "Every strong-with-questions hero that follows — Beowulf, Samson, the Hulk — runs on the Heracles template: power enormous enough to solve anything, and dangerous enough to be the problem itself.", ["main"], "obj.prob.use")],
  [Q("q1", "Why is Heracles a 'problem' as well as a saviour?",
     "The same strength that clears monsters also sacks cities and breaks hospitality — the myths keep both halves",
     ["He works only for pay", "He abandons every labour halfway", "He refuses to fight at all"],
     "Heracles is the honest hero: protector and destroyer are the same quality at different moments.",
     ["main"], "obj.prob.balance"),
   Q("q2", "What role does Heracles play in the mythological world?",
     "The great remover — he handles the dangers no one else can, and his power is what makes him both indispensable and dangerous",
     ["A model king and lawgiver", "A purely comic strong-man", "A villain the other heroes must stop"],
     "The Greeks made him the answer to any impossible problem — and the question of what such power costs.",
     ["main"], "obj.prob.use")])

ASSESSMENT = [
 ("grc.heroes.w05d01.the-catalogue-of-labours", "Why does Heracles owe the twelve labours?",
  "He killed his children in Hera-sent madness — the oracle sentences him to serve Eurystheus",
  ["He wants to win the throne of Tiryns", "Eurystheus hires him as a mercenary", "He seeks the gods' favour for a quest"],
  "The labours are penance, not ambition — the darkest origin for the greatest hero.", ["main"], "obj.labours.reason"),
 ("grc.heroes.w05d02.the-nemean-lion", "How does Heracles overcome the Nemean lion's unbreakable hide?",
  "He strangles it barehanded, then skins it with its own claws — the trophy becomes his signature garb",
  ["He shoots it with a magic bow", "He starves it in its cave", "He blinds it and ties it up"],
  "The lionskin and club that identify him in every image start with this fight.", ["main", "combat"], "obj.lion.fight"),
 ("grc.heroes.w05d03.madness-and-service", "What drives the persecution of Heracles?",
  "Hera's hatred of Zeus's mortal-born son — it produces the madness, the kin-killing, and the sentence of service",
  ["Eurystheus's envy of his strength", "A curse on his father Amphitryon", "His refusal of divine honours"],
  "The whole labour-cycle flows from Hera's jealousy — she is the engine of his suffering.", ["main"], "obj.mad.hate"),
 ("grc.heroes.w05d04.death-and-apotheosis", "How does Heracles die, and what follows?",
  "A poisoned robe from Deianira (the centaur's revenge) — then pyre on Oeta and ascent to Olympus, the only deified hero",
  ["He falls in the last labour at Hades' gate", "He is killed by Eurystheus's soldiers", "He dies old and forgotten"],
  "His end is unique: mortality burned away, divinity ascended.", ["main"], "obj.apo.god"),
 ("grc.heroes.w05d05.strong-man-or-problem", "Why is Heracles a 'problem' as well as a saviour?",
  "The same strength that clears monsters also breaks cities and hospitality — the myths preserve both halves",
  ["He is only dangerous when drunk", "He refuses all labours but easy ones", "He serves the wrong king"],
  "He is the honest hero: the power that protects is the power that wrecks.", ["main"], "obj.prob.balance")]

wpath = 'content/curriculum/greek/greek-heroes-week-05.json'
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
print('week 5 rewritten')

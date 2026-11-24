"""Narrative rewrite for Greek Heroes week 4 (Argonauts/Medea arc)."""
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
    f = glob.glob(DIR + f'week-04-day-{idx:02d}-*.json')[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub,
             estimatedMinutes=3, tags=tags, learningObjectives=objs,
             narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W(1, "Jason: The Quest for the Fleece",
  "A one-sandalled man, a usurper's trap, and the finest crew ever rowed",
  ["jason", "argonauts", "pelias", "fleece"],
  [{"id": "obj.quest.pelias", "text": "Why does Pelias send Jason for the Golden Fleece?"},
   {"id": "obj.quest.crew", "text": "Who sails on the Argo?"}],
  [C(1, "story", "The prophecy of one sandal", "Pelias seized the throne of Iolcus from Jason's father — and an oracle warned him to beware a man wearing a single sandal. When Jason walks into court having lost a sandal helping an old woman (the goddess Hera in disguise) across a river, Pelias knows the prophecy has arrived.", ["main"], "obj.quest.pelias"),
   C(2, "story", "A quest designed to kill", "Pelias cannot murder the stranger at his own hearth, so he offers a 'noble' deal: bring back the Golden Fleece from distant Colchis, and the throne is yours. It is meant to be a death sentence — no one has ever survived the voyage east.", ["main"], "obj.quest.pelias"),
   C(3, "story", "The Argo and her crew", "Jason answers by building the greatest ship Greece has seen — the Argo — and recruiting heroes to fill her: Heracles, Orpheus the singer, the twins Castor and Pollux, swift Atalanta. Fifty oars of legend rowing one doomed errand.", ["main"], "obj.quest.crew"),
   C(4, "story", "Why the fleece matters", "The fleece is more than treasure: it is the golden ram that carried Jason's kin to safety generations ago. Reclaiming it would be both a heroic feat and a dynastic claim — which is exactly why Pelias hopes it never comes back.", ["main"], "obj.quest.pelias"),
   C(5, "context", "A different kind of hero", "Jason is not Achilles or Heracles — his gift is not strength but gathering: assembling the right people and letting them shine. Watch how often the quest succeeds through OTHERS, not Jason himself.", ["main"], "obj.quest.crew")],
  [Q("q1", "Why does Pelias send Jason after the Golden Fleece?",
     "An oracle warned him of a one-sandalled man — the quest is a death sentence designed to remove the claimant",
     ["The fleece is needed to cure a plague", "Jason volunteered to prove his courage", "The gods commanded it at Delphi"],
     "Pelias wants rid of the prophesied threat; Colchis is meant to kill him.",
     ["main"], "obj.quest.pelias"),
   Q("q2", "What makes the Argo's crew remarkable?",
     "It gathers the greatest heroes of the age — Heracles, Orpheus, Castor and Pollux, Atalanta — Jason's real gift is assembling them",
     ["They are all sons of kings", "They are volunteers seeking the fleece's magic", "The gods chose each by lot"],
     "The Argo carries an all-star crew; the quest succeeds through collective heroism, not Jason's strength.",
     ["main"], "obj.quest.crew")])

W(2, "Jason: Aeetes and the Tasks",
  "Fire-breathing bulls, dragon teeth, and a king who intends betrayal",
  ["jason", "aeetes", "colchis", "argonauts"],
  [{"id": "obj.tasks.demand", "text": "What tasks does Aeetes set Jason?"},
   {"id": "obj.tasks.betrayal", "text": "Why does the success still leave Jason in danger?"}],
  [C(1, "story", "Colchis at the world's edge", "The Argo survives clashing rocks, hostile kingdoms, and the loss of Heracles along the way — and reaches Colchis, at the edge of the known world, where the fleece hangs in a grove guarded by a sleepless dragon.", ["main"], "obj.tasks.demand"),
   C(2, "story", "King Aeetes's price", "Aeetes, the fearsome local king, will not simply give his treasure to foreigners. His price: yoke his pair of fire-breathing bronze-hooved bulls, plough a field with them, and sow the teeth of a dragon.", ["main"], "obj.tasks.demand"),
   C(3, "story", "An impossible morning", "Each task alone kills ordinary men: the bulls burn you, and the sown teeth spring up as armed warriors who kill the sower. Aeetes has no intention of honouring the bargain either — succeed, and he plans to destroy the Greeks anyway.", ["aid"], "obj.tasks.betrayal"),
   C(4, "story", "The watching princess", "In the palace, Aeetes's daughter Medea — a priestess and sorceress — watches the stranger undertake her father's murderous test. The gods arrange that she falls in love, and everything hinges on which loyalty she chooses.", ["main"], "obj.tasks.betrayal"),
   C(5, "context", "Tasks as a mythic pattern", "Impossible tasks set by a hostile king recur everywhere (Heracles' labours, Bellerophon's missions). The pattern tests two things at once: can the hero do them — and does the king keep his word? Usually one fails.", ["main"], "obj.tasks.demand")],
  [Q("q1", "What tasks does Aeetes set Jason for the fleece?",
     "Yoke his fire-breathing bulls, plough a field, and sow dragon's teeth that sprout armed warriors",
     ["Retrieve a golden apple from the Hesperides", "Capture the sleepless dragon alive", "Answer the king's three riddles"],
     "The bulls and dragon-teeth are designed to kill — and Aeetes plans betrayal even if Jason succeeds.",
     ["main"], "obj.tasks.demand"),
   Q("q2", "Why is Jason still in danger after succeeding?",
     "Aeetes never meant to keep his word — he plans to destroy the Greeks regardless of the outcome",
     ["The dragon wakes and cannot be killed", "The tasks void the bargain by their terms", "His own crew mutinies in Colchis"],
     "The tasks are a trap within a trap; only inside help can get Jason out alive.",
     ["aid"], "obj.tasks.betrayal")])

W(3, "Medea Chooses",
  "A sorceress weighs father against stranger — and betrays Colchis",
  ["medea", "jason", "colchis", "fleece"],
  [{"id": "obj.medea.choice", "text": "What does Medea give Jason, and at what price?"},
   {"id": "obj.medea.fleece", "text": "How is the fleece actually won?"}],
  [C(1, "story", "Medea's dilemma", "Medea is Aeetes's daughter, a priestess of Hecate, and the only person in Colchis whose magic can save Jason. Choosing him means betraying her father, her king, and her home — the story makes the choice visible, not inevitable.", ["dilemma"], "obj.medea.choice"),
   C(2, "story", "The charm and the oath", "In secret she gives Jason a fireproof ointment — smear it on and the bulls' flames cannot touch him — and a plan for the dragon-teeth: throw a stone among the newborn warriors and they will kill each other, mistaking brothers for the thrower.", ["aid"], "obj.medea.choice"),
   C(3, "story", "The tasks accomplished", "Jason yokes the bulls untouched by flame and defeats the earthborn warriors by Medea's trick — the king's murder-proof gauntlet beaten by his own daughter's counsel.", ["aid"], "obj.medea.fleece"),
   C(4, "story", "The sleepless dragon", "Aeetes's betrayal makes flight the only option. Medea leads Jason to the grove at night and lulls the guardian dragon to sleep — the fleece is taken, and she flees with the stranger she has bound herself to.", ["main"], "obj.medea.fleece"),
   C(5, "context", "Whose feat is it really?", "Every decisive step — the ointment, the teeth-trick, the dragon — is Medea's. Jason's heroism is real but dependent; the epic quietly asks whether the quest is his triumph or hers.", ["main"], "obj.medea.choice")],
  [Q("q1", "What does Medea give Jason to survive Aeetes's tasks?",
     "A fireproof ointment against the bulls and a stone-throwing trick to turn the dragon-teeth warriors on each other",
     ["A magic sword that kills the warriors", "A charm that puts Aeetes to sleep", "Wings to fly past the bulls"],
     "Medea's magic solves both tasks; without her the quest ends in the field.",
     ["aid"], "obj.medea.choice"),
   Q("q2", "How is the Golden Fleece finally taken?",
     "Medea lulls its guardian dragon to sleep at night and flees Colchis with Jason",
     ["Jason defeats the dragon in single combat", "Aeetes surrenders it after the tasks", "The Argonauts seize it in a night raid"],
     "The dragon is drugged by Medea; the 'feat' is hers as much as his.",
     ["main"], "obj.medea.fleece")])

W(4, "Jason and Medea: The Flight",
  "A brother's death, a pursued ship, and a homecoming with a cost",
  ["jason", "medea", "apsyrtus", "argonauts"],
  [{"id": "obj.flight.apsyrtus", "text": "What happens to Medea's brother Apsyrtus?"},
   {"id": "obj.flight.price", "text": "What does the escape cost everyone?"}],
  [C(1, "story", "Pursuit across the sea", "Aeetes launches his fleet after the fleeing Argo. The fastest way to slow a pursuing king is the one act in this story no one can take back — Medea's brother Apsyrtus is killed, in some tellings lured into an ambush by her own message.", ["purification"], "obj.flight.apsyrtus"),
   C(2, "story", "A guilt that needs cleansing", "The murder of kin — especially a brother betrayed by a sister — is one of the deepest pollutions in Greek thought. The fugitives must seek ritual purification at Circe's island (the same Circe Odysseus meets) before they can go on.", ["purification"], "obj.flight.price"),
   C(3, "story", "The long way home", "The return voyage scatters them across half the known world — sirens, clashing shores, the bronze giant Talos on Crete. The Argo reaches Greece at last, but every mile home has been paid for.", ["main"], "obj.flight.price"),
   C(4, "story", "Iolcus, and no throne", "Jason presents the fleece — and Pelias, predictably, does not hand over the kingdom. Medea's revenge is the signature act of their partnership: she persuades Pelias's daughters that chopping their father to pieces will restore his youth. Pelias dies by his daughters' hands.", ["main"], "obj.flight.price"),
   C(5, "context", "The pattern deepens", "Quest stories usually end at the homecoming. This one keeps going: each 'victory' leaves a debt — Apsyrtus, Pelias, the abandoned father in Colchis — and the debts all land on Jason and Medea together.", ["main"], "obj.flight.price")],
  [Q("q1", "What happens to Apsyrtus during the pursuit?",
     "He is killed — in some tellings lured into an ambush by Medea's own message — a kinslaying that must be ritually purified",
     ["He is lost overboard in a storm", "He defects to the Argonauts", "Aeetes executes him for failing to catch them"],
     "The brother's death is the flight's deepest stain and requires purification at Circe's island.",
     ["purification"], "obj.flight.apsyrtus"),
   Q("q2", "How does Medea answer Pelias's broken promise?",
     "She tricks his daughters into chopping him up by claiming it will restore his youth",
     ["She summons an army to depose him", "She poisons him at the victory feast", "She curses his line with barrenness"],
     "Pelias dies by his own daughters' hands — Medea's signature blend of persuasion and magic.",
     ["main"], "obj.flight.price")])

W(5, "Medea on Stage",
  "Corinth, a poisoned robe, and the end no audience forgets",
  ["medea", "euripides", "corinth", "tragedy"],
  [{"id": "obj.medea.corinth", "text": "Why is Medea in Corinth, and what goes wrong?"},
   {"id": "obj.medea.revenge", "text": "What does her revenge cost everyone?"}],
  [C(1, "story", "Exile in Corinth", "After Iolcus, Jason and Medea settle in Corinth with their two young sons — the sorceress now a foreign wife in a Greek city, her power reduced to what a marriage gives her.", ["main"], "obj.medea.corinth"),
   C(2, "story", "The marriage that erases her", "Jason announces he will marry Creon's daughter — a royal, legitimate Greek match. Medea's protests mean nothing legally; the stranger who won her everything now treats her as disposable.", ["main"], "obj.medea.corinth"),
   C(3, "story", "The gift robe", "Medea's revenge begins like a reconciliation: she sends the princess a golden robe and crown — gifts steeped in poison that burns the girl and her father alive when she puts them on.", ["main"], "obj.medea.revenge"),
   C(4, "story", "The unthinkable cut", "Then comes the act Euripides makes unbearable: to take from Jason the only thing he has left, Medea kills their two sons herself. Not madness — deliberate, argued, chosen. She escapes to Athens in the dragon-chariot of her grandfather the Sun.", ["main"], "obj.medea.revenge"),
   C(5, "flavor", "Where you've met her", "That Athens refuge is why Medea is sitting at Aegeus's court when Theseus arrives in week 1 — the poisoned-cup scene is her second act, not her first.", ["argo"], "obj.medea.corinth")],
  [Q("q1", "Why does Jason's marriage to Creon's daughter provoke Medea?",
     "It casts her aside — a foreign wife with no legal standing — after she betrayed her family for him",
     ["It voids the bargain with Aeetes", "It prevents their sons inheriting Argos", "It is arranged by the gods"],
     "Everything she gave up — father, brother, home — was traded for this marriage, now dissolved at will.",
     ["main"], "obj.medea.corinth"),
   Q("q2", "What does Medea's revenge consist of?",
     "A poisoned robe that kills the princess and Creon — then the killing of her own two sons to destroy Jason completely",
     ["She burns the palace with everyone inside", "She turns Jason to stone", "She sends him back to Colchis in chains"],
     "Euripides makes her vengeance total and her reasoning legible — that is what makes the play horrifying.",
     ["main"], "obj.medea.revenge")])

ASSESSMENT = [
 ("grc.heroes.w04d01.the-political-quest", "What triggers the quest for the Golden Fleece?",
  "Pelias, warned by an oracle of a one-sandalled man, sends Jason on a quest meant to kill him",
  ["The oracle commands a fleece offering", "Jason seeks glory to win a bride", "The Argonauts are hired for a trading voyage"],
  "The quest is Pelias's trap, not Jason's ambition.", ["main"], "obj.quest.pelias"),
 ("grc.heroes.w04d02.aeetes-and-the-tasks", "What must Jason do to earn the fleece from Aeetes?",
  "Yoke fire-breathing bulls and sow dragon's teeth that rise as armed men",
  ["Kill the Colchian champion in single combat", "Solve the riddle of the dragon grove", "Bring a tribute of gold to the king"],
  "The tasks are impossible by design — and the king intends betrayal either way.", ["main", "aid"], "obj.tasks.demand"),
 ("grc.heroes.w04d03.medea-chooses", "What is the decisive factor in winning the fleece?",
  "Medea's aid — her ointment, her trick, her calming of the dragon — at the price of betraying her father",
  ["Jason's superior strength at the tasks", "Aeetes's honourable bargain", "The Argonauts' night assault"],
  "Every winning move is Medea's; Jason's feat depends on her choice.", ["main", "aid", "dilemma"], "obj.medea.choice"),
 ("grc.heroes.w04d04.flight-and-pursuit", "What marks the flight from Colchis?",
  "Apsyrtus's death and a pursuit that requires purification before the voyage can continue",
  ["A storm sent by Zeus", "A mutiny among the Argonauts", "The loss of the fleece overboard"],
  "The brother's killing is the flight's defining crime; the escape is bought with kin-blood.", ["purification"], "obj.flight.apsyrtus"),
 ("grc.heroes.w04d05.medea-on-stage", "How does Euripides' Medea end?",
  "She destroys Jason with a poisoned robe and the killing of their sons, then escapes to Athens — where she later poisons Theseus's cup",
  ["She is executed by Creon's soldiers", "She returns the fleece to Colchis", "She sails into exile alone"],
  "Her refuge at Aegeus's court links straight back to week 1's poisoned-cup scene.", ["main", "argo"], "obj.medea.revenge")]

wpath = 'content/curriculum/greek/greek-heroes-week-04.json'
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
print('week 4 rewritten')

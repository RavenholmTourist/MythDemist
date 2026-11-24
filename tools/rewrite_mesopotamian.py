"""Narrative rewrite for Mesopotamian starter pack (5 lessons)."""
import json, io, glob

REVIEW = {"status": "reviewed", "reviewedBy": "Devin (AI editorial review)", "reviewedAt": "2026-11-24",
          "reviewType": "editorial",
          "notes": "AI editorial review by Devin on 2026-11-24: narrative-first rewrite; cards retell the story, verbatim source excerpts preserved. This is not independent scholarly review or scholarly certification; specialist and community review remains recommended."}

def C(i, t, b, r, o, k="story"):
    return {"id": f"card-{i:02d}", "kind": k, "title": t, "body": b,
            "sourceRefIds": r, "objectiveIds": [o]}

def Q(qid, prompt, right, wrongs, expl, r, o):
    return {"id": qid, "type": "single-choice", "prompt": prompt,
            "choices": [{"id": "a", "text": right}] + [{"id": c, "text": t} for c, t in zip("bcd", wrongs)],
            "answerId": "a", "explanation": expl, "sourceRefIds": r, "objectiveIds": [o]}

def W(pat, title, sub, tags, objs, cards, quiz):
    f = glob.glob(f'content/lessons/mesopotamian/**/{pat}.json', recursive=True)[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub, estimatedMinutes=3,
             tags=tags, learningObjectives=objs, narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W("day-01-kingship-excess", "Gilgamesh: The King's Dream",
  "A tyrant so strong the gods must build him a match",
  ["gilgamesh", "uruk", "enkidu", "mesopotamian"],
  [{"id": "obj.gilg.problem", "text": "What kind of king is Gilgamesh at the start?"},
   {"id": "obj.gilg.answer", "text": "What do the gods create in answer?"}],
  [C(1, "Two-thirds god, all problem", "Gilgamesh, king of Uruk, is part divine and entirely too much: he exhausts his own people — young men conscripted for his endless games, brides claimed before their weddings. The city prays for relief.", ["dream"], "obj.gilg.problem"),
   C(2, "The gods' answer is not punishment", "Instead of destroying him, the gods make a COUNTERWEIGHT: a wild man named Enkidu, shaped from clay, running with the herds on the steppe — Gilgamesh's equal in strength.", ["dream"], "obj.gilg.answer"),
   C(3, "A dream foretells him", "Gilgamesh dreams of a meteor — or an axe — that he loves like a wife. His mother Ninsun reads it: a companion is coming who will be as strong as you and will save your life.", ["dream"], "obj.gilg.answer"),
   C(4, "The epic's real engine", "The story that follows is not about a tyrant being punished — it is about the first friendship in world literature, and what it costs. Everything in Gilgamesh turns on the bond formed next.", ["dream"], "obj.gilg.answer", "context"),
   C(5, "Oldest epic, newest problem", "This is the oldest surviving epic (c. 2100 BCE) — and its opening question is still ours: what do you do with a leader no one can stop? The gods' answer: give him an equal, not an enemy.", ["dream"], "obj.gilg.problem", "flavor")],
  [Q("q1", "Why do the people of Uruk cry out to the gods?",
     "Gilgamesh is an unbearable tyrant — exhausting the city with conscription and claiming brides",
     ["The city is under siege", "The harvest has failed", "Gilgamesh refuses to build temples"],
     "He's too strong and too much — the problem is his unchecked greatness, not an external enemy.",
     ["dream"], "obj.gilg.problem"),
   Q("q2", "What do the gods create in answer?",
     "Enkidu — a wild man of the steppe, Gilgamesh's equal and destined companion",
     ["A second king to depose him", "A flood to humble the city", "A prophecy to warn him"],
     "The gods' fix is a counterweight, not a punishment — the first friendship begins.", ["dream"], "obj.gilg.answer")])

W("day-02-enkidu-wild", "Enkidu: The Making of a Man",
  "From the herd to the city — what it costs to become human",
  ["enkidu", "shamhat", "uruk", "mesopotamian"],
  [{"id": "obj.enk.taming", "text": "How is Enkidu drawn out of the wild?"},
   {"id": "obj.enk.cost", "text": "What does he lose in becoming human?"}],
  [C(1, "Wild as the steppe", "Enkidu runs with gazelles, drinks at the water-hole, and frees animals from hunters' traps — a man made of clay, innocent of everything human.", ["change"], "obj.enk.taming"),
   C(2, "The trap that works", "Hunters can't catch him, so they send Shamhat, a temple woman. Six days and seven nights with her do what no snare could: afterwards the gazelles flee from him. He has become human — and wild things sense it.", ["change"], "obj.enk.taming"),
   C(3, "The price of belonging", "Enkidu gains speech, cooked food, beer, clothing — and loses the herd. The epic is blunt about the trade: civilization is a door that closes behind you.", ["change"], "obj.enk.cost"),
   C(4, "To Uruk", "Shamhat brings him to the city — and on the road he hears of Gilgamesh's tyranny over brides. Enkidu's first act as a human is to oppose the king: the equal the gods designed has arrived angry.", ["change"], "obj.enk.cost"),
   C(5, "An older Eden", "This is the world's earliest 'civilization costs innocence' story — two millennia before Genesis, the same pattern: eat, become aware, and the wilderness no longer wants you.", ["change"], "obj.enk.cost", "context")],
  [Q("q1", "How is Enkidu drawn from the wild?",
     "The temple woman Shamhat stays with him — afterwards the animals flee from him, and he is human",
     ["The hunters finally snare him", "Gilgamesh challenges him to combat", "He wanders to Uruk out of curiosity"],
     "Civilization reaches him through intimacy, not force — and the wild rejects him instantly.",
     ["change"], "obj.enk.taming"),
   Q("q2", "What does Enkidu lose by becoming human?",
     "His wild kin — the gazelles flee him, and he can never return to the herd",
     ["His strength", "His freedom to roam only", "His memory of the steppe"],
     "The epic prices civilization in lost kinship — the door closes behind him.", ["change"], "obj.enk.cost")])

W("day-03-friendship-grief", "Gilgamesh and Enkidu: The Wrestle",
  "They meet as enemies and end as the first friendship in literature",
  ["gilgamesh", "enkidu", "friendship", "mesopotamian"],
  [{"id": "obj.fight.start", "text": "How do Gilgamesh and Enkidu meet?"},
   {"id": "obj.fight.bond", "text": "What does the fight produce?"}],
  [C(1, "At the bride's door", "Enkidu blocks Gilgamesh from claiming another bride — and the king of Uruk, unbeaten, meets his match. They wrestle in the street until the city's walls shake.", ["meeting"], "obj.fight.start"),
   C(2, "Mutual recognition", "Gilgamesh wins — barely — and something unexpected happens: the two strongest beings in the world look at each other and stop. They embrace and become inseparable friends.", ["meeting"], "obj.fight.bond"),
   C(3, "The purpose of an equal", "The gods' design works exactly as planned: Gilgamesh's excess energy finally has somewhere to go — partnership instead of tyranny. The city gets relief; the king gets a brother.", ["meeting"], "obj.fight.bond"),
   C(4, "Restlessness follows", "But two strong men idle is its own problem. Gilgamesh proposes a fame-quest: the Cedar Forest and its guardian Huwawa. Enkidu warns him it is dangerous — and goes anyway, because that is what friends do.", ["meeting"], "obj.fight.bond"),
   C(5, "Why the friendship matters", "Gilgamesh is the first epic where the emotional core is a bond between two men, not a conquest or a romance. Enkidu's coming death — the grief that drives the second half — lands only because this friendship is real.", ["meeting"], "obj.fight.bond", "context")],
  [Q("q1", "How do Gilgamesh and Enkidu first meet?",
     "In a wrestling match — Enkidu blocks Gilgamesh from the bride, and they fight until the walls shake",
     ["On a hunting expedition", "At a council of the gods", "When Enkidu raids Uruk's herds"],
     "The city brawl is the meeting — the contest of equals.",
     ["meeting"], "obj.fight.start"),
   Q("q2", "What does the fight produce?",
     "Friendship — they become inseparable, and Gilgamesh's energy finally has a partner instead of victims",
     ["Enkidu is imprisoned", "Gilgamesh is exiled", "A lasting rivalry"],
     "The gods' counterweight works: the king's excess becomes partnership.", ["meeting"], "obj.fight.bond")])

W("day-04-flood-mortality", "The Cedar Forest: Huwawa's Terror",
  "The fame-quest that costs more than it earns",
  ["gilgamesh", "enkidu", "huwawa", "cedar"],
  [{"id": "obj.cedar.quest", "text": "Why do they go to the Cedar Forest?"},
   {"id": "obj.cedar.price", "text": "What does the victory cost?"}],
  [C(1, "A name worth having", "Gilgamesh wants the one thing immortality can't give: a name that outlasts him. The target is Huwawa — the monstrous guardian of the gods' Cedar Forest, whose roar alone can kill.", ["terror"], "obj.cedar.quest"),
   C(2, "Enkidu's foreboding", "Enkidu knows the guardian — he met Huwawa in his wild days — and warns that the giant's terror is the real weapon. The dream-omens Gilgamesh interprets as favour keep pulling them forward anyway.", ["terror"], "obj.cedar.quest"),
   C(3, "The terror defeated", "They reach the forest and do the deed — Huwawa is brought down by their combined strength and the god Shamash's favour. The fame-quest succeeds.", ["terror"], "obj.cedar.quest"),
   C(4, "And the gods notice", "But Huwawa was APPOINTED guardian by the gods — killing him is sacrilege as well as heroism. The victory becomes the charge-sheet: the divine council decides one of the two friends must pay.", ["terror"], "obj.cedar.price"),
   C(5, "The beginning of the grief", "The bill comes due in the next tablets: Enkidu sickens and dies. The fame-quest is the hinge — Gilgamesh gets his name and loses the person who made it bearable.", ["terror"], "obj.cedar.price", "context")],
  [Q("q1", "Why do Gilgamesh and Enkidu go to the Cedar Forest?",
     "For fame — Gilgamesh wants a name that outlasts him, and Huwawa's defeat is the prize",
     ["To steal the gods' cedar", "To rescue a captive priestess", "To fulfill a vow to Shamhat"],
     "The quest is glory-seeking — and the price is far higher than either expects.",
     ["terror"], "obj.cedar.quest"),
   Q("q2", "What is the cost of killing Huwawa?",
     "The gods mark it sacrilege — the council decides a life must pay, and Enkidu sickens and dies",
     ["The forest burns with them", "Gilgamesh is exiled forever", "The cedar turns to ash"],
     "The 'victory' is the bill — Enkidu's death begins the grief that drives the epic's second half.",
     ["terror"], "obj.cedar.price")])

W("day-05-fragmented-source", "Gilgamesh: The Broken Epic",
  "Reading a 4,000-year-old story from pieces of clay",
  ["gilgamesh", "epic", "fragments", "mesopotamian"],
  [{"id": "obj.frag.source", "text": "How does the epic reach us?"},
   {"id": "obj.frag.read", "text": "Why does the fragmentary state matter?"}],
  [C(1, "Clay, not parchment", "Gilgamesh survives on baked clay tablets — cuneiform libraries buried when cities fell. The story you read was literally dug out of the dirt in the 19th century.", ["pennsylvania"], "obj.frag.source"),
   C(2, "A text made of shards", "No single tablet has the whole epic. Scholars assemble it from overlapping fragments across tablets and centuries — the Pennsylvania tablet, the Yale tablet, pieces from Ashurbanipal's library — each filling another's gaps.", ["pennsylvania", "yale"], "obj.frag.source"),
   C(3, "Older than Homer by miles", "The story predates the Iliad by over a thousand years — and the flood account inside it is older than the version in Genesis, raising the famous question of which tradition borrowed from which.", ["yale"], "obj.frag.read"),
   C(4, "What the gaps mean", "The fragments' broken edges aren't just damage — they are part of what the text IS now. You read an epic about loss, assembled out of pieces, about the one thing everyone in it most wants and cannot keep: life without end.", ["pennsylvania"], "obj.frag.read"),
   C(5, "Why read a broken thing?", "Because it still works. Gilgamesh's grief for Enkidu lands across 4,000 years through clay dust — proof that the story was good enough to survive being buried alive.", ["yale"], "obj.frag.read", "flavor")],
  [Q("q1", "How does the Epic of Gilgamesh reach modern readers?",
     "Assembled from broken cuneiform tablets dug out of buried cities — overlapping fragments from different libraries",
     ["A single complete manuscript in Babylon", "Oral recitation preserved unbroken", "Carved on a palace wall"],
     "The epic is a jigsaw of shards — reading it is archaeology.",
     ["pennsylvania", "yale"], "obj.frag.source"),
   Q("q2", "Why does the fragmentary state matter?",
     "The text's brokenness is part of its meaning — an epic about loss literally lost, recovered piece by piece",
     ["It proves the epic is fiction", "It means we can't trust any part", "It makes the text shorter to read"],
     "The gaps are honest — a story about mortality that almost didn't survive its own.",
     ["yale"], "obj.frag.read")])

wpath = glob.glob('content/curriculum/mesopotamian/*week-01.json')[0]
w = json.load(io.open(wpath, encoding='utf-8'))
for day in w['days']:
    les = json.load(io.open(day['lessonPath'], encoding='utf-8'))
    day['title'] = les['title']
json.dump(w, io.open(wpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('mesopotamian rewritten')

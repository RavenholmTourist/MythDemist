"""Narrative rewrite for Slavic starter pack (5 lessons)."""
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
    f = glob.glob(f'content/lessons/slavic/**/{pat}.json', recursive=True)[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub, estimatedMinutes=3,
             tags=tags, learningObjectives=objs, narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W("day-01-baba-yaga", "Baba Yaga: The House on Legs",
  "A witch in a hut that walks — the forest's most dangerous gatekeeper",
  ["baba-yaga", "folktale", "forest", "slavic"],
  [{"id": "obj.baba.hut", "text": "What is Baba Yaga's house?"},
   {"id": "obj.baba.role", "text": "Is she villain, helper, or both?"}],
  [C(1, "The hut that walks", "Deep in the forest stands a hut on chicken legs — it turns and dances and squats to let visitors in only when they ask the right way. Around it, a fence of bones; on the posts, skulls whose eyes burn at night.", ["scene"], "obj.baba.hut"),
   C(2, "The old woman in the mortar", "Baba Yaga herself flies in a mortar, driving with a pestle, sweeping her tracks away with a broom. She is old beyond measure, iron-nosed, and always hungry for news of the outside.", ["scene"], "obj.baba.hut"),
   C(3, "Both monster and test", "The tales never decide her: she eats the unwary, but for the right visitor — the courteous, the patient, the well-advised — she gives impossible tasks and then the help to pass them. She is the forest's gatekeeper, not simply its villain.", ["scene"], "obj.baba.role"),
   C(4, "The riders at the door", "At her gate pass three riders — white for dawn, red for day, black for night — the day's passage personified. Even time itself rides in her service; this witch stands at the world's hinges.", ["scene"], "obj.baba.role"),
   C(5, "Why she's everywhere", "Baba Yaga is the Slavic tradition's indispensable figure: the dangerous border between the everyday world and the deep forest where everything is possible. Every quest in this pack passes her gate.", ["scene"], "obj.baba.role", "flavor")],
  [Q("q1", "What is Baba Yaga's house?",
     "A hut that stands and turns on chicken legs, fenced with bones and burning-eyed skulls",
     ["A stone tower in the deep forest", "A cave beneath a birch tree", "A palace of ice"],
     "The chicken-legged hut is her signature — it moves, and only admits visitors who know how to ask.",
     ["scene"], "obj.baba.hut"),
   Q("q2", "What role does Baba Yaga play in the tales?",
     "Both devourer of the unwary and gatekeeper who aids the courteous — the forest's test, not just its monster",
     ["Pure villain to be destroyed", "A kindly grandmother", "A captive princess in disguise"],
     "Her ambiguity is the point — the forest gives what you're equipped to ask for.",
     ["scene"], "obj.baba.role")])

W("day-02-koschei-hidden-death", "Koschei: Death in an Egg",
  "The deathless villain whose death is hidden at the edge of the world",
  ["koschei", "death", "egg", "slavic"],
  [{"id": "obj.kos.hidden", "text": "Where does Koschei keep his death?"},
   {"id": "obj.kos.chain", "text": "How is he finally killed?"}],
  [C(1, "The undying abductor", "Koschei the Deathless is the Slavic cycle's great villain — a withered sorcerer who abducts brides and heroes' loves and cannot be killed, because his death is not in him.", ["death"], "obj.kos.hidden"),
   C(2, "A nesting doll of death", "His death is hidden inside layers: on the tip of a needle, inside an egg, inside a duck, inside a hare, inside an iron chest, buried under an oak on the island of Buyan at the edge of the world.", ["death"], "obj.kos.hidden"),
   C(3, "Only helpers reach it", "No hero fights Koschei head-on and wins. The path to the egg runs through helpers — a wolf, an eagle, a pike — each earned by a kindness the hero did earlier. The chain of favours is the actual weapon.", ["wolf"], "obj.kos.chain"),
   C(4, "The egg in his face", "When the egg is finally brought to Koschei, the hero doesn't even need to break it: holding it, he can make the sorcerer helpless — crushing it kills him. The most dangerous thing in the world is his own hidden death.", ["wolf"], "obj.kos.chain"),
   C(5, "Death externalized", "The pattern — a giant whose life is hidden outside his body — is one of folklore's most travelled ideas (the giant's heart in the well, the troll's heart in the egg). It says: the unkillable are still fragile — you just have to find where the fragility lives.", ["death"], "obj.kos.hidden", "context")],
  [Q("q1", "Where does Koschei keep his death?",
     "On a needle's tip, in an egg, in a duck, in a hare, in a chest under an oak on the island of Buyan",
     ["In a ring on his finger", "In the roots of the world-tree", "In a stone in his chest"],
     "The nested hiding — needle, egg, duck, hare, chest, island — is the tale's famous riddle.",
     ["death"], "obj.kos.hidden"),
   Q("q2", "How does the hero finally defeat Koschei?",
     "He gains the egg through helpers earned by earlier kindnesses — holding or crushing it ends the sorcerer",
     ["He burns the iron chest on a pyre", "He finds Koschei's true name", "He beheads Koschei in single combat"],
     "The weapon is the favours-chain — kindnesses, not swords, reach the death.",
     ["wolf"], "obj.kos.chain")])

W("day-03-vasilissa-wise", "Vasilissa and the Doll",
  "A dying mother's gift — and the tasks that make a girl survive Baba Yaga",
  ["vasilissa", "doll", "baba-yaga", "slavic"],
  [{"id": "obj.vas.doll", "text": "What does Vasilissa's doll do for her?"},
   {"id": "obj.vas.tasks", "text": "How does she survive Baba Yaga's tasks?"}],
  [C(1, "A mother's last gift", "Vasilissa's dying mother gives her a little doll and a blessing: keep it with you, feed it, and it will advise you. Then she dies, and the stepmother and stepsisters begin to work the girl like a servant.", ["doll"], "obj.vas.doll"),
   C(2, "Sent to the witch", "The stepsisters put out the fire at home and send Vasilissa to Baba Yaga for a light — a mission no one expects her to survive. On the way she feeds her doll and asks its counsel.", ["doll"], "obj.vas.doll"),
   C(3, "Tasks for a meal", "Baba Yaga sets impossible tasks — sort a barn of poppy-seeds from dirt overnight, wash the linen, cook the feast — before she'll part with fire. The doll does the sorting while Vasilissa sleeps; each day the task is done by dawn.", ["task"], "obj.vas.tasks"),
   C(4, "The lantern of skulls", "The witch, outwitted, sends her home with a burning skull on a stick — which flies home and burns the stepmother and stepsisters to ash. The tale is brutal and just: the helpers' cruelty is answered by the very fire they sent for.", ["task"], "obj.vas.tasks"),
   C(5, "The tale's real heroine", "Vasilissa survives not by strength or wit alone but by a chain of rightness — love for the doll, obedience to its counsel, patience through the tasks. The tale's pattern: kindness is the skill that survives the forest.", ["doll", "task"], "obj.vas.tasks", "context")],
  [Q("q1", "What is Vasilissa's doll?",
     "Her dying mother's gift — kept and fed, it advises her and does the impossible tasks while she sleeps",
     ["A charm against Baba Yaga's eye", "Her mother's ghost in miniature", "A toy the stepsisters envied"],
     "The doll is the story's magic: maternal blessing made object.",
     ["doll"], "obj.vas.doll"),
   Q("q2", "How does Vasilissa survive Baba Yaga?",
     "She completes each impossible task through the doll's help and her own courtesy — and is sent home with the burning skull",
     ["She bribes the witch's cat", "She escapes through the fence-gate", "She tricks the witch into the oven"],
     "She wins by following the doll's counsel — the tale rewards patience and rightness.",
     ["task"], "obj.vas.tasks")])

W("day-04-water-king-bargain", "The Water King: The Bargain",
  "A promise made over a bridge — and a father who must pay with his son",
  ["water-king", "bargain", "ivan", "slavic"],
  [{"id": "obj.king.bargain", "text": "What does the merchant promise the Water King?"},
   {"id": "obj.king.escape", "text": "How does the son escape?"}],
  [C(1, "Thirst at the bridge", "A merchant crossing a bridge stops to drink — and a hand from the water seizes him. The Water King demands the thing he loves most at home — or the thing he does not know he has.", ["bridge"], "obj.king.bargain"),
   C(2, "The fatal unknowing", "The merchant promises 'whatever is at home that I don't know about' — the classic trap. While he was away, his wife bore him a son: the bargain binds the child he has never seen.", ["bridge"], "obj.king.bargain"),
   C(3, "The son goes to pay", "Years later the debt is called. The boy — Ivan — must go to the Water King's underwater palace. He does not drown: in these tales the underwater world is simply another kingdom.", ["help"], "obj.king.escape"),
   C(4, "Daughters as guides", "In the underwater palace, the Water King's daughters are his instruments — but one of them helps the boy instead: she tells him which maiden to choose and how to flee. Escape is won by an ally inside the enemy's house.", ["help"], "obj.king.escape"),
   C(5, "The bargain's lesson", "This is the 'rash promise' tale — the thing you don't know you have is always the thing you can't afford to lose. The father's haste is paid by the child; the escape is earned by the one helper inside.", ["bridge", "help"], "obj.king.bargain", "context")],
  [Q("q1", "What does the merchant promise the Water King?",
     "Whatever is at home that he doesn't know about — which turns out to be his newborn son",
     ["All his ships and cargo", "A bride from the king's daughters", "Half his inheritance"],
     "The 'unknown thing' clause is the trap — his haste mortgages a child he hasn't met.",
     ["bridge"], "obj.king.bargain"),
   Q("q2", "How does the son escape the underwater kingdom?",
     "The Water King's own daughter helps him — guiding his choice and his flight from her father's palace",
     ["He holds his breath and swims to the surface", "He kills the Water King", "He bargains for a second chance"],
     "Escape runs through an insider ally — the helper inside the enemy's house.",
     ["help"], "obj.king.escape")])

W("day-05-firebird-quest", "The Firebird: The Shining Quest",
  "A feather of fire, a grey wolf, and a quest that keeps making new demands",
  ["firebird", "wolf", "ivan", "slavic"],
  [{"id": "obj.fire.quest", "text": "What sends Ivan on the quest?"},
   {"id": "obj.fire.wolf", "text": "What is the wolf's role?"}],
  [C(1, "The feather that starts it", "A tsar covets the Firebird — the glowing bird that comes to steal his golden apples. His youngest son Ivan goes to catch it and finds only a feather — but a feather so bright it lights the room.", ["story"], "obj.fire.quest"),
   C(2, "The wolf who eats his horse", "On the road a grey wolf eats Ivan's horse — then, in compensation, becomes his guide and mount: faster than any horse, wiser than any courtier, and the architect of every success Ivan has.", ["wolf"], "obj.fire.wolf"),
   C(3, "Demands that multiply", "Each prize breeds a new demand: the Firebird requires a golden cage; the beautiful princess requires another princess's hand in exchange; each errand to a new tsar spirals. The quest teaches that getting is never the end.", ["story"], "obj.fire.quest"),
   C(4, "The wolf makes it work", "Through every snag, the wolf's counsel rescues Ivan — impersonating him, advising his refusals, turning each 'impossible' exchange around. The hero's real strength is that he listens to the wolf.", ["wolf"], "obj.fire.wolf"),
   C(5, "A chapbook's reach", "The Firebird tale survived in cheap printed chapbooks — folk publishing that carried the stories to generations. The tale's structure — radiant prize, wise animal guide, cascading demands — is one of the world's most copied quest-patterns.", ["provenance"], "obj.fire.quest", "flavor")],
  [Q("q1", "What sends Ivan on the Firebird quest?",
     "His tsar father covets the bird that steals his golden apples — Ivan brings back a feather and the quest grows from there",
     ["The Firebird burns his city", "He seeks the bird to cure his mother", "A dream commands him"],
     "The feather's radiance hooks the tsar — one prize always demands another.",
     ["story"], "obj.fire.quest"),
   Q("q2", "What is the grey wolf's role in the tale?",
     "Ivan's guide and rescuer — after eating his horse, the wolf carries him, advises him, and solves each impossible demand",
     ["A beast Ivan must kill", "The Firebird's guardian", "A villain in disguise"],
     "The wolf is the tale's real hero — Ivan succeeds by listening.",
     ["wolf"], "obj.fire.wolf")])

wpath = glob.glob('content/curriculum/slavic/*week-01.json')[0]
w = json.load(io.open(wpath, encoding='utf-8'))
for day in w['days']:
    les = json.load(io.open(day['lessonPath'], encoding='utf-8'))
    day['title'] = les['title']
json.dump(w, io.open(wpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('slavic rewritten')

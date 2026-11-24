"""Narrative rewrite for Celtic starter pack (5 lessons, the Mabinogion arc)."""
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
    f = glob.glob(f'content/lessons/celtic/**/{pat}.json', recursive=True)[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub, estimatedMinutes=3,
             tags=tags, learningObjectives=objs, narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W("day-01-pwyll-otherworld", "Pwyll and the Otherworld",
  "A prince swaps places with a deathless lord for a year — the opening of the Mabinogion",
  ["pwyll", "arawn", "rhiannon", "celtic"],
  [{"id": "obj.pwyll.swap", "text": "What bargain does Arawn offer Pwyll?"},
   {"id": "obj.pwyll.rhiannon", "text": "What makes Rhiannon's courtship strange?"}],
  [C(1, "A hunt that opens a door", "Pwyll, prince of Dyfed, hunts on a misty morning and chases a strange stag — into a clearing where he meets Arawn, lord of Annwn, the Otherworld. They have offended each other's courtesy.", ["main"], "obj.pwyll.swap"),
   C(2, "The strangest bargain in Welsh myth", "Arawn offers a fix: swap places for one year. Pwyll will rule Annwn in Arawn's shape, fight Arawn's enemy king, and — the catch — share Arawn's queen's bed. Honour demands he touch no one.", ["main"], "obj.pwyll.swap"),
   C(3, "A year well kept", "Pwyll keeps the bargain perfectly: he defeats the enemy in the year-end single combat, and through a whole year in the Otherworld never touches the queen. Returning home, the two kingdoms are bound in friendship.", ["main"], "obj.pwyll.swap"),
   C(4, "Then comes Rhiannon", "The story's second wonder: Rhiannon rides past on a horse no rider can catch — until Pwyll simply asks her to stop. She has come for him, having refused the suitor her father chose. The marriage is made with her consent, not the suitor's claim.", ["main"], "obj.pwyll.rhiannon"),
   C(5, "What the tale is for", "The Mabinogion's first branch teaches the book's values: a bargain kept, a woman choosing her own husband, the Otherworld a mirror to the courtly one. These tales care about honour more than swordplay.", ["main"], "obj.pwyll.swap", "context")],
  [Q("q1", "What is Arawn's bargain with Pwyll?",
     "Swap places for a year — rule Annwn, fight his enemy, and share his queen's bed without touching her",
     ["Foster his son for seven years", "Bring him the magic cauldron", "Fight his champion at midsummer"],
     "The year-long exchange tests courtesy above all — Pwyll keeps it perfectly.",
     ["main"], "obj.pwyll.swap"),
   Q("q2", "What makes Rhiannon's courtship unusual?",
     "She chooses Pwyll herself — riding past uncatchably until he simply asks her to stop, refusing the suitor chosen for her",
     ["She is won in a tournament", "Her father offers her as a prize", "She appears only in dreams"],
     "Her agency is the point — the tale gives her the choosing.",
     ["main"], "obj.pwyll.rhiannon")])

W("day-02-branwen-sovereignty", "Branwen: The Insult That Started a War",
  "A marriage meant to heal — and a kingdom burned for a face-slapped horse",
  ["branwen", "mabinogion", "ireland", "celtic"],
  [{"id": "obj.bran.insult", "text": "What insult poisons the Irish marriage?"},
   {"id": "obj.bran.cost", "text": "What does the war cost?"}],
  [C(1, "The bridge of ships", "Bran the Blessed, giant king of Britain, wades the sea to Ireland for a marriage treaty: his sister Branwen will wed the Irish king Matholwch. The alliance is meant to bind two peoples.", ["insult"], "obj.bran.insult"),
   C(2, "The insult that undoes it", "Bran's half-brother Efnisien, furious he wasn't consulted, mutilates Matholwch's horses — lips, ears, tails. The Irish king treats it as a calculated insult, and the 'peace' is poisoned from the wedding day.", ["insult"], "obj.bran.insult"),
   C(3, "Branwen in the kitchen", "In Ireland, Matholwch's revenge is quiet cruelty: Branwen is demoted to work in the kitchens, her son kept hostage. A starling she trains carries her plea for rescue back to Britain.", ["message"], "obj.bran.cost"),
   C(4, "The war over the sea", "Bran wades across with his army for the rescue — and Ireland offers peace through trickery, hiding warriors in the hall. The battle that follows destroys almost everyone on both sides.", ["main"], "obj.bran.cost"),
   C(5, "The cost of a horse's ear", "From a mutilated horse to a war that annihilates two kingdoms: the tale teaches that small insults, unanswered, compound. Branwen dies of grief homecoming, and the surviving Britons flee with Bran's severed — still-talking — head.", ["main"], "obj.bran.cost", "context")],
  [Q("q1", "What insult poisons the Irish marriage?",
     "Efnisien mutilates Matholwch's horses — the half-brother offended at not being consulted",
     ["The bride is given a false crown", "The feast lacks meat for the guests", "The king refuses the wedding-gift"],
     "A petty vandalism compounds into war — the tale's warning about unchecked insults.",
     ["insult"], "obj.bran.insult"),
   Q("q2", "How does Branwen summon rescue?",
     "She trains a starling to carry her plea across the sea to Bran",
     ["She writes on a birch scroll", "She sends her son secretly", "A merchant smuggles her message"],
     "The trained bird is the detail the tale is famous for.",
     ["message"], "obj.bran.cost")])

W("day-03-manawydan-patience", "Manawydan: The Enchantment",
  "A whole castle gone mist — and patience as the hero's weapon",
  ["manawydan", "rhiannon", "enchantment", "celtic"],
  [{"id": "obj.man.mist", "text": "What happens to Rhiannon and Pryderi?"},
   {"id": "obj.man.mouse", "text": "How does Manawydan break the spell?"}],
  [C(1, "A feast interrupted by mist", "Manawydan — Bran's brother and Branwen's widower-friend — is feasting with Rhiannon and her son Pryderi when a white mist rolls in. When it clears, the palace and every person in it has vanished.", ["main"], "obj.man.mist"),
   C(2, "An empty kingdom", "The three survivors — Manawydan, Rhiannon, Pryderi — walk a depopulated landscape. Pryderi follows a strange boar into a fort and doesn't come out; Rhiannon follows and vanishes too.", ["main"], "obj.man.mist"),
   C(3, "Alone and patient", "Manawydan alone stays — not fighting, not raging, just present. He plants wheat, harvests it, lives quietly in the ruined land, because the other way is already tried.", ["main"], "obj.man.mouse"),
   C(4, "The mouse's secret", "When a mouse steals his grain, he catches it — and instead of killing it, ties it up to hang. A stranger arrives offering ransom for it: the 'mouse' is the enchanter's wife, and the spell is broken for her life.", ["mouse", "reveal"], "obj.man.mouse"),
   C(5, "Patience as victory", "Where Greek heroes win by doing, Manawydan wins by waiting and noticing — the Welsh hero-ideal is different: quiet attention, not force, breaks the enchantment.", ["reveal"], "obj.man.mouse", "context")],
  [Q("q1", "What happens when the mist clears?",
     "The palace and all its people have vanished — only Manawydan, Rhiannon, and Pryderi remain in an empty land",
     ["The castle is buried in snow", "The feast becomes a funeral", "Rhiannon is taken to Annwn"],
     "The mist takes the whole population — the enchantment is total.",
     ["main"], "obj.man.mist"),
   Q("q2", "How is the enchantment finally broken?",
     "Manawydan catches the enchanter's wife disguised as a mouse and ransoms her for the people's return",
     ["He finds the hidden cauldron", "He duels the enchanter", "Rhiannon frees herself by cunning"],
     "Patience plus a single caught mouse — the Welsh hero wins by waiting.",
     ["mouse", "reveal"], "obj.man.mouse")])

W("day-04-math-sovereignty", "Math: Magic and Sovereignty",
  "A king who needs a virgin foot-holder — and a nephew who makes a wife from flowers",
  ["math", "gwydion", "blodeuwedd", "celtic"],
  [{"id": "obj.math.rule", "text": "What is Math's strange royal custom?"},
   {"id": "obj.math.flower", "text": "How is Blodeuwedd made?"}],
  [C(1, "A king's peculiar rule", "Math, king of Gwynedd, can only hold office while his feet rest in a virgin's lap — a magical condition of rule so specific it reads like law. His nephew Gwydion exploits this to start a war for his brother.", ["rule"], "obj.math.rule"),
   C(2, "The flower-wife", "Punished for the war, Gwydion's nephew Lleu has a wife made for him by magic — Blodeuwedd, fashioned from oak, broom, and meadowsweet flowers, the most beautiful woman ever made.", ["rule"], "obj.math.flower"),
   C(3, "The wife who was flowers", "Blodeuwedd loves a stranger and plots her husband's death — he can only be killed under impossible conditions, which she tricks him into demonstrating. She is made of flowers, not flesh — the tale's strange cruelty.", ["testimony"], "obj.math.flower"),
   C(4, "Owl in the oak", "Lleu is not quite killed — he turns into an eagle. Blodeuwedd is punished by being made an owl, shunned by every other bird. Justice in the tale is transformation, not death.", ["testimony"], "obj.math.flower"),
   C(5, "The strangest tale of the four", "The Fourth Branch asks what a person made of flowers owes to human loyalty — and what happens when a created thing chooses for herself. It's the uncanniest of the Mabinogion.", ["testimony"], "obj.math.flower", "context")],
  [Q("q1", "What is Math's peculiar condition of rule?",
     "He can only hold office while his feet rest in a virgin's lap — a magical law of sovereignty",
     ["He must never touch iron", "He rules only at night", "His crown must be remade each year"],
     "The foot-holder condition is the tale's strangest law — Gwydion exploits it to trigger war.",
     ["rule"], "obj.math.rule"),
   Q("q2", "What is Blodeuwedd?",
     "A woman made from flowers — created to be Lleu's wife, who chooses a lover and plots his death",
     ["A fairy who seduces the king", "A sorceress who curses Gwydion", "A giantess from the Otherworld"],
     "Made from oak, broom, and meadowsweet — the flower-wife's betrayal is the Fourth Branch's heart.",
     ["testimony"], "obj.math.flower")])

W("day-05-taliesin-change", "Taliesin: The Shape-Shifter",
  "Chased through a dozen forms — the poet who becomes everything he sings",
  ["taliesin", "cerridwen", "cauldron", "celtic"],
  [{"id": "obj.tal.chase", "text": "How does Taliesin escape Cerridwen?"},
   {"id": "obj.tal.poet", "text": "What does his transformation make him?"}],
  [C(1, "The three drops of wisdom", "The witch Cerridwen brews a cauldron of wisdom for her ugly son — three drops will grant all knowledge. Her servant-boy Gwion stirs it, and the drops splash on his thumb instead.", ["cauldron"], "obj.tal.chase"),
   C(2, "Instant omniscience", "The moment the drops touch his tongue, Gwion knows everything — including that Cerridwen will kill him. He flees by changing shape: a hare, a fish, a bird, a grain of wheat.", ["cauldron"], "obj.tal.chase"),
   C(3, "The chase that can't end", "Cerridwen pursues as a greyhound, an otter, a hawk — and finally as a hen she swallows the wheat-grain that is Gwion. She thinks the chase is done.", ["chase"], "obj.tal.chase"),
   C(4, "Born again as Taliesin", "But swallowing him makes her pregnant — nine months later she births a shining infant and, unable to kill it, casts him into the sea. Rescued from the weir, he grows into Taliesin, the greatest of bards.", ["chase"], "obj.tal.poet"),
   C(5, "Poetry as transformation", "Taliesin's story is the poet's myth of itself: the bard claims to have BEEN everything — the hunt, the grain, the child in the sea. Imagination lets a man wear every shape; that is what the tale says poetry is.", ["cauldron", "chase"], "obj.tal.poet", "flavor")],
  [Q("q1", "How does Gwion escape Cerridwen?",
     "By shape-shifting through animal forms — until she swallows him as a grain of wheat and he is reborn",
     ["By killing her in the chase", "By hiding in the mountains", "By drinking the whole cauldron"],
     "He doesn't escape — he transforms into her rebirth.", ["cauldron", "chase"], "obj.tal.chase"),
   Q("q2", "What does Taliesin's story say about the poet?",
     "That imagination lets the poet BE everything — the shape-shifter claims he has been every form he sings",
     ["That poetry is magic for hire", "That wisdom belongs to the old", "That the poet serves only kings"],
     "The bard's claim — 'I have been all things' — is the tale's myth of poetry itself.",
     ["chase"], "obj.tal.poet")])

wpath = glob.glob('content/curriculum/celtic/*week-01.json')[0]
w = json.load(io.open(wpath, encoding='utf-8'))
for day in w['days']:
    les = json.load(io.open(day['lessonPath'], encoding='utf-8'))
    day['title'] = les['title']
json.dump(w, io.open(wpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('celtic rewritten')

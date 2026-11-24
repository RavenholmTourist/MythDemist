"""Narrative rewrite for Norse starter pack (5 lessons)."""
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
    f = glob.glob(f'content/lessons/norse/**/{pat}.json', recursive=True)[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub, estimatedMinutes=3,
             tags=tags, learningObjectives=objs, narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W("day-01-odin-wisdom", "Odin: The Price of Wisdom",
  "One eye in a well, nine nights on a tree — knowledge is never free",
  ["odin", "mimir", "runes", "norse"],
  [{"id": "obj.odin.eye", "text": "What does Odin give for wisdom?"},
   {"id": "obj.odin.runes", "text": "How does he win the runes?"}],
  [C(1, "One eye for a drink", "Mimir's well holds wisdom itself, and its keeper will share it only at a price. Odin pays with an eye — dropped into the well, where it stays. From then on the wisest god sees the world through one.", ["mimer"], "obj.odin.eye"),
   C(2, "Nine nights on the tree", "For the runes — the sacred letters that carry magic and knowledge — Odin performs a self-sacrifice: hanging nine nights on the world-tree Yggdrasil, wounded by his own spear, offering himself to himself. No food, no drink, nobody's help.", ["runes"], "obj.odin.runes"),
   C(3, "He takes the runes screaming", "At the end of the ordeal, wisdom arrives: he looks down, sees the runes below, and seizes them. The price of the knowledge is the suffering itself — it cannot be shortcut.", ["runes"], "obj.odin.runes"),
   C(4, "The wanderer-god", "Odin is not a thunderbolt king — he walks the world in a grey cloak and broad hat, trading small favours for news. Kings have had their hall conversations with him without ever knowing who sat at their fire.", ["mimer"], "obj.odin.eye"),
   C(5, "Wisdom that still costs", "Every knowledge-gain in Norse myth is paid for — an eye, nine nights, a hand. Watch for the pattern: in this tradition, the universe keeps accounts.", ["mimer"], "obj.odin.eye", "context")],
  [Q("q1", "What does Odin pay for a drink from Mimir's well?",
     "One of his eyes — left in the well as a pledge for wisdom",
     ["A hand of gold", "Nine years of service", "The spear Gungnir"],
     "The well's price is permanent: wisdom bought with sight.", ["mimer"], "obj.odin.eye"),
   Q("q2", "How does Odin win the runes?",
     "By hanging nine nights wounded on Yggdrasil — a self-sacrifice that finally reveals them",
     ["By stealing them from a giant's hall", "By deciphering them on the tree's bark", "By trading an eye to the dwarves"],
     "The runes are won through ordeal, not study — the suffering is the purchase.", ["runes"], "obj.odin.runes")])

W("day-02-thor-protection", "Thor: The Walls' Defender",
  "Red-bearded, blunt, and the only thing between the gods and the giants",
  ["thor", "mjolnir", "giants", "norse"],
  [{"id": "obj.thor.role", "text": "What is Thor's role among the gods?"},
   {"id": "obj.thor.humour", "text": "How does he handle the stolen-hammer humiliation?"}],
  [C(1, "The gods' bouncer", "Where Odin schemes, Thor breaks things. He is the gods' physical answer to the giants who forever threaten Asgard — his hammer Mjolnir is the one weapon the giants genuinely fear.", ["loss"], "obj.thor.role"),
   C(2, "The hammer goes missing", "One morning Thor wakes and Mjolnir is gone — stolen by the giant Thrym, who hides it deep underground and names his price: the goddess Freyja as his bride.", ["loss"], "obj.thor.role"),
   C(3, "The unthinkable disguise", "Freyja refuses — with a rage that shakes the hall. Loki's counter-plan: dress Thor as the bride. The strongest god in the world puts on a wedding gown and veil, fretting that 'the gods will call me unmanly' — but they need the hammer.", ["disguise"], "obj.thor.humour"),
   C(4, "Veiled and vengeful", "At the giant's feast, the 'bride' eats a whole ox and drinks oceans of mead while the giant puzzles over her appetite. The moment the hammer is laid in his lap as a wedding blessing, the veil comes off: Thor takes back Mjolnir and smashes the hall.", ["return"], "obj.thor.humour"),
   C(5, "Why Thor endures", "Thor is the people's god — not clever, not subtle, but reliable: the one who always shows up and always hits the problem. The myths love him for it, and so did the farmers who wore his hammer as an amulet.", ["return"], "obj.thor.role", "flavor")],
  [Q("q1", "What is Thor's role in the Norse world?",
     "The gods' defender — the physical force that keeps the giants from Asgard",
     ["The trickster who causes trouble", "The wise counsellor of Odin", "The god of the harvest"],
     "He is the wall: blunt, strong, and the answer when scheming fails.", ["loss"], "obj.thor.role"),
   Q("q2", "How does Thor recover his stolen hammer?",
     "He disguises himself as Freyja the bride, is admitted to the giant's wedding, and grabs Mjolnir when it's laid in his lap",
     ["He tunnels beneath the giant's hall", "He wins it back in single combat", "Loki steals it back for him"],
     "The plan is humiliation embraced as strategy — the hammer returns with the veil.", ["disguise", "return"], "obj.thor.humour")])

W("day-03-loki-ambiguity", "Loki: The Problem Inside",
  "The gods' best fixer and their worst one — often in the same story",
  ["loki", "trickster", "norse"],
  [{"id": "obj.loki.both", "text": "Why is Loki both rescue and ruin?"},
   {"id": "obj.loki.bound", "text": "What finally happens to him?"}],
  [C(1, "The gods' fixer", "When the gods need a cheat, a shortcut, or a lie that works, Loki is the one they call — he talks them out of debts, tricks giants out of their own plans, and once gives birth to Odin's eight-legged horse.", ["lokasenna"], "obj.loki.both"),
   C(2, "And their ruin", "The same Loki engineers the death of Baldr — the most loved of the gods — by tricking the blind god Hodr into throwing mistletoe, the one thing in the world that can kill him.", ["lokasenna"], "obj.loki.both"),
   C(3, "The flyting", "Cornered at a feast, Loki turns on the entire pantheon: he recites each god's private shame aloud — their cowardice, their secrets — until they finally seize him. The poem is called the Lokasenna, 'Loki's Flyting', and it is as brutal as it sounds.", ["lokasenna"], "obj.loki.both"),
   C(4, "Bound until the end", "The gods bind Loki in a cave beneath the world with the entrails of his own sons, a serpent dripping venom onto his face. His wife holds a bowl to catch the poison; when she empties it, the drips make him writhe — and the earth shakes. He stays bound until Ragnarök, when he will lead the forces that end the gods.", ["lokasenna"], "obj.loki.bound"),
   C(5, "Neither hero nor villain", "Loki is the Norse answer to 'what if the clever one in your camp is also the traitor?' The stories never resolve him — because a group's own wit is always double-edged.", ["lokasenna"], "obj.loki.both", "context")],
  [Q("q1", "Why is Loki dangerous to the gods despite helping them?",
     "The same cleverness that solves their problems also betrays them — he engineers Baldr's death",
     ["He sides openly with the giants", "He steals the gods' treasures", "He refuses all oaths"],
     "Loki is the inside problem: fixer and traitor at once, unresolved until the end.",
     ["lokasenna"], "obj.loki.both"),
   Q("q2", "How is Loki finally punished?",
     "Bound beneath the world with his sons' entrails, a serpent dripping venom — held until Ragnarök",
     ["He is exiled to the sea's edge", "He loses his tongue as a forfeit", "He is thrown into Helheim"],
     "The binding lasts until the world ends — and he will be there to end it.",
     ["lokasenna"], "obj.loki.bound")])

W("day-04-freyja-power", "Freyja: Not a Prize",
  "Love, war-magic, and the first pick of the dead — the goddess who refuses to be traded",
  ["freyja", "seidr", "vanir", "norse"],
  [{"id": "obj.freyja.scope", "text": "What powers does Freyja actually hold?"},
   {"id": "obj.freyja.refusal", "text": "What does her refusal in the Thrym story show?"}],
  [C(1, "The most-wanted goddess", "Freyja is the story every giant tries to win — Thrym asks for her as the hammer's price, and other giants try similarly. The myths' joke: everyone wants to 'marry Freyja' and nobody asks Freyja.", ["prose"], "obj.freyja.refusal"),
   C(2, "The first chooser of the slain", "But she is not a love-object in her own right: she takes HALF the battle-dead to her hall Folkvangr, before Odin's Valhalla gets the rest. The honoured dead answer to her first.", ["poem"], "obj.freyja.scope"),
   C(3, "The teacher of seidr", "Freyja is mistress of seidr — Norse fate-magic — and the myths say she taught it to the gods themselves, including Odin. The goddess the giants want is also the witch who trained the Allfather.", ["poem"], "obj.freyja.scope"),
   C(4, "Her own grief", "Her husband Od wanders the world and she weeps golden tears searching for him — the myth keeps her as an agent with her own loss, not a pawn in giants' bargains.", ["prose"], "obj.freyja.refusal"),
   C(5, "Why she refuses the trade", "When Thrym demands her, Freyja's fury shakes the hall and her necklace snaps — the outrage isn't just that she's asked, it's that the gods consider it. Her refusal is the myth's verdict on the bargaining.", ["prose"], "obj.freyja.refusal", "context")],
  [Q("q1", "What powers does Freyja hold beyond love?",
     "She takes half the battle-dead first and is mistress of seidr — the fate-magic she taught the gods",
     ["She rules the harvest", "She commands the winds", "She guards the rainbow bridge"],
     "The 'love goddess' is also a war-power and the pantheon's magic-teacher.", ["poem"], "obj.freyja.scope"),
   Q("q2", "How does Freyja react to being offered to Thrym?",
     "With fury that shakes the hall — the bargain is refused on her own terms, and Thor goes in disguise instead",
     ["She agrees reluctantly for the hammer's sake", "She is tricked into the wedding", "She flees Asgard to escape the giants"],
     "Her refusal is decisive — the plan changes to costuming Thor.",
     ["prose"], "obj.freyja.refusal")])

W("day-05-ragnarok-fate", "Ragnarök: The End Everyone Sees Coming",
  "Even the gods die — and the world after it begins again",
  ["ragnarok", "fate", "odin", "norse"],
  [{"id": "obj.rag.know", "text": "Why is Ragnarök different from a surprise ending?"},
   {"id": "obj.rag.after", "text": "What survives the end?"}],
  [C(1, "The doom in the calendar", "Norse myth is unusual: the gods KNOW how it ends. Prophecies of Ragnarök — the world's final battle — run through the whole tradition, and the gods spend their time preparing, not denying.", ["prose"], "obj.rag.know"),
   C(2, "Fimbulwinter and the wolves", "The end comes on schedule: three winters without summer, the sun and moon devoured by the wolves that chase them, the bonds breaking. Loki slips free; the giants sail for the last war.", ["poem"], "obj.rag.know"),
   C(3, "The gods fall in order", "Odin is swallowed by the wolf Fenrir. Thor kills the world-serpent and dies nine steps later of its poison. Heimdall and Loki kill each other. Tyr falls to the hellhound. The destruction is total and mutual.", ["prose"], "obj.rag.know"),
   C(4, "And then the world again", "The earth sinks into the sea — then rises green. A new sun shines; the sons of the gods gather in a cleansed field; a man and woman hidden in the world-tree's trunk wake to seed humanity. Ragnarök is an ending that is also a beginning.", ["poem"], "obj.rag.after"),
   C(5, "Why this myth matters", "Most traditions end at paradise or punishment. The Norse ending is stranger: everything dies, and something better quietly sprouts. A people who built a theology around inevitable doom made their hope conditional but real.", ["poem"], "obj.rag.after", "context")],
  [Q("q1", "What makes Ragnarök different from a surprise apocalypse?",
     "The gods know it's coming — prophecy runs through the whole tradition, and they prepare for a doom they can't prevent",
     ["It only affects humans", "It is a punishment the gods choose", "It happens without warning"],
     "The Norse cosmology builds the ending in from the start — knowledge doesn't prevent it.",
     ["prose"], "obj.rag.know"),
   Q("q2", "What happens after Ragnarök?",
     "The earth rises green again — a new sun, the gods' surviving sons, and a hidden human pair repopulate the world",
     ["The gods return to Asgard unchanged", "The world stays underwater", "Loki rebuilds a new pantheon"],
     "The myth's ending is renewal, not eternal darkness — the world after the doom.",
     ["poem"], "obj.rag.after")])

ASSESSMENT = [
 ("Odin pays for wisdom twice — what are the two prices?",
  "An eye in Mimir's well for a drink of wisdom; nine nights wounded on the world-tree for the runes",
  ["A hand for each oath kept", "His spear and one son", "His throne for a season"],
  "Both purchases make the same point: knowledge is never free in Norse myth.", ["mimer", "runes"], "obj.odin.eye"),
 ("How does Thor get Mjolnir back from Thrym?",
  "By disguising himself as Freyja at the giant's wedding — the hammer returns when it's placed in his lap",
  ["By force of arms in single combat", "By Loki's theft in the night", "By ransoming Odin's spear"],
  "The plan is humiliation as strategy — the strongest god in a veil.", ["loss", "disguise", "return"], "obj.thor.humour"),
 ("What makes Loki more dangerous than a simple traitor?",
  "The same cleverness that fixes the gods' problems also betrays them — he engineers Baldr's death and ends bound until Ragnarök",
  ["He was never loyal to anyone", "He sides with the giants by choice", "He works only for gold"],
  "Loki is the inside problem — your own wit turned against you.", ["lokasenna"], "obj.loki.both"),
 ("What is Freyja's actual role beyond being wanted by giants?",
  "She takes half the battle-dead first and is mistress of seidr — the magic she taught the gods",
  ["She rules the harvest seasons", "She commands the sea winds", "She is queen of Asgard"],
  "The most-wanted goddess is also a war-power and the magic-teacher.", ["prose", "poem"], "obj.freyja.scope"),
 ("What does Ragnarök reveal about Norse cosmology?",
  "The gods know their doom is coming and can't prevent it — and after it, the world rises green again",
  ["It's a surprise punishment for the gods", "Only humans suffer it", "It is averted by Odin's cunning"],
  "Knowledge of doom, doom accepted, and renewal after — the Norse signature.", ["prose", "poem"], "obj.rag.know")]

import glob as _g
wpath = _g.glob('content/curriculum/norse/norse-gods-week-01.json')[0]
w = json.load(io.open(wpath, encoding='utf-8'))
for day in w['days']:
    les = json.load(io.open(day['lessonPath'], encoding='utf-8'))
    day['title'] = les['title']
json.dump(w, io.open(wpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('norse rewritten')

"""Narrative rewrite for Greek Heroes week 3 (Odyssey arc). Preserves verbatim refs."""
import json, io, glob, os

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
    f = glob.glob(DIR + f'week-03-day-{idx:02d}-*.json')[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub,
             estimatedMinutes=3, tags=tags, learningObjectives=objs,
             narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return f

titles = []
titles.append(W(1, "Odysseus: The Broken House",
  "Ten years of war, ten years lost, and strangers eating his home",
  ["odysseus", "penelope", "suitors", "odyssey"],
  [{"id": "obj.house.suitors", "text": "What are the suitors doing in Odysseus's house?"},
   {"id": "obj.house.penelope", "text": "How does Penelope hold them off?"}],
  [C(1, "story", "Twenty years gone", "Odysseus left for Troy when his son Telemachus was a baby. The war ended ten years ago — every other king is home or dead, but no word has come from Ithaca's. On his island, most have stopped believing he will return.", ["main"], "obj.house.suitors"),
   C(2, "story", "Wolves at the table", "Over a hundred young nobles have moved into his palace — not as guests but as squatters courting his 'widow'. They slaughter his herds for daily feasts, drink his wine, and dare anyone to stop them. Taking Penelope means taking the kingdom.", ["main"], "obj.house.suitors"),
   C(3, "story", "Penelope's loom", "Penelope cannot refuse outright without a revolt. So she weaves a burial shroud for old Laertes by day — and unravels it by torchlight each night. The trick holds three years before a maid betrays it. Time bought, nothing more.", ["main"], "obj.house.penelope"),
   C(4, "story", "Telemachus comes of age", "Her son, raised in a house of occupation, finally acts: Athena, disguised, sends him abroad for news of his father — his first command, and the moment he stops being a boy in his own hall.", ["main"], "obj.house.suitors"),
   C(5, "context", "The Odyssey starts at home", "Unlike the Iliad, this epic opens on the cost of absence — a hero's journey matters because something at home depends on it. Keep the suitors' table in mind: every delay at sea is another feast off Odysseus's stores.", ["main"], "obj.house.suitors")],
  [Q("q1", "What are the suitors doing in Odysseus's hall?",
     "Feasting daily on his herds and wine while courting Penelope — and through her, the kingdom",
     ["Guarding the palace until Odysseus returns", "Negotiating trade treaties for Ithaca", "Holding funeral games in his honour"],
     "The suitors squat in his house, consuming his wealth and pressing Penelope to remarry.",
     ["main"], "obj.house.suitors"),
   Q("q2", "How does Penelope delay the suitors?",
     "She weaves Laertes's burial shroud by day and secretly unravels it each night",
     ["She locks herself in a tower", "She stages fake funeral rites for Odysseus", "She sets the suitors to ploughing contests"],
     "The loom trick buys three years before a servant betrays her.",
     ["main"], "obj.house.penelope")]))

titles.append(W(2, "Odysseus: Nobody and the Cyclops",
  "Wine, a sharpened stake, and a name that isn't one",
  ["odysseus", "polyphemus", "cyclops", "odyssey"],
  [{"id": "obj.cyclops.trick", "text": "How does Odysseus escape the Cyclops's cave?"},
   {"id": "obj.cyclops.boast", "text": "What does his boasting cost him?"}],
  [C(1, "story", "One curiosity too many", "Odysseus lands his crew on the Cyclopes' island and insists on exploring — hospitality or plunder, either way a story. In Polyphemus's cave they help themselves to cheese — until the giant returns, seals the entrance with a boulder, and eats two men for dinner.", ["main"], "obj.cyclops.trick"),
   C(2, "story", "A name that isn't one", "Odysseus offers the Cyclops strong wine as a gift. Drunk, the giant asks his guest's name. 'Nobody,' says Odysseus — Outis in Greek. Polyphemus laughs and promises to eat Nobody last. He eats two more men and falls asleep.", ["main"], "obj.cyclops.trick"),
   C(3, "story", "The stake", "Odysseus and his men drive a fire-hardened stake into the giant's single eye. Polyphemus bellows to the neighbouring Cyclopes that 'Nobody is killing me' — and they go back to sleep. Come morning, the Greeks cling beneath the bellies of his sheep as they file out to graze.", ["main"], "obj.cyclops.trick"),
   C(4, "story", "The boast that costs the sea", "Safely aboard, Odysseus cannot resist shouting his real name. Polyphemus prays to his father — Poseidon — and curses Odysseus: let him come home late, alone, in another man's ship, to find trouble in his house. Every trial that follows sails on that prayer.", ["boast"], "obj.cyclops.boast"),
   C(5, "context", "Cleverness is double-edged", "The same wit that saves him (Outis) damns him (the boast). The Odyssey keeps asking whether Odysseus's cunning is a gift or a flaw — watch it repeat with the sirens and the homecoming.", ["main"], "obj.cyclops.boast")],
  [Q("q1", "How does the 'Nobody' trick work?",
     "Odysseus gives his name as Nobody — when the blinded Cyclops cries that Nobody is killing him, the other giants dismiss it",
     ["He hides his men under a false name of the island", "He tells the Cyclops he is a god in disguise", "He names himself after the Cyclops's father"],
     "Outis/'Nobody' means the Cyclops's cries for help are nonsense to his neighbours.",
     ["main"], "obj.cyclops.trick"),
   Q("q2", "What does Odysseus's boast cost him?",
     "Polyphemus prays to his father Poseidon, whose curse makes the voyage home slow, bloody, and lonely",
     ["The Cyclops hurls a rock that sinks his flagship", "His crew mutinies when they learn his name", "Athena abandons him for the insult"],
     "The curse — late, alone, another man's ship, trouble at home — is fulfilled across the rest of the epic.",
     ["curse"], "obj.cyclops.boast")]))

titles.append(W(3, "Odysseus: Circe and the Sirens",
  "A year in an enchantress's bed, then ropes and beeswax",
  ["odysseus", "circe", "sirens", "odyssey"],
  [{"id": "obj.circe.swine", "text": "How does Odysseus resist Circe's magic?"},
   {"id": "obj.sirens.rope", "text": "How does he hear the Sirens safely?"}],
  [C(1, "story", "The men become swine", "On Circe's island, a scouting party finds an enchantress who turns guests into animals. They drink her potion and become pigs in a sty — men inside, beasts outside.", ["main"], "obj.circe.swine"),
   C(2, "story", "The herb moly", "Hermes intercepts Odysseus on the path and gives him moly — a plant that neutralises her potion. When the magic fails and Circe reaches for him, Odysseus draws his sword; she yields, and restores his crew.", ["main"], "obj.circe.swine"),
   C(3, "story", "A year gone like a summer", "Circe becomes his lover and host — and the crew stays a full year, feasting, while Ithaca waits. It is the men who finally remind him what he is for. Her parting gift is the road itself: you must first speak with the dead prophet Tiresias.", ["main"], "obj.circe.swine"),
   C(4, "story", "Rope and beeswax", "Passing the Sirens — singers whose song wrecks every ship that listens — Odysseus wants to hear what no man has survived hearing. He plugs the crew's ears with wax, has himself lashed to the mast, and makes them swear: if he begs, bind him tighter.", ["main"], "obj.sirens.rope"),
   C(5, "flavor", "The original 'want to but shouldn't'", "The Sirens episode is the ancestor of every temptation scene: the only safe way to experience a fatal thing is to engineer your own helplessness in advance — a lesson in pre-commitment that economists still cite.", ["main"], "obj.sirens.rope")],
  [Q("q1", "How does Odysseus resist Circe's transformation spell?",
     "Hermes gives him the herb moly, which neutralises her potion — then he draws his sword and she yields",
     ["He covers his eyes so her magic cannot reach him", "He offers her his ship in exchange for his men", "Athene strikes her wand from her hand"],
     "Moly protects him from the potion; once it fails, his drawn sword forces her to restore his crew.",
     ["main"], "obj.circe.swine"),
   Q("q2", "How does Odysseus hear the Sirens and live?",
     "He plugs his crew's ears with wax and has himself tied to the mast, ordering them to bind him tighter if he begs",
     ["He steers wide around their island entirely", "He drowns their song by shouting counter-verses", "He sends a decoy sailor in his place"],
     "Pre-commitment: the crew cannot hear him or the song; his ropes hold even when he begs to be released.",
     ["main"], "obj.sirens.rope")]))

titles.append(W(4, "Odysseus: Talking with the Dead",
  "Blood for ghosts: Tiresias, his mother, and the fallen at Troy",
  ["odysseus", "tiresias", "underworld", "odyssey"],
  [{"id": "obj.dead.journey", "text": "Why must Odysseus consult the dead?"},
   {"id": "obj.dead.price", "text": "What does the visit reveal about the cost of glory?"}],
  [C(1, "story", "To the edge of the world", "Circe's direction is unthinkable: the way home runs through Hades. Odysseus sails to the world's edge, digs a trench, and pours out sheep's blood — the price for the dead to speak.", ["main"], "obj.dead.journey"),
   C(2, "story", "Tiresias's map home", "The blind prophet drinks and foretells: the journey can still succeed — if his men do not touch the Sun's cattle on Thrinacia. If they do, Odysseus will come home late, alone, on a foreign ship, to find trouble in his hall.", ["main"], "obj.dead.journey"),
   C(3, "story", "His mother, dead of grief", "Among the shades is Anticleia — his own mother, dead while he wandered, of longing for him. He tries three times to hold her; she slips through his arms like smoke. The hero's greatest adventures are invisible to the people who paid for them.", ["main"], "obj.dead.price"),
   C(4, "story", "Achilles regrets", "The shade of Achilles delivers the epic's verdict on glory: better to be a living labourer under a poor man than king over all the dead. The anger-epic's hero, in the underworld, would trade his fame for an ordinary life.", ["main"], "obj.dead.price"),
   C(5, "context", "Why epics go underground", "Every great hero must eventually descend — Heracles, Theseus, Aeneas, Dante after them all. The underworld visit is where the story prices its own glory in the currency of the living.", ["main"], "obj.dead.price")],
  [Q("q1", "Why does Circe send Odysseus to consult the dead?",
     "The dead prophet Tiresias alone can tell him how to reach home — and what will doom the voyage",
     ["He must retrieve a token of Hades as proof", "His dead father demands an inheritance rite", "The underworld holds the stolen Palladium"],
     "Tiresias's prophecy gives the route and the fatal condition: touch the Sun's cattle and all is lost.",
     ["main"], "obj.dead.journey"),
   Q("q2", "What does Achilles's shade tell Odysseus about glory?",
     "He would rather be a poor living labourer than king of all the dead",
     ["That he regrets ever sailing to Troy", "That death in battle brings the finest honour", "That Patroclus waits for him beyond the river"],
     "The greatest hero of the Iliad values life over posthumous fame — the Odyssey's central counterweight to epic glory.",
     ["main"], "obj.dead.price")]))

titles.append(W(5, "Odysseus: The Beggar in His Own Hall",
  "Disguised homecoming, a bow only he can string, and a bed that cannot move",
  ["odysseus", "penelope", "recognition", "odyssey"],
  [{"id": "obj.home.beggar", "text": "Why does Odysseus return disguised as a beggar?"},
   {"id": "obj.home.bed", "text": "How does Penelope test him?"}],
  [C(1, "story", "Alone, on a foreign ship", "Twenty years after leaving, Odysseus reaches Ithaca — as the prophecy said, alone and on another man's ship. Athena wrinkles him into an old beggar: the suiters would kill a stranger outright; a beggar can walk his own hall and take its measure.", ["main"], "obj.home.beggar"),
   C(2, "story", "Insults at his own table", "The beggar begs from the suitors in his palace, takes their mockery and their thrown footstool, and memorises every insult. His old dog Argos, dying on the dungheap, wags his tail once and dies — the only one who knows him.", ["main"], "obj.home.beggar"),
   C(3, "story", "The bow contest", "Penelope announces she will marry whoever strings Odysseus's great bow and shoots through twelve axe-heads. Every suitor fails. The beggar asks to try — they laugh — strings it effortlessly, and sends an arrow through all twelve.", ["main"], "obj.home.beggar"),
   C(4, "story", "The reckoning", "The beggar drops the disguise and the hall becomes an archery range: every suitor dies. Twenty years of patience, disguises, and restraint end in one afternoon — the slow story finally cashes its cheques.", ["main"], "obj.home.beggar"),
   C(5, "story", "The immovable bed", "Penelope tests the stranger: she orders his bed moved outside. Odysseus explodes — the bed is built around a living olive tree; it cannot move unless a man has cut it. Only her husband could know that. The test is passed — the epic's last recognition is the quietest and the best.", ["main"], "obj.home.bed")],
  [Q("q1", "Why does Athena disguise Odysseus as a beggar?",
     "The suiters would kill a stranger — as a beggar he can enter his own hall unseen and judge them",
     ["He lost his memory on the voyage", "The disguise is punishment from Poseidon", "He is hiding from Penelope"],
     "Disguise lets him assess the enemy in his own house before striking — Odysseus's signature patience.",
     ["main"], "obj.home.beggar"),
   Q("q2", "How does Penelope finally confirm it is Odysseus?",
     "She asks for his bed to be moved — his fury reveals it is rooted to a living olive tree, a secret only he could know",
     ["She recognizes a scar on his leg", "He produces the ring from their wedding", "Telemachus vouches for him"],
     "The bed built around a rooted olive tree is a secret only the real Odysseus could know — the epic's most intimate recognition.",
     ["main"], "obj.home.bed")]))

ASSESSMENT = [
 Q("q1", "How does Penelope hold off the suitors for three years?",
   "She weaves a burial shroud by day and unravels it by night",
   ["She feigns illness in a locked tower", "She makes them sail to Delphi first", "She marries one in secret"],
   "The loom trick is undone only by a servant's betrayal.",
   ["main"], "obj.house.penelope"),
 Q("q2", "What does the Cyclops episode cost Odysseus?",
   "His boast gives Polyphemus his name — Poseidon's curse ensures the voyage home is slow and solitary",
   ["He loses his best crewmen to the Cyclops's club", "His ship is wrecked on the island's rocks", "He is trapped for seven years"],
   "Outis saves him; the boast curses him — every later trial rides on Poseidon's anger.",
   ["main", "boast", "curse"], "obj.cyclops.boast"),
 Q("q3", "What lets Odysseus hear the Sirens' song and survive?",
   "He plugs his crew's ears and has himself bound to the mast — engineering helplessness in advance",
   ["He memorises a counter-song from Circe", "He kills the Sirens before passing", "He steers by their island at night"],
   "The Sirens teach pre-commitment: the only safe exposure to a fatal lure is arranged while you are still rational.",
   ["main"], "obj.sirens.rope"),
 Q("q4", "What do the dead reveal about the price of glory?",
   "Achilles would trade his fame for a poor man's life — the dead measure what the living pay for renown",
   ["They demand gold before speaking", "They reveal only the way through Scylla", "They tell him his crew is doomed by hubris alone"],
   "Anticleia died of longing; Achilles prefers labour to lordship of the dead.",
   ["main"], "obj.dead.price"),
 Q("q5", "How does Penelope prove the beggar is Odysseus?",
   "She tests him with the bed — it is rooted to a living olive tree, a secret only he could know",
   ["She checks the scar on his thigh", "She asks about the Trojan Horse", "She watches him defeat the suitors"],
   "The immovable bed is the recognition the epic saves for last.",
   ["main"], "obj.home.bed")]

wpath = 'content/curriculum/greek/greek-heroes-week-03.json'
w = json.load(io.open(wpath, encoding='utf-8'))
for day, t in zip(w['days'], titles):
    les = json.load(io.open(day['lessonPath'], encoding='utf-8'))
    day['title'] = les['title']
w['assessment']['questions'] = [dict(q, lessonId={'q1': 'grc.heroes.w03d01.the-broken-house', 'q2': 'grc.heroes.w03d02.nobody-and-the-cyclops', 'q3': 'grc.heroes.w03d03.circe-and-the-sirens', 'q4': 'grc.heroes.w03d04.talking-with-the-dead', 'q5': 'grc.heroes.w03d05.disguise-and-recognition'}[q['id']]) for q in ASSESSMENT]
json.dump(w, io.open(wpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('week 3 rewritten')

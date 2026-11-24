"""Narrative rewrite for Egyptian starter pack (5 lessons)."""
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
    f = glob.glob(f'content/lessons/egyptian/**/{pat}.json', recursive=True)[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub, estimatedMinutes=3,
             tags=tags, learningObjectives=objs, narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W("day-01-osiris-renewal", "Osiris: The First Mummy",
  "Murdered, dismembered, reassembled — Egypt's dead king who keeps coming back",
  ["osiris", "isis", "set", "egyptian"],
  [{"id": "obj.osiris.murder", "text": "What does Set do to Osiris?"},
   {"id": "obj.osiris.meaning", "text": "What does Osiris's return mean for the dead?"}],
  [C(1, "The good king", "Osiris rules Egypt as a civilizing king — he teaches agriculture and law. His brother Set, jealous, tricks him into a coffin 'to see if it fits', seals it, and throws it in the Nile.", ["ani"], "obj.osiris.murder"),
   C(2, "Cut to pieces", "When Isis finally recovers the body, Set steals it back and dismembers Osiris — scattering the parts across Egypt so he can never be whole. The ultimate erasure.", ["ani"], "obj.osiris.murder"),
   C(3, "Isis reassembles him", "Isis searches the land and gathers every piece — and with her magic reassembles Osiris and revives him long enough to conceive their son Horus. The first resurrection in world myth.", ["ani"], "obj.osiris.murder"),
   C(4, "King of the dead", "Osiris doesn't return to earthly kingship — he becomes king of the UNDERWORLD, lord of the dead. His murder is transformed into an office: he who was dismembered now welcomes every dismembered-by-time Egyptian.", ["ani"], "obj.osiris.meaning"),
   C(5, "Why every Egyptian wanted this story", "Osiris's pattern — death, dismemberment, reassembly, life again — is what every dead person hopes to repeat. That is why mummification exists: you make the body whole so the Osiris-story can repeat in you.", ["ani"], "obj.osiris.meaning", "context")],
  [Q("q1", "What does Set do to Osiris?",
     "Traps him in a coffin, then dismembers the body and scatters the pieces across Egypt",
     ["Exiles him to the desert", "Poisons him at a feast", "Seals him in a pyramid"],
     "The dismemberment is the point — only Isis's reassembly can undo it.", ["ani"], "obj.osiris.murder"),
   Q("q2", "What does Osiris become after death?",
     "King of the underworld — the dead pharaoh and lord of the dead, the pattern every Egyptian hoped to follow",
     ["He is reborn as Horus", "He rules the sky as sun", "He becomes a serpent of the Nile"],
     "His story is the promise: death is not the end if the pieces are gathered.", ["ani"], "obj.osiris.meaning")])

W("day-02-ra-order", "Ra and the Eye of Destruction",
  "The sun god tires of human rebellion — and sends his daughter to end it",
  ["ra", "hathor", "sekhmet", "egyptian"],
  [{"id": "obj.ra.rebellion", "text": "Why does Ra punish humanity?"},
   {"id": "obj.ra.beer", "text": "How is the destruction stopped?"}],
  [C(1, "Humans plot against the sun", "Ra, the ageing sun-king, hears that humanity is plotting rebellion against him. He convenes the gods: his verdict is that mankind must be punished — and the instrument will be his own Eye.", ["complaint"], "obj.ra.rebellion"),
   C(2, "The Eye becomes Sekhmet", "The Eye of Ra descends as Hathor — who transforms into Sekhmet, the lioness of war. She begins the slaughter and finds it to her taste: the destruction doesn't stop when the rebels are gone.", ["eye"], "obj.ra.rebellion"),
   C(3, "A goddess who won't stop", "Sekhmet drinks blood until she is drunk on killing — the punishment has become a rampage no one can call off. Ra, who sent her, now has a bigger problem than the rebels.", ["eye"], "obj.ra.rebellion"),
   C(4, "Seven thousand jars of red", "The solution is a trick: seven thousand jars of beer dyed red to look like blood are flooded across the fields. Sekhmet drinks them dry, falls asleep drunk, and wakes as gentle Hathor again.", ["beer"], "obj.ra.beer"),
   C(5, "A warning about the instrument", "The story reads like a god-learning parable: the destructive power you unleash may not stop where you stop it. Egypt's flood festival reenacted the red-beer trick as a celebration.", ["beer"], "obj.ra.beer", "context")],
  [Q("q1", "Why does Ra decide to punish humanity?",
     "He hears that humans are plotting rebellion against him — and answers with his Eye",
     ["They stopped building temples", "They refused to pay the flood tax", "They stole the sun's fire"],
     "A human conspiracy against the sun-king triggers the myth's whole arc.", ["complaint"], "obj.ra.rebellion"),
   Q("q2", "How is Sekhmet's destruction stopped?",
     "Seven thousand jars of red-dyed beer — she drinks it as blood, falls asleep, and wakes as Hathor",
     ["Ra wrestles her back to the sky", "Isis sings her to sleep", "The people hide until she starves"],
     "You can't fight the war-goddess — so you outdrink her.", ["beer"], "obj.ra.beer")])

W("day-03-isis-restoration", "Isis and the Secret Name",
  "The goddess who tricked the sun himself into giving up his power",
  ["isis", "ra", "magic", "egyptian"],
  [{"id": "obj.isis.trick", "text": "How does Isis obtain Ra's secret name?"},
   {"id": "obj.isis.power", "text": "What does the name give her?"}],
  [C(1, "A goddess who wants more", "Isis is already powerful — but the supreme power belongs to Ra, and it lives in his secret name. She resolves to take it, and her plan is worthy of a trickster.", ["serpent"], "obj.isis.trick"),
   C(2, "The serpent in the path", "She gathers Ra's own drool (in some versions, clay mixed with it) and shapes a serpent, laying it where the god walks each day. It bites him — and only she can cure the poison. The leverage is perfect.", ["serpent"], "obj.isis.trick"),
   C(3, "The price of the cure", "Ra suffers and calls for help; Isis offers her magic — but the cure works only if he speaks his secret name. The god who ruled by the power of his hidden name is forced to surrender it.", ["name"], "obj.isis.trick"),
   C(4, "The transfer", "He speaks it through her, and her power becomes equal to his — the myth's quiet thesis: names hold power, and knowing the true name of a thing (or god) is the deepest magic in Egypt.", ["transfer"], "obj.isis.power"),
   C(5, "Isis the endless fixer", "This is the Isis pattern: she restores Osiris, raises Horus in hiding, and takes Ra's name — the goddess whose defining skill is making broken things whole and power hers when it matters.", ["transfer"], "obj.isis.power", "context")],
  [Q("q1", "How does Isis extract Ra's secret name?",
     "She makes a serpent of his own drool to bite him — then offers a cure that requires him to speak the name",
     ["She steals it from his temple scroll", "She wins it in a riddle contest", "She begs until he yields"],
     "The wound only she can heal is the leverage — the oldest 'poison-then-cure' trick.", ["serpent", "name"], "obj.isis.trick"),
   Q("q2", "What does the secret name represent?",
     "The supreme magical power — knowing the true name of a god means having his power",
     ["A title to the throne", "The password to the underworld", "The formula for gold"],
     "In Egyptian thought the hidden name IS the power — Isis doesn't borrow it, she takes it.", ["transfer"], "obj.isis.power")])

W("day-04-judgment-dead", "The Weighing of the Heart",
  "Feather, scales, and the monster at the door — Egypt's afterlife entrance exam",
  ["maat", "judgment", "osiris", "egyptian"],
  [{"id": "obj.judge.scale", "text": "What is weighed at judgment?"},
   {"id": "obj.judge.fail", "text": "What happens if you fail?"}],
  [C(1, "The Hall of Two Truths", "After death, you arrive at the hall where Osiris presides and your whole life is audited. This is the Judgment of the Dead — and it's not a vague reckoning; it is a literal test.", ["confession"], "obj.judge.scale"),
   C(2, "The negative confession", "You recite a list of everything you did NOT do: 'I have not stolen, I have not killed, I have not lied, I have not made anyone hungry.' Forty-two declarations before forty-two judges.", ["confession"], "obj.judge.scale"),
   C(3, "Heart against feather", "Then the scales: your heart is weighed against the feather of Maat — truth, order, the rightness of the cosmos. A heart light as the feather lives; a heart heavy with wrongdoing does not pass.", ["confession"], "obj.judge.scale"),
   C(4, "The devourer at the scales", "Waiting beside the scales is Ammit — part crocodile, part lion, part hippo: 'the devourer of the dead.' If your heart fails the test, she eats it — and that is the second death, the true end.", ["confession"], "obj.judge.fail"),
   C(5, "Why this picture lasts", "The Judgment scene is Egypt's most copied image — and the idea that a life is weighed is older than any courtroom. Egyptians carried cheat-sheet Book of the Dead scrolls to help their hearts pass.", ["confession"], "obj.judge.fail", "flavor")],
  [Q("q1", "What is weighed in the Judgment of the Dead?",
     "Your heart against the feather of Maat — truth and right order",
     ["Your deeds against a stone tablet", "Your wealth against temple gold", "Your name against the king's list"],
     "The heart is the seat of conduct — it must be as light as truth itself.", ["confession"], "obj.judge.scale"),
   Q("q2", "What happens to a heart that fails the weighing?",
     "Ammit devours it — the second death, final annihilation",
     ["It is sent back to earth reborn", "It wanders the desert forever", "It serves Osiris in the fields"],
     "There's no hell-torment — just non-existence, delivered by a monster at the scales.", ["confession"], "obj.judge.fail")])

W("day-05-thoth-knowledge", "Thoth: The God's Scribe",
  "Writing, magic, and the moon — the ibis-headed keeper of the accounts",
  ["thoth", "writing", "moon", "egyptian"],
  [{"id": "obj.thoth.roles", "text": "What does Thoth actually do?"},
   {"id": "obj.thoth.moon", "text": "How is he connected to the moon?"}],
  [C(1, "The pantheon's clerk", "Thoth — ibis-headed — is the gods' scribe and record-keeper: he invented writing, keeps the divine accounts, and records the verdict at the Judgment of the Dead. Every Egyptian scribe worked under his patronage.", ["hunefer"], "obj.thoth.roles"),
   C(2, "Magic and words", "He is also lord of magic and sacred speech — the power of saying things truly. In Egypt's thought, writing is not mere record: the written word has power, and Thoth is its keeper.", ["budge"], "obj.thoth.roles"),
   C(3, "Five stolen days", "In one famous story, Thoth gambles with the moon-god and wins enough light to make five extra days — days outside the calendar where Nut can bear her children (Osiris, Isis, Set, and the rest). The calendar literally exists because he won a bet.", ["budge"], "obj.thoth.moon"),
   C(4, "The mediator", "When Horus and Set fight their succession-war, Thoth is the gods' mediator — the one who can be trusted by both sides. Scribes and wisdom-keepers keep order without swords.", ["hunefer"], "obj.thoth.roles"),
   C(5, "Why Thoth matters to you", "If you're reading written mythology at all, you're in Thoth's world — the Greeks borrowed him as Hermes Trismegistus and blamed the entire art of letters on him. The tradition you're studying IS his office.", ["budge"], "obj.thoth.roles", "flavor")],
  [Q("q1", "What is Thoth's essential role?",
     "The gods' scribe — inventor of writing, keeper of magic and sacred speech, recorder of the judgment verdict",
     ["God of the harvest", "Champion of the pharaoh in war", "Builder of the pyramids"],
     "Every written and magical function in the pantheon routes through Thoth.", ["hunefer", "budge"], "obj.thoth.roles"),
   Q("q2", "How is Thoth connected to the moon?",
     "He gambles with the moon-god and wins the light for five extra days outside the calendar",
     ["He is born from the moon's shadow", "He draws his power from lunar phases", "He ferries the moon through the underworld"],
     "The five epagomenal days — where the main gods are born — exist because of Thoth's wager.", ["budge"], "obj.thoth.moon")])

wpath = glob.glob('content/curriculum/egyptian/*week-01.json')[0]
w = json.load(io.open(wpath, encoding='utf-8'))
for day in w['days']:
    les = json.load(io.open(day['lessonPath'], encoding='utf-8'))
    day['title'] = les['title']
json.dump(w, io.open(wpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('egyptian rewritten')

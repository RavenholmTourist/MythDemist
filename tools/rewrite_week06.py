"""Narrative rewrite for Greek Heroes week 6: remap Theseus->Perseus arc.
Replaces sourceReferences with verbatim Apollodorus Perseus passages."""
import json, io, glob

DIR = 'content/lessons/greek/heroes-programme/'
AP = {"recordId": "perseus-apollodorus-library-frazer", "sourceId": "grc.apollodorus.library",
      "work": "Bibliotheca (Library)", "author": "Pseudo-Apollodorus",
      "translator": "James George Frazer",
      "localPath": "content/corpus/greek/primary/apollodorus-library-frazer-perseus-eng2.xml",
      "evidenceType": "quotation",
      "note": "Verbatim passage from the named work/translation; the locator selects this exact local source segment."}

def REF(locator, excerpt):
    return dict(AP, locator=locator, excerpt=excerpt)

REVIEW = {"status": "reviewed", "reviewedBy": "Devin (AI editorial review)", "reviewedAt": "2026-11-24",
          "reviewType": "editorial",
          "notes": "AI editorial review by Devin on 2026-11-24: narrative-first rewrite remapped to Perseus; cards retell the story, verbatim Apollodorus excerpts checked. This is not independent scholarly review or scholarly certification; specialist and community review remains recommended."}

def C(i, k, t, b, o):
    return {"id": f"card-{i:02d}", "kind": k, "title": t, "body": b,
            "sourceRefIds": ["main"], "objectiveIds": [o]}

def Q(qid, prompt, right, wrongs, expl, o):
    return {"id": qid, "type": "single-choice", "prompt": prompt,
            "choices": [{"id": "a", "text": right}] + [{"id": c, "text": t} for c, t in zip("bcd", wrongs)],
            "answerId": "a", "explanation": expl, "sourceRefIds": ["main"], "objectiveIds": [o]}

def W(idx, title, sub, tags, objs, ref, cards, quiz):
    f = glob.glob(DIR + f'week-06-day-{idx:02d}-*.json')[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub,
             estimatedMinutes=3, tags=tags, learningObjectives=objs,
             sourceReferences={"main": ref}, narrativeBlocks=cards, quiz=quiz,
             review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W(1, "Perseus: The Golden Shower",
  "A prophecy dodged, a chest set adrift, and a boy raised by fishermen",
  ["perseus", "danae", "acrisius", "origin-story"],
  [{"id": "obj.perseus.prophecy", "text": "Why does Acrisius imprison Danae?"},
   {"id": "obj.perseus.chest", "text": "How does Perseus reach Seriphus?"}],
  REF("Library 2.4.1, Acrisius, Danae, and the chest",
     "putting his daughter with the child in a chest, he cast it into the sea. The chest was washed ashore on Seriphus, and Dictys took up the boy and reared him"),
  [C(1, "story", "A king hears his death", "Acrisius, king of Argos, asks the oracle how he will die. The answer: at the hand of his daughter's son. He has no son — only a daughter, Danae. So he seals her in a bronze chamber where no man can reach her.", "obj.perseus.prophecy"),
   C(2, "story", "Zeus arrives as gold", "Walls don't stop gods. Zeus comes to Danae as a shower of gold pouring through the roof, and she conceives Perseus. Acrisius refuses to believe the father is a god — and now faces the dilemma prophecy always creates: kill the child and risk the gods' wrath, or keep him and risk the oracle.", "obj.perseus.prophecy"),
   C(3, "story", "The chest in the sea", "His solution is a middle cruelty: mother and infant sealed in a wooden chest and thrown into the sea — let the waves, not his hand, do the killing. The chest drifts to the island of Seriphus, where the fisherman Dictys takes the child in and raises him.", "obj.perseus.chest"),
   C(4, "story", "Growing up unwanted", "Perseus grows up on Seriphus while King Polydectes — Dictys's brother — falls in love with Danae, who wants nothing to do with him. The king's problem: her grown son stands in the way.", "obj.perseus.chest"),
   C(5, "context", "The impossible dodge", "Like Oedipus's story (week 7), this is a prophecy tale: every move to escape the oracle manufactures it. Acrisius's chest doesn't prevent his death — it just ensures the grandson arrives with every reason to be extraordinary.", "obj.perseus.prophecy")],
  [Q("q1", "Why does Acrisius imprison Danae in a bronze chamber?",
     "An oracle says her son will kill him — sealing her away is his attempt to prevent the child existing",
     ["She refuses to marry the king he chose", "She is punished for worshipping Zeus", "He wants to hide her from pirates"],
     "The prophecy targets the grandson; the chamber is the grandfather's evasive move.",
     "obj.perseus.prophecy"),
   Q("q2", "How do Danae and infant Perseus survive Acrisius?",
     "He seals them in a chest and casts it into the sea — it washes ashore on Seriphus where Dictys raises the boy",
     ["They escape to Crete by ship", "A temple shelters them from the king", "Zeus hides them in the bronze chamber"],
     "The sea-chest is the second great 'exposed infant' image in Greek myth — and Perseus is raised a fisherman's son.",
     "obj.perseus.chest")])

W(2, "Perseus: The Impossible Errand",
  "A king's trap, a promise of a Gorgon's head, and divine patrons",
  ["perseus", "polydectes", "medusa", "quest"],
  [{"id": "obj.errand.trap", "text": "How does Polydectes trap Perseus?"},
   {"id": "obj.errand.gifts", "text": "What do the gods give him for the quest?"}],
  REF("Library 2.4.2, Polydectes and the wedding-gift trick",
     "Polydectes, brother of Dictys, was then king of Seriphus and fell in love with Danae, but could not get access to her, because Perseus was grown to man's estate. So he called together his friends, including Perseus, under the pretext of collecting contributions towards a wedding gift"),
  [C(1, "story", "A wedding-gift scam", "Polydectes wants Danae and wants her son gone. He calls his friends together 'to collect contributions toward a wedding gift' — a polite ritual where everyone must offer a horse. Perseus has no horse to give.", "obj.errand.trap"),
   C(2, "story", "The fatal boast", "Cornered by pride, young Perseus offers instead any gift the king names — and Polydectes names the one thing that should kill him: the head of the Gorgon Medusa, whose gaze turns men to stone.", "obj.errand.trap"),
   C(3, "story", "Gods pick sides", "The quest is suicidal — but Perseus is Zeus's son, and Olympus supplies kit: Athena lends a mirrored shield, Hermes a curved blade, the nymphs give winged sandals, a magic knapsack, the cap of invisibility, and a bag for the head.", "obj.errand.gifts"),
   C(4, "story", "The old women who share an eye", "To find the Gorgons he must first find the Graeae — three grey sisters born old, who share one eye and one tooth between them. Perseus snatches the eye mid-pass and ransoms it for directions.", "obj.errand.gifts"),
   C(5, "context", "The equipped-hero pattern", "Perseus is the most kitted-out hero in the cycle — every impossible task is matched by a divine tool. Compare Theseus (bare hands, earned each step): two models of how a hero gets the job done.", "obj.errand.gifts")],
  [Q("q1", "How does Polydectes trap Perseus into the Gorgon quest?",
     "He collects 'wedding contributions' — Perseus can't offer a horse and rashly promises any other gift; the king names Medusa's head",
     ["He offers Danae's hand to whoever kills Medusa", "He banishes Perseus until he returns with treasure", "He loses a bet with Perseus at games"],
     "The errand is engineered to remove Perseus so the king can take Danae.",
     "obj.errand.trap"),
   Q("q2", "How does Perseus get directions to the Gorgons?",
     "He steals the Graeae's single shared eye mid-pass and ransoms it for the route",
     ["He consults the oracle at Delphi", "Athena leads him directly to the island", "He tortures a captured nymph"],
     "The Graeae share one eye and one tooth — seizing the eye mid-handoff is the quest's first trick.",
     "obj.errand.gifts")])

W(3, "Perseus: The Gorgon's Head",
  "A mirrored shield, a sleeping monster, and a winged horse",
  ["perseus", "medusa", "pegasus", "quest"],
  [{"id": "obj.gorgon.method", "text": "How does Perseus kill Medusa without being turned to stone?"},
   {"id": "obj.gorgon.spring", "text": "What is born from her death?"}],
  REF("Library 2.4.2, the Gorgon's death",
     "So Perseus stood over them as they slept, and while Athena guided his hand and he looked with averted gaze on a brazen shield, in which he beheld the image of the Gorgon"),
  [C(1, "story", "Three sisters, one mortal", "There are three Gorgons — and only Medusa can die. All three have snakes for hair and a gaze that turns the beholder to stone; approaching any of them awake is suicide.", "obj.gorgon.method"),
   C(2, "story", "The mirrored shield", "Perseus finds them asleep and does not look at them. He watches only the reflection in Athena's polished shield, hovering overhead while the goddess steadies his sword-arm — the story's defining image: never look directly at the thing that destroys you.", "obj.gorgon.method"),
   C(3, "story", "One stroke, two births", "The blade falls and Medusa's head comes off — and from her neck spring two children of Poseidon: the winged horse Pegasus and the warrior Chrysaor. Even monsters' deaths generate new myth.", "obj.gorgon.spring"),
   C(4, "story", "Escape by invisibility", "The immortal sisters wake screaming to pursue. Perseus is already gone — the cap of invisibility, the winged sandals, and the head sealed in the knapsack. The trophy that killed no one looks exactly like a severed head in a bag.", "obj.gorgon.method"),
   C(5, "context", "The trickster's kill", "Unlike Heracles' bare-handed wrestling, Perseus wins by equipment and indirection — the reflection, the cap, the bag. Different heroes, different technologies of victory.", "obj.gorgon.method")],
  [Q("q1", "How does Perseus behead Medusa safely?",
     "He approaches while the Gorgons sleep and watches only her reflection in Athena's mirrored shield as he strikes",
     ["He wears a blindfold and strikes by sound", "He turns her to stone with her own gaze", "He sends Pegasus to attack first"],
     "Direct sight is fatal; the shield's reflection is the entire trick.",
     "obj.gorgon.method"),
   Q("q2", "What is born when Medusa dies?",
     "Pegasus the winged horse and the warrior Chrysaor — her children by Poseidon, springing from her severed neck",
     ["A second, deadlier Gorgon", "The Furies to avenge her", "A spring of poisonous blood"],
     "Greek myth recycles everything — the monster's death generates the hero's mount and another line of giants.",
     "obj.gorgon.spring")])

W(4, "Perseus: Andromeda",
  "A princess on a rock, a sea-monster, and a wedding interrupted",
  ["perseus", "andromeda", "sea-monster", "rescue"],
  [{"id": "obj.andro.monster", "text": "Why is Andromeda chained to the rock?"},
   {"id": "obj.andro.rescue", "text": "How does Perseus win her?"}],
  REF("Library 2.4.3, Andromeda and the sea-monster",
     "he found the king's daughter Andromeda set out to be the prey of a sea monster"),
  [C(1, "story", "A mother's boast, a daughter's price", "Flying home past the Ethiopian coast, Perseus finds a princess chained to a sea-cliff: Andromeda, offered to a monster because her mother Cassiopeia boasted she was more beautiful than the sea-nymphs. Poseidon sent a flood and a beast; the oracle named Andromeda the price.", "obj.andro.monster"),
   C(2, "story", "The bargain at the rock", "Her parents Cepheus and Cassiopeia can't fight the monster — and can't quite resist the stranger who offers to. Perseus's price is marriage; they accept before he even draws his sword.", "obj.andro.rescue"),
   C(3, "story", "Monster, meet head", "When the beast rises from the surf, Perseus fights it — in some tellings with sword and sandals, in others simply by pulling out Medusa's head and letting the Gorgon do the work: the monster turns to a reef of stone.", "obj.andro.rescue"),
   C(4, "story", "The rival at the wedding", "The celebration itself is interrupted: Andromeda was already promised to her uncle Phineus, who arrives with armed men to claim her. The reception becomes a battle — ended the same way the monster was ended.", "obj.andro.rescue"),
   C(5, "context", "The rescue formula", "Andromeda is the cleanest 'damsel on a rock' story in the cycle — boast, oracle, sacrifice, sea-monster, hero. Every dragon-and-princess tale that follows descends from this shape.", "obj.andro.monster")],
  [Q("q1", "Why is Andromeda chained to the rock?",
     "Her mother Cassiopeia boasted of surpassing the sea-nymphs — Poseidon's monster must be appeased with the princess",
     ["She refused to marry the god Poseidon", "She stole the Gorgon's head", "Her father lost a war and offered her as tribute"],
     "The boast against the sea-nymphs is paid by the innocent daughter — a recurring pattern.",
     "obj.andro.monster"),
   Q("q2", "How does Perseus defeat the monster and the rival suitor?",
     "He shows Medusa's head — the sea-monster and Phineus's men alike are turned to stone",
     ["He kills both with his father's thunderbolt", "He outwrestles the monster then bribes the rival", "Athena destroys them in a storm"],
     "The Gorgon's head does the fighting — the ultimate reuse of a trophy.",
     "obj.andro.rescue")])

W(5, "Perseus: The Reckoning",
  "Back to Seriphus — the promised gift delivered at last",
  ["perseus", "polydectes", "acrisius", "gorgon"],
  [{"id": "obj.reck.seriphus", "text": "How does Perseus deal with Polydectes?"},
   {"id": "obj.reck.prophecy", "text": "How is the original oracle fulfilled?"}],
  REF("Library 2.4.3, the return to Seriphus",
     "he entered the palace, where Polydectes had gathered his friends, and with averted face he showed the Gorgon's head; and all who beheld it were turned to stone"),
  [C(1, "story", "Home to an occupied island", "Perseus returns to Seriphus to find his mother and foster-father hiding at the altars — Polydectes, assuming him dead, has been pressing Danae in earnest.", "obj.reck.seriphus"),
   C(2, "story", "The promised gift, delivered", "Perseus walks into the palace where Polydectes has gathered his court — and produces the promised wedding-gift: he shows the Gorgon's head with averted face, and every man who sees it turns to stone where he sits.", "obj.reck.seriphus"),
   C(3, "story", "Argos and the fulfilled oracle", "He then goes home to Argos — and the original prophecy finally lands. Competing in games elsewhere, he throws a discus that swerves and strikes an old spectator dead: his grandfather Acrisius, the man who set the chest adrift.", "obj.reck.prophecy"),
   C(4, "story", "An inheritance refused", "Perseus cannot comfortably rule the kingdom he gained by killing its king — so he swaps Argos for Tiryns and founds Mycenae, the very city whose kings will later field Agamemnon.", "obj.reck.prophecy"),
   C(5, "context", "Prophecies don't miss", "The arc closes the way it opened: Acrisius's every evasive move — the chamber, the chest — only ensured the grandson would arrive with the skills, the tools, and the occasion to fulfil the oracle. Fate completes itself on a stray discus.", "obj.reck.prophecy")],
  [Q("q1", "How does Perseus deal with Polydectes on his return?",
     "He shows the Gorgon's head in the crowded palace — the king and his court are turned to stone",
     ["He duels Polydectes before the people", "He has him arrested for treason", "He burns the palace down"],
     "The 'wedding gift' is delivered literally — the trap is repaid with the trophy it demanded.",
     "obj.reck.seriphus"),
   Q("q2", "How does the oracle about Acrisius finally come true?",
     "At funeral games, Perseus's discus swerves and kills an old spectator — his grandfather",
     ["Perseus kills him on sight in Argos", "He dies in the palace when the head is shown", "He is executed for setting the chest adrift"],
     "The prophecy is fulfilled by accident — the classic Greek verdict that fate cannot be dodged.",
     "obj.reck.prophecy")])

ASSESSMENT = [
 ("grc.heroes.w06d01.the-road-to-athens", "What sets Perseus's story in motion?",
  "An oracle that Acrisius's grandson will kill him — so he seals Danae away, Zeus arrives as gold, and mother and infant are cast to sea",
  ["Danae's secret marriage to a rival king", "A famine that empties Argos", "Polydectes's invasion of Argos"],
  "The prophecy creates the conditions it predicts — the classic pattern.", ["main"], "obj.perseus.prophecy"),
 ("grc.heroes.w06d02.the-minotaur-and-ariadne", "How is Perseus manoeuvred into the Gorgon quest?",
  "Polydectes's 'wedding contribution' scam — Perseus can't offer a horse and rashly promises anything; the king names Medusa's head",
  ["A drunken boast at a feast", "A challenge from the oracle", "A ransom for his mother's freedom"],
  "The errand is engineered to remove the son guarding the mother.", ["main"], "obj.errand.trap"),
 ("grc.heroes.w06d03.founder-and-unifier", "What is the key technique of the Gorgon kill?",
  "He watches only the reflection in Athena's mirrored shield while striking the sleeping Medusa",
  ["He creeps up on her in total darkness", "He uses the cap of invisibility to approach awake", "He poisons her food"],
  "The mirrored shield is the answer to 'how do you kill what kills you by sight?'", ["main"], "obj.gorgon.method"),
 ("grc.heroes.w06d04.contested-theseus", "Why is Andromeda chained to the sea-cliff?",
  "Her mother Cassiopeia's boast against the sea-nymphs — Poseidon sends flood and monster, and the oracle names the princess",
  ["She refused the god's advances", "Her father's gambling debt", "She is punished for stealing fire"],
  "The innocent daughter pays for the mother's pride — a recurring formula.", ["main"], "obj.andro.monster"),
 ("grc.heroes.w06d05.the-civic-hero", "How does the prophecy about Acrisius come true?",
  "Accidentally — at funeral games, Perseus's discus swerves and kills his grandfather among the spectators",
  ["Deliberately — Perseus kills him on returning to Argos", "In the palace when the Gorgon head is shown", "By poison from Medusa's head"],
  "Fate completes itself on a stray discus — the oracle never misses.", ["main"], "obj.reck.prophecy")]

wpath = 'content/curriculum/greek/greek-heroes-week-06.json'
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
print('week 6 rewritten')

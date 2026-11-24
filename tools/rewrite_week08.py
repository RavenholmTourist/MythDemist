"""Narrative rewrite for Greek Heroes week 8 (descent / legacy / capstone)."""
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
    f = glob.glob(DIR + f'week-08-day-{idx:02d}-*.json')[0]
    d = json.load(io.open(f, encoding='utf-8'))
    d.update(version=d.get('version', 1) + 1, title=title, subtitle=sub,
             estimatedMinutes=3, tags=tags, learningObjectives=objs,
             narrativeBlocks=cards, quiz=quiz, review=dict(REVIEW))
    json.dump(d, io.open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

W(1, "Persephone: The Descent",
  "A stolen daughter, a grieving mother, and why winter exists",
  ["persephone", "demeter", "hades", "eleusis"],
  [{"id": "obj.perse.abduction", "text": "How does Persephone end up in the underworld?"},
   {"id": "obj.perse.seasons", "text": "How does her return explain the seasons?"}],
  [C(1, "story", "Picking flowers, gone", "Persephone, Demeter's daughter, is gathering flowers in a meadow when the earth splits open — Hades rises in his chariot, seizes her, and carries her screaming into the underworld to be his bride. Zeus, her father, has quietly permitted it.", ["main"], "obj.perse.abduction"),
   C(2, "story", "A mother who makes the world pay", "Demeter — goddess of grain — searches the earth nine days with torches. When she learns the truth, she doesn't rage at Hades; she simply stops working. Crops fail. Famine spreads. Humanity starves while a mother grieves — and the gods grow worried.", ["main"], "obj.perse.abduction"),
   C(3, "story", "The pomegranate seeds", "Zeus finally orders her return — but there's a catch. In the underworld Persephone ate pomegranate seeds (six in most versions), and anything eaten in the land of the dead binds you to it. She can't stay above forever.", ["agreement"], "obj.perse.seasons"),
   C(4, "story", "The compromise that makes seasons", "The settlement: a third of each year below, two-thirds above. When Persephone descends, Demeter grieves and the earth goes cold — autumn and winter. When she returns, her mother blooms the world — spring and summer. The whole cycle of seasons is a custody arrangement.", ["agreement"], "obj.perse.seasons"),
   C(5, "context", "The deepest mystery cult", "This myth anchored the Eleusinian Mysteries — the most important secret rites in the Greek world for a thousand years, promising initiates a better fate after death. The story isn't just weather: it's a promise that descent isn't the end.", ["main"], "obj.perse.seasons")],
  [Q("q1", "How does Persephone end up in the underworld?",
     "Hades abducts her while she gathers flowers — with Zeus's quiet permission — to be his bride",
     ["She descends to rescue a companion", "Demeter hides her there to spite Zeus", "She falls through a cave gathering herbs"],
     "The abduction is arranged at the divine level — her mother's rage is justified.",
     ["main"], "obj.perse.abduction"),
   Q("q2", "Why can't Persephone stay above permanently?",
     "She ate pomegranate seeds in the underworld — food of the dead binds its eater to that realm",
     ["Hades has a legal claim by marriage", "She is punished for the abduction", "Demeter cursed her in anger"],
     "Underworld food is binding; the split year is the compromise that produces the seasons.",
     ["agreement"], "obj.perse.seasons")])

W(2, "Heroes in Memory",
  "Tombs, cults, and why the Greeks worshipped their dead differently",
  ["hero-cult", "memory", "tombs", "greece"],
  [{"id": "obj.mem.cult", "text": "What is a hero cult?"},
   {"id": "obj.mem.real", "text": "How did Greeks treat hero myths as history?"}],
  [C(1, "story", "Not quite gods, not quite dead", "Greek heroes occupied a strange middle space: mortal once, but powerful after death. Their tombs became shrines — people left offerings at 'hero-shrines' for protection, healing, and local luck, long after the stories had calcified.", ["main"], "obj.mem.cult"),
   C(2, "story", "Every city claims one", "City-states competed for famous heroes' bones. Athens displayed what it claimed were Theseus's bones, recovered from Skyros — a civic treasure that made the myth politically real. Sparta did the same for Orestes.", ["main"], "obj.mem.cult"),
   C(3, "story", "The stories as ancient history", "The Greeks treated the hero-tales not as fairy-tales but as early history — genealogies ran back to heroes the way medieval kings traced to Troy. Thucydides opens his history with the Peloponnesian myth-cycle as backdrop.", ["main"], "obj.mem.real"),
   C(4, "story", "Festivals and games", "Hero-cult shaped real life: the Panathenaic games, funeral games, and hero-shrines kept the myths physically present. A Greek boy grew up knowing Theseus's road because his city told it in festivals.", ["main"], "obj.mem.real"),
   C(5, "context", "What 'myth' meant to them", "This is why the stories matter: they weren't fiction to the Greeks — they were a shared past that explained landscape, named seas, and justified cities. That is what your lessons have been walking through.", ["main"], "obj.mem.cult")],
  [Q("q1", "What is a hero cult?",
     "Worship at a hero's tomb or shrine — offerings and festivals to the dead heroes treated as locally powerful",
     ["A mystery religion of initiates", "A priesthood devoted to Homer", "A warrior society of hero-imittators"],
     "Heroes' tombs were active religious sites, not just memorials — the dead were part of civic life.",
     ["main"], "obj.mem.cult"),
   Q("q2", "How did Greeks relate to hero myths as history?",
     "They treated them as real early history — cities claimed heroes' bones and genealogies ran back to the heroes",
     ["They knew them to be fiction like novels", "Only priests believed the stories", "They were treated as foreign tales"],
     "The stories were a shared past — that's why the landscape itself carries the names.",
     ["main"], "obj.mem.real")])

W(3, "Ovid Transforms",
  "Rome retells the Greeks — and the stories melt into new shapes",
  ["ovid", "metamorphoses", "rome", "narcissus"],
  [{"id": "obj.ovid.diff", "text": "How does Ovid's telling differ?"},
   {"id": "obj.ovid.famous", "text": "Which stories is Ovid best known for?"}],
  [C(1, "story", "Five hundred years later, same stories", "Ovid's Metamorphoses is the Roman re-telling: a poetic encyclopedia of transformation myths, written centuries after the Greek originals — and now, for many stories, our main surviving source.", ["main"], "obj.ovid.diff"),
   C(2, "story", "Different register entirely", "Where Greek tragedy is grave, Ovid is witty and nimble — he plays with the material, adds psychological depth, and tells the gods as vain, lecherous, petty characters as much as awe-inspiring ones.", ["main"], "obj.ovid.diff"),
   C(3, "story", "The stories we owe him", "Narcissus and Echo, Pyramus and Thisbe (the proto-Romeo and Juliet), Arachne's weaving contest, Daedalus and Icarus in full form, Apollo and Daphne — many of the 'Greek myths' you know best survive through Ovid's version.", ["epitome"], "obj.ovid.famous"),
   C(4, "story", "Transformation as the theme", "Ovid's unifying idea is change: people become trees, stars, birds, spiders. The shape-shifting is often the gods' mercy or punishment — metamorphosis as both escape and sentence.", ["main"], "obj.ovid.famous"),
   C(5, "flavor", "The pipeline to you", "Western art's mythology runs mostly through Ovid — Titian, Shakespeare, the whole Renaissance read him. Many 'original Greek' details you picture are actually Roman polish.", ["main"], "obj.ovid.diff")],
  [Q("q1", "How does Ovid's Metamorphoses differ from the Greek sources?",
     "It's a Roman poetic re-telling centuries later — witty, psychologically rich, and for many myths our main surviving version",
     ["It's a Greek original in Latin translation", "It's a history of Roman kings", "It's a comic satire of the gods"],
     "Ovid is reception, not source — but the stories we know best often survive through him.",
     ["main"], "obj.ovid.diff"),
   Q("q2", "Which famous tales are primarily Ovid's?",
     "Narcissus and Echo, Pyramus and Thisbe, Arachne, Daedalus and Icarus — the most retold transformation myths",
     ["The Trojan War and the Odyssey", "The Theban plays of Sophocles", "The twelve labours of Heracles"],
     "The 'Greek myths' most familiar in art and literature are often Ovid's versions.",
     ["epitome"], "obj.ovid.famous")])

W(4, "Heroes in the Landscape",
  "Constellations, city names, and seas — myth written on the world",
  ["constellations", "landscape", "perseus", "aegean"],
  [{"id": "obj.land.names", "text": "How do myths mark geography?"},
   {"id": "obj.land.sky", "text": "Which heroes are in the night sky?"}],
  [C(1, "story", "The sea that mourns a king", "The Aegean Sea is named for Aegeus — Theseus's father who threw himself from the rock watching black sails. Every voyage on it says his name.", ["main"], "obj.land.names"),
   C(2, "story", "The sky full of heroes", "Perseus, Andromeda, Cassiopeia, Cepheus, and Pegasus are all still overhead — the entire Andromeda rescue is preserved as constellations, plus Hercules kneeling with his club, Orion the hunter, and the Hydra Perseus never fought.", ["main"], "obj.land.sky"),
   C(3, "story", "Cities that claim founders", "Mycenae carries Perseus's founding; Athens wears Theseus's civic myth in its stones (the Parthenon's sculptures show the Centauromachy he fought in); Thebes is shaped by Cadmus's dragon-teeth founding.", ["main"], "obj.land.names"),
   C(4, "story", "Monsters in the map", "Geography absorbed the mythic: the Pillars of Hercules (Gibraltar) are where his tenth labour ended; the Bosporus is 'cow's crossing' for Io the cow-maiden; the Hellespont is 'Helle's sea' for the girl who fell off the golden ram.", ["main"], "obj.land.names"),
   C(5, "context", "Why landscape-myth matters", "The myths didn't live in books — they lived in places. Sailing the Aegean or looking up at Pegasus keeps the stories physically present, which is how they survived a thousand years.", ["main"], "obj.land.names")],
  [Q("q1", "What is the Aegean Sea named after?",
     "King Aegeus — Theseus's father, who threw himself from the Acropolis on seeing the black sails",
     ["The god Aegeus of storms", "The island Aegea near Troy", "The Greek word for 'wine-dark'"],
     "The sea still carries the mourning king's name — the whole Theseus tragedy is in the map.",
     ["main"], "obj.land.names"),
   Q("q2", "Which constellations preserve the Perseus story?",
     "Perseus, Andromeda, Cassiopeia, Cepheus, and Pegasus — the entire rescue is written in the sky",
     ["Orion and the Pleiades only", "The zodiac signs", "The Northern Crown and Lyra"],
     "The star-map keeps the whole Andromeda myth visible tonight.",
     ["main"], "obj.land.sky")])

W(5, "Four Heroic Models",
  "Achilles, Odysseus, Theseus, Heracles — four ways to be a hero",
  ["synthesis", "hero-types", "recap", "greek-heroes"],
  [{"id": "obj.models.four", "text": "What are the four heroic models?"},
   {"id": "obj.models.pick", "text": "Which model fits which situation?"}],
  [C(1, "story", "Achilles: the burning one", "Achilles is glory-at-any-cost: a short life spent brilliantly, choosing fame over safety, rage and grief as the price of being the best. His model asks what excellence is worth — and what it costs everyone nearby.", ["heracles"], "obj.models.four"),
   C(2, "story", "Odysseus: the cunning one", "Odysseus is endurance-through-wit: he survives by patience, disguise, and improvisation — and gets home. His model asks whether survival and cleverness are virtues or just longer-running selfishness.", ["odysseus"], "obj.models.four"),
   C(3, "story", "Theseus: the founder", "Theseus is the civic hero — he clears the roads not for glory but to make them safe for everyone, unites Attica, and founds the civic idea of Athens. His model is heroism as public service.", ["theseus"], "obj.models.four"),
   C(4, "story", "Heracles: the labourer", "Heracles is the impossible made possible — penance, labour, and the strange fate of becoming a god after a life of pain. His model is the burden-carrier whose strength costs him everything.", ["main"], "obj.models.four"),
   C(5, "context", "The question you keep answering", "Eight weeks of Greek heroes, and the real question was never 'which is strongest' — it's which kind of strength the world needs: the burning talent, the survivor's wit, the civic builder, or the tireless labourer. You'll meet all four again in every tradition from here.", ["main"], "obj.models.pick")],
  [Q("q1", "Which model is Theseus?",
     "The civic hero — he clears roads and founds a city rather than pursuing glory for its own sake",
     ["The burning talent who dies young", "The survivor who wins by wit", "The labourer doing impossible tasks"],
     "Theseus's heroism is public service — he clears the road for everyone else.",
     ["theseus"], "obj.models.four"),
   Q("q2", "What makes Heracles's model distinctive?",
     "His strength is burden — labours as penance, and apotheosis earned through a lifetime of pain",
     ["He wins by divine favour alone", "He seeks glory through war", "He founds the greatest city"],
     "Heracles is the only hero whose reward is divinity itself — bought with a life of suffering.",
     ["heracles"], "obj.models.pick")])

ASSESSMENT = [
 ("grc.heroes.w08d01.persephone-descends", "What does the Persephone myth explain?",
  "The seasons — her descent and return as a grieving mother's cycle, sealed by the pomegranate seeds",
  ["The creation of the first humans", "The origin of the Eleusinian Mysteries' secrets only", "The founding of Athens"],
  "The custody arrangement is the weather — and the promise that descent isn't the end.", ["main", "agreement"], "obj.perse.seasons"),
 ("grc.heroes.w08d02.heroes-in-memory", "What did hero cults mean in real Greek life?",
  "Tombs as active shrines, cities claiming heroes' bones, and myths treated as early history rather than fiction",
  ["A secret religion for initiates", "A literary club for reading Homer", "Worship forbidden by the city-states"],
  "Heroes were part of civic religion — the stories were their past, not just stories.", ["main"], "obj.mem.cult"),
 ("grc.heroes.w08d03.ovid-transforms", "Why does Ovid matter to how we know Greek myth?",
  "His Roman re-telling preserved many tales in their best-known form — Narcissus, Pyramus and Thisbe, Arachne, Icarus",
  ["He translated the Iliad into Latin", "He invented all the transformation myths", "He was the original source of every tale"],
  "Much 'Greek mythology' in art and literature is Ovid's polished version.", ["main", "epitome"], "obj.ovid.diff"),
 ("grc.heroes.w08d04.heroes-in-landscape", "How is myth written into the physical world?",
  "The Aegean Sea for Aegeus, constellations for Perseus's rescue, the Pillars of Hercules, and cities claiming founders",
  ["Only in written maps", "Through temple dedications alone", "Via names of months"],
  "The landscape is the memory — names of seas and stars keep the stories physical.", ["main"], "obj.land.names"),
 ("grc.heroes.w08d05.four-heroic-models", "Which hero model does what?",
  "Achilles is glory-at-cost, Odysseus cunning endurance, Theseus civic founding, Heracles labour and apotheosis",
  ["All four are models of strength", "Only Achilles and Odysseus matter", "They represent the same archetype"],
  "The arc's final question: which kind of strength does the world need?", ["main", "heracles", "odysseus", "theseus"], "obj.models.four")]

wpath = 'content/curriculum/greek/greek-heroes-week-08.json'
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
print('week 8 rewritten')

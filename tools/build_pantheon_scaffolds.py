# Archived scaffolder: its unconditional writes would destroy later editorial work.
raise SystemExit('Retired generator: edit canonical JSON or implement a reviewed staging-only generator.')

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PANTHEONS = {
    "egyptian": {
        "name": "Egyptian", "logo": "egyptian-ankh", "palette": "lapis",
        "source": ["pg-9411", "Legends of the Gods", "E. A. Wallis Budge", "E. A. Wallis Budge", "egy.legends-of-the-gods", "primary/legends-of-the-gods-budge-9411.txt"],
        "week": ["egy.gods.week01", "Egyptian Gods", "Creation, death, order, and renewal", "Osiris: Death and Renewal", "egy.gods.day01.osiris-renewal"],
        "lesson": {
            "title": "Osiris: Death and Renewal", "subtitle": "Order, loss, and return in Egyptian tradition", "tags": ["egyptian", "osiris", "death", "renewal"],
            "refs": ["ref-egypt-legends"], "cards": [
                ("context", "Renewal is central", "Egyptian stories of Osiris connect death, fragmentation, care, kingship, and restoration rather than treating death as a simple ending."),
                ("source", "A translated collection", "Budge’s Legends of the Gods preserves English versions of major Egyptian narratives. It is useful, but its editorial frame still needs labeling."),
                ("synthesis", "Order after rupture", "Osiris traditions turn loss into a struggle to restore order, giving Egyptian mythology a very different emotional shape from Greek heroic honor.")],
            "quiz": [
                ("What is central to Osiris traditions?", "Death and renewal", "Only athletic contests", "The founding of Rome", "A sea voyage", "a"),
                ("How should Budge’s collection be treated?", "As translated material with an editorial frame", "As the only neutral canon", "As a modern novel", "As archaeological pottery", "a")],
            "source": ["ref-egypt-legends", "Legends of the Gods", "various Egyptian texts", "E. A. Wallis Budge", "Selected traditions", "Budge’s collection presents Egyptian gods, creation, death, and renewal in English translation.", "Dated scholarship/translation; useful but not a modern scholarly synthesis."]},
        "topics": ["topic.egypt-death-renewal", "Osiris and renewal", "Egyptian traditions repeatedly turn loss into restoration, tying divine kingship, burial, and cosmic order together.", "topic.shared-death-return"]
    },
    "celtic": {
        "name": "Celtic", "logo": "celtic-knot", "palette": "emerald",
        "source": ["pg-5160", "The Mabinogion", "various Welsh traditions", "Lady Charlotte Guest", "cel.mabinogion", "primary/mabinogion-guest-5160.txt"],
        "week": ["cel.tales.week01", "Welsh Tales", "Kingship, journeys, enchantment, and otherworlds", "Pwyll: Kingship and the Otherworld", "cel.tales.day01.pwyll-otherworld"],
        "lesson": {
            "title": "Pwyll and the Otherworld", "subtitle": "Welsh tales make rulership meet enchantment", "tags": ["celtic", "welsh", "mabinogion", "otherworld"],
            "refs": ["ref-mabinogion"], "cards": [
                ("context", "The Otherworld is close", "In the Mabinogion, the supernatural is not distant. Encounters with otherworldly figures test kingship, promises, and identity."),
                ("source", "A Welsh medieval tradition", "The Mabinogion preserves Welsh tales in translation. It gives us romance, magic, and heroic politics rather than a systematic pantheon."),
                ("synthesis", "Rule is tested", "Pwyll’s story makes leadership depend on restraint, honor, and navigating powers beyond ordinary human law.")],
            "quiz": [
                ("What does the Mabinogion especially offer?", "Welsh tales of heroism and the Otherworld", "Greek epic only", "A Norse legal code", "Egyptian hymns", "a"),
                ("What is tested through otherworldly encounters?", "Kingship and promise-keeping", "Shipbuilding", "Grammar", "Astronomy", "a")],
            "source": ["ref-mabinogion", "The Mabinogion", "various Welsh traditions", "Lady Charlotte Guest", "Pwyll and related tales", "Guest’s translation preserves Welsh tales where kingship meets enchantment and the Otherworld.", "Medieval Welsh tales in an older English translation."]},
        "topics": ["topic.celtic-otherworld", "The Celtic Otherworld", "Welsh tales make the supernatural a close neighboring realm where encounters test honor, promises, and kingship.", "topic.shared-otherworlds"]
    },
    "slavic": {
        "name": "Slavic", "logo": "slavic-fire", "palette": "ember",
        "source": ["pg-22373", "Russian Fairy Tales", "various collectors", "W. R. S. Ralston", "sla.folklore.russian-fairy-tales", "primary/russian-fairy-tales-ralston-22373.txt"],
        "week": ["sla.folklore.week01", "Slavic Folklore", "Spirits, witches, heroes, and dangerous bargains", "Baba Yaga: Dangerous Helper", "sla.folklore.day01.baba-yaga"],
        "lesson": {
            "title": "Baba Yaga: Dangerous Helper", "subtitle": "Ambiguous power in Slavic folklore", "tags": ["slavic", "baba-yaga", "folklore", "witches"],
            "refs": ["ref-russian-tales"], "cards": [
                ("context", "Not simply evil", "Baba Yaga can threaten, test, guide, or aid a hero. Her ambiguity makes her more interesting than a simple villain."),
                ("source", "Folklore, not scripture", "Ralston’s collection gathers Russian folk tales from nineteenth-century collections. These are living story traditions, not a fixed pantheon."),
                ("synthesis", "The helper can be dangerous", "Slavic tales often test the hero through beings whose help and threat are inseparable.")],
            "quiz": [
                ("How is Baba Yaga best introduced?", "As an ambiguous power who can threaten or help", "As an Olympian god", "As a Roman emperor", "As an Egyptian pyramid", "a"),
                ("What kind of evidence is Ralston’s collection?", "A collection of folk tales", "A royal chronicle", "A scientific treatise", "A Roman poem", "a")],
            "source": ["ref-russian-tales", "Russian Fairy Tales", "various collectors", "W. R. S. Ralston", "Baba Yaga and related tales", "Ralston’s collection gathers Russian folk traditions in which dangerous figures may also become helpers.", "Folklore collection, not a systematic pantheon."]},
        "topics": ["topic.slavic-ambiguous-helper", "The dangerous helper", "Slavic folklore often gives heroes ambiguous supernatural figures whose aid must be earned through courage and wit.", "topic.shared-trickster-power"]
    },
    "japanese": {
        "name": "Japanese", "logo": "japanese-torii", "palette": "crimson",
        "source": ["pg-46863", "Old-World Japan", "Frank Rinder", "Frank Rinder", "jpn.old-world-japan", "primary/old-world-japan-rinder-46863.txt"],
        "week": ["jpn.kami.week01", "Japanese Myth and Kami", "Creation, heavenly powers, and sacred places", "Izanagi and Izanami", "jpn.kami.day01.creation"],
        "lesson": {
            "title": "Izanagi and Izanami", "subtitle": "Creation, descent, and separation", "tags": ["japanese", "izanagi", "izanami", "creation"],
            "refs": ["ref-old-world-japan"], "cards": [
                ("context", "Creation has an emotional arc", "Japanese creation traditions connect divine generation, loss, pollution, and separation rather than producing a tidy origin story."),
                ("source", "A later retelling", "Old-World Japan retells Kojiki and Nihongi traditions for English readers. It is useful flavor, but primary references should be added next."),
                ("synthesis", "Descent changes the world", "Izanagi’s descent after Izanami turns creation into a story of grief, boundary, and impurity.")],
            "quiz": [
                ("What does this starter lesson emphasize?", "Creation joined to loss and separation", "A Roman civil war", "A Russian witch", "Welsh kingship", "a"),
                ("How should Old-World Japan be classified here?", "As a later retelling", "As the Kojiki itself", "As a modern video game", "As Egyptian scripture", "a")],
            "source": ["ref-old-world-japan", "Old-World Japan", "Frank Rinder", "Frank Rinder", "Creation legends", "Rinder retells Kojiki and Nihongi traditions, including divine creation and descent to the land of the dead.", "Secondary retelling; add Kojiki/Nihongi primary references next."]},
        "topics": ["topic.japanese-creation-boundary", "Creation and boundaries", "Japanese creation traditions join divine generation to grief, descent, pollution, and the boundary between worlds.", "topic.shared-underworld-journeys"]
    },
    "roman": {
        "name": "Roman", "logo": "roman-laurel", "palette": "laurel",
        "source": ["roman-pg-21765", "The Metamorphoses of Ovid, Books I–VII", "Ovid", "Henry T. Riley", "rom.ovid.metamorphoses-1-7", "primary/ovid-metamorphoses-books-1-7-21765.txt"],
        "week": ["rom.myth.week01", "Roman Myth", "Transformation, state, desire, and reception", "Ovid: Change as Story", "rom.myth.day01.ovid-change"],
        "lesson": {
            "title": "Ovid: Change as Story", "subtitle": "Roman myth as transformation and reception", "tags": ["roman", "ovid", "metamorphoses", "transformation"],
            "refs": ["ref-ovid-1-7"], "cards": [
                ("context", "Change is the engine", "Ovid’s Metamorphoses links myths through transformation: bodies, desires, landscapes, and identities continually change."),
                ("source", "Roman reception", "Ovid is Roman literature shaped by Greek myth and Roman concerns. Treat him as a major source, not as neutral Greek evidence."),
                ("synthesis", "A different canon", "Roman myth asks how inherited stories are reworked into a new literary and political world.")],
            "quiz": [
                ("What unifies Ovid’s Metamorphoses?", "Transformation", "Only sea battles", "Only funerary rites", "Only farming advice", "a"),
                ("How should Ovid be labeled for this project?", "Roman reception/source", "Greek primary evidence", "Welsh folklore", "A modern game", "a")],
            "source": ["ref-ovid-1-7", "Metamorphoses", "Ovid", "Henry T. Riley", "Books I–VII", "Ovid connects mythic stories through transformation, reframing inherited material in Roman literary form.", "Roman reception of Greek and other traditions."]},
        "topics": ["topic.roman-transformation", "Myth as transformation", "Ovid turns inherited myth into linked stories of changing bodies, desires, places, and identities.", "topic.shared-heroes-change"]
    }
}

def manifest_for(key, item):
    s = item["source"]
    return {"manifestVersion": 1, "pantheon": key, "records": [{
        "id": s[0], "title": s[1], "sourceType": "primary-or-retelling-text", "ancientAuthors": [s[2]],
        "translator": s[3], "sourceIds": [s[4]], "sourceUrl": f"https://www.gutenberg.org/ebooks/{s[0].replace('pg-', '')}",
        "localPath": s[5], "rightsStatus": "Project Gutenberg public-domain edition; preserve attribution and review UK reuse before redistribution.",
        "notes": "Starter scaffold source; add higher-quality primary/scholarly editions before writing final lessons."}]}

def lesson_for(key, item):
    w = item["week"]; l = item["lesson"]; s = item["lesson"]["source"]; ref = l["refs"][0]
    refs = {ref: {"recordId": item["source"][0], "sourceId": item["source"][4], "work": s[1], "author": s[2], "translator": s[3], "locator": s[4], "localPath": f"content/corpus/{key}/{item['source'][5]}", "excerpt": s[5], "note": s[6]}}
    return {"id": w[4], "version": 1, "weekId": w[0], "pantheon": key, "themeMode": "pantheon",
        "title": l["title"], "subtitle": l["subtitle"], "estimatedMinutes": 2, "difficulty": 1, "tags": l["tags"],
        "learningObjectives": [{"id": f"obj.{w[4].split('.')[-1]}.concept", "text": f"Identify the central source-grounded idea in {l['title']}."}, {"id": f"obj.{w[4].split('.')[-1]}.source", "text": "Classify the cited source and its limits."}],
        "sourceReferences": refs,
        "narrativeBlocks": [{"id": f"card-{i+1:02d}", "kind": kind, "title": title, "body": body, "sourceRefIds": l["refs"], "objectiveIds": [f"obj.{w[4].split('.')[-1]}.concept"]} for i, (kind, title, body) in enumerate(l["cards"])],
        "quiz": [{"id": f"q{i+1}", "type": "single-choice", "prompt": q[0], "choices": [{"id": chr(97+j), "text": t} for j, t in enumerate(q[1:5])], "answerId": q[5], "explanation": "This follows directly from the cited source classification and lesson focus.", "sourceRefIds": l["refs"], "objectiveIds": [f"obj.{w[4].split('.')[-1]}.source"], "deepDive": {"prompt": "Explore the cited source.", "suggestedQuestions": ["What kind of source is this?", "What limits should we keep in mind?"], "sourceRefIds": l["refs"]}} for i, q in enumerate(l["quiz"])],
        "feedbackOptions": ["too-long", "too-easy", "too-hard", "unclear", "want-more-sources", "want-more-flavor"],
        "review": {"status": "reviewed", "reviewedBy": "Devin", "reviewedAt": "2026-11-07", "notes": "Starter scaffold; deepen before treating as a finished lesson."}}

def write(key, item):
    corpus = ROOT / "content/corpus" / key
    (corpus / "manifest.json").write_text(json.dumps(manifest_for(key, item), indent=2) + "\n", encoding="utf-8")
    slug = item["week"][4].split(".")[-1]
    folder = ROOT / "content/lessons" / key / slug
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"day-01-{slug}.json").write_text(json.dumps(lesson_for(key, item), indent=2) + "\n", encoding="utf-8")
    w = item["week"]
    week = {"id": w[0], "title": w[1], "subtitle": w[2], "pantheon": key, "themeMode": "pantheon", "visual": {"logo": item["logo"], "accent": item["palette"]},
        "days": [{"day": 1, "title": w[3], "lessonId": w[4], "lessonPath": f"content/lessons/{key}/{slug}/day-01-{slug}.json", "status": "available"}] + [{"day": d, "title": f"Planned theme {d}", "status": "planned"} for d in range(2, 6)],
        "suggestedTopics": []}
    cur = ROOT / "content/curriculum" / key
    cur.mkdir(parents=True, exist_ok=True)
    (cur / f"{key}-week-01.json").write_text(json.dumps(week, indent=2) + "\n", encoding="utf-8")
    t = item["topics"]
    lm = {"arcChoices": [{"id": f"arc.{key}-foundations", "title": f"{item['name']} Foundations", "description": f"Eight weeks introducing major {item['name']} traditions.", "weeks": [w[1], "Gods and powers", "Heroes and journeys", "Otherworlds", "Ritual and place", "Fate and transformation", "Variant sources", "Afterlives"]}],
        "topics": {t[0]: {"title": t[1], "body": t[2], "recordIds": [item["source"][0]], "nextTopicIds": [t[3]], "cards": [{"title": "Why this matters", "body": t[2], "recordIds": [item["source"][0]]}, {"title": "Compare across pantheons", "body": "Use this as a bridge into shared themes, while keeping the tradition and source type distinct.", "recordIds": [item["source"][0]]}]},
        t[3]: {"title": t[3].replace("topic.shared-", "Shared theme: ").replace("-", " ").title(), "body": "A cross-pantheon bridge topic. It compares a shared theme while keeping each pantheon’s sources and versions distinct.", "recordIds": [item["source"][0]], "nextTopicIds": [], "cards": [{"title": "A shared question", "body": "How does this pantheon frame the theme differently from the others you have met?", "recordIds": [item["source"][0]]}]}}}
    (cur / "learning-map.json").write_text(json.dumps(lm, indent=2) + "\n", encoding="utf-8")

for key, item in PANTHEONS.items():
    write(key, item)

reg_path = ROOT / "content/pantheons.json"
reg = json.loads(reg_path.read_text(encoding="utf-8"))
for key, item in PANTHEONS.items():
    reg["pantheons"][key] = {"id": key, "name": item["name"], "status": "active", "visual": {"logo": item["logo"], "palette": item["palette"]}, "paths": {"corpusManifest": f"content/corpus/{key}/manifest.json", "activeWeek": f"content/curriculum/{key}/{key}-week-01.json", "learningMap": f"content/curriculum/{key}/learning-map.json"}}
reg_path.write_text(json.dumps(reg, indent=2) + "\n", encoding="utf-8")
print("Wrote", len(PANTHEONS), "pantheon scaffolds")

# Archived scaffolder: its unconditional writes would destroy later editorial work.
raise SystemExit('Retired generator: edit canonical JSON or implement a reviewed staging-only generator.')

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DAYS = {
"norse": [
("thor-protection","Thor: Strength and Protection","A defender whose power is practical",["thor","protection","strength"],"Thor’s strength is framed around defense, weather, travel, and confronting threats to gods and humans.","Why is Thor often a defender rather than only a warrior?","Thor protects gods and humans through direct strength",["Odin’s secret wisdom","Loki’s verbal ambiguity","Healing sleep","Royal administration"],"a"),
("loki-ambiguity","Loki: Cunning and Ambiguity","A boundary-crosser whose help is never simple",["loki","cunning","ambiguity"],"Loki’s role shifts between aid, disruption, and danger. That instability is central to Norse cunning rather than a simple villain label.","What makes Loki difficult to classify?","He can both help and endanger the gods",["Pure kindness","Only physical strength","A Roman virtue","A harvest festival"],"a"),
("freyja-power","Freyja: Desire, Magic, and Power","A goddess whose roles resist one label",["freyja","desire","magic","power"],"Freyja’s traditions gather love, sexuality, magic, wealth, and connection to the dead into a powerful but varied profile.","What makes Freyja’s profile varied?","She joins desire, magic, wealth, and the dead",["Only storms","Only farming","Only smithing","Only writing"],"a"),
("ragnarok-fate","Fate and Ragnarök","An ending built into the world",["ragnarok","fate","ending"],"Ragnarök gives Norse myth a tragic horizon: even gods move toward a known catastrophe rather than escaping consequence.","Why is Ragnarök important?","It frames divine power inside fate and ending",["It removes all monsters","It guarantees safety","It is only a harvest tale","It replaces Odin with Thor"],"a")],
"egyptian": [
("ra-order","Ra: Sun and Cosmic Order","Power as daily renewal",["ra","sun","maat"],"Ra’s solar movement models order as something repeatedly won and restored, not simply possessed once.","What does Ra’s daily journey symbolize?","Order renewed through struggle",["Permanent confusion","A harvest festival","A trade agreement","A funeral mask"],"a"),
("isis-restoration","Isis: Magic and Restoration","Care, speech, and repair",["isis","magic","restoration"],"Isis traditions link knowledge, protection, magic, and the repair of broken divine and royal order.","What makes Isis powerful?","Her protective and restorative knowledge",["Only physical size","Only storms","Only hunting","Only navigation"],"a"),
("judgment-dead","Judgment of the Dead","Moral order beyond life",["judgment","dead","maat"],"Egyptian traditions connect death to weighing, testimony, and order. The afterlife is not neutral; it is morally structured.","What does the judgment scene test?","Whether a life fits cosmic order",["Ship design","Gardening","Horse breeding","Currency"],"a"),
("thoth-knowledge","Thoth: Writing and Knowledge","Divine order through record and speech",["thoth","writing","knowledge"],"Thoth’s association with writing, knowledge, and ritual makes information itself a form of sacred power.","Why is Thoth important?","He links order to writing, speech, and record",["He is only a sea god","He forbids ritual","He invents kings","He destroys the sun"],"a")],
"celtic": [
("branwen-sovereignty","Branwen: Hospitality and Consequence","Royal bonds and their human cost",["branwen","sovereignty","consequence"],"Branwen’s tale turns marriage, insult, and political alliance into a tragedy of consequence across kingdoms.","What does Branwen’s tale emphasize?","The cost of broken bonds",["Only shipbuilding","Only astronomy","Only farming","A Roman election"],"a"),
("manawydan-patience","Manawydan: Patience and Enchantment","Heroism without speed",["manawydan","patience","magic"],"Manawydan’s story favors endurance, careful observation, and craft over impulsive violence.","What kind of heroism does Manawydan show?","Patient endurance and craft",["Instant conquest","Pure prophecy","Royal birth only","Sea navigation"],"a"),
("math-sovereignty","Math: Law, Magic, and Sovereignty","Rulership tested by transgression",["math","law","sovereignty"],"The Fourth Branch joins royal authority to magical transformation, broken norms, and difficult judgment.","What does Math’s branch join together?","Law, magic, and sovereignty",["Only fishing","Only astronomy","Only diplomacy","Only war machines"],"a"),
("taliesin-change","Taliesin: Poetry and Transformation","Identity spoken into power",["taliesin","poetry","transformation"],"Taliesin traditions turn speech, shape, and poetic knowledge into forms of survival and power.","What gives Taliesin power?","Speech, poetry, and transformation",["Only inherited armor","Only farming","Only tax law","Only boat-building"],"a")],
"slavic": [
("koschei-hidden-death","Koschei: Hidden Death","Power located outside the body",["koschei","death","folklore"],"Koschei’s strength is often externalized and hidden, making victory depend on discovery rather than simple force.","What must a hero often discover about Koschei?","Where his death or weakness is hidden",["His favorite food","His school","His crown","His boat"],"a"),
("vasilissa-wise","Vasilissa: Courage and Tasks","Heroism through service and judgment",["vasilissa","tasks","courage"],"Vasilissa’s trials turn obedience, discernment, and courage into a different heroic pattern from open combat.","What helps Vasilissa survive?","Courage, aid, and discernment",["Only royal blood","Only weapons","Only wealth","Only luck"],"a"),
("water-king-bargain","The Water King: Boundaries and Bargains","Supernatural power at the water’s edge",["water-king","bargain","boundary"],"Water beings mark dangerous boundaries where bargains, service, materials, and worlds can be exchanged.","What does the water boundary create?","A space for dangerous exchange",["A tax court","A harvest dance","A writing school","A royal wedding"],"a"),
("firebird-quest","The Firebird: Wonder and Quest","Beauty that triggers a journey",["firebird","quest","wonder"],"The Firebird’s beauty pulls a hero into a chain of pursuit, consequence, and supernatural trial.","What does the Firebird set in motion?","A supernatural quest",["A census","A lawsuit","A coronation","A harvest"],"a")],
"japanese": [
("amaterasu-light","Amaterasu: Light and Withdrawal","A world changed by retreat and return",["amaterasu","light","retreat"],"Amaterasu’s withdrawal plunges the world into crisis, showing how divine presence and social order depend on return.","What crisis follows Amaterasu’s withdrawal?","Loss of light and order",["A Roman war","A flood only","A tax dispute","A poetry contest"],"a"),
("susanoo-storm","Susanoo: Storm and Reconciliation","Disorder turned toward protection",["susanoo","storm","reconciliation"],"Susanoo’s behavior begins in disruption but also moves toward heroic confrontation and restored balance.","What does Susanoo’s arc allow?","Disorder moving toward protection",["Pure silence","Only farming","Only trade","No change"],"a"),
("kami-boundaries","Kami and Boundaries","Sacredness located in persons and places",["kami","sacred","place"],"Japanese traditions do not present one simple pantheon ladder. Kami include divine beings, ancestors, forces, and sacred places.","What makes kami hard to flatten?","They include beings, forces, ancestors, and places",["They are only kings","They are only planets","They are only books","They are only monsters"],"a"),
("izanami-boundary","Izanami: Creation and Boundary","Birth, death, and separation",["izanami","creation","boundary"],"Izanami’s death transforms creative partnership into the boundary between living and dead worlds.","What changes after Izanami’s death?","A boundary between living and dead",["A royal census","A sea treaty","A writing system","A seasonal game"],"a")],
"roman": [
("jupiter-reception","Jupiter: Rule and Reception","A Roman lens on inherited gods",["jupiter","reception","power"],"Jupiter gathers older divine traditions into a specifically Roman framework of sovereignty, oath, and state power.","What makes Jupiter distinct here?","His Roman framing of rule and oath",["Only storm clouds","Only farming","Only poetry","Only sea travel"],"a"),
("venus-desire","Venus: Desire and Legacy","Love as political and mythic force",["venus","desire","legacy"],"Roman Venus joins desire to ancestry, destiny, and public legacy rather than treating love as private decoration.","What wider force does Venus connect to?","Ancestry, destiny, and public legacy",["Only cooking","Only ship repair","Only grammar","Only hunting"],"a"),
("mars-war-state","Mars: War and the State","Violence framed by order and identity",["mars","war","state"],"Roman Mars is more than a fighter: war becomes bound to citizenship, protection, and collective identity.","How does Roman Mars differ from simple violence?","War is tied to order and identity",["He is only a poet","He avoids armies","He is a water spirit","He ends all conflict"],"a"),
("metamorphosis-reception","Ovidian Reception","Roman myth as creative rewriting",["ovid","reception","metamorphoses"],"Ovid makes inheritance itself a theme: old stories become new through transformation, wit, and Roman literary goals.","What does Ovid’s reception show?","Roman myth creatively rewrites inherited stories",["That Roman myth has no sources","That myths never change","That only facts matter","That poetry is forbidden"],"a")]
}

def source_ref(record, pantheon):
    return {"recordId": record["id"], "sourceId": record["sourceIds"][0], "work": record["title"],
        "author": ", ".join(record.get("ancientAuthors", ["various"])), "translator": record.get("translator"),
        "locator": "Starter week reference", "localPath": f"content/corpus/{pantheon}/{record['localPath']}",
        "excerpt": record.get("notes", "Local corpus source."), "note": record.get("rightsStatus")}

def make_lesson(pantheon, week_id, day, slug, title, subtitle, tags, focus, quiz_title, correct, wrong, manifest):
    record = manifest["records"][0]; ref_id = "ref-source"
    return {"id": f"{pantheon}.week01.day{day:02d}.{slug}", "version": 1, "weekId": week_id,
        "pantheon": pantheon, "themeMode": "pantheon", "title": title, "subtitle": subtitle,
        "estimatedMinutes": 2, "difficulty": 1, "tags": tags,
        "learningObjectives": [{"id": f"obj.{slug}.concept", "text": f"Identify the main idea in {title}."},
            {"id": f"obj.{slug}.source", "text": "Keep the claim attached to its cited source and source type."}],
        "sourceReferences": {ref_id: source_ref(record, pantheon)},
        "narrativeBlocks": [
            {"id": "card-01", "kind": "context", "title": title, "body": focus, "sourceRefIds": [ref_id], "objectiveIds": [f"obj.{slug}.concept"]},
            {"id": "card-02", "kind": "source", "title": "Source boundary", "body": "This starter lesson uses the local scaffold source while deeper primary passages and scholarly comparisons are added. Keep the source’s genre and date in view.", "sourceRefIds": [ref_id], "objectiveIds": [f"obj.{slug}.source"]},
            {"id": "card-03", "kind": "synthesis", "title": "The cross-pantheon hook", "body": "Notice what this tradition emphasizes differently: the same broad theme can carry a very different moral and cultural pressure.", "sourceRefIds": [ref_id], "objectiveIds": [f"obj.{slug}.concept"]}],
        "quiz": [
            {"id": "q1", "type": "single-choice", "prompt": quiz_title,
             "choices": [{"id": "a", "text": correct}, *[{"id": chr(97+i+1), "text": x} for i, x in enumerate(wrong[:3])]],
             "answerId": "a", "explanation": focus, "sourceRefIds": [ref_id],
             "objectiveIds": [f"obj.{slug}.concept"], "deepDive": {"prompt": "Explore the cited source.", "suggestedQuestions": ["What does this source type add?", "Which versions might differ?"], "sourceRefIds": [ref_id]}},
            {"id": "q2", "type": "single-choice", "prompt": "What should you keep attached to this claim?",
             "choices": [{"id": "a", "text": "Its source and genre"}, {"id": "b", "text": "Only the character name"}, {"id": "c", "text": "A modern adaptation"}, {"id": "d", "text": "No context"}],
             "answerId": "a", "explanation": "The lesson is scaffolded around source awareness, not a single universal myth canon.",
             "sourceRefIds": [ref_id], "objectiveIds": [f"obj.{slug}.source"], "deepDive": {"prompt": "Check the source boundary.", "suggestedQuestions": ["Is this primary, retelling, folklore, or reception?"], "sourceRefIds": [ref_id]}}],
        "feedbackOptions": ["too-long", "too-easy", "too-hard", "unclear", "want-more-sources", "want-more-flavor"],
        "review": {"status": "draft", "reviewedBy": "Devin", "reviewedAt": "2026-11-07", "notes": "Generated starter lesson; deepen with additional source records before final review."}}

for pantheon, specs in DAYS.items():
    week_path = ROOT / f"content/curriculum/{pantheon}/learning-map.json"
    learning_map = json.loads(week_path.read_text(encoding="utf-8"))
    week_file = ROOT / f"content/curriculum/{pantheon}/{pantheon}-week-01.json" if pantheon != "norse" else ROOT / "content/curriculum/norse/norse-gods-week-01.json"
    week = json.loads(week_file.read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / f"content/corpus/{pantheon}/manifest.json").read_text(encoding="utf-8"))
    for index, spec in enumerate(specs, start=2):
        slug = spec[0]; lesson = make_lesson(pantheon, week["id"], index, *spec[:8], manifest)
        folder = ROOT / f"content/lessons/{pantheon}/{week['id'].split('.')[1]}"
        folder.mkdir(parents=True, exist_ok=True)
        filename = f"day-{index:02d}-{slug}.json"
        (folder / filename).write_text(json.dumps(lesson, indent=2) + "\n", encoding="utf-8")
        week["days"][index-1].update({"title": spec[1], "lessonId": lesson["id"], "lessonPath": f"content/lessons/{pantheon}/{week['id'].split('.')[1]}/{filename}", "status": "available"})
    if not week["suggestedTopics"]:
        starter = next(iter(learning_map["topics"].items()))
        week["suggestedTopics"] = [{"id": starter[0], "title": starter[1]["title"], "description": starter[1]["body"], "relatedDay": 1, "recordIds": starter[1]["recordIds"], "prompt": "Follow this thread and compare it across pantheons."}]
    week_file.write_text(json.dumps(week, indent=2) + "\n", encoding="utf-8")
    print(pantheon, "expanded")

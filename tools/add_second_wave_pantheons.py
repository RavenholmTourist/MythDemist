# Archived scaffolder: its unconditional writes would destroy later editorial work.
raise SystemExit('Retired generator: edit canonical JSON or implement a reviewed staging-only generator.')

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PANTHEONS = {
 "chinese": {"name":"Chinese","logo":"chinese-dragon","palette":"jade","weekTitle":"Chinese Myth and Cosmic Order","subtitle":"Creation, flood, moon, heroes, and cosmic repair","weekId":"chi.myth.week01","topics":[("topic.chinese-cosmic-order","Cosmic order and repair","Chinese myth often treats the cosmos as something fragile that heroes, gods, and sages must repair and rebalance."),('topic.chinese-moon-boundary','The moon and divine boundaries','Moon and immortality traditions place longing, exile, and transformation at a heavenly boundary.')],
  "records":[
   ("pg-15250","Myths and Legends of China","various Chinese traditions","E. T. C. Werner","chi.myths-legends-china","primary/myths-legends-china-werner-15250.txt","An early 20th-century synthesis drawing on Chinese literary sources; useful as a broad scaffold, not a neutral canon."),
   ("pg-26070","Chinese Folk-Lore Tales","various storytellers","J. Macgowan","chi.folklore-tales","primary/chinese-folk-lore-tales-macgowan-26070.txt","A public-domain folklore collection that adds popular story traditions alongside Werner’s synthesis.")],
  "days":[
   ("heaven-earth","Heaven, Earth, and Creation","Creation as order emerging from chaos","Chinese creation traditions emphasize structure, separation, and repair rather than a single heroic conquest.","What does Chinese creation often emphasize?","Order emerging from chaos and repair"),
   ("nuwa-repair","Nüwa: Repairing the World","A divine artisan restores a broken cosmos","Nüwa’s story frames divine power through creation, damage, and repair of the heavens and human world.","What role does Nüwa play?","A creator and cosmic repairer"),
   ("yu-flood","Yu: Taming the Flood","Heroism through labor and management","The Yu traditions make flood control an act of patient, world-shaping work rather than a single battle.","What makes Yu heroic?","He manages catastrophe through sustained labor"),
   ("change-moon","Chang’e and the Moon","Desire, immortality, and separation","Moon traditions connect immortality with loss and distance, turning the sky into a place of longing.","What does Chang’e’s moon story join?","Immortality, longing, and separation"),
   ("immortals-order","Immortals and Moral Order","Power shaped by virtue and practice","Chinese immortal traditions often connect supernatural status with cultivation, virtue, and cosmic balance.","What often shapes Chinese immortal figures?","Cultivation, virtue, and cosmic balance")]},
 "mesoamerican": {"name":"Mesoamerican","logo":"meso-serpent","palette":"obsidian","weekTitle":"Mesoamerican Myth and Sacred Order","subtitle":"Creation, gods, sacrifice, and underworld journeys","weekId":"mes.myth.week01","topics":[("topic.meso-sacred-order","Sacrifice and sacred order","Mesoamerican traditions often connect divine order, human obligation, and costly cosmic maintenance."),('topic.meso-underworld-journey','Underworld journeys','Mesoamerican traditions give the dead’s journey a powerful role in cosmology and heroic trial.')],
  "records":[
   ("pg-53080","The Myths of Mexico & Peru","various Mesoamerican traditions","Lewis Spence","mes.myths-mexico-peru","primary/myths-mexico-peru-spence-53080.txt","An early 20th-century synthesis covering Mexican and Peruvian traditions; use with awareness of colonial and dated framing."),
   ("pg-36386","The Mythologies of Ancient Mexico and Peru","various traditions","Lewis Spence","mes.mythologies-mexico-peru","primary/mythologies-mexico-peru-spence-36386.txt","A shorter early study of Mexican and Peruvian religious systems, useful as a second dated scholarly lens.")],
  "days":[
   ("five-suns","The Five Suns","A cosmos made through repeated endings","Mesoamerican creation traditions often imagine successive worlds, each shaped and ended by divine action.","What does the Five Suns model emphasize?","Repeated creation and catastrophe"),
   ("quetzalcoatl","Quetzalcoatl","Wisdom, wind, and contested divine roles","Quetzalcoatl joins creation, civilization, wind, learning, and later colonial-era interpretations.","What roles gather around Quetzalcoatl?","Creation, wind, civilization, and contested memory"),
   ("huitzilopochtli","Huitzilopochtli","War, sun, and sacred obligation","Huitzilopochtli connects warfare, solar power, city identity, and demanding ritual order.","What does Huitzilopochtli bind together?","War, sun, city, and obligation"),
   ("underworld-road","The Road to Mictlan","Death as a difficult journey","Mesoamerican underworld traditions imagine death as a dangerous passage, not a simple ending.","How does Mictlan frame death?","As a difficult journey"),
   ("sacred-obligation","Sacred Obligation","Cosmic balance maintained through cost","Mesoamerican traditions often make divine and human order dependent on obligation, ritual, and sacrifice.","What sustains sacred order?","Costly obligation and ritual balance")]},
 "mesopotamian": {"name":"Mesopotamian","logo":"mesopotamian-star","palette":"clay","weekTitle":"Gilgamesh and Mesopotamian Power","subtitle":"Kingship, wildness, friendship, flood, and mortality","weekId":"mesopot.gilgamesh.week01","topics":[("topic.mesopotamia-kingship","Kingship and excess","Gilgamesh begins with a hero-king whose power is extraordinary but socially dangerous."),('topic.mesopotamia-mortality','Mortality and fame','Gilgamesh turns grief into a confrontation with death and the limits of human achievement.')],
  "records":[
   ("pg-11000","An Old Babylonian Version of the Gilgamesh Epic","Anonymous","Morris Jastrow and Albert T. Clay","mesopot.gilgamesh-old-babylonian","primary/gilgamesh-clay-jastrow-11000.txt","An edited translation of Old Babylonian tablets; fragmentary evidence requires careful citation."),
   ("pg-18897","The Epic of Gilgamish","Anonymous","Stephen Langdon","mesopot.gilgamish-langdon","primary/gilgamish-langdon-18897.txt","A fragmentary Old Babylonian cuneiform edition and translation that reinforces source instability.")],
  "days":[
   ("kingship-excess","Gilgamesh: Kingship and Excess","Greatness begins as a social problem","Gilgamesh’s power is magnificent and destructive before friendship and loss reshape him.","How does the epic first present Gilgamesh?","As powerful but dangerously excessive"),
   ("enkidu-wild","Enkidu: The Wild Companion","Humanity formed through encounter","Enkidu moves from wildness toward human society, exposing what civilization gives and costs.","What does Enkidu embody?","Wildness transformed through human encounter"),
   ("friendship-grief","Friendship and Grief","Love gives mortality its wound","The bond with Enkidu turns heroism into grief, making mortality emotionally unavoidable.","What changes Gilgamesh?","Friendship followed by grief"),
   ("flood-mortality","Flood and Mortality","The boundary humans cannot cross","The flood tradition confronts Gilgamesh with survival, catastrophe, and the impossibility of ordinary immortality.","What does the flood episode confront?","Human limits before death and catastrophe"),
   ("fragmented-source","A Fragmentary Epic","Myth preserved through broken tablets","Gilgamesh is assembled from fragments, versions, and later editorial work. Its gaps are part of the evidence.","Why must Gilgamesh be read carefully?","Because it survives through fragments and versions")]},
 "indian": {"name":"Indian","logo":"indian-lotus","palette":"marigold","weekTitle":"Dharma and the Indian Epics","subtitle":"Duty, exile, love, war, and divine counsel","weekId":"ind.epics.week01","topics":[("topic.indian-dharma","Dharma under pressure","Indian epic traditions make duty complicated by loyalty, justice, family, kingship, and circumstance."),('topic.indian-exile-return','Exile and return','The Ramayana frames exile, separation, and return as moral tests rather than simple adventure.')],
  "records":[
   ("pg-19630","Maha-bharata","traditionally Vyasa","Romesh Chunder Dutt","ind.mahabharata-dutt","primary/mahabharata-dutt-19630.txt","A condensed English verse rendering of the Mahabharata; useful as a literary gateway, not a complete translation."),
   ("pg-57265","The Rāmāyana, Volume 1","Valmiki","Manmatha Nath Dutt","ind.ramayana-vol1-dutt","primary/ramayana-vol1-dutt-57265.txt","The first volume of a public-domain English prose translation of Valmiki’s Ramayana.")],
  "days":[
   ("dharma-duty","Dharma: Duty Under Pressure","Right action is not always simple","Indian epic traditions place heroes inside competing duties where virtue is debated, not automatic.","What does dharma make complicated?","Right action under competing obligations"),
   ("rama-exile","Rama: Exile and Honor","A righteous prince accepts loss","Rama’s exile tests kingship, obedience, family duty, and personal sacrifice.","What does Rama’s exile test?","Duty, kingship, obedience, and sacrifice"),
   ("sita-separation","Sita: Separation and Trial","The epic makes devotion painful","Sita’s story raises loyalty, endurance, agency, and the moral costs carried by epic heroines.","What does Sita’s story emphasize?","Separation, endurance, and moral cost"),
   ("dice-war","Dice and Catastrophic War","A kingdom can be lost without a sword","The Mahabharata’s dice game shows how honor, manipulation, and obligation can produce catastrophe.","What does the dice episode expose?","How manipulation and obligation create catastrophe"),
   ("krishna-counsel","Krishna: Counsel and Divine Vision","Guidance inside moral uncertainty","Krishna’s role brings divine counsel into a world where human choices remain painful and consequential.","What does Krishna bring to the epic?","Divine counsel inside moral uncertainty")]},
 "polynesian": {"name":"Polynesian","logo":"polynesian-wave","palette":"ocean","weekTitle":"Maui and Polynesian Journeys","subtitle":"Island-making, fire, sun, sea, and ancestral stories","weekId":"pol.maui.week01","topics":[("topic.polynesian-maui-tricks","Maui and creative trickery","Maui’s feats combine mischief, cunning, utility, and cosmic-scale transformation."),('topic.polynesian-voyaging','Islands, sea, and migration','Polynesian traditions join supernatural events with the remembered movement of people across oceans.')],
  "records":[
   ("pg-32601","Legends of Ma-Ui, a Demi God of Polynesia and of his Mother Hina","various Polynesian traditions","W. D. Westervelt","pol.legends-maui","primary/legends-ma-ui-westervelt-32601.txt","A collection centered on Maui traditions across Polynesian islands; preserves regional variation."),
   ("pg-39195","Legends of Gods and Ghosts (Hawaiian Mythology)","various Hawaiian traditions","W. D. Westervelt","pol.hawaiian-mythology","primary/hawaiian-mythology-westervelt-39195.txt","A Hawaiian mythology collection useful for local variation and supernatural beings.")],
  "days":[
   ("maui-trickster","Maui: The Creative Trickster","Cleverness changes the world","Maui’s deeds make intelligence, daring, and mischief into forces that reshape nature.","What drives Maui’s power?","Cunning, daring, and useful mischief"),
   ("fishing-islands","Fishing Up Islands","A trick becomes geography","Maui’s island-fishing traditions turn divine play into a story of land, origin, and human dwelling.","What does Maui’s fishing create?","Islands and a story of origin"),
   ("snaring-sun","Snaring the Sun","Limiting a cosmic force for human life","Maui’s sun-snaring story places trickster force in service of a more livable world.","What does Maui constrain?","The sun’s dangerous power"),
   ("finding-fire","Finding Fire","A gift won through persistence","Fire traditions join cleverness, necessity, and the transfer of a cosmic gift to humans.","What does Maui seek for people?","Fire and the knowledge to use it"),
   ("pele-volcano","Pele and Sacred Volcanic Power","Place-bound divine force","Hawaiian volcano traditions tie deity, landscape, emotion, and danger into a living geography.","What does Pele connect?","Divine force and volcanic place")]}
}

def source_ref(record, pantheon, role, locator, note):
    return {"recordId": record[0], "sourceId": record[4], "work": record[1], "author": record[2], "translator": record[3], "locator": locator, "localPath": f"content/corpus/{pantheon}/{record[5]}", "excerpt": record[6], "note": note}

def lesson(key, week, index, spec, records):
    slug,title,subtitle,focus,q,correct = spec
    pid = f"{key}.week01.day{index:02d}.{slug}"
    refs = {
      "ref-primary": source_ref(records[0], key, "primary", f"Primary scaffold source — {title}", "Use the named collection/translation and preserve its dated or editorial frame."),
      "ref-secondary": source_ref(records[1], key, "secondary", f"Comparative corpus source — {title}", "Use as a second source lens; do not blend separate traditions into one canon.")}
    return {"id":pid,"version":1,"weekId":week,"pantheon":key,"themeMode":"pantheon","title":title,"subtitle":subtitle,"estimatedMinutes":3,"difficulty":1,"tags":[key,*title.split()[:2]],"learningObjectives":[{"id":f"obj.{slug}.concept","text":f"Identify the main source-grounded idea in {title}."},{"id":f"obj.{slug}.sources","text":"Distinguish primary, collection, synthesis, folklore, and reception evidence."}],"sourceReferences":refs,"narrativeBlocks":[
      {"id":"card-01","kind":"context","title":title,"body":focus,"sourceRefIds":["ref-primary","ref-secondary"],"objectiveIds":[f"obj.{slug}.concept"]},
      {"id":"card-02","kind":"source","title":"What the first source adds","body":"The first corpus source gives the broad story-world and vocabulary. Keep its editor, translator, and date in view rather than treating it as a neutral myth file.","sourceRefIds":["ref-primary"],"objectiveIds":[f"obj.{slug}.sources"]},
      {"id":"card-03","kind":"source","title":"What the second source adds","body":"The second corpus record gives a different genre, region, or editorial lens. Comparing them helps you see where a tradition is stable and where it varies.","sourceRefIds":["ref-secondary"],"objectiveIds":[f"obj.{slug}.sources"]},
      {"id":"card-04","kind":"method","title":"How to read this tradition","body":"Ask who preserved the story, what kind of work it appears in, whether it is primary myth, folklore, synthesis, or reception, and what claim the passage can actually support.","sourceRefIds":["ref-primary","ref-secondary"],"objectiveIds":[f"obj.{slug}.sources"]},
      {"id":"card-05","kind":"synthesis","title":"The cross-pantheon hook","body":"This gives you a comparative theme, not a blended canon. Keep the source boundary attached while you connect it to other pantheons.","sourceRefIds":["ref-primary","ref-secondary"],"objectiveIds":[f"obj.{slug}.concept"]}],
      "quiz":[{"id":"q1","type":"single-choice","prompt":q,"choices":[{"id":"a","text":correct},{"id":"b","text":"A single universal myth canon"},{"id":"c","text":"Only modern entertainment"},{"id":"d","text":"Unrelated historical data"}],"answerId":"a","explanation":focus,"sourceRefIds":["ref-primary","ref-secondary"],"objectiveIds":[f"obj.{slug}.concept"],"deepDive":{"prompt":"Inspect the two corpus records.","suggestedQuestions":["What genre is each source?","What claim can each support?"],"sourceRefIds":["ref-primary","ref-secondary"]}},
      {"id":"q2","type":"single-choice","prompt":"What should stay attached to this claim?","choices":[{"id":"a","text":"Its source type, translator/editor, and pantheon"},{"id":"b","text":"Only the character name"},{"id":"c","text":"Only the modern summary"},{"id":"d","text":"Nothing"}],"answerId":"a","explanation":"The app keeps source boundaries visible so comparisons do not erase differences between traditions.","sourceRefIds":["ref-primary","ref-secondary"],"objectiveIds":[f"obj.{slug}.sources"],"deepDive":{"prompt":"Check the source boundary.","suggestedQuestions":["Is this primary, folklore, retelling, synthesis, or reception?"],"sourceRefIds":["ref-primary","ref-secondary"]}}],
      "feedbackOptions":["too-long","too-easy","too-hard","unclear","want-more-sources","want-more-flavor"],"review":{"status":"draft","reviewedBy":"Devin","reviewedAt":"2026-11-07","notes":"Second-wave generated lesson; five-card structure and two-source boundary included."}}

def topic(tid,title,body,records,next_ids):
    return tid,{"title":title,"body":body,"recordIds":records,"nextTopicIds":next_ids,"cards":[{"title":"Why it matters","body":body,"recordIds":records},{"title":"Compare carefully","body":"Use this thread to compare pantheons without erasing source type, region, or transmission history.","recordIds":records}]}

def write_pantheon(key,item):
    corpus=ROOT/"content/corpus"/key
    manifest={"manifestVersion":1,"pantheon":key,"records":[{"id":r[0],"title":r[1],"sourceType":"public-domain-corpus-text","ancientAuthors":[r[2]],"translator":r[3],"sourceIds":[r[4]],"sourceUrl":f"https://www.gutenberg.org/ebooks/{r[0].replace('pg-','')}","localPath":r[5],"rightsStatus":"Project Gutenberg public-domain edition; preserve attribution and review UK reuse before redistribution.","notes":r[6]} for r in item["records"]]}
    (corpus/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
    week={"id":item["weekId"],"title":item["weekTitle"],"subtitle":item["subtitle"],"pantheon":key,"themeMode":"pantheon","visual":{"logo":item["logo"],"accent":item["palette"]},"days":[],"suggestedTopics":[]}
    folder=ROOT/"content/lessons"/key/item["weekId"].split(".")[1]
    folder.mkdir(parents=True,exist_ok=True)
    for i,spec in enumerate(item["days"],1):
      doc=lesson(key,item["weekId"],i,spec,item["records"])
      filename=f"day-{i:02d}-{spec[0]}.json"; relpath=f"content/lessons/{key}/{item['weekId'].split('.')[1]}/{filename}"
      (folder/filename).write_text(json.dumps(doc,indent=2)+"\n",encoding="utf-8")
      week["days"].append({"day":i,"title":spec[1],"lessonId":doc["id"],"lessonPath":relpath,"status":"available"})
    records=[r[0] for r in item["records"]]
    t1,t2=item["topics"]
    shared={"chinese":"topic.shared.otherworld-boundaries","mesoamerican":"topic.shared.fate-return","mesopotamian":"topic.shared.fate-return","indian":"topic.shared.war-honor","polynesian":"topic.shared.cunning-power"}[key]
    lmap={"arcChoices":[{"id":f"arc.{key}-foundations","title":f"{item['name']} Foundations","description":f"Eight weeks introducing major {item['name']} traditions.","weeks":[item["weekTitle"],"Divine order","Heroes and journeys","Death and boundaries","Sacred places","Fate and duty","Folklore variants","Afterlives"]}],"topics":dict([
      topic(t1[0],t1[1],t1[2],records,[t2[0],shared]),
      topic(t2[0],t2[1],t2[2],records,[t1[0],shared])])}
    week["suggestedTopics"]=[{"id":t1[0],"title":t1[1],"description":t1[2],"relatedDay":1,"recordIds":records,"prompt":"Follow this thread and compare it across pantheons."}]
    cur=ROOT/"content/curriculum"/key; cur.mkdir(parents=True,exist_ok=True)
    (cur/f"{key}-week-01.json").write_text(json.dumps(week,indent=2)+"\n",encoding="utf-8")
    (cur/"learning-map.json").write_text(json.dumps(lmap,indent=2)+"\n",encoding="utf-8")

for k,v in PANTHEONS.items(): write_pantheon(k,v)
reg_path=ROOT/"content/pantheons.json"; reg=json.loads(reg_path.read_text(encoding="utf-8"))
for k,v in PANTHEONS.items():
 reg["pantheons"][k]={"id":k,"name":v["name"],"status":"active","visual":{"logo":v["logo"],"palette":v["palette"]},"paths":{"corpusManifest":f"content/corpus/{k}/manifest.json","activeWeek":f"content/curriculum/{k}/{k}-week-01.json","learningMap":f"content/curriculum/{k}/learning-map.json"}}
reg_path.write_text(json.dumps(reg,indent=2)+"\n",encoding="utf-8")
print("wrote second-wave pantheons",list(PANTHEONS))

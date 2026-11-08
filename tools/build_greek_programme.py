"""Guarded one-time editorial migration. Canonical JSON is authoritative after migration.
Default execution is read-only; --apply requires the exact printed input digest.
Version-2 lessons are never overwritten, including after subsequent hand editing.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path
from source_evidence import normalize, source_segments, source_text

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {'iliad': 'pg-02199', 'odyssey': 'pg-01727', 'arg': 'pg-00830', 'lib': 'perseus-apollodorus-library-frazer', 'epi': 'perseus-apollodorus-epitome-frazer', 'plut': 'pg-00674', 'aes': 'pg-08604', 'soph': 'pg-00031', 'eur': 'pg-15081', 'women': 'perseus-trojan-women-coleridge', 'hymn': 'pg-00348', 'pindar': 'pg-10717', 'ovid': 'pg-26073', 'frazer': 'pg-56002'}
# Each question has one defensible answer and two parallel, plausible misconceptions.
# The third question is reserved for the weekly assessment, never used as daily practice.
BANK = [
('2-1', 'iliad', 'Book 1, Chryses and the plague', 'come to the ships of the Achaeans to free his daughter',
 'Chryses offers ransom for his captive daughter. Agamemnon refuses him; Apollo sends plague, and the army must confront the cost of its leader’s decision.',
 ('Who asks the Achaeans to release his daughter?', 'Chryses', 'Priam', 'Calchas'),
 ('Why does the plague become an army-wide problem?', 'Agamemnon’s insult to Apollo’s priest brings divine punishment.', 'Achilles has already killed Hector.', 'The ransom has been paid to the wrong king.'),
 ('Which sequence opens the Iliad’s crisis?', 'A rejected petition leads to plague and a dispute among leaders.', 'Patroclus dies before Chryses visits the camp.', 'Priam offers ransom before Achilles withdraws.')),
('2-2', 'iliad', 'Book 1, the taking of Briseis', 'Briseis',
 'Agamemnon must return Chryseis, but demands another captive as compensation. He takes Briseis from Achilles, who withdraws from fighting. Both women are treated as prizes in the leaders’ dispute.',
 ('What does Agamemnon take from Achilles?', 'Briseis', 'The armour made by Hephaestus', 'The Trojan king’s ransom'),
 ('What is Achilles’ immediate response to the insult?', 'He withdraws his fighting support.', 'He kills Agamemnon in the assembly.', 'He leads the assault on Troy that night.'),
 ('Why distinguish Briseis from Chryseis?', 'Returning Chryseis prompts Agamemnon to take Briseis from Achilles.', 'They are two names for the same captive.', 'Briseis is the priest who demands ransom.')),
('2-3', 'iliad', 'Book 9, Achilles answers the embassy', 'Him do I hate even as the gates of hell',
 'Odysseus, Phoenix, and Ajax visit Achilles with an offer of gifts. Achilles does not accept a return on those terms: compensation has not settled the injury to his standing or his doubts about fighting.',
 ('What does the embassy offer Achilles?', 'Gifts and restored standing if he returns to battle', 'A command to leave Troy without his men', 'The kingship of Troy after Hector’s surrender'),
 ('Why is the embassy more than a payment negotiation?', 'Achilles questions honour, trust, and the value of risking his life.', 'Achilles does not understand what the gifts are worth.', 'The visitors have come without Agamemnon’s permission.'),
 ('How does Book 9 complicate heroic honour?', 'Material rewards do not automatically restore damaged trust.', 'A larger reward immediately ends Achilles’ anger.', 'The embassy proves Achilles cares only about armour.')),
('2-4', 'iliad', 'Book 18, news of Patroclus’ death', 'Patroclus',
 'Patroclus fights in Achilles’ armour and is killed. News of his death turns Achilles from withdrawal toward vengeance against Hector; the return to battle grows out of bereavement, not a successful settlement by gifts.',
 ('Whose death changes Achilles’ decision to fight?', 'Patroclus’', 'Agamemnon’s', 'Priam’s'),
 ('What makes the borrowed armour important?', 'It links Patroclus’ intervention to Achilles’ absent role.', 'It makes Patroclus immune to divine interference.', 'It proves Hector has already accepted a truce.'),
 ('What most directly motivates Achilles’ return?', 'Grief for Patroclus and the desire to avenge him', 'Acceptance of the original embassy without further loss', 'A promise that he will now survive the war')),
('2-5', 'iliad', 'Book 24, Priam’s appeal', 'Think of your father',
 'Priam enters the enemy camp to ransom Hector’s body. He asks Achilles to remember his own father. The two men mourn, and Achilles agrees to release the body and allow time for burial.',
 ('What does Priam ask Achilles to return?', 'Hector’s body', 'Helen’s wedding gifts', 'Patroclus’ armour'),
 ('Why does Priam mention Achilles’ father?', 'He appeals to a shared vulnerability across enemy lines.', 'He claims Achilles’ father ordered Hector’s death.', 'He offers Achilles a new military alliance.'),
 ('What changes in Book 24 without undoing the war?', 'Achilles recognises Priam’s grief and permits Hector’s burial.', 'Priam’s appeal brings Hector back to life.', 'Achilles agrees to lead Troy against Agamemnon.')),
('3-1', 'odyssey', 'Book 1, Telemachus and the suitors', 'suitors',
 'Odysseus is absent while suitors consume his household’s resources and press Penelope to marry. Athena encourages Telemachus to act. Homecoming begins as a crisis for those waiting at home, not just an adventure abroad.',
 ('Who is struggling with the suitors in Ithaca?', 'Telemachus', 'Nestor', 'Polyphemus'),
 ('What makes the suitors a threat to the household?', 'They consume its resources while pursuing Penelope.', 'They are guarding it against the returning king.', 'They have already escorted Odysseus home.'),
 ('Why begin with Ithaca rather than only Odysseus’ travels?', 'His absence has social costs for the household he hopes to regain.', 'The poem has forgotten who its returning hero is.', 'Ithaca has already completed the recognition of Odysseus.')),
('3-2', 'odyssey', 'Book 9, the Cyclops and the false name', 'Noman',
 'Trapped by Polyphemus, Odysseus uses wine, a false name, a stake, and the sheep to escape. He later reveals his identity in a boast, allowing the Cyclops to invoke Poseidon against him.',
 ('What helps Odysseus conceal who attacked the Cyclops?', 'A false name', 'A forged letter from Zeus', 'A disguise as Athena'),
 ('How does the later boast undermine the escape?', 'It gives Polyphemus the identity needed for his curse.', 'It wakes the Cyclops before the men leave the cave.', 'It returns the stolen sheep to the cave.'),
 ('What tension does the Cyclops episode expose?', 'Clever secrecy wins escape, but the desire for credit creates danger.', 'Strength alone succeeds where planning fails.', 'Revealing a name guarantees divine protection.')),
('3-3', 'odyssey', 'Book 12, instructions about the Sirens', 'Sirens',
 'Circe warns Odysseus about the Sirens. The crew must block their ears with wax; Odysseus can listen only while bound to the mast, with orders that prevent his later wishes from overruling the plan.',
 ('How are the crew protected from the Sirens’ song?', 'Wax blocks their ears.', 'They all bind themselves to the mast.', 'They answer with a louder song.'),
 ('Why does Odysseus give instructions before hearing the song?', 'The plan anticipates that temptation will change his wishes.', 'The crew have already heard the song safely.', 'Circe has promised the Sirens will remain silent.'),
 ('Which distinction matters in the Sirens plan?', 'The crew avoid hearing, while Odysseus listens under restraint.', 'Every sailor listens without any restraint.', 'Odysseus uses the false name from the Cyclops episode.')),
('3-4', 'odyssey', 'Book 11, Achilles among the dead', 'paid servant in a poor man’s house',
 'Odysseus encounters Achilles among the dead and praises his status. Achilles answers by preferring even a poor living servant’s life to rule among the dead. The exchange tests the value of glory against the loss of life.',
 ('How does the dead Achilles respond to praise of his status?', 'He says he would rather be alive in humble service.', 'He asks Odysseus to win another war for him.', 'He says death has fulfilled every heroic wish.'),
 ('What does Achilles’ reply challenge?', 'The assumption that posthumous glory compensates for lost life', 'The fact that Odysseus fought at Troy', 'The possibility of remembering the dead'),
 ('How should this passage qualify a reading of heroic fame?', 'The dead hero himself voices a cost that praise can conceal.', 'It proves every Greek text rejects honour.', 'It is an account of a funeral contest, not an encounter with the dead.')),
('3-5', 'odyssey', 'Book 23, Penelope’s test of the bed', 'bed',
 'Penelope does not accept the stranger’s identity on appearance alone. Her instruction about moving their bed draws out knowledge of its construction around a rooted olive tree: a private, shared history becomes evidence of identity.',
 ('What does Penelope use to test Odysseus?', 'Their marriage bed', 'The Cyclops’ cup', 'A shield left at Troy'),
 ('Why is the bed a strong recognition test?', 'Its construction is knowledge shared within their marriage.', 'Every visitor to Ithaca has seen it moved.', 'Athena has written Odysseus’ name on it.'),
 ('What does the recognition scene add to the idea of return?', 'Reaching home is not the same as being recognised and trusted.', 'Physical arrival makes all further tests unnecessary.', 'Penelope recognises him because he describes Troy’s walls.')),
('4-1', 'arg', 'Book 1, Pelias and the one-sandalled man', 'one sandal',
 'Pelias fears a prediction about a man wearing one sandal. Jason arrives matching that sign, and Pelias sends him after the Golden Fleece. The voyage grows from a ruler’s fear and a dangerous assignment, not a neutral sporting contest.',
 ('Who sends Jason after the fleece?', 'Pelias', 'Aeetes', 'Alcinous'),
 ('Why does the opening connect politics with the quest?', 'Pelias uses the expedition against someone he fears.', 'Jason has already been crowned king of Colchis.', 'The fleece is being awarded at an athletic festival.'),
 ('Which detail explains Pelias’ alarm?', 'Jason matches the warning about a man with one sandal.', 'Jason returns carrying the fleece before the voyage.', 'Medea arrives in Iolcus before Jason is born.')),
('4-2', 'arg', 'Book 3, Aeetes’ challenge', 'bulls',
 'Aeetes requires Jason to yoke dangerous bulls, plough a field, and sow dragon’s teeth. Armed men will spring from the sowing. Jason needs Medea’s protective drugs and instructions to survive the task.',
 ('What must Jason sow in Aeetes’ field?', 'Dragon’s teeth', 'Pomegranate seeds', 'Olive stones'),
 ('What does Medea supply for the challenge?', 'Protective drugs and practical instructions', 'A ship that completes the ploughing', 'A treaty abolishing Aeetes’ test'),
 ('Why is it misleading to call Jason’s success unaided strength?', 'The challenge is overcome with Medea’s specialist help.', 'Jason completes the test before he meets Aeetes.', 'The bulls turn out to be ordinary farm animals.')),
('4-3', 'arg', 'Book 3, Medea’s conflict and aid', 'Medea',
 'Medea is caught between her household and her desire to help Jason. Apollonius gives sustained attention to her distress and deliberation, while divine intervention also shapes her desire. Her aid is decisive, but her freedom is not uncomplicated.',
 ('Whose knowledge makes Jason’s test survivable?', 'Medea’s', 'Pelias’', 'Hector’s'),
 ('What conflict shapes Medea’s decision?', 'Helping Jason conflicts with loyalty to her father’s household.', 'Choosing which Athenian office to hold', 'Deciding whether to bury Patroclus'),
 ('How can we describe Medea without erasing the poem’s tensions?', 'She deliberates and acts within family pressures and divine influence.', 'She is merely a reward with no decisions in the plot.', 'She has no connection to Colchis or Aeetes.')),
('4-4', 'arg', 'Book 4, the killing of Apsyrtus', 'Apsyrtus',
 'Escape with the fleece does not finish the moral story. In Apollonius’ version, Medea helps lure Apsyrtus into an encounter where Jason kills him. The flight requires a reckoning with the bloodshed, including purification by Circe.',
 ('Who kills Apsyrtus in Apollonius’ account?', 'Jason', 'Pelias', 'Heracles'),
 ('What makes the return voyage morally troubled?', 'The escape involves betrayal and bloodshed requiring purification.', 'The fleece has been returned voluntarily to Aeetes.', 'The crew have forgotten where Iolcus is.'),
 ('Which claim preserves the source boundary?', 'Apollonius’ Apsyrtus episode should not be silently replaced by another version.', 'Every account gives exactly the same killing of Apsyrtus.', 'Euripides’ Medea narrates the whole outward voyage on stage.')),
('4-5', 'eur', 'Medea, opening speech of the Nurse', 'Would that the hull of Argo',
 'Euripides starts in Corinth after the expedition. Jason has made a new marriage, and the Nurse fears what the abandoned Medea may do. This tragedy reshapes the heroic past into a crisis of oaths, exile, family, and revenge.',
 ('Where does Euripides’ Medea begin?', 'Corinth, after the voyage', 'Colchis, before Jason arrives', 'Troy, before Achilles withdraws'),
 ('What distinguishes this play from the Argonautica?', 'It stages a later crisis rather than narrating the quest itself.', 'It is a handbook arranging the twelve labours.', 'It is a victory ode for Jason’s chariot race.'),
 ('Why should the two works not be treated as one continuous transcript?', 'They are different authors’ works with different genres and dramatic purposes.', 'Euripides is the translator of Apollonius.', 'The Nurse is an eyewitness narrator in the Argonautica.')),
('5-1', 'lib', 'Library 2.4.12, the oracle and the initial ten labours', 'Pythian priestess then first called him Hercules',
 'After the killing of his children in madness, Heracles receives an oracle directing service to Eurystheus. The initial instruction is ten labours; the familiar total becomes twelve when Eurystheus refuses to count two feats.',
 ('How many labours does the oracle initially require?', 'Ten', 'Twelve', 'Seven'),
 ('Why does the catalogue eventually reach twelve?', 'Eurystheus refuses the Hydra labour because Iolaus helped and the Augeas labour because it was for hire.', 'Heracles performs two extra labours after being received among the gods.', 'The Pythian priestess revises her oracle after Heracles reaches Tiryns.'),
 ('Which parts of the account contribute to the total of twelve?', 'The oracle assigns ten; Eurystheus later refuses to count two feats.', 'The oracle assigns twelve before Heracles begins.', 'The Library repeats two labours without explaining why.')),
('5-2', 'lib', 'Library 2.5.1, the Nemean lion', '2.5.1',
 'Heracles finds that arrows do not defeat the Nemean lion. He blocks one entrance of its cave, enters by the other, and overcomes it by grappling. The episode makes method, not simply a bigger weapon, decisive.',
 ('How does Heracles overcome the Nemean lion?', 'By grappling and choking it', 'By poisoning its drinking water', 'By having Jason trap it in the Argo'),
 ('Why does the cave matter to the method?', 'Blocking an entrance limits the lion’s escape.', 'The cave supplies arrows that pierce the hide.', 'The cave is the court where Eurystheus judges him.'),
 ('What makes this feat an example of adaptation?', 'Failed arrows lead Heracles to change his approach.', 'The first arrow kills the lion immediately.', 'Eurystheus fights the lion while Heracles watches.')),
('5-3', 'lib', 'Library 2.4.12, madness, purification, and service', 'was driven mad through the jealousy of Hera',
 'In the Library, Hera sends madness and Heracles kills his children. He is purified and consults Delphi; the oracle directs him to serve Eurystheus. This is this work’s sequence, not a universal chronology for every Heracles play.',
 ('What precedes the labours in this account?', 'Madness, the killing of his children, purification, and an oracle', 'His marriage to Hebe among the gods', 'His escape from the Cretan labyrinth'),
 ('Who directs Heracles to serve Eurystheus?', 'The Delphic oracle', 'Priam', 'The Athenian assembly'),
 ('Why attach the sequence to the Library?', 'Different works can place the family catastrophe differently.', 'The Library is a modern superhero adaptation.', 'Eurystheus writes every ancient account of Heracles.')),
('5-4', 'lib', 'Library 2.7.7, the pyre and reception among the gods', 'constructed a pyre',
 'The poisoned garment causes Heracles unbearable suffering. He has a pyre built on Mount Oeta; the Library then tells of his ascent to heaven, reconciliation with Hera, and marriage to Hebe. Apotheosis means reception into divine life, not survival by ordinary healing.',
 ('Where is Heracles’ pyre built?', 'Mount Oeta', 'Mount Olympus in the Athenian assembly', 'The cave of Polyphemus'),
 ('What does apotheosis mean in this episode?', 'Heracles is received among the gods.', 'Heracles becomes king of Troy.', 'Heracles is restored to service under Eurystheus.'),
 ('Which passage directly supports this ending?', 'Library 2.7.7', 'Library 2.5.2, the Hydra labour', 'Library 2.4.12, the oracle and initial service')),
('5-5', 'pindar', 'Olympian 2, opening invocation', 'Olympian feast was founded',
 'At the opening of Olympian 2, Pindar moves from Zeus to Herakles and then to the victor Theron. Herakles’ association with the festival helps place a contemporary victory within a prestigious sacred and heroic frame.',
 ('Whose victory does Olympian 2 celebrate?', 'Theron’s', 'Achilles’', 'Oedipus’'),
 ('What is Herakles doing in this opening?', 'Connecting the festival’s heroic foundation with praise of the victor', 'Confessing the murder of Laius', 'Explaining the bed test to Penelope'),
 ('What distinguishes this use of Herakles from the Library’s list?', 'The ode praises a victor rather than arranging a sequence of labours.', 'The ode claims to be a complete prose biography.', 'The Library is the speech Theron gives at his victory.')),
('6-1', 'plut', 'Life of Theseus, road to Athens', 'Periphetes',
 'Plutarch tells how Theseus travels to Athens by land and confronts violent figures along the road. The young hero models himself on Heracles, but his journey also prepares his recognition in Athens.',
 ('Which journey shapes Theseus’ early exploits?', 'The overland road to Athens', 'The voyage to Colchis', 'The march from Troy with Hector'),
 ('Why compare these deeds with Heracles’?', 'Theseus’ emulation is part of Plutarch’s account of his ambition.', 'They prove Theseus and Heracles are the same person.', 'They show Plutarch is narrating the Iliad’s opening.'),
 ('Which source supplies this biographical framing?', 'Plutarch’s Life of Theseus', 'Pindar’s Olympian 2', 'The Homeric Hymn to Demeter')),
('6-2', 'epi', 'Epitome 1.8-1.9, Ariadne and the thread', 'Ariadne',
 'In the Epitome, Ariadne helps Theseus escape the labyrinth by providing a thread. Defeating the Minotaur is only part of the problem: he also needs a way back out. The victory depends on assistance as well as force.',
 ('What does Ariadne give Theseus for the labyrinth?', 'A thread', 'A wax seal for his ears', 'A dragon’s tooth'),
 ('What problem does her help solve?', 'Finding the way out after entering the maze', 'Winning an election at Athens', 'Preventing Apollo’s plague at Troy'),
 ('What does the thread qualify about the heroic victory?', 'Theseus’ success depends on another person’s practical aid.', 'The Minotaur has already left Crete.', 'Theseus needs no knowledge of the maze.')),
('6-3', 'plut', 'Life of Theseus, unification of Attica', 'one city',
 'Plutarch credits Theseus with bringing the inhabitants of Attica into one political community. The story presents a founder of civic order, not merely a monster-killer; it is a later biography’s account of a legendary past.',
 ('What political achievement does Plutarch attribute to Theseus?', 'Uniting Attica in one civic community', 'Founding the kingdom of Colchis', 'Replacing Zeus as ruler of Olympus'),
 ('How should this claim be framed?', 'As Plutarch’s legendary foundation narrative, not contemporary documentation', 'As a surviving law written by Theseus himself', 'As an episode narrated by Achilles in the Iliad'),
 ('What changes when the hero becomes a civic founder?', 'His deeds explain the community’s institutions and belonging.', 'His story ceases to have political meaning.', 'The source becomes an eyewitness record of prehistoric Athens.')),
('6-4', 'plut', 'Life of Theseus, alternative accounts of Ariadne', 'Ariadne',
 'Plutarch records disagreements about Ariadne rather than giving one uncontested ending. The variations are evidence about how a story was transmitted and used, not errors to conceal by blending every account together.',
 ('What should we do when Plutarch records conflicting accounts?', 'Keep the alternatives attached to their reported sources.', 'Combine incompatible details into one certain sequence.', 'Discard every version except the best-known modern one.'),
 ('Why is Ariadne useful for studying variants?', 'Her fate is told differently in accounts Plutarch discusses.', 'Every source preserves her own written testimony.', 'Her story appears only in one surviving sentence.'),
 ('Which statement respects variant evidence?', 'Plutarch reports alternatives; his report does not establish one eyewitness history.', 'All variants must have happened consecutively.', 'A later biography cannot preserve any earlier traditions.')),
('6-5', 'plut', 'Life of Theseus, the unification narrative', 'one city',
 'Compare two source-specific roles: Plutarch’s Theseus brings Attica into a civic community, while the Library’s Heracles serves Eurystheus through imposed labours. These are useful contrasts, not exhaustive definitions of either hero.',
 ('Which pairing fits the cited accounts?', 'Theseus and civic unification; Heracles and imposed service', 'Theseus and the Sirens; Heracles and Penelope’s bed', 'Theseus and Troy’s ransom; Heracles and the Golden Fleece'),
 ('Why call these roles a comparison rather than fixed definitions?', 'Each work selects only part of a larger heroic tradition.', 'Both works were dictated by the same hero.', 'A hero can appear in only one genre.'),
 ('What evidence is needed for the comparison?', 'Both Plutarch’s unification account and the Library’s service account', 'Only an Iliad quotation about Achilles', 'Only a modern ranking of heroic strength')),
('7-1', 'aes', 'Agamemnon, opening Watchman and the return', 'I pray the gods to quit me of my toils',
 'A watchman awaits the beacon announcing Troy’s fall. Agamemnon’s victorious return will not restore a peaceful house: Clytemnestra kills him, and the sacrifice of Iphigenia stands among the grievances that the play brings home from war.',
 ('What signal does the Watchman await?', 'A beacon announcing Troy’s fall', 'The Sirens’ song', 'An oracle naming Laius’ killer'),
 ('Why is victory an insecure ending here?', 'The returning king faces violence and unresolved grievances at home.', 'The Greek army has not yet sailed for Troy.', 'Clytemnestra is absent from the play.'),
 ('Which contrast with Odysseus’ return is useful but limited?', 'Agamemnon’s return exposes lethal household conflict rather than achieving reunion.', 'Both homecomings end with the same bed test.', 'Neither poem connects war with household damage.')),
('7-2', 'aes', 'Eumenides, Orestes submits his act to judgement', 'With blood for blood avenging my loved sire',
 'Orestes has killed his mother to avenge his father. In Eumenides, Athena establishes a court to hear the conflict, and the pursuing Erinyes must also be addressed. The ending stages a negotiated civic settlement, not the disappearance of every competing claim.',
 ('Whose killing has brought Orestes before judgement?', 'His mother’s', 'Hector’s', 'The Minotaur’s'),
 ('What changes in the handling of the conflict?', 'A court hears claims that a blood feud cannot resolve by another killing.', 'Orestes is declared never to have used violence.', 'The Erinyes are revealed to be ordinary Athenian soldiers.'),
 ('Why is “law simply replaces religion” a poor summary?', 'Divine figures and the Erinyes remain central to the settlement.', 'The play contains no court or judgement.', 'Athena is absent from the proceedings.')),
('7-3', 'soph', 'Antigone, Creon’s burial decree', 'For Polyneices ’tis ordained that none',
 'Creon forbids burial of Polyneices after the attack on Thebes. Antigone defies him in the name of obligations to her brother and the gods. The play tests Creon’s assertion of civic authority against duties his decree cannot simply erase.',
 ('Whose burial does Creon forbid?', 'Polyneices’', 'Patroclus’', 'Laius’'),
 ('What motivates Antigone’s defiance?', 'Obligations to her brother and divine burial duties', 'A desire to recover the Golden Fleece', 'An order from Agamemnon’s embassy'),
 ('Which summary avoids flattening the conflict?', 'A ruler’s decree collides with familial and divine obligations.', 'Both characters agree that burial has no religious meaning.', 'The play is chiefly about identifying Laius’ murderer.')),
('7-4', 'soph', 'Oedipus the King, Oedipus’ proclamation', 'And on the murderer this curse I lay',
 'To free Thebes from plague, Oedipus seeks Laius’ killer and curses the unknown culprit. The investigation eventually identifies Oedipus himself. The skill and determination used to protect the city turn back upon its ruler.',
 ('What crime does Oedipus investigate?', 'The killing of Laius', 'The theft of Briseis', 'The murder of Agamemnon'),
 ('What gives his curse dramatic irony?', 'The unknown killer he condemns will prove to be himself.', 'The audience knows Laius is still ruling Thebes.', 'Creon has already confessed to the killing.'),
 ('What changes during the investigation?', 'The investigator becomes the person his inquiry exposes.', 'Oedipus abandons inquiry because no witnesses exist.', 'The plague is solved by recovering the fleece.')),
('7-5', 'women', 'Trojan Women, Poseidon’s opening speech', 'Scamander',
 'Troy has fallen. Euripides focuses on captive women awaiting allocation to Greek masters, with further losses still ahead. The same war that can furnish heroic fame appears here through enslavement, separation, and mourning.',
 ('Whose situation is central after Troy’s fall?', 'Captive Trojan women', 'Victorious athletes at Olympia', 'Suitors waiting in Ithaca'),
 ('What perspective does the play add to accounts of victory?', 'The consequences borne by conquered and enslaved people', 'An account in which Troy has not yet been attacked', 'An assurance that captives suffer no further losses'),
 ('How should this play enter a comparison with the Iliad?', 'As another work’s perspective on war, not a missing transcript from Homer', 'As the final book written by Homer himself', 'As proof that no Greek work ever praised a warrior')),
('8-1', 'hymn', 'Homeric Hymn to Demeter, lines 370-383', 'sweet pomegranate seed to eat',
 'Demeter’s withdrawal threatens the growth that sustains mortals. Persephone returns, but the pomegranate binds her to time below as well. The hymn’s settlement concerns divine power, human survival, and reunion with a lasting limit.',
 ('What food binds Persephone to the underworld?', 'Pomegranate seed', 'The cattle of the Sun', 'The Nemean lion’s flesh'),
 ('Why is the return not an unconditional rescue?', 'Persephone must still spend part of her time below.', 'Demeter never sees her daughter again.', 'Hades gives up all claims before she eats.'),
 ('What should a source-specific reading avoid?', 'Reducing the hymn to a universal story of a voluntary romantic journey', 'Noticing Demeter’s grief and the threat to crops', 'Keeping the hymn distinct from later versions')),
('8-2', 'odyssey', 'Book 11, Achilles’ reply among the dead', 'paid servant in a poor man’s house',
 'Return to Achilles’ answer among the dead: he prefers humble life to kingship over the departed. This is a literary encounter with a remembered hero; it is not by itself evidence of a particular community’s hero-cult ritual.',
 ('What does Achilles prefer to rule among the dead?', 'A humble life among the living', 'Another funeral contest', 'A new suit of divine armour'),
 ('What can this passage establish directly?', 'How the Odyssey stages Achilles’ speech about death', 'The exact ritual of every historical hero cult', 'The beliefs of all Greeks in every period'),
 ('What additional evidence would a claim about local hero cult require?', 'Evidence about the particular sanctuary, community, and practice', 'Only the fact that a hero speaks in an epic', 'Only a comparison of modern film heroes')),
('8-3', 'ovid', 'Metamorphoses 8.169-182, Ariadne and the crown', 'barbarously deserts his companion',
 'In Ovid’s Roman epic, Theseus abandons Ariadne after the escape from Crete. Liber helps the deserted woman and sets her crown among the stars. Transformation moves the narrative beyond the hero’s successful escape.',
 ('What becomes a constellation in this episode?', 'Ariadne’s crown', 'Theseus’ sword', 'The Minotaur’s cave'),
 ('Why label Ovid as Roman reception here?', 'His later Latin epic reshapes material also found in Greek traditions.', 'He is the Greek eyewitness who built the labyrinth.', 'He is the translator of the Epitome.'),
 ('Which comparison keeps the sources distinct?', 'Compare Ovid’s crown transformation with the Epitome’s thread episode.', 'Use Ovid to silently correct every earlier Greek account.', 'Treat Riley’s explanatory summaries as Ovid’s own Latin lines.')),
('8-4', 'frazer', 'Studies in Greek Scenery, introductory discussion of Pausanias and Sipylus', 'stately tomb',
 'Frazer discusses Pausanias’ familiarity with Mount Sipylus, including monuments linked with Tantalus, Pelops, and Niobe. Here Frazer is describing an ancient writer’s observations; the paragraph is not Frazer’s own eyewitness confirmation of those heroes.',
 ('Whose observations is Frazer discussing in this passage?', 'Pausanias’', 'Achilles’', 'Penelope’s'),
 ('What does a named legendary tomb establish by itself?', 'An association between a place and a story, not proof the hero lived there', 'A contemporary birth certificate for the hero', 'The historical truth of every attached episode'),
 ('Why keep Frazer’s scholarly layer visible?', 'His interpretation of ancient testimony is not the ancient testimony itself.', 'He is the original author of the Homeric Hymns.', 'A modern scholarly work cannot mention ancient geography.')),
('8-5', 'iliad', 'Book 24, Priam appeals to Achilles', 'Think of your father',
 'Compare four selected roles, not four fixed personalities: Achilles facing grief, Odysseus recognised at home, Heracles serving Eurystheus, and Theseus founding civic order. Each contrast needs evidence from its own work.',
 ('Which pairing belongs to the cited Odyssey scene?', 'Odysseus and Penelope’s recognition test', 'Achilles and the Cretan thread', 'Theseus and Patroclus’ armour'),
 ('Why does this comparison need more than an Iliad citation?', 'Claims about the other heroes require their own source passages.', 'The Iliad contains every surviving heroic narrative.', 'A comparison has no factual claims to support.'),
 ('What is the strongest course-wide conclusion?', 'Heroic roles vary by episode, genre, and community; comparisons must retain those boundaries.', 'All four heroes express one unchanging moral code.', 'Later biographies are eyewitness records of the heroic age.')),
]


def question(number, row, objectives, refs, slot):
    prompt, correct, wrong1, wrong2 = row
    texts = [correct, wrong1, wrong2]
    shift = slot % 3
    texts = texts[-shift:] + texts[:-shift] if shift else texts
    choices = [{'id': chr(97 + i), 'text': text} for i, text in enumerate(texts)]
    explanation = correct.rstrip('.!?') + '. Compare the named passage with the distinction in the question.'
    return {'id': f'q{number}', 'type': 'single-choice', 'prompt': prompt, 'choices': choices, 'answerId': next(c['id'] for c in choices if c['text'] == correct), 'explanation': explanation, 'sourceRefIds': refs, 'objectiveIds': [objectives[number % len(objectives)]['id']]}


def reference(records, key, locator, anchor, quote_length=300):
    record = records[SOURCES[key]]
    path = 'content/corpus/greek/' + record['localPath']
    segments = [s for s in source_segments(ROOT / path) if s['evidenceType'] == 'source-text']
    if key in {'iliad', 'odyssey', 'arg'}:
        book = locator.split(',')[0]
        segments = [s for s in segments if s['locator'] == book]
    if key in {'lib', 'epi'}:
        location_match = re.search(r'Library\s+(\d+)\.(\d+)\.(\d+)', locator) if key == 'lib' else re.search(r'Epitome\s+(\d+)\.(\d+)', locator)
        if location_match:
            numbers = location_match.groups()
            labels = ['book', 'chapter', 'section'] if key == 'lib' else ['chapter', 'section']
            location = ' · '.join(f'{kind} {n}' for kind, n in zip(labels, numbers))
            segments = [s for s in segments if s['locator'] == location]
        selected = next((s for s in segments if normalize(anchor).casefold() in s['text'].casefold()), None)
        if selected is None:
            raise ValueError(f'Missing source anchor in cited section: {key} / {locator} / {anchor}')
        text = selected['text']
        start = text.casefold().index(normalize(anchor).casefold())
        start = text.rfind(' ', 0, max(0, start - 80)) + 1
    else:
        selected = next((s for s in segments if normalize(anchor).casefold() in s['text'].casefold()), None)
        if selected is None:
            raise ValueError(f'Missing source anchor: {key} / {locator} / {anchor}')
        text = selected['text']; start = text.casefold().index(normalize(anchor).casefold())
        start = text.rfind(' ', 0, max(0, start - 80)) + 1
    end = text.find(' ', start + quote_length)
    end = end if end >= 0 else len(text)
    quote = text[start:end]
    # A local character anchor is reproducible, not an invented ancient line number.
    return {'recordId': record['id'], 'sourceId': ('grc.homeric-hymns' if key == 'hymn' else record['sourceIds'][0]), 'work': record['title'], 'author': ', '.join(record.get('ancientAuthors', record.get('authors', []))) or 'James George Frazer', 'translator': record.get('translator', 'not applicable'), 'locator': f'{locator}; {selected["locator"]}, normalized characters {start}-{end}', 'localPath': path, 'excerpt': quote, 'evidenceType': 'quotation', 'note': 'Verbatim local text with whitespace normalized. Lesson analysis is interpretation, not part of this quotation.'}


def build():
    records = {r['id']: r for r in json.loads((ROOT / 'content/corpus/greek/manifest.json').read_text(encoding='utf-8'))['records']}
    changes = {}
    lesson_paths = {}
    for path in sorted((ROOT / 'content/lessons/greek/heroes-programme').glob('*.json')):
        doc = json.loads(path.read_text(encoding='utf-8'))
        key = f'{int(path.name[5:7])}-{int(path.name[12:14])}'
        lesson_paths[key] = path
    for key, source, locator, anchor, scene, q1, q2, assessment in BANK:
        path = lesson_paths[key]
        doc = json.loads(path.read_text(encoding='utf-8'))
        doc['sourceReferences'] = {'main': reference(records, source, locator, anchor)}
        if key == '5-1':
            doc['sourceReferences']['hydra'] = reference(records, 'lib', 'Library 2.5.2, labour not counted without independent victory', 'Eurystheus said that this labour should not be reckoned among the ten')
            doc['sourceReferences']['augeas'] = reference(records, 'lib', 'Library 2.5.5, labour refused as hired work', 'Eurystheus would not admit this labour either among the ten')
        if key == '5-3':
            doc['sourceReferences']['oracle'] = reference(records, 'lib', 'Library 2.4.12, the Pythian oracle assigns service', 'serving Eurystheus for twelve years')
        if key == '5-4':
            doc['sourceReferences']['main'] = reference(records, source, locator, anchor, quote_length=520)
        if key in {'6-5', '8-5'}:
            doc['sourceReferences']['heracles'] = reference(records, 'lib', 'Library 2.4.12, service to Eurystheus', 'serving Eurystheus for twelve years')
        if key == '8-5':
            doc['sourceReferences']['odysseus'] = reference(records, 'odyssey', 'Book 23, recognition and the bed', 'bed')
            doc['sourceReferences']['theseus'] = reference(records, 'plut', 'Life of Theseus, unification of Attica', 'one city')
        refs = list(doc['sourceReferences'])
        doc['narrativeBlocks'][0]['body'] = scene
        doc['narrativeBlocks'][1]['body'] = 'Source quotation (translation; whitespace normalized): “' + doc['sourceReferences']['main']['excerpt'] + '”'
        doc['narrativeBlocks'][2]['body'] = 'Interpretation: ' + doc['narrativeBlocks'][2]['body']
        if key == '7-3':
            doc['narrativeBlocks'][2]['body'] = 'Interpretation: the play puts Creon’s claims about civic order under pressure from obligations to kin and the gods. That does not make all competing claims equally justified.'
        if key == '8-1':
            doc['narrativeBlocks'][2]['body'] = 'Interpretation: reunion is qualified by a continuing underworld claim. Avoid reducing the hymn’s divine negotiations and ritual setting to a simple calendar allegory.'
        doc['narrativeBlocks'][3]['body'] = 'Source discipline: ' + q2[1] + '. Keep this work’s version distinct from other accounts.'
        if key == '8-4':
            doc['narrativeBlocks'][2]['body'] = 'Interpretation: places can preserve stories without proving their events. Frazer’s dated scholarship must be checked against the ancient testimony he discusses.'
        doc['learningObjectives'][0]['text'] = 'Explain this episode: ' + q1[0]
        doc['learningObjectives'][1]['text'] = 'Use the cited passage to explain: ' + q2[0]
        for block in doc['narrativeBlocks']:
            block['sourceRefIds'] = refs
        doc['quiz'] = [question(1, q1, doc['learningObjectives'], refs, len(changes)), question(2, q2, doc['learningObjectives'], refs, len(changes) + 1)]
        doc['version'] = 2
        doc['review'] = {'status': 'draft', 'reviewedBy': 'Devin', 'reviewedAt': '2026-11-08', 'notes': 'Corrective editorial pass: quotations mechanically matched to local text; passage selection and interpretations still require independent scholarly review. Not scholarly certification.'}
        changes[path] = doc
    # Week 1 retains its authored prose, but every displayed reference is replaced with a real quotation.
    week1 = json.loads((ROOT / 'content/curriculum/greek/greek-heroes-week-01.json').read_text(encoding='utf-8'))
    starters = [
      [('What does the Iliad’s opening foreground?', 'Achilles’ anger and its cost', 'The founding of Athens', 'Jason’s marriage in Corinth'), ('How does the Odyssey’s opening differ?', 'It foregrounds a widely travelled hero and his return.', 'It begins with Achilles’ refusal of gifts.', 'It begins with the Nemean lion.')],
      [('What does Achilles withdraw from after the quarrel?', 'Fighting for the Achaean army', 'Ruling Athens', 'Searching for the fleece'), ('Why is anger not merely private here?', 'Its consequences fall on the fighting community.', 'It never affects any other character.', 'It concerns only a footrace at Olympia.')],
      [('Which hero is described as widely travelled in the Odyssey?', 'Odysseus', 'Heracles', 'Theseus'), ('What makes cunning an incomplete guarantee of success?', 'Judgement and restraint still matter alongside clever plans.', 'It makes divine hostility impossible.', 'It removes the need to regain a household.')],
      [('Who supplies essential help to Jason?', 'Medea', 'Antigone', 'Penelope'), ('How do the Argonautica and Medea differ?', 'Epic narrates the quest; tragedy stages a later crisis.', 'Both are the same author’s diary.', 'Both are victory odes for Pelias.')],
      [('Which hero does Plutarch link to Athens’ civic foundation?', 'Theseus', 'Achilles', 'Jason'), ('Why identify the author when comparing heroes?', 'Genre and purpose shape the version being told.', 'Every work preserves an identical sequence.', 'A later biography is always an eyewitness account.')]
    ]
    for i, day in enumerate(week1['days']):
        path = ROOT / day['lessonPath']; doc = json.loads(path.read_text(encoding='utf-8'))
        for refid, old in list(doc['sourceReferences'].items()):
            key = next(k for k, value in SOURCES.items() if value == old['recordId'])
            if key == 'lib': key = 'plut'
            anchor = {'iliad': 'Sing, O goddess', 'odyssey': 'Tell me, O Muse', 'arg': 'Beginning with thee', 'eur': 'Would that the hull of Argo', 'plut': 'one city'}[key]
            doc['sourceReferences'][refid] = reference(records, key, {'iliad': 'Book 1, opening', 'odyssey': 'Book 1, opening', 'arg': 'Book 1, opening', 'eur': 'Medea, Nurse’s opening', 'plut': 'Life of Theseus, civic unification'}[key], anchor)
        refs = list(doc['sourceReferences'])
        for block in doc['narrativeBlocks']:
            if block['kind'] == 'source':
                block['body'] = 'Source quotations are available under the source buttons. They are translations, not the lesson author’s wording. Compare the work and locator before drawing conclusions.'
            block['sourceRefIds'] = refs
        doc['quiz'] = [question(j + 1, row, doc['learningObjectives'], refs, i + j) for j, row in enumerate(starters[i])]
        doc['version'] = 2
        doc['review'] = {'status': 'draft', 'reviewedBy': 'Devin', 'reviewedAt': '2026-11-08', 'notes': 'Corrective source/quiz pass; independent scholarly review pending.'}
        changes[path] = doc
    for w in range(1, 9):
        path = ROOT / f'content/curriculum/greek/greek-heroes-week-{w:02d}.json'
        week = json.loads(path.read_text(encoding='utf-8'))
        questions = []
        for i, day in enumerate(week['days']):
            doc = changes[ROOT / day['lessonPath']]
            if w == 1:
                rows = [
                  ('Why compare the openings of the Iliad and Odyssey?', 'They introduce different heroic problems rather than one moral template.', 'They are accounts of the same scene.', 'They prove every hero has the same ending.'),
                  ('Which consequence links Achilles’ quarrel to the wider war?', 'His withdrawal removes a crucial fighter from the army.', 'It moves the war from Troy to Athens.', 'It sends Jason to Colchis.'),
                  ('What must a return narrative address beyond travel?', 'Recognition and the household awaiting the traveller', 'Only the number of ships in the fleet', 'Only the weapons used to kill monsters'),
                  ('Why keep Apollonius and Euripides distinct?', 'Their genres and narrative settings shape different presentations of Medea.', 'They are aliases for Homer.', 'One is an eyewitness translation of the other.'),
                  ('What is a responsible claim about Plutarch’s Theseus?', 'Plutarch presents a legendary founder through later biography.', 'Plutarch records his personal meeting with Theseus.', 'Theseus wrote Plutarch’s account of Athens.')]
                row = rows[i]
            else:
                row = next(item[-1] for item in BANK if item[0] == f'{w}-{i+1}')
            q = question(i + 1, row, doc['learningObjectives'], list(doc['sourceReferences']), w + i)
            questions.append({'lessonId': doc['id'], 'question': q})
        week['assessment'] = {'title': week['title'] + ' assessment', 'prompt': 'Five new questions revisit the week’s events, interpretations, and source distinctions. Taking the assessment completes the week; missed answers remain practice priorities.', 'questionCount': 5, 'questions': questions}
        changes[path] = week
    path = ROOT / 'content/curriculum/programmes.json'
    programme = json.loads(path.read_text(encoding='utf-8'))
    for entry in programme['arc.greek-heroes']['weeks']:
        entry['assessment'] = changes[ROOT / entry['weekPath']]['assessment']
    changes[path] = programme
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', metavar='INPUT_SHA256', help='Apply once, only to the exact audited version-1 inputs')
    args = parser.parse_args()
    paths = sorted([* (ROOT / 'content/lessons/greek/heroes-programme').glob('*.json'), * (ROOT / 'content/lessons/greek/greek-heroes').glob('*.json'), * (ROOT / 'content/curriculum/greek').glob('greek-heroes-week-*.json'), ROOT / 'content/curriculum/programmes.json'])
    digest = hashlib.sha256(b''.join(path.read_bytes() for path in paths)).hexdigest()
    if any(json.loads(path.read_text(encoding='utf-8')).get('version', 1) >= 2 for path in paths if 'lessons' in path.parts):
        if args.apply:
            parser.error('Migration already applied. Canonical JSON may contain later edits; overwriting is forbidden.')
        print('Migration retired: canonical version-2 lesson JSON is authoritative. Run content_pipeline.py --check.')
        return
    print('Input SHA256:', digest)
    changes = build()
    print(f'Prepared {len(changes)} documents; no files written unless --apply matches the input digest.')
    if args.apply:
        if args.apply != digest:
            parser.error('Inputs changed or digest is incorrect; refusing to overwrite.')
        for path, doc in changes.items():
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print('Applied once. Further generation is disabled for these lessons.')


if __name__ == '__main__':
    main()

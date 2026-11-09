"""Run with python -B tools/test_regressions.py. Uses only temporary test storage."""
import json
import io
import subprocess
import sys
from contextlib import redirect_stderr, redirect_stdout
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest.mock import patch
from http.server import ThreadingHTTPServer

from mythos_server import Handler
from mythos_assistant import validate
from build_greek_programme import reference
from source_evidence import source_segments, check_reference

ROOT = Path(__file__).resolve().parents[1]


class RegressionTests(unittest.TestCase):
    def assert_editorially_reviewed(self, lesson):
        review = lesson['review']
        self.assertEqual(review['status'], 'reviewed', lesson['id'])
        self.assertEqual(review['reviewType'], 'editorial', lesson['id'])
        self.assertIn('AI editorial review', review['notes'], lesson['id'])
        self.assertIn('not independent scholarly review', review['notes'], lesson['id'])

    def test_server_does_not_serve_configuration(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / '.env').write_text('DUMMY_TEST_VALUE=not-a-secret')
            (root / 'index.html').write_text('test app')
            with patch('mythos_server.ROOT', root):
                server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                base = f'http://127.0.0.1:{server.server_port}'
                try:
                    self.assertEqual(urllib.request.urlopen(base + '/').status, 200)
                    for path in ['/.env', '/%2eenv', '/content/../.env', '/tools/mythos_server.py', '/content/']:
                        with self.assertRaises(urllib.error.HTTPError):
                            urllib.request.urlopen(base + path)
                finally:
                    server.shutdown()
                    server.server_close()
                    thread.join()

    def test_read_only_pipeline_and_invalid_build_do_not_write(self):
        import content_pipeline
        with patch.object(Path, 'write_text', side_effect=AssertionError('validation attempted a write')), patch('content_pipeline.build_retrieval_index') as build:
            with redirect_stdout(io.StringIO()):
                content_pipeline.main(check_only=True)
            with patch('content_pipeline.check_links', side_effect=lambda lesson, errors: errors.append('injected validation failure')):
                with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    content_pipeline.main(check_only=False)
            build.assert_not_called()

    def test_read_only_pipeline_accepts_excluded_personal_only_texts(self):
        import content_pipeline
        original_exists = Path.exists
        local_only = {'euripides-medea-35451.txt', 'euripides-bacchae-35173.txt', 'euripides-trojan-women-35171.txt'}

        def without_personal_copies(path):
            if path.name in local_only and 'content' in path.parts and 'corpus' in path.parts:
                return False
            return original_exists(path)

        with patch.object(Path, 'exists', without_personal_copies), patch('content_pipeline.build_retrieval_index') as build, redirect_stdout(io.StringIO()):
            content_pipeline.main(check_only=True)
            build.assert_not_called()

    def test_reviewed_content_requires_independent_attribution_and_typed_evidence(self):
        import content_pipeline
        lesson = {
            'id': 'test.lesson',
            'sourceReferences': {'legacy': {'recordId': 'test-source'}},
            'learningObjectives': [],
            'narrativeBlocks': [],
            'quiz': [],
            'review': {'status': 'reviewed', 'reviewedBy': 'Devin', 'reviewedAt': '2026-01-01', 'notes': 'Generated prose.'}
        }
        errors = []
        content_pipeline.check_links(lesson, errors)
        self.assertTrue(any('reviewType' in error for error in errors))
        self.assertTrue(any('untyped source references' in error for error in errors))

    def test_retired_generator_cannot_overwrite_canonical_lessons(self):
        lesson = ROOT / 'content/lessons/greek/heroes-programme/week-02-day-01-the-quarrel-and-the-ransom.json'
        before = lesson.read_bytes()
        for args in [[], ['--apply', 'not-the-input-digest']]:
            process = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/build_greek_programme.py'), *args], capture_output=True)
            self.assertEqual(process.returncode, 0 if not args else 2)
            self.assertEqual(lesson.read_bytes(), before)
        for name in ['build_pantheon_scaffolds.py', 'expand_pantheon_weeks.py', 'add_second_wave_pantheons.py', 'add_small_traditions.py', 'enrich_passage_locators.py', 'enrich_second_sources.py', 'deepen_generated_lessons.py']:
            process = subprocess.run([sys.executable, '-B', str(ROOT / 'tools' / name)], capture_output=True)
            self.assertEqual(process.returncode, 1, name)
            self.assertIn(b'Retired generator', process.stderr)
        self.assertEqual(lesson.read_bytes(), before)

    def test_quote_and_locator_tampering_rejected(self):
        path = ROOT / 'content/lessons/greek/heroes-programme/week-02-day-01-the-quarrel-and-the-ransom.json'
        ref = json.loads(path.read_text(encoding='utf-8'))['sourceReferences']['main']
        self.assertTrue(check_reference({**ref, 'excerpt': 'A fabricated quotation not in the translation.'}, ROOT))
        self.assertTrue(check_reference({**ref, 'locator': 'Book 1; Book 1, normalized characters 0-1'}, ROOT))
        self.assertTrue(check_reference({**ref, 'evidenceType': 'paraphrase'}, ROOT))

    def test_xml_excerpt_selector_uses_the_claim_anchor(self):
        manifest = json.loads((ROOT / 'content/corpus/greek/manifest.json').read_text(encoding='utf-8'))
        records = {item['id']: item for item in manifest['records']}
        cases = [
            ('Library 2.4.12, oracle and labours', 'Pythian priestess then first called him Hercules', ('ten labours',)),
            ('Library 2.5.2, Hydra labour', 'Eurystheus said that this labour should not be reckoned among the ten', ('not be reckoned among the ten',)),
            ('Library 2.5.5, Augeas labour', 'Eurystheus would not admit this labour either among the ten', ('not admit this labour either among the ten',)),
            ('Library 2.7.7, pyre and apotheosis', 'constructed a pyre', ('Mount Oeta', 'obtained immortality')),
        ]
        for locator, anchor, phrases in cases:
            ref = reference(records, 'lib', locator, anchor, quote_length=520)
            for phrase in phrases:
                self.assertIn(phrase, ref['excerpt'])
            self.assertEqual(check_reference(ref, ROOT), [])

    def test_unsupported_answer_rejected(self):
        raw = json.dumps({'answer': 'Unrelated invented assertion.', 'coverage': 'supported', 'citations': [{'chunkId': 'known', 'claim': 'Other claim.'}]})
        with self.assertRaises(ValueError):
            validate(raw, [{'id': 'known', 'text': 'A passage about something else.'}])

    def test_xml_notes_are_separate(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'source.xml'
            path.write_text('<TEI><div subtype="book" n="2"><div subtype="section" n="7"><p>Ancient text.<note>Modern claim.</note> More text.</p></div></div></TEI>')
            segments = source_segments(path)
            self.assertEqual(segments[0]['text'], 'Ancient text. More text.')
            self.assertEqual(segments[1]['evidenceType'], 'editorial-note')
            self.assertNotIn('Modern claim', segments[0]['text'])

    def test_greek_evidence_and_quizzes(self):
        programme = json.loads((ROOT / 'content/curriculum/programmes.json').read_text(encoding='utf-8'))['arc.greek-heroes']
        index = json.loads((ROOT / 'content/index.json').read_text(encoding='utf-8'))
        indexed_arc = next(item for item in index['arcChoices'] if item['id'] == 'arc.greek-heroes')
        answers = set()
        for module in programme['weeks']:
            week = json.loads((ROOT / module['weekPath']).read_text(encoding='utf-8'))
            self.assertEqual(len(week['assessment'].get('questions', [])), 5, week['id'])
            indexed_week = next(item for item in indexed_arc['programmeWeeks'] if item['weekId'] == week['id'])
            self.assertEqual(indexed_week['assessment'], week['assessment'], week['id'])
            for day in week['days']:
                lesson = json.loads((ROOT / day['lessonPath']).read_text(encoding='utf-8'))
                for ref in lesson['sourceReferences'].values():
                    self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
                for q in lesson['quiz']:
                    answers.add(q['answerId'])
                    self.assertNotIn(q['prompt'], ['Which source-backed point best captures this lesson?', 'What is the best reading practice for this lesson?'])
                    self.assertNotIn('That source context is irrelevant.', [c['text'] for c in q['choices']])
        self.assertGreater(len(answers), 1)

    def test_heracles_quotes_reach_the_claim_and_distractors_are_usable(self):
        base = ROOT / 'content/lessons/greek/heroes-programme'
        catalogue = json.loads((base / 'week-05-day-01-the-catalogue-of-labours.json').read_text(encoding='utf-8'))
        self.assertIn('ten labours', catalogue['sourceReferences']['main']['excerpt'])
        self.assertIn('not be reckoned among the ten', catalogue['sourceReferences']['hydra']['excerpt'])
        self.assertIn('not admit this labour either among the ten', catalogue['sourceReferences']['augeas']['excerpt'])
        lion = json.loads((base / 'week-05-day-02-the-nemean-lion.json').read_text(encoding='utf-8'))
        opening = json.loads((base / 'week-05-day-03-madness-and-service.json').read_text(encoding='utf-8'))
        self.assertIn('driven mad', opening['sourceReferences']['main']['excerpt'])
        self.assertIn('serving Eurystheus', opening['sourceReferences']['main']['excerpt'])
        apotheosis = json.loads((base / 'week-05-day-04-death-and-apotheosis.json').read_text(encoding='utf-8'))
        pindar = json.loads((base / 'week-05-day-05-strong-man-or-problem.json').read_text(encoding='utf-8'))
        self.assertIn('Arcesilaus', ' '.join(choice['text'] for choice in pindar['quiz'][0]['choices']))
        excerpt = apotheosis['sourceReferences']['main']['excerpt']
        self.assertIn('constructed a pyre', excerpt)
        self.assertIn('obtained immortality', excerpt)
        self.assertIn('Mount Oeta', excerpt)
        pindar = json.loads((base / 'week-05-day-05-strong-man-or-problem.json').read_text(encoding='utf-8'))
        for lesson in (catalogue, lion, apotheosis, pindar):
            for question in lesson['quiz']:
                texts = [choice['text'] for choice in question['choices']]
                self.assertEqual(len(set(texts)), len(texts))
                self.assertFalse(any(phrase in text for text in texts for phrase in (
                    'Athenian assembly', 'cave of Polyphemus', 'Jason trap it in the Argo',
                    'Oedipus’', 'Achilles’', 'confessing the murder of Laius',
                    'explaining the bed test to Penelope'
                )))
                self.assertNotIn('..', question['explanation'])
        assessment = json.loads((ROOT / 'content/curriculum/greek/greek-heroes-week-05.json').read_text(encoding='utf-8'))['assessment']['questions']
        catalogue_check = assessment[0]['question']
        self.assertIn('hydra', catalogue_check['sourceRefIds'])
        self.assertIn('augeas', catalogue_check['sourceRefIds'])
        apotheosis_check = assessment[3]['question']
        self.assertIn('Library 2.5.2', ' '.join(choice['text'] for choice in apotheosis_check['choices']))
        self.assertNotIn('Chryses', ' '.join(choice['text'] for choice in apotheosis_check['choices']))
        self.assertIn('Iolaus', ' '.join(choice['text'] for choice in assessment[1]['question']['choices']))

    def test_norse_starter_pack_has_passage_specific_evidence(self):
        files = sorted((ROOT / 'content/lessons/norse').rglob('*.json'))
        self.assertEqual(len(files), 5)
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertTrue(all(ref.get('evidenceType') == 'quotation' for ref in lesson['sourceReferences'].values()), lesson['id'])
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            cards = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
            self.assertNotIn('starter lesson uses the local scaffold source', cards, lesson['id'])
            self.assertNotIn('additional corpus record gives a second lens', cards, lesson['id'])
            self.assertNotIn('What should you keep attached to this claim?', [item['prompt'] for item in lesson['quiz']])

    def test_celtic_starter_pack_is_welsh_source_specific(self):
        files = sorted((ROOT / 'content/lessons/celtic').rglob('*.json'))
        self.assertEqual(len(files), 5)
        collected = []
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertTrue(all(ref['sourceId'] == 'cel.mabinogion' for ref in lesson['sourceReferences'].values()))
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation')
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            combined = ' '.join(
                [block['body'] for block in lesson['narrativeBlocks']]
                + [question['prompt'] for question in lesson['quiz']]
            )
            self.assertNotIn('starter lesson uses the local scaffold source', combined)
            self.assertNotIn('additional corpus record gives a second lens', combined)
            collected.append((lesson, combined))
        by_title = {lesson['title']: text for lesson, text in collected}
        self.assertIn('one stroke', by_title['Pwyll and the Otherworld'])
        self.assertIn('starling', by_title['Branwen: Hospitality and Consequence'])
        self.assertIn('Llwyd', by_title['Manawydan: Patience and Enchantment'])
        self.assertIn('Goewin', by_title['Math: Law, Magic, and Sovereignty'])
        self.assertIn('Gwion', by_title['Taliesin: Poetry and Transformation'])

    def test_egyptian_starter_pack_distinguishes_text_and_editorial_layers(self):
        files = sorted((ROOT / 'content/lessons/egyptian').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            expected_version = 3 if lesson['id'] in {
                'egy.gods.day01.osiris-renewal',
                'egyptian.week01.day02.ra-order',
                'egyptian.week01.day03.isis-restoration',
                'egyptian.week01.day05.thoth-knowledge',
            } else 2
            self.assertEqual(lesson['version'], expected_version, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation')
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            text = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
            self.assertNotIn('starter lesson uses the local scaffold source', text)
            titles[lesson['title']] = text
        self.assertIn('Papyrus of Ani', titles['Osiris: Kingship in a Funerary Hymn'])
        ra = json.loads(next(path for path in files if 'ra-order' in path.name).read_text(encoding='utf-8'))
        self.assertIn('Legend of the Destruction of Mankind', ra['sourceReferences']['complaint']['locator'])
        self.assertIn('secret name', titles['Isis and Ra’s Secret Name'])
        self.assertIn('Chapter 125', titles['Judgment of the Dead'])
        self.assertIn('Papyrus of Hunefer', titles['Thoth: Writing and Sacred Speech'])
        osiris = json.loads(next(path for path in files if 'osiris-renewal' in path.name).read_text(encoding='utf-8'))
        self.assertIn('Horus is established on thy throne', osiris['sourceReferences']['ani']['excerpt'])
        self.assertIn('let thine Eye go against', ra['sourceReferences']['eye']['excerpt'])
        self.assertIn('and she gave no further attention to men and women.', ra['sourceReferences']['beer']['excerpt'])
        judgment = json.loads(next(path for path in files if 'judgment-dead' in path.name).read_text(encoding='utf-8'))
        self.assertIn('I have not lied.', judgment['sourceReferences']['confession']['excerpt'])
        thoth = json.loads(next(path for path in files if 'thoth-knowledge' in path.name).read_text(encoding='utf-8'))
        self.assertIn('Budge', thoth['sourceReferences']['budge']['note'])
        self.assertIn('what I abominate is sin.', thoth['sourceReferences']['hunefer']['excerpt'])

    def test_japanese_starter_pack_distinguishes_retellings_and_folktale(self):
        files = sorted((ROOT / 'content/lessons/japanese').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation')
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('Onogoro', titles['Izanagi and Izanami'])
        self.assertIn('Heavenly Rock Dwelling', titles['Amaterasu: Light and Withdrawal'])
        self.assertIn('flayed with a backward flaying', titles['Susanoo: Disruption and Consequence'])
        self.assertIn('folktale', titles['Urashima Taro: A Return Across Time'])
        self.assertIn('Land of Gloom', titles['Izanami: Death and Separation'])
        urashima = next(path for path in files if 'kami-boundaries' in path.name)
        lesson = json.loads(urashima.read_text(encoding='utf-8'))
        self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-4018'})

    def test_slavic_starter_pack_uses_named_ralston_passages(self):
        files = sorted((ROOT / 'content/lessons/slavic').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-22373'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation')
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            combined = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
            self.assertNotIn('starter lesson uses the local scaffold source', combined)
            titles[lesson['title']] = combined
        self.assertIn('Vasilissa the Fair', titles['Baba Yaga in Vasilissa the Fair'])
        self.assertIn('egg', titles['Koschei: Hidden Death'])
        self.assertIn('doll', titles['Vasilissa: Courage and Tasks'])
        self.assertIn('crystal bridge', titles['The Water King: Bargains and Impossible Tasks'])
        self.assertIn('chapbook', titles['The Firebird: A Chapbook Quest'])

    def test_ovid_plain_text_parser_separates_poem_from_editorial_apparatus(self):
        books_1_7 = ROOT / 'content/corpus/roman/primary/ovid-metamorphoses-books-1-7-21765.txt'
        books_8_15 = ROOT / 'content/corpus/roman/primary/ovid-metamorphoses-books-8-15-26073.txt'
        roman_manifest = json.loads((ROOT / 'content/corpus/roman/manifest.json').read_text(encoding='utf-8'))
        first_volume = next(item for item in roman_manifest['records'] if item['id'] == 'roman-pg-21765')
        self.assertEqual(first_volume['sourceType'], 'primary-text-translation')
        segments = source_segments(books_1_7)
        proem = next(s for s in segments if s['locator'] == 'Book I · Proem [I.1-4]')
        self.assertEqual(proem['evidenceType'], 'source-text')
        self.assertIn('My design leads me to speak of forms changed into new bodies.', proem['text'])
        lycaon = next(s for s in segments if s['locator'].startswith('Book I · Fable VII'))
        self.assertIn('he becomes a wolf', lycaon['text'])
        self.assertFalse(any('EXPLANATION.' in s['text'] for s in segments if s['evidenceType'] == 'source-text'))
        self.assertTrue(any('God reduces Chaos into order' in s['text'] and s['evidenceType'] == 'editorial-note' for s in segments))
        fake_summary = {
            'evidenceType': 'quotation',
            'excerpt': 'God reduces Chaos into order.',
            'localPath': 'content/corpus/roman/primary/ovid-metamorphoses-books-1-7-21765.txt',
            'locator': 'Book I synopsis',
        }
        self.assertTrue(check_reference(fake_summary, ROOT))
        roman_segments = source_segments(books_8_15)
        mars = next(s for s in roman_segments if s['locator'].startswith('Book XIV · Fable XII') and s['evidenceType'] == 'source-text')
        self.assertIn('Mavors', mars['text'])
        caesar = next(s for s in roman_segments if s['locator'].startswith('Book XV · Fable VIII') and s['evidenceType'] == 'source-text')
        self.assertIn('snatched the soul', caesar['text'])

    def test_roman_lessons_cite_ovid_verse_not_rileys_synopses(self):
        files = sorted((ROOT / 'content/lessons/roman').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertIn('Book ', ref['locator'], lesson['id'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('Daphne', titles['Ovid: Change as Story'])
        self.assertIn('wolf', titles['Jupiter and Lycaon: Judgment and Change'])
        self.assertIn('Adonis', titles['Venus and Adonis: Warning and Loss'])
        self.assertIn('Quirinus', titles['Mars, Romulus, and Roman Foundation'])
        self.assertIn('star', titles['Ovid, Caesar, and Poetic Apotheosis'])

    def test_mesopotamian_lessons_cite_named_fragmentary_tablet_passages(self):
        files = sorted((ROOT / 'content/lessons/mesopotamian').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertTrue(any(name in ref['locator'] for name in ['Tablet', 'tablet']), ref['locator'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('dream', titles["Gilgamesh's Dream of a Companion"].lower())
        self.assertIn('shepherds', titles['Enkidu: From the Herd to Erech'])
        self.assertIn('wrestle', titles['Gilgamesh and Enkidu: The First Contest'])
        self.assertIn('Huwawa', titles["The Cedar Forest: Huwawa's Terror"])
        self.assertIn('fragmentary', titles['Gilgamesh: Reading Across Fragments'].lower())
        self.assertNotIn('universal flood', ' '.join(titles.values()).lower())

    def test_mesopotamian_parser_separates_tablet_verse_and_editorial_apparatus(self):
        clay = ROOT / 'content/corpus/mesopotamian/primary/gilgamesh-clay-jastrow-11000.txt'
        langdon = ROOT / 'content/corpus/mesopotamian/primary/gilgamish-langdon-18897.txt'
        clay_segments = source_segments(clay)
        dream = next(s for s in clay_segments if s['locator'] == 'Pennsylvania Tablet · Column I')
        self.assertEqual(dream['evidenceType'], 'source-text')
        self.assertIn('I loved him as a woman', dream['text'])
        yale = next(s for s in clay_segments if s['locator'] == 'Yale Tablet · Column IV')
        self.assertIn('seven-fold terror', yale['text'])
        apparatus = next(s for s in clay_segments if s['locator'].endswith('editorial apparatus'))
        self.assertEqual(apparatus['evidenceType'], 'editorial-note')
        self.assertIn('INTRODUCTION', apparatus['text'])
        self.assertFalse(any('COMMENTARY ON THE PENNSYLVANIA TABLET' in s['text'] for s in clay_segments if s['evidenceType'] == 'source-text'))
        langdon_segments = source_segments(langdon)
        struggle = next(s for s in langdon_segments if s['locator'] == 'Langdon edition · Column III · fragment 2')
        self.assertIn('They grappled with each other', struggle['text'])
        self.assertFalse(any('INTRODUCTION' in s['text'] for s in langdon_segments if s['evidenceType'] == 'source-text'))

    def test_chinese_starter_pack_names_its_modern_compilations(self):
        files = sorted((ROOT / 'content/lessons/chinese').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 5, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertIn('normalized characters', ref['locator'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('Taoist', titles["P'an Ku: A Taoist Creation Account"])
        self.assertIn('Ssu-ma Cheng', titles['Nue Kua: Repairing the Heavens'])
        self.assertIn('Werner', titles['Shen I: The Nine False Suns'])
        self.assertIn('Heng O', titles['Heng O: Flight to the Moon'])
        self.assertIn('Macgowan', titles['A Benevolent Life and the Coming Flood'])
        self.assertNotIn('Yu: Taming the Flood', titles)

    def test_chinese_manifest_distinguishes_synthesis_from_folklore_collection(self):
        manifest = json.loads((ROOT / 'content/corpus/chinese/manifest.json').read_text(encoding='utf-8'))
        werner = next(item for item in manifest['records'] if item['id'] == 'pg-15250')
        macgowan = next(item for item in manifest['records'] if item['id'] == 'pg-26070')
        self.assertEqual(werner['sourceType'], 'secondary-synthesis')
        self.assertIn('not a primary-source translation', werner['notes'])
        self.assertEqual(macgowan['sourceType'], 'folklore-retelling-collection')

    def test_chinese_parser_keeps_named_chapters_and_tales_separate(self):
        werner_path = ROOT / 'content/corpus/chinese/primary/myths-legends-china-werner-15250.txt'
        macgowan_path = ROOT / 'content/corpus/chinese/primary/chinese-folk-lore-tales-macgowan-26070.txt'
        werner_segments = source_segments(werner_path)
        creation = next(s for s in werner_segments if s['locator'].startswith('Chapter III'))
        self.assertIn('His task occupied eighteen thousand years', creation['text'])
        self.assertTrue(any(s['evidenceType'] == 'editorial-note' and 'Werner edition · notes' == s['locator'] for s in werner_segments))
        folklore = source_segments(macgowan_path)
        reward = next(s for s in folklore if s['locator'] == 'THE REWARD OF A BENEVOLENT LIFE')
        self.assertIn('Before very long a great flood will take place', reward['text'])
        front_matter = next(s for s in folklore if s['locator'] == 'Macgowan edition · front matter and contents')
        self.assertEqual(front_matter['evidenceType'], 'editorial-note')
        self.assertFalse(any(s['locator'] == 'CONTENTS' and s['evidenceType'] == 'source-text' for s in folklore))

    def test_indian_epic_lessons_use_named_books_and_sections(self):
        files = sorted((ROOT / 'content/lessons/indian').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 4, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertIn('normalized characters', ref['locator'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('peace', titles["Krishna's Counsel: Peace Before War"].lower())
        self.assertIn('fourteen years', titles['Rama: Accepting the Exile'].lower())
        self.assertIn('Sita', titles['Sita: Choosing the Forest'])
        self.assertIn('Draupadi', titles['The Dice Game: Draupadi Questions the Wager'])
        self.assertIn('sandals', titles["Bharata: Governing in Rama's Name"])
        self.assertNotIn('Bhagavad Gita', ' '.join(titles.values()))

    def test_indian_parser_separates_preface_and_scopes_epic_units(self):
        mahabharata = source_segments(ROOT / 'content/corpus/indian/primary/mahabharata-dutt-19630.txt')
        dice = next(s for s in mahabharata if s['locator'] == 'Book IV · DYUTA')
        self.assertIn('Doth a crowned king and husband stake his wife', dice['text'])
        krishna = next(s for s in mahabharata if s['locator'] == 'Book VII · UDYOGA')
        self.assertIn('Seek not war and death of kinsmen', krishna['text'])
        self.assertTrue(any(s['locator'] == 'Dutt edition · preface and introduction' and s['evidenceType'] == 'editorial-note' for s in mahabharata))
        self.assertFalse(any("TRANSLATOR'S EPILOGUE" in s['text'] for s in mahabharata if s['evidenceType'] == 'source-text'))
        ramayana = source_segments(ROOT / 'content/corpus/indian/primary/ramayana-vol1-dutt-57265.txt')
        sita = next(s for s in ramayana if s['locator'] == 'Ayodhyakandam · Section XXVII')
        self.assertIn('I shall go before thee', sita['text'])
        sandals = next(s for s in ramayana if s['locator'] == 'Ayodhyakandam · Section CXII')
        self.assertIn('made over the task of government unto thy sandals', sandals['text'])
        self.assertFalse(any('THE RAMAYANA IN AN ENGLISH GARB' in s['text'] for s in ramayana if s['evidenceType'] == 'source-text'))

    def test_finnish_starter_pack_uses_named_kalevala_runos(self):
        files = sorted((ROOT / 'content/lessons/finnish').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-5186'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertIn('Rune ', ref['locator'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('seven hundred years', titles['Väinämöinen: Birth and Song'].lower())
        self.assertIn('flour, salt, and money', titles['The Sampo: A Threefold Mill'])
        self.assertIn('lifeless', titles['Ilmarinen: The Bride of Gold'])
        self.assertIn('Pohjola', titles['Louhi: The Sun and Moon Hidden'])
        self.assertIn('cheat-cake', titles['Kullervo: The Cheat-Cake'].lower())

    def test_kalevala_parser_excludes_front_matter_from_runo_evidence(self):
        full = source_segments(ROOT / 'content/corpus/finnish/primary/kalevala-crawford-5186.txt')
        runo = next(s for s in full if s['locator'] == 'Rune X · Ilmarinen forges the Sampo')
        self.assertEqual(runo['evidenceType'], 'source-text')
        self.assertIn('On one side the flour is grinding', runo['text'])
        self.assertTrue(any(s['locator'] == 'Crawford edition · front matter and contents' and s['evidenceType'] == 'editorial-note' for s in full))
        self.assertFalse(any('Contents' in s['text'] for s in full if s['evidenceType'] == 'source-text'))
        volume_one = json.loads((ROOT / 'content/corpus/finnish/manifest.json').read_text(encoding='utf-8'))
        self.assertIn('not an independent witness', next(item for item in volume_one['records'] if item['id'] == 'pg-5184')['notes'])

    def test_mesoamerican_starter_pack_keeps_regional_source_scope(self):
        files = sorted((ROOT / 'content/lessons/mesoamerican').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 4, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-53080'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertIn('Chapter ', ref['locator'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('Nanahuatl', titles["Nanahuatl: The Sun's Birth"])
        self.assertIn('Toltec', titles['Quetzalcoatl: Departure from Tollan'])
        self.assertIn('Coatepec', titles['Huitzilopochtli: Birth and Battle'])
        self.assertIn('Mictlan', titles['Mictlan: A Journey after Death'])
        self.assertIn('Nahua', titles['The Mexica Foundation Omen'])
        self.assertNotIn('all Mesoamerican', ' '.join(titles.values()).lower())

    def test_spence_parser_scopes_mexican_maya_and_peruvian_chapters(self):
        path = ROOT / 'content/corpus/mesoamerican/primary/myths-mexico-peru-spence-53080.txt'
        segments = source_segments(path)
        mexica = next(s for s in segments if s['locator'] == 'Chapter II · MEXICAN MYTHOLOGY')
        self.assertIn('the Centzonuitznaua', mexica['text'])
        migration = next(s for s in segments if s['locator'] == 'Chapter I · THE CIVILISATION OF MEXICO')
        self.assertIn('eagle of great size and majesty', migration['text'])
        maya = next(s for s in segments if s['locator'] == 'Chapter V · MYTHS OF THE MAYA')
        self.assertNotIn('eagle of great size and majesty', maya['text'])
        editorial = next(s for s in segments if s['locator'] == 'Spence edition · front matter and contents')
        self.assertEqual(editorial['evidenceType'], 'editorial-note')

    def test_maya_starter_pack_labels_spences_popol_vuh_summary(self):
        files = sorted((ROOT / 'content/lessons/maya').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-56550'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
                self.assertIn('Spence summary', ref['locator'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('wooden', titles['Wooden People and the Flood'].lower())
        self.assertIn('Vukub-Cakix', titles['Vukub-Cakix and the Hero Twins'])
        self.assertIn('Xibalba', titles['The Hero Twins Receive a Call from Xibalba'])
        self.assertIn('House of Bats', titles["Xibalba's Houses of Ordeal"])
        self.assertIn('Spence', titles["The Twins' Death and Return"])
        record = next(item for item in json.loads((ROOT / 'content/corpus/maya/manifest.json').read_text(encoding='utf-8'))['records'] if item['id'] == 'pg-56550')
        self.assertEqual(record['sourceType'], 'secondary-synthesis')
        self.assertIn('not a direct translation', record['notes'])

    def test_popol_vuh_spence_parser_separates_story_summaries_and_commentary(self):
        segments = source_segments(ROOT / 'content/corpus/maya/primary/popol-vuh-56550.txt')
        first_book = next(s for s in segments if s['locator'] == 'Spence summary · First Book')
        self.assertIn('mannikins carved out of wood', first_book['text'])
        second_book = next(s for s in segments if s['locator'] == 'Spence summary · Second Book')
        self.assertIn('Hun-Came and Vukub-Came', second_book['text'])
        commentary = next(s for s in segments if s['locator'] == 'Spence commentary · Cosmogony')
        self.assertEqual(commentary['evidenceType'], 'editorial-note')
        self.assertTrue(any(s['locator'] == 'Spence edition · preface and source history' and s['evidenceType'] == 'editorial-note' for s in segments))

    def test_yoruba_pack_stays_planned_until_community_specific_sources_exist(self):
        registry = json.loads((ROOT / 'content/pantheons.json').read_text(encoding='utf-8'))
        self.assertEqual(registry['pantheons']['yoruba']['status'], 'planned')
        gates = json.loads((ROOT / 'content/curriculum/programme-gates.json').read_text(encoding='utf-8'))
        self.assertNotIn('arc.yoruba-traditions', gates)
        self.assertEqual(gates['arc.akan-traditions']['prerequisiteArcIds'], ['arc.origins-across-pantheons'])
        manifest = json.loads((ROOT / 'content/corpus/yoruba/manifest.json').read_text(encoding='utf-8'))
        nassau = next(item for item in manifest['records'] if item['id'] == 'pg-38038')
        dayrell = next(item for item in manifest['records'] if item['id'] == 'pg-34655')
        self.assertEqual(nassau['sourceType'], 'colonial-era-ethnographic-synthesis')
        self.assertIn('not a Yoruba community source', nassau['notes'])
        self.assertEqual(dayrell['sourceType'], 'folklore-retelling-collection')
        self.assertIn('do not label its tales Yoruba', dayrell['notes'])

    def test_polynesian_starter_pack_keeps_maui_versions_island_labeled(self):
        files = sorted((ROOT / 'content/lessons/polynesian').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-32601'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertTrue(ref['locator'].startswith('Chapter '), ref['locator'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('Hawaii', titles["Maui's Family Across Island Accounts"])
        self.assertIn('Kualii', titles['Hawaiian Maui and the Fishing Hook'])
        self.assertIn('Samoan', titles['Maui: The Sun-Snaring Variant'])
        self.assertIn('Kaupo', titles['Hawaiian Maui: Finding Fire'])
        self.assertIn('New Zealand', titles['Hina: A Hawaiian Ascent to the Moon'])
        manifest = json.loads((ROOT / 'content/corpus/polynesian/manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(next(x for x in manifest['records'] if x['id'] == 'pg-32601')['sourceType'], 'secondary-synthesis')

    def test_maui_parser_scopes_numbered_westervelt_chapters(self):
        segments = source_segments(ROOT / 'content/corpus/polynesian/primary/legends-ma-ui-westervelt-32601.txt')
        fishing = next(s for s in segments if s['locator'] == 'Chapter II · MAUI THE FISHERMAN')
        self.assertIn('Chant of Kualii', fishing['text'])
        sun = next(s for s in segments if s['locator'] == 'Chapter IV · MAUI SNARING THE SUN.')
        self.assertIn('The Samoans tell the same story', sun['text'])
        moon = next(s for s in segments if s['locator'] == 'Chapter XV · HINA, THE WOMAN IN THE MOON.')
        self.assertIn('The New Zealand legend says', moon['text'])
        self.assertTrue(any(s['locator'] == 'Westervelt edition · front matter and contents' and s['evidenceType'] == 'editorial-note' for s in segments))

    def test_akan_gold_coast_stories_keep_fanti_and_collection_boundaries(self):
        files = sorted((ROOT / 'content/lessons/akan').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 3, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-66923'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertTrue(ref['locator'].startswith('Story '), ref['locator'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('Fanti-land', titles['Anansi and the Pot of Wisdom'])
        self.assertIn('Nyankupon', titles['How Anansi Earned the Name Spider Tales'])
        self.assertIn('Nothing', titles['Anansi and Nothing: A Gold Coast Story'])
        self.assertIn('Thunder', titles['Thunder and Anansi: The Gifted Stick'])
        self.assertIn('drowned', titles['Anansi the Blind Fisherman'].lower())
        manifest = json.loads((ROOT / 'content/corpus/akan/manifest.json').read_text(encoding='utf-8'))
        gold_coast = next(item for item in manifest['records'] if item['id'] == 'pg-66923')
        jamaica = next(item for item in manifest['records'] if item['id'] == 'pg-72735')
        self.assertEqual(gold_coast['sourceType'], 'regional-folklore-collection')
        self.assertIn('individual story provenance varies', gold_coast['notes'])
        self.assertIn('not direct evidence for Akan practice', jamaica['notes'])

    def test_gold_coast_folktale_parser_excludes_front_matter(self):
        segments = source_segments(ROOT / 'content/corpus/akan/primary/west-african-folk-tales-66923.txt')
        wisdom = next(s for s in segments if s['locator'] == 'Story II · HOW WISDOM BECAME THE PROPERTY OF THE HUMAN RACE')
        self.assertIn('in Fanti-land', wisdom['text'])
        self.assertEqual(wisdom['evidenceType'], 'source-text')
        front = next(s for s in segments if s['locator'] == 'Barker and Sinclair edition · introduction and contents')
        self.assertEqual(front['evidenceType'], 'editorial-note')
        self.assertIn('Gold Coast peoples', front['text'])

    def test_inuit_starter_pack_is_scoped_to_rasmussens_greenland_collection(self):
        files = sorted((ROOT / 'content/lessons/inuit').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-28932'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('willow bushes', titles['The Coming of Men'].lower())
        self.assertIn('bear', titles['The Woman and Her Bear Foster-Son'].lower())
        self.assertIn('underworld', titles['Kúnigseq Visits the Land of Shades'].lower())
        self.assertIn('raven', titles['The Raven and the Goose'].lower())
        self.assertIn('star', titles['The Man Who Became a Star'].lower())
        bayliss = next(item for item in json.loads((ROOT / 'content/corpus/inuit/manifest.json').read_text(encoding='utf-8'))['records'] if item['id'] == 'pg-24569')
        self.assertIn('Central Inuit and Bering Strait', bayliss['notes'])

    def test_rasmussen_parser_labels_greenland_stories_and_excludes_intro(self):
        segments = source_segments(ROOT / 'content/corpus/inuit/primary/eskimo-folk-tales-28932.txt')
        origin = next(s for s in segments if s['locator'] == 'The Coming Of Men, A Long, Long While Ago')
        self.assertIn('little children came out of the earth', origin['text'].lower())
        raven = next(s for s in segments if s['locator'] == 'The Raven And The Goose')
        self.assertIn('simply splashed it black all over', raven['text'])
        intro = next(s for s in segments if s['locator'] == 'Rasmussen edition · introduction and contents')
        self.assertEqual(intro['evidenceType'], 'editorial-note')
        self.assertIn('various parts of Greenland', intro['text'])

    def test_homer_parser_excludes_editorial_book_synopses(self):
        iliad = source_segments(ROOT / 'content/corpus/greek/primary/homer-iliad-2199.txt')
        iliad_summary = next(s for s in iliad if s['locator'] == 'Book 1 · editorial summary')
        iliad_text = next(s for s in iliad if s['locator'] == 'Book 1')
        self.assertIn('The quarrel between Agamemnon and Achilles', iliad_summary['text'])
        self.assertEqual(iliad_summary['evidenceType'], 'editorial-note')
        self.assertTrue(iliad_text['text'].startswith('Sing, O goddess'))

        odyssey = source_segments(ROOT / 'content/corpus/greek/primary/homer-odyssey-1727.txt')
        odyssey_heading = next(s for s in odyssey if s['locator'] == 'Book 1 · editorial heading')
        odyssey_text = next(s for s in odyssey if s['locator'] == 'Book 1')
        self.assertIn('THE GODS IN COUNCIL', odyssey_heading['text'])
        self.assertTrue(odyssey_text['text'].startswith('Tell me, O Muse'))
        self.assertNotIn('TELEMACHUS TO THE SUITORS', odyssey_text['text'][:80])

    def test_baltic_sampler_is_explicitly_one_lithuanian_labeled_retelling(self):
        files = sorted((ROOT / 'content/lessons/baltic').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-66919'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertIn('Pyle retelling', ref['locator'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('stepsister', titles['The Exiled Princes'])
        self.assertIn('bear', titles['The Animals Become Helpers'].lower())
        self.assertIn('milk', titles["Three Roads and a Tree's Warning"])
        self.assertIn('dragon', titles['The Dragon and the Youngest Prince'].lower())
        self.assertIn('Pyle', titles['Betrayal, Healing, and Return'])
        manifest = json.loads((ROOT / 'content/corpus/baltic/manifest.json').read_text(encoding='utf-8'))
        pyle = next(item for item in manifest['records'] if item['id'] == 'pg-66919')
        lang = next(item for item in manifest['records'] if item['id'] == 'pg-6746')
        self.assertEqual(pyle['sourceType'], 'modern-folktale-retelling')
        self.assertIn('no underlying source text or oral informant', pyle['notes'])
        self.assertEqual(lang['sourceType'], 'multiregional-fairy-tale-anthology')

    def test_pyle_parser_scopes_the_named_lithuanian_tale(self):
        segments = source_segments(ROOT / 'content/corpus/baltic/primary/fairy-tales-far-near-66919.txt')
        story = next(s for s in segments if s['locator'] == 'Pyle retelling · The Princes And The Friendly Animals')
        self.assertEqual(story['evidenceType'], 'source-text')
        self.assertIn('three Princes', story['text'])
        self.assertTrue(any(s['locator'] == 'Pyle edition · front matter and contents' and s['evidenceType'] == 'editorial-note' for s in segments))

    def test_basque_lessons_use_websters_labourd_story_segments(self):
        files = sorted((ROOT / 'content/lessons/basque').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 2, lesson['id'])
            self.assert_editorially_reviewed(lesson)
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-34902'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('ring', titles['The Tartaro and the Talking Ring'].lower())
        self.assertIn('Acheria', titles['Acheria the Fox'])
        self.assertIn('Heren-Suge', titles['The Grateful Tartaro and the Heren-Suge'])
        self.assertIn('Basa-Andre', titles['Basa-Jauna and the Three Brothers'])
        self.assertIn('fairy', titles["The Servant at the Fairy's"].lower())
        record = json.loads((ROOT / 'content/corpus/basque/manifest.json').read_text(encoding='utf-8'))['records'][0]
        self.assertEqual(record['sourceType'], 'field-collected-folklore-translation')
        self.assertIn('chiefly in Labourd', record['notes'])

    def test_webster_parser_separates_basque_tales_from_editorial_sections(self):
        segments = source_segments(ROOT / 'content/corpus/basque/primary/basque-legends-webster-34902.txt')
        tartaro = next(s for s in segments if s['locator'] == 'THE TARTARO.')
        self.assertEqual(tartaro['evidenceType'], 'source-text')
        self.assertIn('Estefanella Hirigarray', tartaro['text'])
        editorial = next(s for s in segments if s['locator'] == 'I.--LEGENDS OF THE TARTARO.')
        self.assertEqual(editorial['evidenceType'], 'editorial-note')
        self.assertTrue(any(s['locator'] == 'Webster edition · introduction and contents' for s in segments))

    def test_cherokee_stories_use_named_mooney_sections(self):
        files = sorted((ROOT / 'content/lessons/cherokee').rglob('*.json'))
        self.assertEqual(len(files), 5)
        titles = {}
        for path in files:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(lesson['version'], 3, lesson['id'])
            self.assertEqual(len(lesson['narrativeBlocks']), 5, lesson['id'])
            self.assertEqual(len(lesson['quiz']), 2, lesson['id'])
            self.assertEqual({ref['recordId'] for ref in lesson['sourceReferences'].values()}, {'pg-45634'})
            for ref in lesson['sourceReferences'].values():
                self.assertEqual(ref.get('evidenceType'), 'quotation', lesson['id'])
                self.assertTrue(ref['locator'].startswith('Myth '), ref['locator'])
                self.assertEqual(check_reference(ref, ROOT), [], lesson['id'])
            titles[lesson['title']] = ' '.join(block['body'] for block in lesson['narrativeBlocks'])
        self.assertIn('Water-beetle', titles['How the World Was Made'])
        self.assertIn('Selu', titles["Kana'ti and Selu: Game and Corn"])
        self.assertIn('Uktena', titles["Agan-Unitsi's Search for the Uktena"])
        self.assertIn('Cherokee Advocate', titles['The Rabbit and the Tar Wolf'])
        self.assertIn('does not validate treatments', titles['Origin of Disease and Medicine'])
        record = json.loads((ROOT / 'content/corpus/cherokee/manifest.json').read_text(encoding='utf-8'))['records'][0]
        self.assertEqual(record['sourceType'], 'ethnographic-folklore-collection')
        self.assertIn('chiefly among Eastern Cherokee', record['notes'])

    def test_mooney_parser_separates_numbered_myths_from_historical_notes(self):
        segments = source_segments(ROOT / 'content/corpus/cherokee/primary/myths-cherokee-mooney-45634.txt')
        world = next(s for s in segments if s['locator'] == 'Myth 1 · HOW THE WORLD WAS MADE')
        self.assertIn('Water-beetle', world['text'])
        uktena = next(s for s in segments if s['locator'].startswith('Myth 50 ·'))
        self.assertIn('The Keen-eyed', uktena['text'])
        intro = next(s for s in segments if s['locator'] == 'Mooney edition · introduction, history, and contents')
        self.assertEqual(intro['evidenceType'], 'editorial-note')
        self.assertIn('Qualla reservation', intro['text'])

    def test_ai_editorial_review_requires_an_explicit_scope_note(self):
        from content_pipeline import check_links
        lesson = json.loads((ROOT / 'content/lessons/greek/heroes-programme/week-02-day-01-the-quarrel-and-the-ransom.json').read_text(encoding='utf-8'))
        lesson['review'] = {
            'status': 'reviewed',
            'reviewedBy': 'Devin (AI editorial review)',
            'reviewedAt': '2026-11-09',
            'reviewType': 'editorial',
            'notes': 'AI editorial review; not independent scholarly review or scholarly certification.',
        }
        errors = []
        check_links(lesson, errors)
        self.assertFalse(any('reviewType' in error or 'review note' in error for error in errors))
        lesson['review']['notes'] = 'Reviewed.'
        errors = []
        check_links(lesson, errors)
        self.assertTrue(any('not scholarly certification' in error for error in errors))

    def test_all_active_lessons_have_audited_status_and_planned_source_gaps_are_flagged(self):
        registry = json.loads((ROOT / 'content/pantheons.json').read_text(encoding='utf-8'))
        statuses = {key: item['status'] for key, item in registry['pantheons'].items()}
        lessons = sorted((ROOT / 'content/lessons').rglob('*.json'))
        self.assertEqual(len(lessons), 135)
        for path in lessons:
            lesson = json.loads(path.read_text(encoding='utf-8'))
            if statuses[lesson['pantheon']] == 'active':
                self.assertEqual(lesson['review']['status'], 'reviewed', lesson['id'])
                self.assertEqual(lesson['review']['reviewType'], 'editorial', lesson['id'])
                self.assertIn('AI editorial review', lesson['review']['notes'], lesson['id'])
            else:
                self.assertEqual(lesson['review']['status'], 'needs-revision', lesson['id'])
                self.assertIn('source', lesson['review']['notes'].lower(), lesson['id'])


if __name__ == '__main__':
    unittest.main()

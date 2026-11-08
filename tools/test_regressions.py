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


if __name__ == '__main__':
    unittest.main()

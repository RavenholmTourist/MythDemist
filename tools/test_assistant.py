import json
import unittest
from unittest.mock import patch
from mythos_assistant import load_index, retrieve, validate, answer, prompt


class AssistantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = load_index()
        cls.chunk = {'id': 'known', 'recordId': 'source', 'text': 'A sufficiently long quotation from a local source.', 'pantheon': 'greek', 'title': 'Local source', 'locator': 'Book 1', 'terms': ['quotation'], 'evidenceType': 'source-text'}

    def test_supported_retrieval(self):
        chunks = retrieve('What does Anansi do?', self.index, tradition='akan')
        self.assertTrue(chunks)
        self.assertTrue(all(c['pantheon'] == 'akan' for c in chunks))
        self.assertTrue(any('anansi' in c['text'].lower() for c in chunks))

    def test_no_matching_passages(self):
        self.assertEqual(retrieve('qwzxvbnmplokjhgfdsa', self.index), [])

    def test_context_and_notes(self):
        other = {**self.chunk, 'id': 'other', 'pantheon': 'norse'}
        note = {**self.chunk, 'id': 'note', 'evidenceType': 'editorial-note'}
        chunks = retrieve('quotation', {'chunks': [self.chunk, other, note]}, tradition='greek')
        self.assertEqual([c['id'] for c in chunks], ['known'])
        self.assertIn('coverageType=', prompt('question', chunks)[1]['content'])

    def test_valid_quotation(self):
        quote = self.chunk['text']
        raw = json.dumps({'answer': quote, 'coverage': 'partial', 'citations': [{'chunkId': 'known', 'claim': quote}]})
        self.assertEqual(validate(raw, [self.chunk])['answer'], quote)

    def test_bad_shapes_and_unaccounted_claims(self):
        quote = self.chunk['text']
        valid = {'answer': quote, 'coverage': 'partial', 'citations': [{'chunkId': 'known', 'claim': quote}]}
        bad = [
            {**valid, 'answer': quote + ' An invented assertion.'},
            {**valid, 'coverage': 'supported'},
            {**valid, 'citations': [{'chunkId': 'invented', 'claim': quote}]},
            {**valid, 'citations': [{'chunkId': 'known', 'claim': 'A claim not present in the local evidence.'}]},
            {**valid, 'citations': []},
            {**valid, 'answer': 5},
            {**valid, 'citations': ['not an object']},
            {**valid, 'coverage': 'not-covered'},
            {**valid, 'extra': True},
        ]
        for value in bad:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate(json.dumps(value), [self.chunk])
        with self.assertRaises(ValueError):
            validate('not json', [self.chunk])

    def test_provider_failure_and_invalid_output_fallback(self):
        with patch('mythos_assistant.retrieve', return_value=[self.chunk]):
            for side_effect, value in [(RuntimeError('private provider detail'), None), (None, '{bad json'), (None, None)]:
                with patch('mythos_assistant.llm_call', side_effect=side_effect, return_value=value):
                    response = answer('question')
                    self.assertEqual(response['mode'], 'retrieval-only')
                    self.assertEqual(response['evidence'], [self.chunk])
                    self.assertNotIn('private provider detail', json.dumps(response))

    def test_model_selection_is_not_semantic_certification(self):
        # Even a verbatim quotation is partial evidence: relevance is not mechanically proven.
        quote = self.chunk['text']
        raw = json.dumps({'answer': quote, 'coverage': 'partial', 'citations': [{'chunkId': 'known', 'claim': quote}]})
        with patch('mythos_assistant.retrieve', return_value=[self.chunk]), patch('mythos_assistant.llm_call', return_value=raw):
            response = answer('question')
        self.assertEqual(response['mode'], 'generated')
        self.assertEqual(response['coverage'], 'partial')


if __name__ == '__main__':
    unittest.main()

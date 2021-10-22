import unittest

from app.similarity_scorer import SimilarityScorer


class TestSimilarityScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = SimilarityScorer()
        self.sentences = [
            "Einen Brief quer durch die USA schicken – in nur 10 Tagen!",
            "Eine revolutionäre Entwicklung, dauerte der Postversand um 1850 \
doch ein bis zwei Monate.",
            "Möglich machte es der sogenannte Pony-Express.",
            "Am 3. April 1860 begann eine Stafette furchtloser junger Männer, \
Briefe entlang der mehr als 3000 km langen Strecke zwischen Kalifornien und \
Missouri zuzustellen – hoch zu Ross, den widrigen Wetterverhältnissen und \
feindlichen Überfällen trotzend.",
            "Allem Pioniergeist zum Trotz schienen die Gründer jedoch aufs \
falsche Pferd gesetzt zu haben.",
            "Denn bereits 18 Monate später wurde der Pony-Express eingestellt.",
            "Zwei Tage, nachdem das erste transkontinentale Telegramm per \
Telegraf verschickt wurde."
            "",
        ]

    def test_score_for_same_sentence(self):
        test_sentences = {"a": self.sentences[1], "b": self.sentences[1]}
        result = self.scorer.compute_similarity_matrix(test_sentences)["matrix"][0][1]
        self.assertAlmostEqual(result, 1.0, places=5)

    def test_score_for_different_sentences(self):
        test_sentences = {
            "a": self.sentences[0],
            "b": self.sentences[1],
        }
        result = self.scorer.compute_similarity_matrix(test_sentences)["matrix"][0][1]
        self.assertLessEqual(result, 0.5)

    def test_id_extraction(self):
        test_sentences = {
            i: sent for i in range(len(self.sentences)) for sent in self.sentences
        }
        result = self.scorer.compute_similarity_matrix(test_sentences)["ids"]
        expected = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(result, expected)

    def test_empty_query(self):
        query = {}
        result = self.scorer.compute_similarity_matrix(query)
        expected = {"ids": [], "matrix": [[0.0]]}
        self.assertEqual(result, expected)

    def test_query_only_one_sentence(self):
        query = {"a": self.sentences[2]}
        result = self.scorer.compute_similarity_matrix(query)["matrix"][0][0]
        self.assertAlmostEqual(result, 1, places=5)

    def test_multiple_sentences(self):
        test_sentences = self.sentences * 3
        query = {i: sent for i in range(len(test_sentences)) for sent in test_sentences}
        result = self.scorer.compute_similarity_matrix(query)["matrix"][0][
            len(self.sentences)
        ]
        self.assertAlmostEqual(result, 1, places=5)

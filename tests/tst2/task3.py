import string
import unittest

from test2.task3 import count_sentences, WordsRanker, WordFrequency


class CountSentencesTestCase(unittest.TestCase):
    def test_empty_text_should_have_0_sentences(self):
        self.assertEqual(0, count_sentences(""))

    def test_text_with_1_sentence_should_have_1_sentence(self):
        self.assertEqual(1, count_sentences("Sentence."))

    def test_text_with_1_sentence_with_ellipsis_should_have_1_sentence(self):
        self.assertEqual(1, count_sentences("Sentence..."))

    def test_text_with_weird_characters_with_2_sentences_should_have_2_sentences(self):
        self.assertEqual(2, count_sentences("This costs 20$. It's not free."))

    def test_should_see_sentence_that_ends_with_question(self):
        self.assertEqual(1, count_sentences("Yeah?"))

    def test_should_see_sentence_that_ends_with_several_question(self):
        self.assertEqual(1, count_sentences("Yeah???"))

    def test_should_see_sentence_that_ends_with_exclamation(self):
        self.assertEqual(1, count_sentences("Yeah!"))

    def test_should_see_sentence_that_ends_with_several_exclamations(self):
        self.assertEqual(1, count_sentences("Yeah!!!"))

    def test_should_see_sentence_that_ends_with_question_and_exclamation(self):
        self.assertEqual(1, count_sentences("Yeah?!"))

    def test_should_see_sentence_that_ends_with_exclamation_and_question(self):
        self.assertEqual(1, count_sentences("Yeah!?"))

    def test_auto_generated_text_should_have_100_sentences(self):
        text = ""
        for i in range(20):
            text += "Sentence."
        self.assertEqual(20, count_sentences(text))

    def test_example_text_should_have_16_sentences(self):
        with open("../../test2/text.txt") as file:
            text = file.read()
            self.assertEqual(16, count_sentences(text))


class WordRankerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ranker = WordsRanker(10)

    def test_one_letter_should_receive_freq_1(self):
        ranks = self.ranker.rank_words("a")
        self.assertEqual([WordFrequency("a", 1)], ranks)

    def test_works_with_punctuation(self):
        ranks = self.ranker.rank_words("a. b a!? a.")
        self.assertEqual([WordFrequency("a", 3), WordFrequency("b", 1)], ranks)

    def test_one_twice_letter_should_receive_freq_2(self):
        ranks = self.ranker.rank_words("a a")
        self.assertEqual([WordFrequency("a", 2)], ranks)

    def test_one_100_times_letter_should_receive_freq_100(self):
        ranks = self.ranker.rank_words("a " * 100)
        self.assertEqual([WordFrequency("a", 100)], ranks)

    def test_should_work_for_russian_words(self):
        ranks = self.ranker.rank_words("слово " * 50 + "letter")
        self.assertEqual([WordFrequency("слово", 50), WordFrequency("letter", 1)], ranks)

    def test_should_find_subwords(self):
        ranks = self.ranker.rank_words("apply kotlin$Plugin_latest")
        self.assertEqual(
            [
                WordFrequency("apply", 1),
                WordFrequency("kotlin", 1),
                WordFrequency("plugin", 1),
                WordFrequency("latest", 1),
            ],
            ranks,
        )

    def test_the_most_common_word_should_be_the_first(self):
        text = "word слово letter " * 100 + "слово"
        ranks = self.ranker.rank_words(text)
        self.assertEqual(WordFrequency("слово", 101), ranks[0])

    def test_should_only_output_10_words(self):
        text = " ".join(string.ascii_letters)
        ranks = self.ranker.rank_words(text)
        self.assertEqual(10, len(ranks))

    def test_treat_uppercase_and_lowercase_the_same(self):
        ranks = self.ranker.rank_words("word wOrD")
        self.assertEqual([WordFrequency("word", 2)], ranks)

    def test_treat_uppercase_and_lowercase_the_same_big(self):
        letters = string.ascii_letters[:10]
        text = (" ".join(letters) + " ") * 100 + (" ".join(letters).upper() + " ") * 100
        expected_ranks = set([WordFrequency(letter, 200) for letter in letters])
        ranks = self.ranker.rank_words(text)
        self.assertEqual(expected_ranks, set(ranks))


if __name__ == "__main__":
    unittest.main()

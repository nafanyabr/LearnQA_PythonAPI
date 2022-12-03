import pytest

class TestPhraseLength:
    def test_check_phrase_len(self):
        phrase = input("Set a phrase less than 15 symbols length: ")
        assert len(phrase) < 15, 'Phrase gte 15 symbols!'

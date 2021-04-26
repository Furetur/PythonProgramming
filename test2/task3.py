import re
from collections import Counter
from dataclasses import dataclass
from typing import List

letter_pattern = "[а-яА-Яa-zA-Z]"
word_pattern = re.compile(f"{letter_pattern}+")
sentence_pattern = re.compile("[^!\.\?]+[!\.\?]+")


def count_sentences(text: str) -> int:
    return len(sentence_pattern.findall(text))


@dataclass(frozen=True)
class WordFrequency:
    word_pattern: str
    frequency: int


class WordsRanker:
    def __init__(self, top_size):
        self.top_size = top_size

    def rank_words(self, text) -> List[WordFrequency]:
        counter: "Counter" = Counter()
        for match in word_pattern.findall(text):
            counter[match.lower()] += 1
        return [WordFrequency(word, freq) for word, freq in counter.most_common(self.top_size)]


if __name__ == "__main__":
    with open("text.txt") as file:
        text = file.read()
        ranker = WordsRanker(10)
        print("Top words:")
        for word_freq in ranker.rank_words(text):
            print(f"{word_freq} --> {word_freq.frequency} times.")

        print(f"There are {count_sentences(text)} sentences in the text.")

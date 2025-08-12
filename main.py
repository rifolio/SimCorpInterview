import re
import argparse
from collections import Counter
from typing import Counter as CounterType, Iterable


class WordFrequencyCounter:
    WORD_REGEX = re.compile(r"\b[\w']+\b", flags=re.UNICODE)

    def __init__(self, case_sensitive: bool = False) -> None:
        self.case_sensitive = case_sensitive

    def tokenize(self, text: str) -> Iterable[str]:
        for token in self.WORD_REGEX.findall(text):
            yield token if self.case_sensitive else token.lower()

    def tokenize_stream(self, stream: Iterable[str]) -> Iterable[str]:
        for line in stream:
            for token in self.WORD_REGEX.findall(line):
                yield token if self.case_sensitive else token.lower()

    def count_from_file(self, file_path: str) -> CounterType[str]:
        with open(file_path, "r", encoding="utf-8") as file_obj:
            text = file_obj.read()
        return Counter(self.tokenize(text))

    def count_from_large_file(self, file_path: str) -> CounterType[str]:
        with open(file_path, "r", encoding="utf-8") as file_obj:
            return Counter(self.tokenize_stream(file_obj))

    @staticmethod
    def _bucket_top_k(counter: CounterType[str], k: int | None) -> list[tuple[str, int]]:
        if not counter:
            return []
        max_freq = max(counter.values())
        buckets: list[list[str]] = [[] for _ in range(max_freq + 1)]
        for word, freq in counter.items():
            buckets[freq].append(word)

        result: list[tuple[str, int]] = []
        remaining = k if k is not None and k > 0 else None
        for freq in range(max_freq, 0, -1):
            if not buckets[freq]:
                continue
            for word in buckets[freq]:
                result.append((word, freq))
                if remaining is not None:
                    remaining -= 1
                    if remaining == 0:
                        return result
        return result

    def top_from_file(self, file_path: str, k: int | None = None, large: bool = False) -> list[tuple[str, int]]:
        counter = self.count_from_large_file(file_path) if large else self.count_from_file(file_path)
        return self._bucket_top_k(counter, k)

    def top_pythonic(self, file_path: str, k: int) -> list[tuple[str, int]]:
        counter = self.count_from_file(file_path)
        return counter.most_common(k)


def top_words_from_file(file_path: str, k: int | None = None, case_sensitive: bool = False) -> list[tuple[str, int]]:
    return WordFrequencyCounter(case_sensitive=case_sensitive).top_from_file(file_path, k=k, large=False)


def top_words_from_large_file(file_path: str, k: int | None = None, case_sensitive: bool = False) -> list[tuple[str, int]]:
    return WordFrequencyCounter(case_sensitive=case_sensitive).top_from_file(file_path, k=k, large=True)


def top_words_pythonic(file_path: str, k: int, case_sensitive: bool = False) -> list[tuple[str, int]]:
    return WordFrequencyCounter(case_sensitive=case_sensitive).top_pythonic(file_path, k)
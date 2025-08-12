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



def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Path to text file to analyze")
    parser.add_argument("--k", type=int, default=None, help="top-k words or <=0 to return all")
    parser.add_argument("--case-sensitive", action="store_true", help="default to case-insensitive")
    parser.add_argument("--large", action="store_true", help="line-by-line for large inputs, non memory leak")
    parser.add_argument(
        "--method",
        choices=["bucket", "pythonic"],
        default="bucket",
        help="bucket-based O(n) selection or super pythonic Counter.most_common, almost like cheating XD",
    )
    parser.add_argument("--print-limit", type=int, default=None, help="n results to print")

    args = parser.parse_args()

    counter = None
    wf = WordFrequencyCounter(case_sensitive=args.case_sensitive)

    if args.method == "bucket":
        results = wf.top_from_file(args.file, k=args.k, large=args.large)
        if args.stats:
            counter = wf.count_from_large_file(args.file) if args.large else wf.count_from_file(args.file)
    else:
        counter = wf.count_from_large_file(args.file) if args.large else wf.count_from_file(args.file)
        if args.k is None or (isinstance(args.k, int) and args.k <= 0):
            results = [(w, c) for w, c in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))]
        else:
            results = counter.most_common(args.k)

    lines = [f"{word}\t{count}" for word, count in results]
    if args.print_limit is not None and args.print_limit > 0:
        lines = lines[: args.print_limit]

    print("\n".join(lines))

if __name__ == "__main__":
    main()
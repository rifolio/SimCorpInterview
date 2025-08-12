# SimCorp - Word Counter

<img src="https://img.shields.io/badge/-Python-blue?style=for-the-badge">

Solution for second round interview.

## Task

Given a text file, count the occurrence of each unique word in the file.

### Example

A file containing the string "Go do that thing that you do so well" should find these counts:

- **1**: Go
- **2**: do
- **2**: that
- **1**: thing
- **1**: you
- **1**: so
- **1**: well

## Installation

### macOS/Linux

```bash
python3.12 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

## Usage

### Basic Usage

```bash
python main.py <filename>
```

### Command Line Arguments

| Argument           | Type       | Default  | Description                                                                                |
| ------------------ | ---------- | -------- | ------------------------------------------------------------------------------------------ |
| `file`             | positional | required | Path to text file to analyze                                                               |
| `--k`              | int        | None     | top-k words or ≤0 to return all                                                            |
| `--case-sensitive` | flag       | False    | default to case-insensitive                                                                |
| `--large`          | flag       | False    | line-by-line for large inputs, non memory leak                                             |
| `--method`         | choice     | "bucket" | bucket-based O(n) selection or super pythonic Counter.most_common, almost like cheating XD |
| `--print-limit`    | int        | None     | n results to print                                                                         |

## When to Use Each Option

### `--case-sensitive`

- **Use when**: need to distinguish between "Word", "word", and "WORD"
- **Skip when**: want to count "The" and "the" as the same word

### `--large`

- **Use when**: files larger than available RAM
- **Skip when**: small files (<100MB)

### `--method`

- **"bucket"** (default):
  - Use for: most cases, especially with top-k selection --> O(n) time complexity, memory efficient
- **"pythonic"**:
  - Use for: specifically need Counter.most_common(), on-eliner

### `--k`

- **Specify a number**: only the top N most frequent words

# SimCorp - Word Counter

Solution for second round interview.

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

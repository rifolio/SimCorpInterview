import os
import random
import string

target_size_mb = 20
file_path = f"text_files/random_text_{target_size_mb}mb.txt"
target_size_bytes = target_size_mb * 1024 * 1024

os.makedirs(os.path.dirname(file_path), exist_ok=True)

with open(file_path, "w", encoding="utf-8") as f:
    written = 0
    chunk_size = 1024 * 1024
    while written < target_size_bytes:
        words = ["".join(random.choices(string.ascii_letters + " ", k=10)) for _ in range(chunk_size // 11)]
        text_chunk = " ".join(words)
        f.write(text_chunk)
        written += len(text_chunk.encode("utf-8"))
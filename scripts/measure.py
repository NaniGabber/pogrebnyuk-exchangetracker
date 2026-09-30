from pathlib import Path
from time import perf_counter
from tracemalloc import get_traced_memory, start, stop

from exchangetracker.sources.jsonl_file import (
    read_jsonl_eager,
    read_jsonl_lazy,
)

path = Path("data/large.jsonl")


def benchmark_lazy():
    start()
    t0 = perf_counter()
    count = 0
    for _ in read_jsonl_lazy(path):
        count += 1

    elapsed = perf_counter() - t0
    _, peak = get_traced_memory()
    stop()
    return count, elapsed, peak / (1024 * 1024)


def benchmark_eager():
    start()
    t0 = perf_counter()
    rows = read_jsonl_eager(path)
    elapsed = perf_counter() - t0
    _, peak = get_traced_memory()
    stop()
    return len(rows), elapsed, peak / (1024 * 1024)


lazy_rows, lazy_time, lazy_mem = benchmark_lazy()
eager_rows, eager_time, eager_mem = benchmark_eager()

print("=== LAZY ===")
print(f"Rows: {lazy_rows}")
print(f"Time: {lazy_time:.3f} s")
print(f"Peak memory: {lazy_mem:.2f} MB")

print()

print("=== EAGER ===")
print(f"Rows: {eager_rows}")
print(f"Time: {eager_time:.3f} s")
print(f"Peak memory: {eager_mem:.2f} MB")

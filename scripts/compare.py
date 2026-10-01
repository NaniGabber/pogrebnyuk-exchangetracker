import time
import tracemalloc

from pathlib import Path

from exchangetracker.domain.parsing import to_exchange_rate
from exchangetracker.services.pipeline import (
    PipelineStats,
    collect,
    deduplicate,
)
from exchangetracker.sources.jsonl_file import read_jsonl_lazy

path = Path("data/large.jsonl")


def lazy():
    stats = PipelineStats()
    parsed = (to_exchange_rate(row) for row in read_jsonl_lazy(path))
    valid = (rate for rate in parsed if rate is not None)
    collect(
        deduplicate(valid, stats),
        stats,
    )

    return stats.kept


def greedy():
    rows = list(read_jsonl_lazy(path))
    parsed = [to_exchange_rate(row) for row in rows]
    valid = [rate for rate in parsed if rate is not None]
    seen = set()
    unique = []

    for rate in valid:
        if rate.key not in seen:
            seen.add(rate.key)
            unique.append(rate)

    return len(unique)


for name, fn in (("генераторний конвеєр", lazy), ("проміжні списки", greedy)):
    tracemalloc.start()
    t0 = time.perf_counter()
    n = fn()
    elapsed = time.perf_counter() - t0
    peak = tracemalloc.get_traced_memory()[1] / 1024 / 1024
    tracemalloc.stop()
    print(f"{name:22} " f"{n} записів " f"{elapsed:.2f} с " f"пік {peak:.1f} МБ")

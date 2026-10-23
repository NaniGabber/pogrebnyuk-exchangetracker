from tests.conftest import FakeSource

from exchangetracker.services.pipeline import Pipeline, PipelineStats, batched


def test_invalid_rows_are_counted():
    rows = [
        {
            "asset": "USD",
            "type": "currency",
            "rate": "41.25",
            "date": "2026-10-01",
        },
        {
            "asset": "",
            "type": "currency",
            "rate": "48.10",
            "date": "2026-10-02",
        },
    ]

    stats = PipelineStats()
    source = FakeSource(rows)

    result = list(Pipeline._parse(source, stats))

    assert len(result) == 1
    assert stats.read == 2
    assert stats.invalid == 1


def test_batched_splits_tail():
    assert [len(b) for b in batched(range(7), 3)] == [3, 3, 1]

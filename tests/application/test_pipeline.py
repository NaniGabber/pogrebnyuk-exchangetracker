from itertools import islice

from exchangetracker.services.pipeline import Pipeline, PipelineStats
from tests.conftest import FakeSource


def test_parse_is_lazy() -> None:
    consumed = 0

    row = {
        "asset": "USD",
        "type": "currency",
        "rate": 41.5,
        "date": "2026-10-08",
    }

    def endless():
        nonlocal consumed

        while True:
            consumed += 1
            yield row

    source = FakeSource(endless())
    stats = PipelineStats()

    taken = list(islice(Pipeline._parse(source, stats), 3))

    assert len(taken) == 3
    assert consumed == 3

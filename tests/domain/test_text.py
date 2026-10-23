from exchangetracker.domain.text import normalize_title


def test_normalize_title_strips_spaces() -> None:
    assert normalize_title("  USD  ") == "usd"


def test_normalize_title_lowercases() -> None:
    assert normalize_title("USD") == "usd"


def test_normalize_title_collapses_whitespace() -> None:
    assert normalize_title("Python    Developer") == "python developer"

from legacy.loader import process

def test_legacy_output_is_stable():
    rows = process("data/exchange_data.json")

    assert rows == [
        ['usd', 'currency', 41.25, '2026-10-01'],
        ['eur', 'currency', 48.1, '2026-10-02'],
        ['xau', 'metal', 4550.0, '2026-10-03'],
        ['xag', 'metal', 52.3, '2026-10-04'],
        ['gbp', '', 53.2, '2026-10-06'],
        ['chf', 'currency', 0, '2026-10-10']
    ]
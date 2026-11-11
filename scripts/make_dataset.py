import json
import pathlib
import random
from datetime import date, timedelta

random.seed(7)

assets = ["USD", "EUR", "GBP", "JPY", "XAU", "XAG"]

types = {
    "USD": "currency",
    "EUR": "currency",
    "GBP": "currency",
    "JPY": "currency",
    "XAU": "metal",
    "XAG": "metal",
}

start_date = date(2020, 1, 1)

path = pathlib.Path("data/large.jsonl")

prev = None

with path.open("w", encoding="utf-8") as f:
    for i in range(200_000):
        if i % 10 == 3 and prev is not None:
            row = dict(prev)
        else:
            asset = random.choice(assets)

            random_day = start_date + timedelta(days=random.randint(0, 2500))

            row = {
                "asset": (asset if i % 11 else f"  {asset.lower()}  "),
                "type": types[asset],
                "rate": (
                    str(round(random.uniform(10, 5000), 2))
                    if i % 7
                    else random.choice(
                        [
                            "невідомо",
                            "",
                            "N/A",
                            "курс відсутній",
                        ]
                    )
                ),
                "date": (random_day.isoformat() if i % 13 else ""),
            }

        if i % 1000 == 0:
            row = dict(row, asset="")

        f.write(json.dumps(row, ensure_ascii=False) + "\n")

        prev = row

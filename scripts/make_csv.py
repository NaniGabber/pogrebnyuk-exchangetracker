import csv
import random
from datetime import date, timedelta

ASSETS = ["USD", "EUR", "GBP", "JPY", "CHF", "PLN"]


with open("data/rates.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow(["asset", "type", "rate", "date"])

    start = date(2026, 1, 1)

    for _ in range(5000):
        writer.writerow(
            [
                random.choice(ASSETS),
                "currency",
                round(random.uniform(20, 60), 4),
                start + timedelta(days=random.randint(0, 365)),
            ]
        )

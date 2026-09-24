import argparse
from pathlib import Path

from tabulate import tabulate

from .services.market_data import (
    convert_usd_to_uah,
    get_currency_rates_privat,
    get_currency_rates_yahoo,
    get_metal_prices_usd,
    get_usd_uah,
)
from .services.pipeline import (
    count_by_asset,
    load_exchange_rates,
)


def show_privat_rates(rates: list[dict]) -> None:
    table = [
        [
            row["ccy"],
            row["base_ccy"],
            row["buy"],
            row["sale"],
        ]
        for row in rates
    ]

    print(
        tabulate(
            table,
            headers=["Валюта", "База", "Купівля", "Продаж"],
            tablefmt="grid",
        )
    )


def show_yahoo_rates(
    rates: dict[str, float],
    usd_uah: float,
) -> None:
    print("\nКурси валют (Yahoo Finance → UAH):")

    table = [
        [
            currency,
            f"{rate:.4f}",
            f"{rate * usd_uah:.2f}",
        ]
        for currency, rate in rates.items()
    ]

    print(
        tabulate(
            table,
            headers=["Валюта", "До USD", "Еквівалент у UAH"],
            tablefmt="grid",
        )
    )


def show_metals(
    prices_usd: dict[str, float],
    prices_uah: dict[str, float],
) -> None:
    print("\nКотирування металів:")

    table = [
        [
            metal,
            f"{usd_price:.2f}",
            f"{prices_uah[metal]:.2f}",
        ]
        for metal, usd_price in prices_usd.items()
    ]

    print(tabulate(table, headers=["Метал", "USD", "UAH"], tablefmt="grid"))


def main() -> None:
    parser = argparse.ArgumentParser(prog="exchangetracker")
    parser.add_argument("path", type=Path, nargs="?", help="JSON файл з даними")

    args = parser.parse_args()

    if args.path:
        rates = load_exchange_rates(args.path)

        print(f"Завантажено записів: {len(rates)}")

        for asset, count in count_by_asset(rates).most_common():
            print(f"{asset}: {count}")

    usd_uah = get_usd_uah()
    privat_rates = get_currency_rates_privat()
    yahoo_rates = get_currency_rates_yahoo("USD", ["EUR", "GBP", "JPY"])

    metals_usd = get_metal_prices_usd()

    metals_uah = convert_usd_to_uah(metals_usd, usd_uah)

    show_privat_rates(privat_rates)
    show_yahoo_rates(yahoo_rates, usd_uah)
    show_metals(metals_usd, metals_uah)


if __name__ == "__main__":
    main()

import argparse
import logging
from collections.abc import Callable
from pathlib import Path

from tabulate import tabulate

from .config import Settings
from .errors import ExchangeTrackerError, SourceError
from .logging_setup import setup
from .services.market_data import (
    convert_usd_to_uah,
    get_currency_rates_privat,
    get_currency_rates_yahoo,
    get_metal_prices_usd,
    get_usd_uah,
)
from .services.pipeline import Pipeline, PipelineStats
from .services.ports import Source
from .sources.csv_file import CsvSource
from .sources.jsonl import JsonlSource

FACTORIES: dict[str, Callable[[Path], Source]] = {
    ".jsonl": JsonlSource,
    ".csv": CsvSource,
}

logger = logging.getLogger(__name__)


def build_source(path: Path) -> Source:
    try:
        factory = FACTORIES[path.suffix]
    except KeyError:
        raise SourceError(f"unsupported file type: {path.suffix}") from None
    return factory(path)


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
    settings = Settings()

    parser = argparse.ArgumentParser(prog="exchangetracker")
    parser.add_argument("paths", type=Path, nargs="+", help="файли з даними")
    parser.add_argument("--preview", type=int, default=10, help="Показати перші n записів")
    parser.add_argument("--common", nargs="?", help="Порахувати кількість за валютою")
    parser.add_argument("--stats", action="store_true", help="Вивести результати опрацювання файлу")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="перекриває значення з .env і змінних середовища",
    )

    def read_stats(stats: PipelineStats) -> None:
        print("Read:", stats.read)
        print("Invalid:", stats.invalid)
        print("Duplicates:", stats.duplicates)
        print("Kept:", stats.kept)

        print("Assets:", dict(stats.by_asset))

        print("Rate count:", stats.rate_count)
        print("Rate sum:", round(stats.rate_sum, 2))
        print("Rate min:", stats.rate_min)
        print("Rate max:", stats.rate_max)
        print("Rate avg:", None if stats.rate_avg is None else round(stats.rate_avg, 2))

    args = parser.parse_args()

    setup(args.log_level or settings.log_level)

    if args.paths:
        try:
            sources = [build_source(path) for path in args.paths]
            stats = Pipeline(sources).run()
        except ExchangeTrackerError as exc:
            logger.error("%s", exc)
            raise SystemExit(1) from exc

        if args.common:
            for asset, count in stats.by_asset.most_common():
                print(f"{asset}: {count}")

        if args.stats:
            read_stats(stats)
    else:
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

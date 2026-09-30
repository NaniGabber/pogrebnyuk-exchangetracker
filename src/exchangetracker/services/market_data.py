from functools import lru_cache

import requests
import yfinance as yf

PRIVAT_API_URL = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"


def safe_request(url: str):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Помилка при запиті {url}: {e}")
        return []


@lru_cache(maxsize=1)
def get_usd_uah() -> float:
    data = safe_request(PRIVAT_API_URL)

    usd = next(
        (float(currency["sale"]) for currency in data if currency["ccy"] == "USD"),
        None,
    )

    if usd is None:
        raise ValueError("Не вдалося отримати курс USD/UAH")

    return usd


def get_currency_rates_privat() -> list[dict]:
    return safe_request(PRIVAT_API_URL)


def get_currency_rates_yahoo(
    base: str,
    targets: list[str],
) -> dict[str, float]:
    rates = {}

    for target in targets:
        ticker = f"{target}{base}=X"

        data = yf.Ticker(ticker).history(period="5d")

        if data.empty:
            print(f"Немає даних для {target}")
            continue

        rates[target] = float(data["Close"].iloc[-1])

    return rates


def get_metal_prices_usd() -> dict[str, float]:
    metals = {
        "Gold (XAU)": "GC=F",
        "Silver (XAG)": "SI=F",
        "Platinum (XPT)": "PL=F",
        "Palladium (XPD)": "PA=F",
    }

    prices = {}

    for name, ticker in metals.items():
        data = yf.Ticker(ticker).history(period="5d")

        if data.empty:
            print(f"Немає даних для {name}")
            continue

        prices[name] = float(data["Close"].iloc[-1])

    return prices


def convert_usd_to_uah(
    prices: dict[str, float],
    usd_uah: float,
) -> dict[str, float]:
    return {name: price * usd_uah for name, price in prices.items()}

from functools import lru_cache

import requests
import yfinance as yf
from tabulate import tabulate

PRIVAT_API_URL = ("https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5")

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
    url = PRIVAT_API_URL
    data = safe_request(url)
    usd = next((float(c["sale"]) for c in data if c["ccy"] == "USD"), None)
    if usd is None:
        raise ValueError("Не вдалося отримати курс USD/UAH")
    return usd


def get_currency_rates_privat() -> list[dict[str, str]]:
    url = PRIVAT_API_URL
    return safe_request(url)


def get_currency_rates_yahoo(base: str, targets: list[str]) -> dict[str, float]:
    return {t: yf.Ticker(f"{t}{base}=X").history(period="1d")["Close"].iloc[-1] for t in targets}


def get_metal_prices_usd() -> dict[str, float]:
    metals = {
        "Gold (XAU)": "GC=F",
        "Silver (XAG)": "SI=F",
        "Platinum (XPT)": "PL=F",
        "Palladium (XPD)": "PA=F"
    }
    return {name: yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1] for name, ticker in metals.items()}


def convert_usd_to_uah(prices: dict[str, float], usd_uah: float) -> dict[str, float]:
    return {name: price * usd_uah for name, price in prices.items()}


def show_privat_rates(rates: list[dict[str, str]]) -> None:
    table = [[c['ccy'], c['base_ccy'], c['buy'], c['sale']] for c in rates]
    print(tabulate(table,
                    headers=["Валюта", "База", "Купівля", "Продаж"],
                    tablefmt="grid"))

def show_yahoo_rates(rates: dict[str, float], usd_uah: float) -> None:
    print("\nКурси валют (Yahoo Finance → UAH):")
    for cur, val in rates.items():
        print(f"{cur}/USD: {val:.2f} → {val * usd_uah:.2f} UAH")


def show_metals(prices_usd: dict[str, float], prices_uah: dict[str, float]) -> None:
    print("\nКотирування металів:")
    for name, usd_price in prices_usd.items():
        uah_price = prices_uah[name]
        print(f"{name}: {usd_price:.2f} USD ≈ {uah_price:.2f} UAH")


def main() -> None:
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


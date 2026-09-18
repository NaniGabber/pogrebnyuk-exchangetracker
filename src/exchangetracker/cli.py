import requests
import yfinance as yf
from typing import Dict, List


def get_usd_uah() -> float:
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    data = requests.get(url).json()
    usd = next((float(c["sale"]) for c in data if c["ccy"] == "USD"), None)
    if usd is None:
        raise ValueError("Не вдалося отримати курс USD/UAH")
    return usd


def get_currency_rates_privat() -> List[Dict[str, str]]:
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
    return requests.get(url).json()


def get_currency_rates_yahoo(base: str, targets: List[str]) -> Dict[str, float]:
    return {t: yf.Ticker(f"{t}{base}=X").history(period="1d")["Close"].iloc[-1] for t in targets}


def get_metal_prices_usd() -> Dict[str, float]:
    metals = {
        "Gold (XAU)": "GC=F",
        "Silver (XAG)": "SI=F",
        "Platinum (XPT)": "PL=F",
        "Palladium (XPD)": "PA=F"
    }
    return {name: yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1] for name, ticker in metals.items()}


def convert_usd_to_uah(prices: Dict[str, float], usd_uah: float) -> Dict[str, float]:
    return {name: price * usd_uah for name, price in prices.items()}


def show_privat_rates(rates: List[Dict[str, str]]) -> None:
    print("Курси валют (ПриватБанк):")
    for c in rates:
        print(f"{c['ccy']} -> {c['base_ccy']}: Buy={c['buy']} Sell={c['sale']}")


def show_yahoo_rates(rates: Dict[str, float], usd_uah: float) -> None:
    print("\nКурси валют (Yahoo Finance → UAH):")
    for cur, val in rates.items():
        print(f"{cur}/USD: {val:.2f} → {val * usd_uah:.2f} UAH")


def show_metals(prices_usd: Dict[str, float], prices_uah: Dict[str, float]) -> None:
    print("\nКотирування металів:")
    for name in prices_usd:
        print(f"{name}: {prices_usd[name]:.2f} USD ≈ {prices_uah[name]:.2f} UAH")


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


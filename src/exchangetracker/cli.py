import requests

def main() -> None:
   
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"

    response = requests.get(url)
    data = response.json()

    print("Курси валют ПриватБанк:")
    for item in data:
        print(f"{item['ccy']} -> {item['base_ccy']}: "
              f"Buy = {item['buy']}, Sell = {item['sale']}")



if __name__ == "__main__":
    main()

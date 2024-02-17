import requests

def get_exchange_rate(base_currency, target_currency):
    url = f"http://api.nbp.pl/api/exchangerates/tables/a/?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rates_table = data[0]['rates']
        exchange_rate = None
        for rate in rates_table:
            if rate['code'] == target_currency:
                exchange_rate = rate['mid']
                break
        if exchange_rate is not None:
            return exchange_rate
        else:
            print(f"Exchange rate for {target_currency} not found.")
            return None
    else:
        print("Failed to fetch exchange rate data.")
        return None
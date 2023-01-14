import requests
import json
from config import exchanges


class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = str(exchanges[quote.lower()])
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = str(exchanges[base.lower()])
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        url = f'https://api.apilayer.com/exchangerates_data/convert?from={quote_ticker}&to={base_ticker}&amount={amount}'
        headers = {'apikey': 'tDLc9WC9YYYQwuGsxoHrj6YEoJuy5Ihf'}
        response = requests.get(url, headers=headers)
        response_json = json.loads(response.content)
        price = round(response_json['result'], 2)

        return price
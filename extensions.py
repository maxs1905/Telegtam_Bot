import requests
import json
from config import keys, EXCHANGE_RATE_API_KEY

class APIException(Exception):
    pass
class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковую волюту {base}.')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать волюту {quote}.')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать волюту {base}.')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректное значение {amount}.')
        url = f'https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{quote_ticker}'

        responce = requests.get(url)
        if responce.status_code != 200:
            raise APIException(f'Ошибка запроса')

        data = responce.json()
        if quote_ticker not in data['conversion_rates']:
            raise APIException(f'Не удалось получить данные для валюты {base_ticker}.')
        price = data['conversion_rates'][base_ticker]
        total_base = price * amount

        return total_base
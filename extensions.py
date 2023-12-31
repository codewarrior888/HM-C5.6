import json
import requests
from config import currencies


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        try:
            base = currencies[base.lower()]
        except KeyError:
            raise APIException(f'Валюта "{base}" не найдена!\nУзнать доступные валюты:/values')

        try:
            quote = currencies[quote.lower()]
        except KeyError:
            raise APIException(f'Валюта "{quote}" не найдена!\nУзнать доступные валюты:/values')

        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError as e:
            raise APIException(f'Ошибка: {e}. Не удалось обработать количество {amount}!')

        url = f'https://api.apilayer.com/exchangerates_data/convert?to={base}&from={quote}&amount={amount}'

        headers = {
            'apikey': 'APIKEY'
        }

        response = requests.request('GET', url, headers=headers)

        if response.status_code != 200:
            raise APIException(f'Неполучилось загрузить данные. Код ошибки: {response.status_code}')

        try:
            data = json.loads(response.text)
            result = data["info"]["rate"]
            converted_value = round(result * amount, 2)
            return f'Цена {amount} {quote} в {base} = {converted_value}'
        except KeyError as e:
            raise APIException(f'Ошибка: {e}. Убедитесь, присутствуют ли в ответе ожидаемые параметры.')

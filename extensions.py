import json
import requests
from config import exchanges, EXCHTOKEN


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r0 = requests.get(f"http://api.exchangeratesapi.io/latest?access_key={EXCHTOKEN}&symbols={base_key}")
        r = requests.get(f"http://api.exchangeratesapi.io/latest?access_key={EXCHTOKEN}&symbols={sym_key}")
        resp0 = json.loads(r0.content)
        resp = json.loads(r.content)
        new_price0 = resp0['rates'][base_key]
        new_price1 = resp['rates'][sym_key]
        new_price0 = round(new_price0, 12)
        new_price1 = round(new_price1, 12)
        new_price = new_price1 / new_price0 * amount
        new_price = round(new_price, 12)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message

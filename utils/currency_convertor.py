from pycbrf import ExchangeRates
from datetime import datetime
from decimal import Decimal


def get_currency_converter(currency: str) -> Decimal:
    current_date = datetime.now().strftime("%Y-%m-%d")
    rates = ExchangeRates(current_date)
    currency = _check_currency(currency)
    current_data = list(filter(lambda el: el.code == currency, rates.rates))[0].rate
    return current_data


def _check_currency(currency):
    if currency == 'BYR':
        return 'BYN'
    return currency
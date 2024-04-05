import requests as req

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base, quote, amount):
        url = f"https://min-api.cryptocompare.com/data/price?fsym={base}&tsyms={quote}"
        response = req.get(url)
        if response.status_code == 200:
            data = response.json()
            if quote in data:
                price = data[quote] * amount
                return price
            else:
                raise APIException(f"Цена для {quote} не найдена в ответе API.")
        else:
            raise APIException("Произошла ошибка при выполнении запроса.")


class Names:
    def __init__(self):
        pass

    def get_current_names(self):
        url = "https://min-api.cryptocompare.com/data/top/totalvolfull?limit=10&tsym=USD"
        response = req.get(url)
        data = response.json()
        names = [coin['CoinInfo']['Name'] for coin in data['Data']]
        return ', '.join(names)




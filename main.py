import telebot
from my_token import token
from tech import CurrencyConverter, APIException, Names

bot = telebot.TeleBot(token.TOKEN, parse_mode=None)

options = {"Биткоин": "BTC", "Эфириум": "ETH"}

@bot.message_handler(commands=['start', 'help', 'values'])
def send_welcome(message):
    if message.text == '/start':
        text = """Этот бот показывает курсы валют Биткоина и Эфириума в долларах и евро.
                  При вводе команды '/values' показывает курсы Биткоина и Эфириума в долларах, евро и рублях.
                  С детальной информацией вы можете ознакомиться по команде '/help'.
                  Для перевода по текущему курсу Биткоина или Эфириума введите команду '/convert'."""
        bot.send_message(message.chat.id, text)

    elif message.text == '/help':
        text = "Введите '/values', '/start', или '/help', чтобы получить информацию. Чтобы конвертировать валюту введите, например, BTC 1 RUB"
        bot.send_message(message.chat.id, text)

    elif message.text == '/values':
        names = Names()
        bot.send_message(message.chat.id, f"Самые популярные валюты: {names.get_current_names()}")



@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    parts = text.split()

    # Проверяем, соответствует ли сообщение формату для конвертации
    if len(parts) == 3:
        try:
            base_currency, amount_str, quote_currency = parts
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Сумма должна быть больше нуля.")

            price = CurrencyConverter.get_price(base_currency, quote_currency, amount)
            bot.send_message(message.chat.id, f"{amount} {base_currency} = {price} {quote_currency}")
        except ValueError as e:
            bot.send_message(message.chat.id, f"Ошибка: {e}")
        except APIException as e:
            bot.send_message(message.chat.id, f"Ошибка API: {e}")
    else:
        if '/start' in text or '/help' in text or '/values' in text:
            send_welcome(message)
        else:
            bot.send_message(message.chat.id, "Неверный формат команды. Используйте формат: <исходная валюта> <сумма> <целевая валюта>, например: USD 1000 BTC")


if __name__ == '__main__':
    bot.polling()

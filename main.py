import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Приветствуйю тебя, жаждующий узнать все про всех! Давай начнем. Чтобы узнать, что я могу тебе поведать, введи команду /help"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = "Я могу перевести тебе одну валюту в другую при помощи сервиса exchangerates, что бы узнать доступные - введи команду /values. " \
           "Вид запроса: конвертируемая валюта итоговая валюта кол-во"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()

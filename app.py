import telebot
from extensions import APIException, Convertor
from config import TOKEN, currencies
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = ('Добро пожаловать в SimpleExchangeBot!\nВведите команду в следующем формате:\n<базовая валюта> \
<котируемая валюта> <кол-во>\nУвидеть список всех доступных валют: /values')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for keys in currencies.keys():
        text = '\n'.join((text, keys, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    parameters = message.text.split(' ')
    try:
        if len(parameters) != 3:
            raise APIException('Неверное количество параметров!\n\nВведите команду в следующем формате:\
\n<базовая валюта> <котируемая валюта> <кол-во>')

        answer = Convertor.get_price(*parameters)
    except APIException as e:
        bot.reply_to(message, f'Ошибка в команде:\n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Неизвестная ошибка:\n{e}')
    else:
        bot.reply_to(message, answer)


bot.polling(none_stop=True)

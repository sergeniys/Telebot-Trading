import telebot
from telebot import types
import pandas as pd
import requests
from matplotlib import pyplot as plt
import io
import emoji
import os

from tradingview_ta import TA_Handler, Interval

API_TOKEN = 'Token'
bot = telebot.TeleBot(API_TOKEN)

#commands
bot.delete_my_commands(scope=None, language_code=None)
bot.set_my_commands(
    commands=[
        telebot.types.BotCommand("start", "начать"),
        telebot.types.BotCommand("site", "cfqn"),
    ],

)
telebot.types.ReplyKeyboardRemove()
adminID = '645869035'


tickers = [
    "IRAO",
    "SVCB",
    "FLOT",
    "AFLT",
    "ALRS",
    "CBOM",
    "FEES",
    "GAZP",
    "GMKN",
    "GMK",
    "HYDR",
    "MSTT",
    "MTSS",
    "NLMK",
    "NVTK",
    "PLZL",
    "ROSN",
    "RTKM",
    "SBER",
    "TRNFP",
    "VTBR",
    "YDEX",
"SMLT"
]
@bot.message_handler(commands=['zametki'])
def zamet(message):
    msg = bot.reply_to(message, 'Введите заметку')
    bot.register_next_step_handler(msg, writez)
def writez(message):
    with open('messagetip.txt', 'a', encoding='utf-8') as file:
        file.write(emoji.demojize(message.text + '\n'))
        file.close()
    with open('messagetip.txt', 'r', encoding='utf-8') as file:
        notes = file.read()
        bot.send_message(message.chat.id, f'{emoji.emojize(notes)}')

        file.close()

@bot.message_handler(commands=['redact'])
def step_two(message):
    if message.chat.id == 645869035:

        with open('messagetip.txt', 'r') as file:
            notes = file.read()
            bot.send_message(message.chat.id, f'{emoji.emojize(notes)}')
            file.close()
        os.system(r'nul>messagetip.txt')
        msg = bot.reply_to(message, 'Введите редактированную заметку')
        bot.register_next_step_handler(msg, redi)



def redi(message):

    with open('messagetip.txt', 'a', encoding='utf-8') as file:

        file.write(emoji.demojize(message.text + '\n'))
        file.close()
    with open('messagetip.txt', 'r', encoding='utf-8') as file:
        notes = file.read()
        bot.send_message(message.chat.id, f'{emoji.emojize(notes)}')
        file.close()

@bot.message_handler(commands=tickers)
def draw_graph(message):
    ticker = message.text[1:]
    j = requests.get(
        f'http://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}/candles.json?from=2024-02-02&interval=24').json()
    data = [{k: r[i] for i, k in enumerate(j['candles']['columns'])} for r in j['candles']['data']]

    frame = pd.DataFrame(data)
    plt.close('all')
    plt.clf()
    plt.rcdefaults()
    plt.switch_backend('agg')
    del frame
    frame = pd.DataFrame(data)
    plt.figure()
    plt.plot(frame['close'])
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    photo = io.BytesIO(buffer.getvalue())
    try:
        recom = TA_Handler(
            symbol= message.text[1:],
            screener="russia",
            exchange="MOEX",
            interval=Interval.INTERVAL_1_DAY
        )
        cost = data[-1]['close']

        buy = recom.get_analysis().summary['BUY']
        sell = recom.get_analysis().summary['SELL']
        neutral = recom.get_analysis().summary['NEUTRAL']
        bot.send_photo(message.chat.id, photo, caption=f'Цена: {cost}, рекомендации Trading view:\nЗа покупку - {buy}\
    \nЗа продажу - {sell} \
                                                   \nНейтрально - {neutral}\n')
    except:
        cost = data[-1]['close']

    bot.send_photo(message.chat.id, photo, caption=f'Цена: {cost}, рекомендации Trading view на этом хосте пока не доступны(')
    buffer.truncate(0)

#menubuttons
@bot.message_handler(commands=['start'])
def keyboard(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Заметки😮')
    item2 = types.KeyboardButton('Чат для приколов💣')
    item3 = types.KeyboardButton('Акции moex сейчас📈')
    item4 = types.KeyboardButton('Git /  стек')
    markup.add(item3, item1, item2, item4)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user), reply_markup=markup)

# @bot.message_handler(func=lambda message: True)
# def forward_message(message):
#     print(f'пересланно: {message.text}')
#     channel_id = '1002048452238'
#
#     bot.forward_message(chat_id=channel_id, from_chat_id=message.chat.id, message_id=message.message_id)
#

#forfun
# @bot.message_handler(content_types=['text'])
# def all_messages(message):
#     bot.forward_message(-1002048452238, message.chat.id, message.message_id)

@bot.message_handler(content_types=['text'])
def tickers(message):
    bot.forward_message(-#перссылка сообщений, message.chat.id, message.message_id)
    if message.text == 'Акции moex сейчас📈':
        bot.send_message(message.chat.id, "Графики, цены и рекомендации:\nНажми на тикер для котировок\nВсе котировки с февраля 2024\n\
/IRAO - Интер Рао\n \
/SVCB - Совкомбанк\n\
/FLOT - Совкомфлот\n\
/AFLT - Аэрофлот\n\
/ALRS - АЛРОСА\n\
/CBOM - Центральный Банк Москвы\n\
/FEES - Федеральная сетевая компания\n\
/GAZP - Газпром\n\
/GMK - Норильский никель\n\
/HYDR - ОАО Гидроэлектросети\n\
/MSTT - М.Видео\n\
/MTSS - Мобильные ТелеСистемы\n\
/NLMK - НЛМК\n\
/NVTK - НОВАТЭК\n\
/PLZL - Полюс\n\
/ROSN - Роснефть\n\
/RTKM - Ростелеком\n\
/SBER - Сбербанк\n\
/TRNFP - Транснефть\n\
/VTBR - ВТБ\n\
/YDEX - Яндекс\n\
/SMLT - Самолет \n")
    elif message.text == 'Заметки😮':
        with open('messagetip.txt', 'r', encoding='utf-8') as file:
            notes = file.read()
            bot.send_message(message.chat.id, f'Здесь можно оставить любое сообщение\отзыв которое хотите анонимно для всех - команда /zametki\n\
{emoji.emojize(notes)}')
            file.close()

    elif message.text == 'Git /  стек':
        bot.send_message(message.chat.id, f'Стек:\n\
telebot, pandas, requests, matplotlib, io, emoji, os\n\
https://github.com/sergeniys')
    elif message.text == 'Чат для приколов💣':
        bot.send_message(message.chat.id, 'https://t.me/+f2mF54K9i4k5NGIy')
    elif message.text == 'Бот дай скин':
        bot.send_message(message.chat.id, 'Для продолжения необходимо пополнить баланс: 2200700886197218')
    elif message.text == 'бот дай скин':
        bot.send_message(message.chat.id, 'Для продолжения необходимо пополнить баланс: 2200700886197218')

if __name__ == '__main__':
    bot.infinity_polling()

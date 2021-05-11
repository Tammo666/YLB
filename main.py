import telebot
from bs4 import BeautifulSoup as BS
import requests
from telebot import types

TOKEN = '1746024855:AAGscfH-NRnz-BG90HbqCb9loSm0gem5_8c'
BOT_NAME = 'Lyceumfirst' #t.me/Lyceumfirst_bot  \\\ Lyceumfirst_bot


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/help" or  message.text == '/start':
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
        keyboard.add(key_yes)  # добавляем кнопку в клавиатуру
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        bot.send_message(message.from_user.id, text='Хочешь немного погуглить?', reply_markup=keyboard)

    elif '/googli' in message.text:
        goo_search(message)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def goo_search(message):
    query = message.text
    query = query.split('/googli ')[1]
    ver_query = query.replace(' ', '+')
    url = 'https://www.google.com/search?q=' + ver_query + '&hl=ru&'

    response = requests.get(url)
    soap_resp = BS(response.content, 'lxml')
    with open('content.txt', 'w', encoding='utf-8') as google:
        google.write(soap_resp.prettify())

    links = soap_resp.find_all('a')
    all_links = {}
    for i in links:
        try:
            if 'href="/url?q=https://' in str(i):
                hell_thing = ((str(i).split('">')[0]).split('href="/url?q=')[1]).split('&')[0]
                if '.google.' not in hell_thing:
                    all_links[hell_thing] = (str(i).split('class="BNeawe vvjwJb AP7Wnd">')[1]).split('</div>')[0]
        except:
            continue

    keyboard = types.InlineKeyboardMarkup()
    for i in all_links:
        print(i, all_links[i])
        url_button = types.InlineKeyboardButton(text=all_links[i], url=i)
        keyboard.add(url_button)
    bot.send_message(message.chat.id, "Вот что нам (мне и достопочтенному Googlу) удалось найти:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Пиши \"/googli\" со своим вопросом и прозрей')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Тогда, мы полагаем, для нас обоих лучше прекратить эту беседу')


bot.polling(none_stop=True, interval=0)

import telebot,json,html
from telebot import types
from os import listdir

#откртыие json файла и его чтение
with open("crypto_parcing.json",'r') as jsn:
    cryptos = json.load(jsn)

#токен который дает ботфазер при создание своего бота в телеграме
token = "427181756:AAHi7IGhdWPL4O65xjpRmm5r2CoVxRHFrq0"

bot = telebot.TeleBot(token)

states = dict()#словарь с пользователями массив состояний

for filename in listdir('DB'):
    chat_id = int(filename.rstrip('.txt'))
    with open('DB/'+filename, 'r') as state:
        states[chat_id] = state.read()


def save_state(chat_id, new_state):
    states[chat_id] = new_state
    with open('DB/{0}.txt', format(chat_id), 'w') as file:
        file.write(new_state)

    return True


standardMarkup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
standardMarkup.add(

    types.KeyboardButton(text="Новости"),
    types.KeyboardButton(text="Курс"),
    types.KeyboardButton(text="Описание монет")
)


newsMarkup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
standardMarkup.add(

    types.KeyboardButton(text="Рубрики"),
    types.KeyboardButton(text="Ещё"),
    types.KeyboardButton(text="Меню")
)



def hand(message, reply_markup=None):
    print("i see new message", message.text)
    #bot.send_message(message.chat.id, "Твое сообщение: " + message.text)
    bot.send_message(message.chat.id, "Привет", reply_markup=reply_markup)



@bot.message_handler(commands=["menu"])
def of(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_curs = types.KeyboardButton(text="Курс",) # применяет кусок кода вот того (*)
    button_money = types.KeyboardButton(text="Описание монет",)#после выбора применяет то что распарсили и находится в json
    button_news = types.KeyboardButton(text="Новости", )
    states[message.chat.id] = "selectingTask"
    keyboard.add(button_curs,button_money, button_news)
    bot.send_message(message.chat.id, "выбери команду", reply_markup=keyboard)


@bot.message_handler(commands=["coin"])
def rate(massage):

    cmd = massage.text.strip().split()

    name = cmd[1].lower()
    title = html.escape(cryptos[name][0])
    desc = html.escape(cryptos[name][1])

    if len(cmd) > 1 and name in cryptos:
        bot.send_message(massage.chat.id,"<b>{0}</b> - {1}".format(title, desc), parse_mode="HTML")
    else:
        bot.send_message(massage.chat.id, "В нашей базе нет такой криптовалюты и её описания ")


#вот этот код(*)
@bot.message_handler(content_types=["text"])
def default_test(message):
    if message.chat.id in states:
        if states[message.chat.id] == "selectingTask":
            if message.text == "Курс":
                hand(message, reply_markup=types.ReplyKeyboardRemove())
                keyboard = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text="coinmarketcap", url="https://coinmarketcap.com/")
                keyboard.add(url_button)
                bot.send_message(message.chat.id, "Нажми на кнопку и перейди на сайт,чтобы посмотреть курс валют.", reply_markup=keyboard)
                states[message.chat.id]="free"#сброс состояние обозначил как free

            elif message.text == "Описание монет":
                bot.send_message(message.chat.id,"Введи /coin и название интересующей тебя монеты. Например /coin Monero ")
                states[message.chat.id] = "free"

            elif message.text == "Новости":
                pass
                save_state(message.chat.id, "news")


            else:
                bot.send_message(message.chat.id,"Вы ввели неправильную команду. Введите /menu и отправьте. После чего выберите команду ")



bot.polling(none_stop=True) #запуск бота

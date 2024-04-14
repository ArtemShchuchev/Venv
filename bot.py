import telebot
import keyboards as kb
import os
TOKEN = os.getenv("TELEG_TOKEN", "00000000")
bot = telebot.TeleBot(TOKEN)


##


@bot.callback_query_handler(func=lambda c: c.data == 'button1')
def process_callback_button1(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('btn'))
def process_callback_kb1btn1(callback_query):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 2:
        bot.answer_callback_query(callback_query.id, text='Нажата вторая кнопка')
    elif code == 5:
        bot.answer_callback_query(
            callback_query.id,
            text='Нажата кнопка с номером 5.\nА этот текст может быть длиной до 200 символов 😉',
            show_alert=True)
    else:
        bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, f'Нажата инлайн кнопка! code={code}')


##


@bot.message_handler(commands=['start'])
def process_start_command(message):
    bot.send_message(message.chat.id, 'Привет!', reply_markup=kb.greet_kb)


@bot.message_handler(commands=['hi1'])
def process_hi1_command(message):
    bot.send_message(message.chat.id, 'Первое - изменяем размер клавиатуры', reply_markup=kb.greet_kb1)


@bot.message_handler(commands=['hi2'])
def process_hi2_command(message):
    bot.send_message(message.chat.id, 'Второе - прячем клавиатуру после одного нажатия', reply_markup=kb.greet_kb2)


@bot.message_handler(commands=['hi3'])
def process_hi3_command(message):
    bot.send_message(message.chat.id, 'Третье - добавляем больше кнопок', reply_markup=kb.markup3)


@bot.message_handler(commands=['hi4'])
def process_hi4_command(message):
    bot.send_message(message.chat.id, 'Четвертое - расставляем кнопки в ряд', reply_markup=kb.markup4)


@bot.message_handler(commands=['hi5'])
def process_hi5_command(message):
    bot.send_message(message.chat.id, 'Пятое - добавляем ряды кнопок', reply_markup=kb.markup5)


@bot.message_handler(commands=['hi6'])
def process_hi6_command(message):
    bot.send_message(message.chat.id, "Шестое - запрашиваем контакт и геолокацию\n"
                        "Эти две кнопки не зависят друг от друга", reply_markup=kb.markup_request)


@bot.message_handler(commands=['hi7'])
def process_hi7_command(message):
    bot.send_message(message.chat.id, 'Седьмое - все методы вместе', reply_markup=kb.markup_big)


@bot.message_handler(commands=['rm'])
def process_rm_command(message):
    bot.send_message(message.chat.id, 'Убираем шаблоны сообщений', reply_markup=telebot.types.ReplyKeyboardRemove())


##


@bot.message_handler(commands=['1'])
def process_command_1(message):
    bot.send_message(message.chat.id, 'Первая инлайн кнопка', reply_markup=kb.inline_kb1)


@bot.message_handler(commands=['2'])
def process_command_2(message):
    bot.send_message(message.chat.id, 'Отправляю все возможные кнопки', reply_markup=kb.inline_kb_full)

help_message = '''
    "Это урок по клавиатурам.",
    "Доступные команды:\n",
    "/start - приветствие",
    "\nШаблоны клавиатур:",
    "/hi1 - авто размер",
    "/hi2 - скрыть после нажатия",
    "/hi3 - больше кнопок",
    "/hi4 - кнопки в ряд",
    "/hi5 - больше рядов",
    "/hi6 - запрос локации и номера телефона",
    "/hi7 - все методы"
    "/rm - убрать шаблоны",
    "\nИнлайн клавиатуры:",
    "/1 - первая кнопка",
    "/2 - сразу много кнопок",
    sep="\n"
'''


@bot.message_handler(commands=['help'])
def process_help_command(message):
    bot.send_message(message.chat.id, help_message)


if __name__ == '__main__':
    bot.infinity_polling()
    
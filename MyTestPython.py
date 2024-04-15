from telebot import TeleBot
from telebot.types import (
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
import random
import os

TOKEN = os.getenv("TELEG_TOKEN", "00000000")
HELP = """
/help(/справка) - эта справка.
/add(/добавь) - добавить задачу в список
\t(ожидаю, время и название задачи)
/show(/покажи) - показать задачи на выбранное время.
/rand(/случайно) - добавить случайную задачу на сегодня"""
RANDOM_TASKS = ["Записаться на курс в Нетологию", "Написать Гвидо письмо", "Покормить кошку", "Помыть машину"]

bot = TeleBot(TOKEN)
# todo = { chatid: { дата: [] } }
todo = {}

###
# commandStr = message.text.split(maxsplit=2)
###


def addTask(chatid, time, task):
    time = time.lower()
    if chatid in todo:
        usertodo = todo[chatid]
        if time in usertodo:
            usertodo[time].append(task)
        else:
            usertodo[time] = [task]


inlineKeys = ['Добавить задачу', "Случайная задача", "Покажи задачи"]

def buttons(isEmptyTodo):
    exceptKey = "Покажи задачи" if isEmptyTodo else ""
    key = [InlineKeyboardButton(txt, callback_data=txt) for txt in inlineKeys if txt != exceptKey]
    keyboard = InlineKeyboardMarkup(row_width=2).add(*key)
    return keyboard


@bot.message_handler(commands=['start'])
def welcome(message):
    first_name = message.from_user.first_name
    chatid = message.chat.id
    
    if chatid not in todo:
        todo[chatid] = {}
        todoEmpty = True
    else:
        todoEmpty = False
    
    mes = '''{}, добро пожаловать в бота "Список дел"!\n
            Выбери необходимую инструкцию.'''.format(first_name)
    bot.send_message(chatid, mes, reply_markup=buttons(todoEmpty))


@bot.callback_query_handler(func=lambda call: call.data == 'Добавить задачу')
def add(callback_query):
    message = callback_query.message
    chatid = message.chat.id
    
    mes = 'Введи время задачи (сегодня, завтра, 12.03.2024...)'
    answer = bot.edit_message_text(chat_id=callback_query.from_user.id,
                          message_id=message.message_id, text=mes)
    bot.register_next_step_handler(answer, dateInput)


def dateInput(message):
    time = message.text.lower()
    mes = 'Введите задачу (купить молоко, отдохнуть...)'
    answer = bot.send_message(message.chat.id, mes)
    bot.register_next_step_handler(answer, taskInput, time)


def taskInput(message, date):
    chatid = message.chat.id
    task = message.text
    addTask(chatid, date, task)
    
    mes = 'Задача "{}" добавлена на {}'.format(task, date)
    bot.send_message(chatid, mes)
    
    mes = 'Выбери необходимую инструкцию.'
    bot.send_message(chatid, mes, reply_markup=buttons(False))


@bot.callback_query_handler(func=lambda call: call.data == 'Случайная задача')
def rand(callback_query):
    message = callback_query.message
    date = 'сегодня'
    task = random.choice(RANDOM_TASKS)
    addTask(message.chat.id, date, task)
    
    mes = 'Задача "{}" добавлена на {}'.format(task, date)
    bot.answer_callback_query(callback_query.id, text=mes)
    
    mes = 'Выбери необходимую инструкцию.'
    if message.text != mes:
        todoEmpty = len(todo[message.chat.id]) == 0
        bot.edit_message_text(chat_id=callback_query.from_user.id,
                              message_id=message.message_id,
                              text=mes, reply_markup=buttons(todoEmpty))


@bot.callback_query_handler(func=lambda call: call.data == 'Покажи задачи')
def show(callback_query):
    message = callback_query.message
    chatid = message.chat.id
    
    bot.edit_message_text(chat_id=callback_query.from_user.id,
                          message_id=message.message_id, text=('-' * 9))
    key = [KeyboardButton(txt) for txt in todo[chatid].keys()]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*key)
    bot.send_message(chatid, 'Выбери интересующее время...', reply_markup=keyboard)
    
    bot.register_next_step_handler(message, dateChoice)
    

def dateChoice(message):
    chatid = message.chat.id
    usertodo = todo[chatid]
    time = message.text.lower()
    mes = 'Список задач на {}:'.format(time)
    if time in usertodo:
        for task in usertodo[time]:
            mes += '\n- ' + task
    bot.send_message(chatid, mes, reply_markup=ReplyKeyboardRemove())
    mes = 'Выбери необходимую инструкцию.'
    todoEmpty = len(todo[message.chat.id]) == 0
    bot.send_message(chatid, mes, reply_markup=buttons(todoEmpty))


if __name__ == '__main__':
    print('Бот запущен!')
    bot.infinity_polling()
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


def addTask(chatid, time, task):
    time = time.lower()
    
    if chatid in todo:
        usertodo = todo[chatid]
        if time in usertodo:
            usertodo[time].append(task)
        else:
            usertodo[time] = [task]
    #else:
    #    todo[chatid] = {time: [task]}
    
    #mes = 'Задача "{}" добавлена на {}'.format(task, time)
    #bot.send_message(chatid, mes)


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
    

@bot.message_handler(commands=['help', 'справка'])
def help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['add', 'todo', 'добавь'])
def add(message):
    commandStr = message.text.split(maxsplit=2)
    date = commandStr[1]
    task = commandStr[2]
    addTask(message.chat.id, date, task) 


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
    
    key = [KeyboardButton(txt) for txt in todo[chatid].keys()]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*key)
        
    #bot.send_message(chatid, 'Выбери интересующее время...', reply_markup=keyboard)
    
    mes = 'Выбери интересующее время...'
    bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=message.message_id, text='...')
    
    #bot.register_next_step_handler(message, dateChoice)
    chatid = message.chat.id
    if len(todo[chatid]) == 0:
        bot.send_message(chatid, 'Список задач пуст!')
    else:
        #bot.send_message(chatid, 'Есть задачи на:')
        #for time in todo[chatid].keys():
        #    mes = '* ' + time
        #    bot.send_message(chatid, mes)
        #bot.send_message(chatid, 'Напиши интересующее время...')
        #bot.register_next_step_handler(message, dateChoice)
        
        #keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        key = [KeyboardButton(txt) for txt in todo[chatid].keys()]
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*key)
        
        #key = list()
        #for time in todo[chatid].keys():
        #    key.append(KeyboardButton(text=str(time)))
        #
        #for k in key:
        #    keyboard.add(k)
            
        bot.send_message(chatid,
                     'Выбери интересующее время...',
                     reply_markup=keyboard)
        
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
    # Постоянно обращается к серверам телеграм
    bot.infinity_polling()
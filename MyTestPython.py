import telebot
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
    
    mes = 'Задача "{}" добавлена на {}'.format(task, time)
    bot.send_message(chatid, mes)
    
    

bot = telebot.TeleBot(TOKEN)

def buttons(message):
    #bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='...')
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_rand = telebot.types.InlineKeyboardButton(text="Случайная задача",
                                                     callback_data='добавить случайную задачу')
    button_show = telebot.types.InlineKeyboardButton(text="Покажи задачи",
                                                     callback_data='Покажи задачи')
    
    keyboard.add(button_rand, button_show)
    mes = message.text + 'Выбери необходимую инструкцию.'
    bot.send_message(message.chat.id, mes, reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def welcome(message):
    first_name = message.from_user.first_name
    chatid = message.chat.id
    todo[chatid] = {}
    message.text = '{}, добро пожаловать в бота "Список дел"!'.format(first_name)
    #bot.send_message(chatid, '{}, добро пожаловать в бота "Список дел"!'.format(first_name))
    #bot.send_message(message.chat.id, HELP)
    buttons(message)
    
@bot.message_handler(commands=['help', 'справка'])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=['add', 'todo', 'добавь'])
def add(message):
    commandStr = message.text.split(maxsplit=2)
    date = commandStr[1]
    task = commandStr[2]
    addTask(message.chat.id, date, task) 

@bot.callback_query_handler(func=lambda call: call.data == 'добавить случайную задачу')
def rand(callback_query):
    message = callback_query.message
    chatid = callback_query.from_user.id
    bot.answer_callback_query(callback_query.id)
    messageid = message.message_id
    
    
    
    date = 'сегодня'
    task = random.choice(RANDOM_TASKS)
    addTask(message.chat.id, date, task)
    #bot.edit_message_text(chat_id=chatid, message_id=messageid, text='...')
    buttons(message)

@bot.message_handler(func=lambda message: message.text == 'Покажи задачи')
def show(message):
    chatid = message.chat.id
    usertodo = todo[chatid]
    if len(usertodo) == 0:
        bot.send_message(chatid, 'Список задач пуст!')
    else:
        #bot.send_message(chatid, 'Есть задачи на:')
        #for time in usertodo.keys():
        #    mes = '* ' + time
        #    bot.send_message(chatid, mes)
        #bot.send_message(chatid, 'Напиши интересующее время...')
        #bot.register_next_step_handler(message, dateChoice)
        
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        key = list()
        for time in usertodo.keys():
            key.append(telebot.types.KeyboardButton(text=str(time)))
        
        for k in key:
            keyboard.add(k)
            
        bot.send_message(chatid,
                     'Выбери интересующее время...',
                     reply_markup=keyboard)
        
        bot.register_next_step_handler(message, dateChoice)
    
def dateChoice(message):
    chatid = message.chat.id
    usertodo = todo[chatid]
    time = message.text.lower()
    keyboard = telebot.types.ReplyKeyboardRemove()
    mes = 'Список задач на ' + time
    bot.send_message(chatid, mes, reply_markup=keyboard)
    if time in usertodo:
        for task in usertodo[time]:
            mes = '- ' + task
            bot.send_message(chatid, mes)
    else:
        bot.send_message(chatid, 'Нет задач на: {}'.format(time))

if __name__ == '__main__':
    print('Бот запущен!')
    # Постоянно обращается к серверам телеграм
    bot.infinity_polling()
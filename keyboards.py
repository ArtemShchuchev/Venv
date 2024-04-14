from telebot import types

button_hi = types.KeyboardButton('Привет! 👋')

greet_kb = types.ReplyKeyboardMarkup()
greet_kb.add(button_hi)

greet_kb1 = types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_hi)

greet_kb2 = types.ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True).add(button_hi)

button1 = types.KeyboardButton('1️⃣')
button2 = types.KeyboardButton('2️⃣')
button3 = types.KeyboardButton('3️⃣')

markup3 = types.ReplyKeyboardMarkup().add(
    button1).add(button2).add(button3)

markup4 = types.ReplyKeyboardMarkup().row(
    button1, button2, button3)

markup5 = types.ReplyKeyboardMarkup().row(
    button1, button2, button3).add(types.KeyboardButton('Средний ряд'))

button4 = types.KeyboardButton('4️⃣')
button5 = types.KeyboardButton('5️⃣')
button6 = types.KeyboardButton('6️⃣')
markup5.row(button4, button5)
markup5.add(button6)

markup_request = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
).add(types.KeyboardButton('Отправить свою локацию 🗺️', request_location=True))

markup_big = types.ReplyKeyboardMarkup()

markup_big.add(button1, button2, button3, button4, button5, button6)
markup_big.row(button1, button2, button3, button4, button5, button6)

markup_big.row(button4, button2)
markup_big.add(button3, button2)
markup_big.add(button1)
markup_big.add(button6)
markup_big.add(types.KeyboardButton('9️⃣'))

inline_btn_1 = types.InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = types.InlineKeyboardMarkup().add(inline_btn_1)

inline_kb_full = types.InlineKeyboardMarkup(row_width=2).add(inline_btn_1)
inline_kb_full.add(types.InlineKeyboardButton('Вторая кнопка', callback_data='btn2'))
inline_btn_3 = types.InlineKeyboardButton('кнопка 3', callback_data='btn3')
inline_btn_4 = types.InlineKeyboardButton('кнопка 4', callback_data='btn4')
inline_btn_5 = types.InlineKeyboardButton('кнопка 5', callback_data='btn5')
inline_kb_full.add(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.row(inline_btn_3, inline_btn_4, inline_btn_5)
inline_kb_full.add(types.InlineKeyboardButton("query=''", switch_inline_query=''))
inline_kb_full.add(types.InlineKeyboardButton("query='qwerty'", switch_inline_query='qwerty'))
inline_kb_full.add(types.InlineKeyboardButton("Inline в этом же чате", switch_inline_query_current_chat='wasd'))
inline_kb_full.add(types.InlineKeyboardButton('Уроки aiogram', url='https://surik00.gitbooks.io/aiogram-lessons/content/'))

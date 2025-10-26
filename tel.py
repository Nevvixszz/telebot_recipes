import telebot
from telebot import types
bot = telebot.TeleBot("8367813428:AAHFnC_nl_kyToj51RC-E_N3TKPQU6Yc88U")
user_choice = {}
from salats import salat

def keybord():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn3 = types.KeyboardButton('🔍 Поиск по ID')
    keyboard.add(btn3)
    return keyboard
@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id, "Привет!\n\nЯ - твой помощник по еде!\n\nХочешь начать готовить? Нажимай на /food или на клавиатуру снизу.", reply_markup=keybord())
@bot.message_handler(func=lambda message: message.text == '🔍 Поиск по ID')
def search_button(message):
    send(message)
@bot.message_handler(commands=['food'])
def send(message):
    markup = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton("Выпечка", callback_data="Выпечка")
    but2 = types.InlineKeyboardButton("Салаты", callback_data="Салаты")
    but3 = types.InlineKeyboardButton("Основные блюда", callback_data="Основные блюда")
    markup.add(but1, but2)
    markup.add(but3)
    bot.send_message(message.chat.id, "Введите категорию", reply_markup=markup)
@bot.callback_query_handler(func=lambda call: True)
def ide(call):
    category = call.data
    user_choice[call.from_user.id] = category
    avaible_foods = []
    for id, food in salat.items():
        if food['category'] == category:
            avaible_foods.append(f"{id}. {food['name']}")
    foods_text = "\n".join(avaible_foods)
    bot.send_message(call.message.chat.id, f"Введите ID {category}:\n\nДоступные Блюда: {foods_text}", reply_markup=keybord())
@bot.message_handler(content_types=['text'])
def send_salat(message):
    user_id = message.from_user.id
    if user_id not in user_choice:
        bot.send_message(message.chat.id, "Сначала выберите категорию через /food", reply_markup=keybord())
        return
    try:
        food_id = int(message.text)
        category = user_choice[user_id]
        if food_id in salat and salat[food_id]['category'] == category:
            food_data = salat[food_id]
            response = f"{food_data['name'].upper()}\n\n"
            response += f"{food_data['url']}\n\n"
            response += f"{food_data['recipe']}"
            bot.send_message(message.chat.id, response, reply_markup=keybord())
        else:
            bot.send_message(message.chat.id, f"Блюдо не найдено в категории {category}", reply_markup=keybord())
    except ValueError:
        bot.send_message(message.chat.id, "Нет такого ID!")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

bot.polling()
import telebot
from telebot import types
import random
import time

token = "7559557907:AAE0ya-hXv5r4kIPbWk7I6FUzezRHvK_JR0"

# Создание экземпляра бота
bot = telebot.TeleBot(token)

is_choice_done = False
is_text_input = False
is_algoritm_done = False
current_text = ""
text_history = [] # история текстов


"""Обработчик команды /start"""
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!\nЗдесь ты можешь посчитать количество палиндромов в тексте")

"""Обработчик команды /input"""
@bot.message_handler(commands=['input'])
def button_message(message):
    #Создаем клавиатуру и добавляем туда кнопки выбора
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Задать текст самостоятельно')
    markup.add('Сгенерировать текст')
    bot.send_message(message.chat.id, "Выбери тип ввода текста", reply_markup=markup)
    bot.register_next_step_handler(message, select_and_input)


"""Обработчик нажатий на кнопки"""
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global current_text
    if call.data == "change_text":
        bot.send_message(call.message.chat.id, f"Измените текст: {current_text}")
        bot.register_next_step_handler(call.message, process_input_text)
    elif call.data == "process_text":
        bot.send_message(call.message.chat.id, "Алгоритм выполняется...")
        time.sleep(2)  # Имитация задержки
        bot.delete_message(call.message.chat.id, call.message.message_id)
        find_palindromes(call.message, current_text)
    elif call.data == "new_text":
        button_message(call.message)


"""Обработка команды /history"""
@bot.message_handler(commands=['history'])
def show_history(message):
    if text_history:
        history_text = "\n\n".join(f"{i+1}. {text}" for i, text in enumerate(text_history))
        bot.send_message(message.chat.id, f"История задания текстов:\n\n{history_text}")
    else:
        bot.send_message(message.chat.id, "История задания текстов пуста.")



"""Выбор типа ввода текста и его ввод"""
def select_and_input(message):
    text = message.text
    if text == 'Задать текст самостоятельно':
        bot.send_message(message.chat.id, "Введите текст для обработки:")
        bot.register_next_step_handler(message, process_input_text)
    elif text == 'Сгенерировать текст':
        letter = random_text()
        global current_text
        current_text = letter
        text_history.append(letter)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(text="Отправить текст на обработку", callback_data="process_text"))
        bot.send_message(message.chat.id, f"Сгенерированный текст: {letter}", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Ошибка выбора, попробуй еще раз")


"""Ввод с клавиатуры"""
def process_input_text(message):
    global current_text
    current_text = message.text
    text_history.append(current_text)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Изменить текст", callback_data="change_text"))
    markup.add(types.InlineKeyboardButton(text="Отправить текст на обработку", callback_data="process_text"))
    bot.send_message(message.chat.id, f"Вы ввели следующий текст:{current_text}", reply_markup=markup)

"""Генерация текста"""
def random_text():
    letters = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ '
    length = random.randint(20, 100)  # Генерация случайной длины
    return ''.join(random.choice(letters) for _ in range(length))

"""Алгоритм нахождения палиндромов"""
def find_palindromes(message, text):
    words = text.split()
    palindromes = [word for word in words if word.lower() == word.lower()[::-1]]
    if palindromes:
        bot.send_message(message.chat.id, f"Палиндромы в тексте:{', '.join(palindromes)}")
    else:
        bot.send_message(message.chat.id, "Список палиндромов пуст.")

    # Добавляем кнопку для задания нового текста
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Задать новый текст", callback_data="new_text"))
    bot.send_message(message.chat.id, "Хотите задать новый текст?", reply_markup=markup)

bot.infinity_polling()

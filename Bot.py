import telebot
from telebot import types

# Инициализация бота с токеном
bot = telebot.TeleBot('8865048374:AAFfd25GaQgNWOrv39-g3FWN0gbB5DHRXt8')  # Замените на свой

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я Огонёк. Напишите что-нибудь, и я отправлю ваше сообщение администрации, а потом пришлю вам их ответ!")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(message.chat.id, f"Вы написали: {message.text}")

# Запуск бота
bot.polling(none_stop=True, interval=0)
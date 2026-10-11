import telebot

# ⚠️ Отзови старый токен у @BotFather и вставь новый сюда
BOT_TOKEN = '8865048374:AAFfd25GaQgNWOrv39-g3FWN0gbB5DHRXt8'

bot = telebot.TeleBot(BOT_TOKEN)


# ====== НАСТРОЙКИ КОМАНД ======
# Ключ — что пишет пользователь, значение — что отвечает бот
REPLIES = {
    '!правила': "📜 <b>Правила чата:</b>\nhttps://example.com/rules",
    #'!faq':     "❓ <b>FAQ:</b>\nhttps://example.com/faq",
    #'!админы':  "👮 <b>Администрация:</b>\n@admin1, @admin2",
}
# ==============================


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я Огонёк. Напишите что-нибудь, и я отправлю ваше "
        "сообщение администрации, а потом пришлю вам их ответ!"
    )


@bot.message_handler(func=lambda m: m.text and m.text.strip().lower() in REPLIES)
def handle_commands(message):
    key = message.text.strip().lower()
    bot.send_message(
        message.chat.id,
        REPLIES[key],
        parse_mode='HTML',
        disable_web_page_preview=False
    )


bot.polling(none_stop=True)
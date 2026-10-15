import os
import telebot

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])

# ⚠️ ID админского чата (с минусом, например -1001234567890)
ADMIN_CHAT_ID = -4611124047

bot = telebot.TeleBot(BOT_TOKEN)

# ====== ПАМЯТЬ: сообщение в админ-чате -> ID игрока ======
# Ключ: message_id сообщения в админ-чате
# Значение: chat_id игрока в ЛС
forward_map = {}
# ========================================================


# ====== КОМАНДЫ ======
REPLIES = {
    '!ФЫР': "<b>Фыр фыр</b>",
    '!правила': "📜 <b>Правила чата:</b>\nhttps://teletype.in/@seventhpass/TgRulesSP",
    #'!сервер':     "🔥 <b>Наш сервер:</b>\nhttps://seventhpass.site/",
    #'!админы':  "👮 <b>Администрация:</b>\n@admin1, @admin2",
}


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я Огонёк. Напишите мне что угодно, и я передам "
        "ваше сообщение администрации, а потом пришлю их ответ!"
    )


# ====== 1. Сообщения из ГРУПП (команды типа !правила) ======
@bot.message_handler(
    func=lambda m: (
        m.chat.type in ('group', 'supergroup')
        and m.text
        and m.text.strip().lower() in REPLIES
    )
)
def handle_group_commands(message):
    key = message.text.strip().lower()
    bot.send_message(
        message.chat.id,
        REPLIES[key],
        parse_mode='HTML'
    )


# ====== 2. Ответ админа в админ-чате (reply на пересланное) ======
@bot.message_handler(
    func=lambda m: (
        m.chat.id == ADMIN_CHAT_ID
        and m.reply_to_message is not None
        and m.reply_to_message.message_id in forward_map
    ),
    content_types=['text', 'photo', 'video', 'document', 'sticker', 'voice']
)
def admin_reply(message):
    player_id = forward_map[message.reply_to_message.message_id]

    try:
        # Пересылаем ответ админа игроку (сохраняя reply-связь)
        bot.copy_message(
            chat_id=player_id,
            from_chat_id=message.chat.id,
            message_id=message.message_id
        )
        bot.reply_to(message, "✅ Ответ отправлен игроку")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Не удалось отправить: {e}")


# ====== 3. Личка: игрок пишет боту ======
@bot.message_handler(
    func=lambda m: m.chat.type == 'private',
    content_types=['text', 'photo', 'video', 'document', 'sticker', 'voice']
)
def from_player(message):
    # Игнорируем команды вроде /start
    if message.text and message.text.startswith('/'):
        return

    username = f"@{message.from_user.username}" if message.from_user.username else "без username"
    name = message.from_user.full_name

    header = (
        f"📩 <b>Сообщение от игрока</b>\n"
        f"👤 {name} ({username})\n"
        f"🆔 <code>{message.from_user.id}</code>\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"👇 <i>Ответьте reply'ом на это сообщение</i>"
    )

    # Отправляем заголовок в админ-чат
    bot.send_message(ADMIN_CHAT_ID, header, parse_mode='HTML')

    # Пересылаем само сообщение игрока
    sent = bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id
    )

    # Запоминаем: это сообщение в админке -> этот игрок
    forward_map[sent.message_id] = message.chat.id

    bot.reply_to(message, "✅ Ваше сообщение отправлено администрации. Ожидайте ответа!")


bot.polling(none_stop=True)
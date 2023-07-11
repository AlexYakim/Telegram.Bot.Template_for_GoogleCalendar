import telebot

bot = telebot.TeleBot('This_must_be_TelegramBot`s_access_Token')


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = telebot.types.InlineKeyboardMarkup()

    get_event_btn = telebot.types.InlineKeyboardButton('Get events', callback_data='events')
    send_event_btn = telebot.types.InlineKeyboardButton('Set events', callback_data='send')
    markup.add(send_event_btn, get_event_btn)
    auth_btn = telebot.types.InlineKeyboardButton('Authorisation', callback_data='auth')
    markup.add(auth_btn)
    bot.send_message(message.chat.id,
                     f"Hi! How I`m may help you {message.from_user.first_name} ?",
                     reply_markup=markup)


bot.polling(non_stop=True)

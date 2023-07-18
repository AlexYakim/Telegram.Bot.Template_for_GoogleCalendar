import telebot
import sqlite3

bot = telebot.TeleBot('This_must_be_TelegramBot`s_access_Token')

SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']

connectDB = sqlite3.connect('Creds_Data_Base.db')
cursorDB = connectDB.cursor()
cursorDB.execute('CREATE TABLE IF NOT EXISTS CredsDT('
                            'Telegram_ID TEXT PRIMARY KEY,'
                            'user_name TEXT, '
                            'PickleCreds BLOB)')
connectDB.commit()
connectDB.close()


@bot.message_handler(commands=['start'])
def start_bot(message):
    markup = telebot.types.InlineKeyboardMarkup()

    connect = sqlite3.connect('Creds_Data_Base.db')
    cursor = connect.cursor()
    result = cursor.execute('SELECT'
                            ' CASE'
                            ' WHEN COUNT(*) = 0 THEN 0'
                            ' WHEN COUNT(*) != 0 AND Telegram_ID = ? THEN 1'
                            ' END'
                            ' FROM CredsDT', (message.chat.id,))
    result = result.fetchone()
    if result is not None and result[0] == 1:
        get_event_btn = telebot.types.InlineKeyboardButton('Get events', callback_data='events')
        send_event_btn = telebot.types.InlineKeyboardButton('Set events', callback_data='send')
        markup.add(send_event_btn, get_event_btn)
    else:
        auth_btn = telebot.types.InlineKeyboardButton('Authorisation', callback_data='auth')
        markup.add(auth_btn)
    bot.send_message(message.chat.id,
                     f"Hi! How I`m may help you {message.from_user.first_name} ?",
                     reply_markup=markup)
    connect.close()


@bot.callback_query_handler(func=lambda call: call.data == 'auth')
def auth(call):
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    first_name = call.message.chat.first_name
    if (call.message.chat.last_name != None):
        last_name = call.message.chat.last_name
        first_name += ' ' + last_name
    connect = sqlite3.connect('Creds_Data_Base.db')
    cursor = connect.cursor()
    pickle_file = pickle.dumps(creds)
    cursor.execute('INSERT INTO CredsDT(Telegram_ID,user_name, PickleCreds)'
                   'VALUES(?,?,?);', (call.message.chat.id, first_name + ' ', pickle_file))
    connect.commit()
    connect.close()


@bot.callback_query_handler(func=lambda call: call.data == 'events')
def get_events(call):
    pass


@bot.callback_query_handler(func=lambda call: call.data == 'send')
def send_event(call):
    pass


bot.polling(non_stop=True)

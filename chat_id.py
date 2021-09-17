import telebot

bot = telebot.TeleBot("2014175408:AAHLiO-80uvjVL2qNbybs6FaVSmwlFUU6iY")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"Ваш chat_id: {message.chat.id}\nУкажите его в соответствующем поле в конфиге")
    print("chat_id был выслан в ваш телеграм")
    bot.stop_bot()

bot.polling()
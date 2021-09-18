import telebot, json
TOKEN = None
config = {
    "time" : "16:00",
    "login" : "yourlogin",
    "password" : "yourpassword",
    "chat_id" : None,
    "TOKEN" : TOKEN,
    "mode" : 1
}


try: #Загрузка конфига
    with open("config.json", "r") as f:
        config = json.load(f)
        TOKEN = config["TOKEN"]

except:
    with open("config.json", "w") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"Ваш chat_id: {message.chat.id}\nУкажите его в соответствующем поле в конфиге")
    print("chat_id был выслан в ваш телеграм")
    bot.stop_bot()

bot.polling()
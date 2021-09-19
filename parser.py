from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from telebot.types import Message
import telebot
import time
import json

time_take = "16:00"
login = "yourlogin"
password = "yourpassword"
chat_id = None
TOKEN = None
mode = 1
mode_bool = True
config = {
    "time" : time_take,
    "login" : login,
    "password" : password,
    "chat_id" : chat_id,
    "TOKEN" : TOKEN,
    "mode" : mode
}

try: #Загрузка конфига
    with open("config.json", "r") as f:
        config = json.load(f)
        time_take = config["time"]
        login = config["login"]
        password = config["password"]
        chat_id = config["chat_id"]
        TOKEN = config["TOKEN"]
        mode = config["mode"]

except:
    with open("config.json", "w") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

if login == "yourlogin" or password == "yourpassword" or chat_id == None or TOKEN == None:
    print("Смените значение логина, пароля, chat_id и TOKEN в конфиге")
    quit()

if mode == 2:
    mode_bool = False

bot = telebot.TeleBot(TOKEN) #Создание бота
print("Ожидание назначенного времени")
while True:
    if datetime.now().strftime("%H:%M") == time_take or mode_bool == True:
        day = datetime.today().isoweekday() #Получения дня недели
        driver = webdriver.Chrome(ChromeDriverManager().install())
        url = "https://eljur.gospmr.org/authorize?return_uri=%2Fjournal-app" #Адрес сайта
        xpath_column = f"/html/body/div[1]/div[2]/main/div/div[2]/div/div[1]/div[2]/div[2]/div/div[2]/div/div[{day}]" #Xpath колонки оценок

        driver.get(url)
        driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[1]/div/input').send_keys(login) #Отправка логина
        driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[2]/div/input').send_keys(password) #Отправка пароля
        driver.find_element_by_xpath('//*[@id="loginviewport"]/div/div/form/div[2]/button').click()

        time.sleep(3)
        driver.get("https://eljur.gospmr.org/journal-student-grades-action/u.2025")
        time.sleep(3)
        file = open("appraisals.txt", "w", encoding="UTF-8")
        for x in range(100):
            x += 1
            try:
                name = driver.find_element_by_xpath(f"{xpath_column}/div[{x}]").get_attribute("name") #Поиск элемента по xpath и получение атрибута name
                appraisals = driver.find_element_by_xpath(f"{xpath_column}/div[{x}]/div[1]").text #Поиск элемента по xpath, получение атрибута text
                if appraisals == " ": #Проверка на пустое значение
                    appraisals = "None"
                file.write(f"{name}: {appraisals}\n")
                print(f"{name}: {appraisals}")
                
            except:
                break
        file.close()
        with open("appraisals.txt", "r", encoding="UTF-8") as f:
            bot.send_message(chat_id, f.read()) #Отправка сообщения в телеграм

        driver.close()
        print("Выполненно")

        if mode == 1:
            quit()

        print("Ожидание следующего цикла")
        time.sleep(70)

    else:
        try: #Проверка обновления конфига
            with open("config.json", "r") as f:
                config = json.load(f)
                time_take = config["time"]

        except:
            with open("config.json", "w") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

        time.sleep(30)


bot.polling()
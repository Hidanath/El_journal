from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from telebot.types import Message
import telebot
import time
import json

url = "https://eljur.gospmr.org/authorize?return_uri=%2Fjournal-app" #Адрес сайта
sunday = True 
time_take = "16:00" #Время
login = "yourlogin" #Логин
password = "yourpassword" #Пароль
chat_id = None #Chat id бота
TOKEN = None #Токен бота
mode = 1 #Режим работы 1 - одноразовый запуск,2 - по времени
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

if login == "yourlogin" or password == "yourpassword" or chat_id == None or TOKEN == None: #Проверки на пустые значения
    print("Смените значение логина, пароля, chat_id и TOKEN в конфиге")
    exit()

bot = telebot.TeleBot(TOKEN) #Создание бота

if mode == 2:
    mode_bool = False
    print("Ожидание назначенного времени")
else:
    print("Успешный запуск")

while True:
    if datetime.now().strftime("%H:%M") == time_take or mode_bool == True:
        day = datetime.today().isoweekday() #Получения дня недели
        day_now = day

        if day == 7: #Обработка воскресенья
            if sunday: #Проверка переключателя
                if mode == 1: #Если режим 1 выход из программы
                    print("Исключение воскресенье")
                    exit()

                sunday = False #Смена переключателя
                print("Исключение воскресенье")
                continue

            else:
                try: #Проверка обновления конфига
                    with open("config.json", "r") as f:
                        config = json.load(f)
                        time_take = config["time"]

                except:
                    with open("config.json", "w") as f:
                        json.dump(config, f, ensure_ascii=False, indent=4)

                time.sleep(30)
                continue
        
        sunday = True #Смена переключателя
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[1]/div/input').send_keys(login) #Отправка логина
        driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div/form/div[1]/div[2]/div/input').send_keys(password) #Отправка пароля
        driver.find_element_by_xpath('//*[@id="loginviewport"]/div/div/form/div[2]/button').click()

        time.sleep(3)
        file = open("marks.txt", "w", encoding="UTF-8")
        for x in range(100):
            x += 1
            try: #Сработает если закончаться предметы
                if day >= 2:
                    day_now = day + 1

                section = driver.find_element_by_xpath(f"/html/body/div[1]/div[2]/main/div/div[2]/div/div[2]/div/div[3]/div[{day_now}]/div[2]/div[{x}]") 
                try: #Сработает если оценки нет
                    name = section.find_element_by_xpath("./div[2]/span").text #Получение названия предмета
                    mark = section.find_element_by_xpath("./div[3]/div/div").get_attribute("value") #Получение оценки
                    print(f"{name}: {mark}")
                    file.write(f"{name}: {mark}\n")

                except:
                    pass
                
            except:
                break
        file.close()
        with open("marks.txt", "r", encoding="UTF-8") as f:
            if f.read() == "":
                bot.send_message(chat_id, "Ты сегодня не получил оценок")
            else:
                bot.send_message(chat_id, f.read()) #Отправка сообщения в телеграм

        driver.close()
        print("Выполненно")

        if mode == 1:
            exit()

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
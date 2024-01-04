import requests
import datetime
import telebot;

bot = telebot.TeleBot('6757266848:AAGYeXGinI_2xkGRpCFxhipygiFWNJQKml8'); 

# Задаем координаты населенного пункта 
lat = 55.75396 # широта Москвы 
lon = 37.620393 # долгота Москвы 

# Задаем параметры запроса 
params = { 
    'lat': lat, 
    'lon': lon, 
    'lang': 'ru_RU', # язык ответа 
    'limit': 7, # срок прогноза в днях 
    'hours': True, # наличие почасового прогноза 
    'extra': True # подробный прогноз осадков 
} 



# Задаем значение ключа API 
api_key = '43ebef2e-f9f9-4e1e-aba5-90ef543722a6' 

# Задаем URL API 
url = 'https://api.weather.yandex.ru/v2/forecast' 

# Делаем запрос к API 

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    #print(message.text)
    if message.text == "/start":
        bot.send_message(message.from_user.id, f'Приветсвую в нашем маленьком боте. Воспользуйся меню чтобы увидеть команды.')
    elif message.text == "/command1":
        today = datetime.datetime.today()
        now = today.strftime('%d.%m.%Y') # дата в формате Д.М.Г
        print(now)
        response = requests.get(url, params=params, headers={'X-Yandex-API-Key': api_key})
        if response.status_code == 200: 
        # Преобразуем ответ в JSON формат 
            data = response.json() 
            # Выводим данные о текущей погоде 
            #bot.send_message(message.from_user.id, f'Температура воздуха: {data["fact"]["temp"]} °C\nОщущается как: {data["fact"]["feels_like"]} °C\nПогодное описание: {data["fact"]["condition"]}') 
            #Считаем суточные осадки
            prec_total = 0
            today_prec_morning = data["forecasts"]["date" == now]["parts"]["morning"]["prec_mm"]
            #print(today_prec_morning)
            today_prec_day = data["forecasts"]["date" == now]["parts"]["day"]["prec_mm"]
            #print(today_prec_day)
            today_prec_night = data["forecasts"]["date" == now]["parts"]["night"]["prec_mm"]
            #print(today_prec_night)
            prec_total = today_prec_morning + today_prec_day + today_prec_night
            #print(prec_total)
            
            if  prec_total == 0:
 # Выводим данные о текущей погоде 
                bot.send_message(message.from_user.id, f'Температура воздуха: {data["fact"]["temp"]} °C\nОщущается как: {data["fact"]["feels_like"]} °C\nПогодное описание: {data["fact"]["condition"]}\nОжидаемые осадки сегодня: ' + str(prec_total) + 'mm\nСегодня можно и на мойку заехать') 
                #bot.send_message(message.from_user.id, f'Ожидаемые осадки сегодня: ' + str(prec_total) + 'mm')
                #bot.send_message(message.from_user.id, 'Сегодня можно и на мойку заехать')
            else:
                bot.send_message(message.from_user.id, f'Температура воздуха: {data["fact"]["temp"]} °C\nОщущается как: {data["fact"]["feels_like"]} °C\nПогодное описание: {data["fact"]["condition"]}\nОжидаемые осадки сегодня: ' + str(prec_total) + 'mm\nНу помытся конечно можно, но ты дороги видел? ') 
                #bot.send_message(message.from_user.id, f'Ожидаемые осадки сегодня: ' + str(prec_total) + 'mm')
                #bot.send_message(message.from_user.id, 'Ну помытся конечно можно, но ты дороги видел?')
            bot.send_message(message.from_user.id, 'Данные получены из сервиса Яндекс.Погода')
        else: 
            # Выводим код ошибки 
            print(f'Ошибка: {response.status_code}')
    else:
        bot.send_message(message.from_user.id, 'Ой, я тебя не понял, воспользуйся меню пожалуйста')

bot.polling(none_stop=True, interval=0)



# Проверяем статус ответа 

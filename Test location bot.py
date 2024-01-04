import requests
import datetime
import telebot;
# API бота в ТГ
bot = telebot.TeleBot('6853640241:AAFJ9ouD8jf44dviH6TbZRQwo4LA7szyy5o'); 

#получение города из переменной cords (Координаты или название)
def get_address_from_coords(input_coords):
    PARAMS = {
        "apikey": "cbe3ba4d-a3b9-4b22-9ff1-5d7a8d136a57",   #API геокодера яндекс
        "format": "json",
        "lang": "ru_RU",
        "kind": "locality",
        "geocode": input_coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        out_coords = json_data["response"]["GeoObjectCollection"]["featureMember"]["GeoObject"]["Point"]["pos"]
        return out_coords

    except Exception as e:
        #единственное что тут изменилось, так это сообщение об ошибке.
        return "Не могу определить адрес по этой локации/координатам.\nОтправь мне локацию или координаты (долгота, широта):"

# Задаем параметры запроса 
params = { 
    #'lon': lon, 
    #'lang': 'ru_RU', # язык ответа 
    'limit': 7, # срок прогноза в днях 
    'hours': True, # наличие почасового прогноза 
    'extra': True # подробный прогноз осадков 
} 

def start(update, context):
    #эта строка отправляет сообщение пользователю с просьбой послать локацию или координаты
    update.message.reply_text('Отправь мне локацию или координаты (долгота, широта):')



def location(update, context):
    #получаем обьект сообщения (локации)
    message = update.message
    #вытаскиваем из него долготу и ширину
    current_position = (message.location.longitude, message.location.latitude)
    #создаем строку в виде ДОЛГОТА,ШИРИНА
    coords = f"{current_position[0]},{current_position[1]}"
    #отправляем координаты в нашу функцию получения адреса
    address_str = get_address_from_coords(coords)
    #вовщращаем результат пользователю в боте
    update.message.reply_text(address_str)

# Задаем значение ключа API Яндекс погоды
api_key = '43ebef2e-f9f9-4e1e-aba5-90ef543722a6' 

# Задаем URL API 
url = 'https://api.weather.yandex.ru/v2/forecast' 

# Делаем запрос к API 

@bot.message_handler(content_types=['text'])
def text(update, context):
    #получаем текст от пользователя
    coords = update.message.text
    #отправляем текст в нашу функцио получения адреса из координат
    address_str = get_address_from_coords(coords)
    #вовщращаем результат пользователю в боте
    update.message.reply_text(address_str)

@bot.message_handler(content_types=['location'])
def location(update, context):
    #получаем обьект сообщения (локации)
    message = update.message
    #вытаскиваем из него долготу и ширину
    current_position = (message.location.longitude, message.location.latitude)
    #создаем строку в виде ДОЛГОТА,ШИРИНА
    coords = f"{current_position[0]},{current_position[1]}"
    #отправляем координаты в нашу функцию получения адреса
    address_str = get_address_from_coords(coords)
    #вовщращаем результат пользователю в боте
    update.message.reply_text(address_str)


bot.polling(none_stop=True, interval=5)
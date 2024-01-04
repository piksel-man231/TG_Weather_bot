#Подлкючаем библиотеку requests
import requests
#Подключаем нужные для бота модули из библиотеки telegram.ext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

#это наша функция для получения адреса по координатам. С ней мы знакомы.
def get_address_from_coords(coords):
    PARAMS = {
        "apikey": "cbe3ba4d-a3b9-4b22-9ff1-5d7a8d136a57",
        "format": "json",
        "lang": "ru_RU",
        "kind": "house",
        "geocode": coords
    }

    try:
        r = requests.get(url="https://geocode-maps.yandex.ru/1.x/", params=PARAMS)
        json_data = r.json()
        address_str = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"][
            "GeocoderMetaData"]["AddressDetails"]["Country"]["AddressLine"]
        return address_str

    except Exception as e:
        #единственное что тут изменилось, так это сообщение об ошибке.
        return "Не могу определить адрес по этой локации/координатам.\n\nОтправь мне локацию или координаты (долгота, широта):"


#Эта функция будет использоваться когда человек первый нажал в боте START
def start(update, context):
    #эта строка отправляет сообщение пользователю с просьбой послать локацию или координаты
    update.message.reply_text('Отправь мне локацию или координаты (долгота, широта):')

#Эта функция будет использоваться, если пользователь послал в бота любой текст.
#Мы ожидаем координаты, но если прийдет что-то другое не страшно, ведь мы описали в функции получения адреса возвращение ошибки в случае чего.  
def text(update, context):
    #получаем текст от пользователя
    coords = update.message.text
    #отправляем текст в нашу функцио получения адреса из координат
    address_str = get_address_from_coords(coords)
    #вовщращаем результат пользователю в боте
    update.message.reply_text(address_str)

#Эта функция будет использоваться, если пользователь послал локацию.
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

#Это основная функция, где запускается наш бот
def main():
    #создаем бота и указываем его токен
    updater = Updater("6853640241:AAFJ9ouD8jf44dviH6TbZRQwo4LA7szyy5o", use_context=True)
    #создаем регистратор событий, который будет понимать, что сделал пользователь и на какую функцию надо переключиться.
    dispatcher = updater.dispatcher

    #регистрируем команду /start и говорим, что после нее надо использовать функцию def start
    dispatcher.add_handler(CommandHandler("start", start))
    #регистрируем получение текста и говорим, что после нее надо использовать функцию def text
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    #регистрируем получение локации и говорим, что после нее надо использовать функцию def location
    dispatcher.add_handler(MessageHandler(Filters.location, location))
    #запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    #запускаем функцию def main
    main()
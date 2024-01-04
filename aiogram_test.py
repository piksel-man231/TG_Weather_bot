import requests
import datetime
import asyncio
import logging
from CFG_reader import config
from aiogram import Bot, Dispatcher, types, utils, F
from aiogram.types import Message, Location
from aiogram.filters.command import Command

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=config.bot_token.get_secret_value())
# Диспетчер
dp = Dispatcher()

#Параметры запроса и сам запрос у геокодера
def get_address_from_coords(input):
    PARAMS = {
        "apikey": config.geo_token.get_secret_value(),   #API геокодера яндекс
        "format": "json",
        "lang": "ru_RU",
        "kind": "locality",
        "geocode": input
    }

    r = requests.get(url="https://geocode-maps.yandex.ru/1.x/?", params=PARAMS)
    # print(r)
    json_data = r.json()
    out_coords = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    #print(out_coords)
    return out_coords
    if (r != '<Response [200]>'):
        #единственное что тут изменилось, так это сообщение об ошибке.
        return "Не могу определить адрес по этой локации/координатам.\nОтправь мне локацию или координаты (долгота, широта):"
    
# Задаем значение ключа API 
api_key = config.weather_token.get_secret_value() 

# Задаем URL API 
url_w = 'https://api.weather.yandex.ru/v2/forecast' 

lon = 0
lat = 0

@dp.message(Command("start"))
async def start_answer(message: types.Message):
    await message.answer("Привет, пришли мне локацию любым спомобом\n - Название\n - Координаты\n - Точку в телеграме")

@dp.message(F.location)
async def loc_handler(message: Location):
    #print(message)
    msg = message.location
    print(msg)
    lon = msg.longitude
    lat = msg.latitude
    print(lon,"_", lat)
    await message.answer("Координаты получены!\nМожно запускать команду из меню")
    return lat, lon


address_str = 0


# Задаем параметры запроса для погоды
params = { 
    'lon': lon,
    'lat': lat, 
    'lang': 'ru_RU', # язык ответа 
    'limit': 7, # срок прогноза в днях 
    'hours': True, # наличие почасового прогноза 
    'extra': True # подробный прогноз осадков 
}


async def cmd_answer(message: types.Message):
    today = datetime.datetime.today()
    now = today.strftime('%d.%m.%Y') # дата в формате Д.М.Г
    print(now)
    print(str(lon) + "-_-_-_-_-" + str(lat))
    response = requests.get(url_w, params=params, headers={'X-Yandex-API-Key': api_key})
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
            await message.answer(f'Температура воздуха: {data["fact"]["temp"]} °C\nОщущается как: {data["fact"]["feels_like"]} °C\nПогодное описание: {data["fact"]["condition"]}\nОжидаемые осадки сегодня: ' + str(prec_total) + 'mm\nСегодня можно и на мойку заехать') 
        else:
            await message.answer(f'Температура воздуха: {data["fact"]["temp"]} °C\nОщущается как: {data["fact"]["feels_like"]} °C\nПогодное описание: {data["fact"]["condition"]}\nОжидаемые осадки сегодня: ' + str(prec_total) + 'mm\nНу помытся конечно можно, но ты дороги видел? ') 
    else:
        await message.r

dp.message.register(cmd_answer, Command("command1"))

@dp.message()
async def answer(message: types.Message):
    input = message.text
    #отправляем координаты в нашу функцию получения адреса
    address_str = get_address_from_coords(input)
    #вовщращаем результат пользователю в боте
    coords = address_str.split()
    lon = address_str[0]
    lat = address_str[1]
    await message.answer("Окей, теперь мы знаем в каком вы городе\nМожно запускать команду из меню")
    return lon, lat





if __name__ == "__main__":
    asyncio.run(main())
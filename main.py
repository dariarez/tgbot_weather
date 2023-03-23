import requests
import telebot
from telebot import types


bot = telebot.TeleBot('your_token')
api = 'your_api'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton("/Weather")
    btn2 = types.InlineKeyboardButton("/Forecast")
    markup.add(btn1, btn2)
    bot.reply_to(message, "Hi there. Want to know the weather? Click the button that you interesting in)", reply_markup=markup)

    @bot.message_handler(commands=['Weather'])
    def send_welcome(message):
        msg = bot.send_message(message.chat.id, text="Type city you want to know more")
        bot.register_next_step_handler(msg, weather_now)

    def weather_now(message):
        message_text = message.text
        url = f'http://api.openweathermap.org/data/2.5/weather?q={message_text}&appid={api}&units=metric'
        response = requests.get(url)
        data = response.json()
        if message_text == "/stop":
            bot.send_message(message.chat.id, text="Searching stoped")
            exit()
        else:
            temp = ([data['main']['temp']])
            country = ([data['sys']['country']])
            feels_like = ([data['main']['feels_like']])
            humidity = ([data['main']['humidity']])
            pressure = ([data['main']['pressure']])
            clouds = ([data['clouds']['all']])
            bot.send_message(message.chat.id, text= f"Great!The weather in {message_text} is: \nTemperature {temp}; \nCountry {country}; \nFells like {feels_like}; \nHumidity{humidity}; \nPressure {pressure}; \nClouds {clouds}.")

    @bot.message_handler(commands=['Forecast'])
    def send_welcome(message):
        msg2 = bot.send_message(message.chat.id, text="Type city you want to know more")
        bot.register_next_step_handler(msg2, weather_forecast)

    def weather_forecast(message):
        message_text = message.text
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={message_text}&appid={api}&units=metric'
        response = requests.get(url)
        data = response.json()
        if message_text == "/stop":
            bot.send_message(message.chat.id, text="Searching stoped")
            exit()
        else:
           for i in range(len(data['list'])):
            date = [data['list'][i]['dt_txt']]
            country = [data['city']['country']]
            weather = [data['list'][i]['main']]
            bot.send_message(message.chat.id, text= f"Geat!The weather forecast in {message_text},{country} is: \n{date}; \nweather {weather} ")

bot.infinity_polling()
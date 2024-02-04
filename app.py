from flask import Flask
import weather
import WeatherDataBase

import schedule
import time

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    schedule.every().seconds.do(do_weather, "440112")
    while True:
        schedule.run_pending()
        time.sleep(1)
    return 1


def do_weather(city):
    # print(f'{WeatherDataAll.WeatherDataAll(weather.get_weather_info(city, "all"))}')
    print(f'{WeatherDataBase.WeatherDataBase(weather.get_weather_info(city,"base"))}')


if __name__ == '__main__':
    app.run()

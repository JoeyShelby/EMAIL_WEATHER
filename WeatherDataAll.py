# 天气预报数据
from datetime import datetime


class Cats:
    def __init__(self, date, week, dayweather, nightweather, daytemp, nighttemp, daywind, nightwind, daypower,
                 nightpower, daytemp_float, nighttemp_float):
        self.date = date
        self.week = week
        self.dayweather = dayweather
        self.nightweather = nightweather
        self.daytemp = daytemp
        self.nighttemp = nighttemp
        self.daywind = daywind
        self.nightwind = nightwind
        self.daypower = daypower
        self.nightpower = nightpower
        self.daytemp_float = daytemp_float
        self.nighttemp_float = nighttemp_float

    def __str__(self):
        return f"Cats(date={self.date}, week={self.week}, dayweather={self.dayweather}, nightweather={self.nightweather}, daytemp={self.daytemp}, nighttemp={self.nighttemp}, daywind={self.daywind}, nightwind={self.nightwind}, daypower={self.daypower}, nightpower={self.nightpower}, daytemp_float={self.daytemp_float}, nighttemp_float={self.nighttemp_float})"


class WeatherDataAll:
    def __init__(self, json_data):
        city = json_data['forecasts'][0]['city']
        adcode = json_data['forecasts'][0]['adcode']
        province = json_data['forecasts'][0]['province']
        reporttime = json_data['forecasts'][0]['reporttime']
        casts = json_data['forecasts'][0]['casts']
        self.city = city
        self.adcode = adcode
        self.province = province
        self.reporttime = datetime.strptime(reporttime, "%Y-%m-%d %H:%M:%S")  # convert string to datetime object  
        self.casts = [Cats(**cat) for cat in casts]  # convert list of dictionaries to list of Cats objects  

    def __str__(self):
        return f"WeatherDataAll(city={self.city}, adcode={self.adcode}, province={self.province}, reporttime={self.reporttime}, casts=[{', '.join([str(cat) for cat in self.casts])}])"

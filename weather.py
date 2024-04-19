import json
import config
import requests
from flask import current_app

url = config.weatherUrl
params = {"key": config.key, "output": "JSON"}


# 调用高德天气查询接口，获得天气数据 extensions(气象类型) 可选值：base/all base:返回实况天气 all:返回预报天气
def get_weather_info(city, extensions):
    params['city'] = city
    params['extensions'] = extensions

    response = requests.get(url, params)
    if response.status_code != 200:
        current_app.logger.error('调用高德天气查询API失败！response.status_code != 200')
        return '调用高德天气查询API失败！'

    # 获得返回 JSON 数据
    weather_json = json.loads(response.text)

    if weather_json['status'] != '1':
        current_app.logger.error("高德天气查询API返回数据异常: " + weather_json['info'])
        return "高德天气查询API返回数据异常: " + weather_json['info']

    return weather_json

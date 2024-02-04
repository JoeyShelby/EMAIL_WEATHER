import json
import requests

url = "https://restapi.amap.com/v3/weather/weatherInfo"
params = {"key": "be34e4b95407d8210a923118e6084a8f",
          "output": "JSON"}


# 调用高德天气查虚拟接口，获得天气数据 extensions(气象类型) 可选值：base/all base:返回实况天气 all:返回预报天气
def get_weather_info(city, extensions):
    params['city'] = city
    params['extensions'] = extensions

    response = requests.get(url, params)
    if response.status_code != 200:
        return '调用高德天气查询API失败！'

    # 获得返回 JSON 数据
    weather_json = json.loads(response.text)
    print(weather_json)

    if weather_json['status'] != '1':
        return "高德天气查询API返回数据异常: " + weather_json['info']

    return weather_json

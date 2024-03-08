# 获取adcode（区域编码），城市信息等
import json
import GeocodeData
import config
import requests
from flask import current_app

url = config.geoUrl
params = {"key": config.key, "output": "JSON"}


# 调用高德地理编码查询接口
def get_geocode_data(address):
    params['address'] = address

    response = requests.get(url, params)
    if response.status_code != 200:
        current_app.logger.error('调用高德地理编码查询API失败！response.status_code != 200')
        return '调用高德地理编码查询API失败！'

    geocodeData_json = json.loads(response.text)

    if geocodeData_json['status'] != '1':
        current_app.logger.error("高德地理编码查询API返回数据异常: " + geocodeData_json['info'])
        return "高德地理编码查询API返回数据异常: " + geocodeData_json['info']
    return GeocodeData.GeocodeData(geocodeData_json)


# 根据地址，获得区域编码 adcode
def get_adcode(address):
    geocodeData = get_geocode_data(address)
    return geocodeData.geocodes[0].adcode


if __name__ == "__main__":
    get_adcode("湖南省怀化市洪江市安江镇")

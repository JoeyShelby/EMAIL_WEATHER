import os

from flask_sqlalchemy import SQLAlchemy

# 数据库连接：
db = SQLAlchemy()
HOSTNAME = "118.XXX.XXX.XXX"
PORT = 3306
USERNAME = "root"
PASSWORD = "XXXXXX"
DATABASE = "email_weather"
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

# 设置邮箱登录及邮箱服务器信息
mail_host = 'smtp.163.com'
mail_user = 'XXXXXXX'
mail_pass = 'XXXXXXXX'
sender = 'XXXXXXXXXXXXX'

# 高德天气API
weatherUrl = "https://restapi.amap.com/v3/weather/weatherInfo"
# 高德地理编码API
geoUrl = 'https://restapi.amap.com/v3/geocode/geo?parameters'
# key
key = 'XXXXXXXXXXXXXXXX'


# 日志保存路径
log_dir_name = "D:" + os.sep + "logs"

# 启动和停止服务需要的校验密码
ADMINPASSWORD = 'XXXXXX@123'

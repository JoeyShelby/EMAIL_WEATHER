import datetime
import smtplib
from email.mime.text import MIMEText
import WeatherDataAll
import weather

# 设置登录及服务器信息
mail_host = 'smtp.163.com'
mail_user = 'joeyshelby'
mail_pass = 'AXUNLFDDYADWXICE'
sender = 'joeyshelby@163.com'

# Open file
fileHandler = open("D:\CODE\Python\EMAIL_WEATHER\static\\receivers.txt", "r")
# Get list of all lines in file
listOfLines = fileHandler.readlines()

# 登录、获取天气数据、发送邮件
try:
    smtpObj = smtplib.SMTP()
    # 连接到服务器
    smtpObj.connect(mail_host, 25)
    # 登录到服务器
    smtpObj.login(mail_user, mail_pass)
    # 循环读取receivers文件，发送邮件
    for line in listOfLines:
        line = line.strip().split(',')
        receiver = line[0]
        city = line[1]
        # 获取天气信息
        weather_data_all = WeatherDataAll.WeatherDataAll(weather.get_weather_info(city, "all"))
        weather_info = f'{weather_data_all.city}{weather_data_all.casts[0].date}日白天天气{weather_data_all.casts[0].dayweather}，夜间天气{weather_data_all.casts[0].nightweather}，最高温{weather_data_all.casts[0].daytemp}℃，最低温{weather_data_all.casts[0].nighttemp}℃'
        # 设置email信息
        # 邮件内容设置
        message = MIMEText(weather_info, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = f'{weather_data_all.city}{weather_data_all.casts[0].date}天气{weather_data_all.casts[0].dayweather}'
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receiver
        # 发送邮件
        smtpObj.sendmail(
            sender, receiver, message.as_string())
    # 退出
    smtpObj.quit()
    print('success')
except smtplib.SMTPException as e:
    print('error', e)  # 打印错误

# Close file
fileHandler.close()

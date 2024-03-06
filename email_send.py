import smtplib
from email.mime.text import MIMEText
from flask import current_app
import WeatherDataAll
import weather
import config
import User

# 邮箱登录配置
mail_host = config.mail_host
mail_user = config.mail_user
mail_pass = config.mail_pass
sender = config.sender


def send_today_weather(app):
    # 获得所有接收邮件的用户
    with app.app_context():
        users = User.get_all_users()
    # 登录、获取天气数据、发送邮件
    try:
        smtpObj = smtplib.SMTP(port=465)
        # 连接到服务器
        smtpObj.connect(mail_host)
        # 登录到服务器
        smtpObj.login(mail_user, mail_pass)
        # 循环读取receivers文件，发送邮件
        for user in users:
            # 获取天气信息
            weather_data_all = WeatherDataAll.WeatherDataAll(weather.get_weather_info(user.city_code, "all"))
            weather_info = f'白天{weather_data_all.casts[0].dayweather}，{weather_data_all.casts[0].daytemp}℃；\n夜间{weather_data_all.casts[0].nightweather}，{weather_data_all.casts[0].nighttemp}℃。'
            # 设置email信息
            # 邮件内容设置
            message = MIMEText(weather_info, 'plain', 'utf-8')
            # 邮件主题
            message[
                'Subject'] = f'{weather_data_all.city}{weather_data_all.casts[0].date}{weather_data_all.casts[0].dayweather}'
            # 发送方信息
            message['From'] = sender
            # 接受方信息
            message['To'] = user.email
            # 发送邮件
            smtpObj.sendmail(
                sender, user.email, message.as_string())
            # 记录日志
            with app.app_context():
                current_app.logger.info(f'{user.email}:{weather_data_all}')
        # 退出
        smtpObj.quit()
    except smtplib.SMTPException as e:
        with app.app_context():
            current_app.logger.error(f'邮件登录或发送过程出错{e}')

from flask import Flask, current_app
import email_send
import LogHandler
import schedule
import time

app = Flask(__name__)
# 添加日志配置
app.logger.addHandler(LogHandler.getLogHandler())
# 激活上下文
ctx = app.app_context()
ctx.push()


@app.route('/')
def hello_world():  # put application's code here
    index = 0
    # 每天七点执行
    schedule.every().days.at('07:15').do(email_send.send_today_weather)
    # 每秒执行，测试用
    # schedule.every().seconds.do(email_send.send_today_weather)
    while True:
        # 每10秒记录一次日志
        index = index + 1
        if index % 10 == 0:
            current_app.logger.info(f'HeartBeating{index}')
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    app.run()

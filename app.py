from flask import Flask, current_app
import email_send
import LogHandler
import time
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
# 添加日志配置
handler = LogHandler.getLogHandler()
app.logger.addHandler(handler)
# 激活上下文
ctx = app.app_context()
ctx.push()
# 创建一个后台调度器（BackgroundScheduler）对象，并启动了调度器
scheduler = BackgroundScheduler()
scheduler.start()
# 一个标识位，如果已经触发任务，便不能再触发
can_trigger = True


@app.route('/')
def hello_world():
    global can_trigger
    if can_trigger:
        can_trigger = False
        return trigger()
    return '请勿重复调用'


# 触发定时任务
def trigger():
    # 添加定时任务，每10s打印日志
    scheduler.add_job(heartbeat, trigger='interval', seconds=10)
    # 添加定时任务，每日发送天气信息
    # scheduler.add_job(email_send.send_today_weather, trigger='cron', hour=23, minute=15)
    # 发邮件测试
    scheduler.add_job(email_send.send_today_weather, args=[app], trigger='interval', seconds=10)
    # 添加定时任务，每日0点更新日志配置
    scheduler.add_job(update_logFile, trigger='cron', hour=0, minute=0)

    return "已成功触发定时任务"


# 心跳日志
def heartbeat():
    with app.app_context():
        current_app.logger.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' HEARTBEATING')
    return


# 每日更新日志配置
def update_logFile():
    global handler
    app.logger.removeHandler(handler)
    # 添加日志配置
    handler = LogHandler.getLogHandler()
    app.logger.addHandler(handler)


if __name__ == '__main__':
    app.run()

from flask import Flask, current_app, render_template, request
import User
import config
import email_send
import LogHandler
import time
from config import db
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
# 一个标识位，如果已经触发后台定时任务，便不能再触发
can_trigger = True
# 数据库配置
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def hello_world():
    return render_template('index.html', can_trigger=can_trigger)


# 启动后台任务
@app.route('/start')
def start():
    global can_trigger
    if can_trigger:
        can_trigger = False
        trigger()
    return render_template('index.html', can_trigger=can_trigger)


# 维护用户信息
@app.route('/updateUser', methods=['POST'])
def updateUser():
    email = request.form['email']
    city_code = request.form['city_code']
    # 查到原User
    userOld = User.get_user_by_email(email)
    userNew = User.User(handle=f'UserBO:{email},{city_code}', email=email, city_code=city_code, nickname=email)
    # 用户不存在，新建用户
    if not userOld:
        User.insert_user(userNew)
    # 用户已存在，更新
    else:
        User.update_user(userOld.handle, userNew)
    confirm_user = User.get_user_by_email(email)
    confirm_user.password = '打码'
    return render_template('index.html', user=confirm_user)


# 触发定时任务
def trigger():
    # 添加定时任务，每10s打印日志
    scheduler.add_job(heartbeat, trigger='interval', seconds=10)
    # 添加定时任务，每日发送天气信息
    scheduler.add_job(email_send.send_today_weather, args=[app], trigger='cron', hour=23, minute=15)
    # 发邮件测试 每10s 慎用
    # scheduler.add_job(email_send.send_today_weather, args=[app], trigger='interval', seconds=10)
    # 添加定时任务，每日0点更新日志配置
    scheduler.add_job(update_logFile, trigger='cron', hour=0, minute=0)

    return "已成功触发定时任务"


# 心跳日志
def heartbeat():
    with app.app_context():
        current_app.logger.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' HEARTBEATING')
    return


# 每日更新日志配置，以创建新的日志文件
def update_logFile():
    global handler
    app.logger.removeHandler(handler)
    # 添加日志配置
    handler = LogHandler.getLogHandler()
    app.logger.addHandler(handler)


if __name__ == '__main__':
    app.run()

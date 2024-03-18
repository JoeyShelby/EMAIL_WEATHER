import os
from flask import Flask, current_app, render_template, request, jsonify
import User
import config
import email_send
import LogHandler
import time
from config import db
from apscheduler.schedulers.background import BackgroundScheduler

import city

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
    log(" app_hello_world()")
    return render_template('index.html', can_trigger=can_trigger, logs=get_logs())


# 启动或关闭后台任务
@app.route('/switch', methods=['POST'])
def switch():
    password = request.form['password']
    if password == config.ADMINPASSWORD:
        global can_trigger
        if can_trigger:  # 开启定时任务
            can_trigger = False
            trigger(True)
            log(" app_switch()_开启定时任务")
        else:  # 关闭定时任务
            can_trigger = True
            trigger(False)
            log(" app_switch()_关闭定时任务")
    else:
        log(f" app_switch()_密码错误{password}")
    return render_template('index.html', can_trigger=can_trigger, logs=get_logs())


# 维护用户信息接口
@app.route('/updateUser', methods=['POST'])
def updateUser():
    email = request.form['email']
    region = request.form['region']
    if not email or not region:
        log(f" app_updateUser()_维护失败 email:{email},city_code:{region}")
        return render_template('index.html', user="维护失败", can_trigger=can_trigger, logs=get_logs())
    city_code = city.get_adcode(region)
    log(f" app_updateUser()_email:{email},city_code:{city_code}")
    # 查到原User
    userOld = User.get_user_by_email(email)
    userNew = User.User(handle=f'UserBO:{email},{city_code}', email=email, city_code=city_code, city_desc=region,
                        nickname=email)
    # 用户不存在，新建用户
    if not userOld:
        User.insert_user(userNew)
        log(f" app_updateUser()_新建用户：{User}")
    # 用户已存在，更新
    else:
        User.update_user(userOld.handle, userNew)
    confirm_user = User.get_user_by_email(email)
    confirm_user.password = '打码'
    log(f" app_updateUser()_更新用户：{confirm_user}")
    return render_template('index.html', user=confirm_user, can_trigger=can_trigger, logs=get_logs())


# 获取所有日志文件名
def get_logs():
    directory = config.log_dir_name  # 修改为你要获取文件名的目录路径
    logs = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return logs


# 返回对应的日志内容
@app.route('/log/<filename>')
def get_file_content(filename):
    filepath = config.log_dir_name + os.sep + filename  # 修改为你要获取内容的文件路径
    log(f" app_get_file_content(filename)_查询日志：{filepath}")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()  # 使用read()方法读取整个文件内容
            return content
    else:
        return jsonify({'error': 'File not found'})


# 启动或关闭定时任务
def trigger(a):
    if a:
        # 添加定时任务，每日0点更新日志配置
        scheduler.add_job(update_logFile, trigger='cron', hour=0, minute=0)
        # 添加定时任务，每10s打印日志
        scheduler.add_job(log, args=[" HEARTBEAT"], trigger='interval', seconds=10)
        # 添加定时任务，每分钟执行一次【send_weather_by_time】
        scheduler.add_job(email_send.send_to_user_on_time, args=[app], trigger='interval', minutes=1)
        # 测试用 每10s发送一次邮件 慎用
        # scheduler.add_job(email_send.send_today_weather, args=[app], trigger='interval', seconds=10)
        log(f" app_trigger(a)_启动定时任务")
        return "已成功触发定时任务"
    else:
        # 关闭定时任务
        scheduler.shutdown(wait=False)
        log(f" app_trigger(a)_关闭定时任务")
        return "已关闭定时任务"


# 心跳日志
def log(content):
    with app.app_context():
        current_app.logger.info(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + content)
    return


# 每日更新日志配置，以创建新的日志文件
def update_logFile():
    global handler
    app.logger.removeHandler(handler)
    # 添加日志配置
    handler = LogHandler.getLogHandler()
    app.logger.addHandler(handler)
    log(f" app_update_logFile()_更新日志配置")


if __name__ == '__main__':
    app.run()

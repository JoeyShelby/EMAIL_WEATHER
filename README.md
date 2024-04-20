# 缘起

这个小工具的诞生于一个悲伤的故事......
# 项目结构

```python
EMAIL_WEATHER:
    │  app.py             -flask应用主入口
    │  city.py            -地区相关的一些方法，主要是通过地址信息获得地区编码adcode
    │  config.py          -配置文件：数据库连接、邮箱地址、日志保存路径等
    │  Dockerfile         -使用Docker配置到服务器上
    │  email_send.py      -发送邮件相关方法
    │  GeocodeData.py     -地理数据类，用来解析高德地理编码查询API返回的JSON数据
    │  LogHandler.py      -日志配置
    │  README.md
    │  email_weather.sql  -数据库脚本
    │  requirements.txt   -python 项目环境配置文件
    │  tree.txt
    │  User.py            -用户类ORM
    │  weather.py         -天气相关方法
    │  WeatherDataAll.py  -完全天气信息类，用来解析高德天气查询API返回的JSON数据
    │  WeatherDataBase.py -基础天气信息类，用来解析高德天气查询API返回的JSON数据
    │
    ├─.idea
    │
    ├─static
    │      address.css    -三级联动地址查询插件
    │      address.js     -三级联动地址查询插件
    │
    ├─templates
    │      index.html     -首页
    │
    ├─venv
    │
    └─__pycache__
```

# 部署

## 下载项目

直接 copy 整个项目

## 环境

我用的是 `Python 3.11.1`

依赖的安装可在搜索引擎搜索 `requirements.txt 安装` 等关键词进行安装

## 数据库

需要安装好数据库，并用 `email_weather.sql` 中的 sql 脚本生成数据库以及表。我用的是MySQL数据库。

在 `config` 文件中配置好数据库相关配置

```python
# 数据库连接：
db = SQLAlchemy()
HOSTNAME = "172.178.xx.xxx"    #域名
PORT = 3306                    #端口
USERNAME = "root"              #数据库用户名
PASSWORD = "123456"            #数据库密码
DATABASE = "email_weather"     #数据库名  
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
```

## 邮箱

首先搜索 `开通 SMTP`相关资料，开通 SMTP

然后在 `config` 文件中配置：

```python
# 设置邮箱登录及邮箱服务器信息
mail_host = 'smtp.163.com'  # SMTP 域名
mail_user = 'XXXXXX'    # 邮箱用户名
mail_pass = 'XXXXXXXXXXX' # SMTP授权码
sender = 'XXXXXXXXXXXXX' # 发送邮箱
```

## 天气API

获取天气信息，这里我用的是高德天气信息API

具体参考  [天气查询-基础 API 文档-开发指南-Web服务 API|高德地图API (amap.com)](https://lbs.amap.com/api/webservice/guide/api/weatherinfo)

在 `config` 文件中配置：

```python
# 高德天气API
weatherUrl = "https://restapi.amap.com/v3/weather/weatherInfo"
# api的key
key = 'be34e4b95407d8210a923118e6084a8f'
```

##  地理编码API

用户输入地址，通过该API获取地理编码，以获取天气信息

具体参考 [地理/逆地理编码-基础 API 文档-开发指南-Web服务 API|高德地图API (amap.com)](https://lbs.amap.com/api/webservice/guide/api/georegeo)

```python
# 高德地理编码API
geoUrl = 'https://restapi.amap.com/v3/geocode/geo?parameters'
```

## 部署到服务器

### 1. 上传文件

将整个项目文件上传到服务器上

### 2. DOCKER

需要服务器上有Docker环境

- 在命令行中，进入应用程序的根目录，并运行以下命令来构建Docker镜像：

> docker build -t email_weather .

- 运行 docker 容器

> docker run -p 5000:5000  -v /home/EMAIL_WEATHER:/app  -v /etc/localtime:/etc/localtime  email_weather

这里的 `-v /home/EMAIL_WEATHER:/app` 挂载是为了把容器的整个/app 根目录挂载到服务器的程序根目录，方便修改代码及查看日志。

`-v /etc/localtime:/etc/localtime` 是把容器的时间配置文件挂载到服务器的时间配置文件，以防止容器的时区不便于修改。

具体时区修改方法可搜索`linux 修改时区`

- 运行服务

`docker exec -it` 容器ID `/bin/bash` 进入到容器内，cd到 `/app` 目录下，运行`python app.py`命令

# 预览

![image-20240420120200071](../../source/images/EMAIL_WEATHER/image-20240420120200071.png)

![image-20240420120636678](../../source/images/EMAIL_WEATHER/image-20240420120636678.png)

# 坑

## SMTP端口

SMTP默认端口是25，但一般服务器厂商为了防止骚扰邮件服务，都会锁掉25端口。所以这里我用了SSL类型的SMTP连接，应该用的是465端口：

```python
# 连接到SMTP服务器
# smtpObj.connect(mail_host)   <----这样不行
smtpObj = smtplib.SMTP_SSL(mail_host)

```

## 待优化点

1. 保密性
2. 数据库很容易被大量数据写入

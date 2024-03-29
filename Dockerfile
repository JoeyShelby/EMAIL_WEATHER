# 使用Python作为基础镜像
FROM python:3.11.1
# 设置工作目录
WORKDIR /app
# 创建日志目录
RUN mkdir logs
# 复制应用代码到容器中
COPY . /app
# 设置pip源，并更新pip
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --upgrade pip
# 安装依赖项
RUN pip install -r requirements.txt
# 暴露应用端口
EXPOSE 5000
# 设置启动命令
# CMD ["python", "app.py"]

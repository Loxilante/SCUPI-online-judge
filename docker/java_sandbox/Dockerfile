# 使用Python官方镜像作为基础镜像
FROM python:3.9

# 设置环境变量，防止Python写字节码
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 设置工作目录
WORKDIR /code

# 安装g++用于编译C++代码
RUN apt-get update && apt-get install -y g++
RUN apt-get install vim -y
RUN apt-get install -y --fix-missing openjdk-17-jdk

# 安装依赖
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# 拷贝项目
COPY . /code/
RUN g++ /code/judge/excuting.cpp -o /code/judge/excuting.exe
# 安装uwsgi
RUN pip install uwsgi

CMD ["uwsgi", "--http-socket", "0.0.0.0:80", "--file", "/code/java_sandbox/wsgi.py"]
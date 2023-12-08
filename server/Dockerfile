# 使用 Python 3.10 镜像
FROM python:3.10

# 设置工作目录
WORKDIR /app

# 复制 Python 依赖文件并安装依赖
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# 复制服务端代码到容器内
COPY ./server/ ./

# 给启动脚本可执行权限
RUN chmod +x ./start.sh

# 设置容器启动时执行的命令
CMD ["./start.sh"]

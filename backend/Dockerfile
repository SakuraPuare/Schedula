FROM ubuntu:22.04

WORKDIR /app

COPY . /app

RUN apt update && apt install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "main.py"]

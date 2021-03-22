FROM python:latest

RUN useradd -ms /bin/bash fastapi

USER fastapi

WORKDIR /app

COPY requirements.txt ./
RUN python -m venv venv && \
    /fastapi/venv/bin/pip install \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    -r requirements.txt

COPY frontend frontend

EXPOSE 9090

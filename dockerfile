FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install pymongo

# Запуск HTTP та Socket серверів у одному контейнері
CMD ["sh", "-c", "python3 socket_server.py & python3 main.py"]

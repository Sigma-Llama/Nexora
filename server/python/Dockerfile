FROM python:3.12.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir mysql-connector-python python-dotenv websockets requests

CMD ["python", "main.py"]
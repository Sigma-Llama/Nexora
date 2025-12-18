FROM python:3.12.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt \
	mysql-connector-python python-dotenv cryptography requests

CMD ["python", "main.py"]
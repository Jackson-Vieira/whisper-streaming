FROM python:3.10.12-slim

WORKDIR /app

RUN apt update && apt install -y ffmpeg

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--ssl-keyfile", "./.certs/key.pem", "--ssl-certfile", "./.certs/cert.pem"]

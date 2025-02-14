FROM python:3.10.8

WORKDIR /app/backend

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["sh", "-c", "uvicorn src.app:app --host 0.0.0.0 --port ${PORT} --workers 1 --limit-concurrency 10"]

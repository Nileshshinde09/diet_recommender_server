FROM python:3.10.8

WORKDIR /app/backend

COPY requirements.txt .  

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . . 

EXPOSE 8080
# Use Gunicorn for better memory management
CMD ["gunicorn", "src.app:app", "--bind", "0.0.0.0:${PORT}"]
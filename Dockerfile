FROM python:3.10-slim

# Türkçe karakter desteği için bu iki satır eklendi
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

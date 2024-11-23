FROM python:3.9-slim

WORKDIR /api-flask

COPY . .

RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    python3-pyaudio \
    && apt-get clean

RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5111

CMD ["python", "server.py", "--host=0.0.0.0", "--port=5111"]
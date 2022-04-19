FROM python:3.10-alpine3.14

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "bot_processor.py"]
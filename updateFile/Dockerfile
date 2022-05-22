FROM python:3.8

FROM python:3.8-slim-buster

WORKDIR /updated

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "updater.py"]
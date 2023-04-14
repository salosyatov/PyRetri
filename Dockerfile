FROM python:3.9-slim

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

WORKDIR ${HOME}

COPY . /landmarks_app
WORKDIR /landmarks_app
RUN python setup.py  install

RUN pip install aiogram requests Pillow python-dotenv

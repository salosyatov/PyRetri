FROM python:3.9-slim

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install matplotlib
WORKDIR ${HOME}

COPY . /landmarks_app
WORKDIR /landmarks_app
RUN python setup.py  install

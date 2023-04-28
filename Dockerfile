FROM python:3.9-slim

RUN pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
WORKDIR ${HOME}

COPY bot /landmarks_app/bot
COPY configs /landmarks_app/configs
COPY pyretri /landmarks_app/pyretri
COPY data/landmarks /landmarks_app/data/landmarks
COPY data/features/landmarks /landmarks_app/data/features/landmarks
COPY data_jsons /landmarks_app/data_jsons
COPY main /landmarks_app/main
COPY bot.py /landmarks_app/bot.py
COPY setup.py /landmarks_app/setup.py

WORKDIR /landmarks_app
RUN python setup.py  install

FROM python:3.10
LABEL Maintainer="valtrois"

WORKDIR /home/app
COPY . .
RUN pip install -r requirements.txt

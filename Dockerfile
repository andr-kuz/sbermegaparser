FROM python:3.10
LABEL Maintainer="valtrois"

WORKDIR /home/app
COPY . .
RUN apt-get update
RUN apt-get install -y gstreamer1.0-libav libnss3-tools libatk-bridge2.0-0 libcups2-dev libxkbcommon-x11-0 libxcomposite-dev libxrandr2 libgbm-dev libgtk-3-0 libdbus-glib-1-2
RUN pip install -r requirements.txt
RUN playwright install

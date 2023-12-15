FROM python:3.10
LABEL Maintainer="andr-kuz"

WORKDIR /home/app
COPY . .
RUN pip install -r requirements.txt
RUN apt update
RUN apt install -y xvfb # virtual display

RUN apt install -y firefox-esr # firefox browser

RUN apt install -y wget
RUN wget -P /tmp https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y /tmp/google-chrome-stable_current_amd64.deb

RUN apt install -y gstreamer1.0-libav libnss3-tools libatk-bridge2.0-0 libcups2-dev libxkbcommon-x11-0 libxcomposite-dev libxrandr2 libgbm-dev libgtk-3-0 libdbus-glib-1-2
RUN playwright install

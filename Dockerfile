FROM python:3.6.1

LABEL maintainer="Philip Hughes <p@hews.co>"

RUN mkdir /app
WORKDIR /app

COPY ["autoswatch/",      "/app/autoswatch"]
COPY ["tests/",           "/app/tests"]
COPY ["docker/*",         "/app/"]
COPY ["requirements.txt", \
      "setup.py",         \
      "setup.cfg",        "/app/"]

RUN pip install -r requirements.txt

EXPOSE 5000

CMD "./cmd.sh"

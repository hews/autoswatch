FROM python:3.6.1

LABEL maintainer="Philip Hughes <p@hews.co>"

RUN groupadd -r flask && useradd -r -g flask flask

RUN mkdir /app
WORKDIR /app

COPY ["setup.py",  \
      "setup.cfg", "/app/"]

# TODO: How best to handle this…?
RUN pip install -e . && \
    pip install -e .[tests] && \
    pip install -e .[tests-guard]

COPY ["autoswatch/",      "/app/autoswatch"]
COPY ["tests/",           "/app/tests"]
COPY ["docker/*",         "/app"]

RUN chown -R flask /app
USER flask

EXPOSE 5000

CMD "./cmd.sh"

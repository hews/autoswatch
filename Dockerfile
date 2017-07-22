FROM python:3.6.1

LABEL maintainer="Philip Hughes <p@hews.co>"

RUN groupadd -r flask && useradd -r -g flask flask

RUN mkdir -p /app/autoswatch
WORKDIR /app

COPY ["setup.py",  \
      "setup.cfg", \
      "VERSION",   "/app/"]

# TODO: How best to handle this…
#  Right now, thinking Dockerfile & Dockerfile.test, but that may
#  be too much maintenance and heavy lifting just to save from a few
#  test libs being installed.
RUN pip install -e . && \
    pip install -e .[tests] && \
    pip install -e .[tests-guard]

COPY ["autoswatch/", "/app/autoswatch"]
COPY ["tests/",      "/app/tests"]
COPY ["docker/*",    "/app/"]

RUN chown -R flask /app
USER flask

EXPOSE 5000 5001
ENV TERM=xterm

CMD "./cmd.sh"

FROM python:3.6.1

LABEL maintainer="Philip Hughes <p@hews.co>"

RUN mkdir /app
WORKDIR /app

ADD ["autoswatch",       "/app/autoswatch"]
ADD ["requirements.txt", "/app"]
ADD ["setup.py",         "/app"]

ENV FLASK_APP="autoswatch" \
    FLASK_DEBUG="true"

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]

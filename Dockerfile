FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "app.py"
ENV FLASK_ENV "production"
ENV FLASK_DEBUG False

RUN mkdir /app
WORKDIR /app

ADD . /app

RUN pip install -U pip && \
    pip install -Ur requirements.txt

EXPOSE 5000

CMD flask run --host=0.0.0.0

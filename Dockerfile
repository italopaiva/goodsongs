FROM python:3.4-alpine

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ENV FLASK_APP=run.py
ENV FLASK_DEBUG=1
ENV RUNNING_FROM_DOCKER=1

CMD ["flask", "run", "--host", "0.0.0.0"]

ADD . /app

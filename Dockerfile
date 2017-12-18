FROM python:3.4-alpine

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ENV RUNNING_FROM_DOCKER=1

CMD ["python", "run.py"]

ADD . /app

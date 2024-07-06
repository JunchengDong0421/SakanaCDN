# Single Dockerfile for all settings since small app
FROM python:3.9-slim AS build

WORKDIR /usr/src/SakanaStorage

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/SakanaStorage/wheels -r requirements.txt

FROM python:3.9-slim

RUN mkdir -p /home/SakanaStorage

RUN addgroup --system sknstorage && adduser --system --group sknstorage

ENV HOME=/home/SakanaStorage
ENV APP_HOME=/home/SakanaStorage/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/uploads
RUN mkdir $APP_HOME/instance
RUN mkdir $APP_HOME/logs
WORKDIR $APP_HOME

COPY --from=build /usr/src/SakanaStorage/wheels /wheels
COPY --from=build /usr/src/SakanaStorage/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN chown -R sknstorage:sknstorage $APP_HOME

USER sknstorage

CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]

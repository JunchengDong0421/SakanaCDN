# Single Dockerfile for all settings since small app
FROM python:3.9-slim as build

WORKDIR /usr/src/SakanaCDN

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/SakanaCDN/wheels -r requirements.txt

FROM python:3.9-slim

RUN mkdir -p /home/SakanaCDN

RUN addgroup --system skncdn && adduser --system --group skncdn

ENV HOME=/home/SakanaCDN
ENV APP_HOME=/home/SakanaCDN/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY --from=build /usr/src/SakanaCDN/wheels /wheels
COPY --from=build /usr/src/SakanaCDN/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME

RUN chown -R skncdn:skncdn $APP_HOME

USER skncdn

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]

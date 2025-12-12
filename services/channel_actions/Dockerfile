FROM python:3.12.12-alpine3.23

#для healthcheck
RUN apk add --no-cache curl


WORKDIR /channel_actions

# Оптимизация пересборки контейнера в случаях когда библиотеки не изменились
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN addgroup -g 1000 channel_actions && \
    adduser -u 1000 -G channel_actions -D -s /bin/sh channel_actions && \
    chown -R channel_actions:channel_actions /channel_actions &&  chmod -R 775 /channel_actions

USER channel_actions

EXPOSE 8010

CMD ["python3", "main.py"]
FROM python:3.12.12-alpine3.23

#для healthcheck
RUN apk add --no-cache curl


WORKDIR /video_postprocess

# Оптимизация пересборки проекта в случаях когда библиотеки не изменились
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN addgroup -g 1000 video_postprocess && \
    adduser -u 1000 -G video_postprocess -D -s /bin/sh video_postprocess && \
    chown -R video_postprocess:video_postprocess /video_postprocess &&  chmod -R 775 /video_postprocess

USER video_postprocess

EXPOSE 8040

CMD ["python3", "main.py"]
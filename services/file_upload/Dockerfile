FROM python:3.12.12-alpine3.23

#для healthcheck
RUN apk add --no-cache curl


WORKDIR /file_upload

# Оптимизация пересборки проекта в случаях когда библиотеки не изменились
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN addgroup -g 1000 file_upload && \
    adduser -u 1000 -G file_upload -D -s /bin/sh file_upload && \
    chown -R file_upload:file_upload /file_upload &&  chmod -R 775 /file_upload

USER file_upload

EXPOSE 8030

CMD ["python3", "main.py"]
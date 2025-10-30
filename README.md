# Что это за проект?
Проект вдохновлённый хакатонским проектом [simple videohosting](https://github.com/Hexorcists/simple_videohosting) над которым я работал который я решил снова написать с нуля

# Предварительная настройка
## SSL сертификаты
Если у вас нет своих SSL сертификатов, то для начала нужно установить [OpenSSL](https://www.openssl.org), это нужно для создания SSL сертификатов для безопасного соединения с PostgreSQL и RabbitMQ

Генерация сертификатов для PostgreSQL
```bash
openssl genrsa -out ./certs/postgres/rootCA.key 4096
openssl req -x509 -new -nodes -key ./certs/postgres/rootCA.key -sha256 -days 3650 -out ./certs/postgres/rootCA.crt -subj "/C=RU/ST=Moscow/L=Moscow/O=postgres/OU=CA/CN=postgres"
openssl genrsa -out ./certs/postgres/server.key 2048
openssl req -new -key ./certs/postgres/server.key -out ./certs/postgres/server.csr -subj "/C=RU/ST=Moscow/L=Moscow/O=postgres/OU=IT/CN=postgres"
openssl x509 -req -in ./certs/postgres/server.csr -CA ./certs/postgres/rootCA.crt -CAkey ./certs/postgres/rootCA.key -CAcreateserial -out ./certs/postgres/server.crt -days 365 -sha256
```

Генерация сертификатов для Rabbitmq
```bash
openssl genrsa -out ./certs/rabbitmq/rootCA.key 4096
openssl req -x509 -new -nodes -key ./certs/rabbitmq/rootCA.key -sha256 -days 3650 -out ./certs/rabbitmq/rootCA.crt -subj "/C=RU/ST=Moscow/L=Moscow/O=rabbitmq/OU=CA/CN=rabbitmq"
openssl genrsa -out ./certs/rabbitmq/server.key 2048
openssl req -new -key ./certs/rabbitmq/server.key -out ./certs/rabbitmq/server.csr -subj "/C=RU/ST=Moscow/L=Moscow/O=rabbitmq/OU=IT/CN=rabbitmq"
openssl x509 -req -in ./certs/rabbitmq/server.csr -CA ./certs/rabbitmq/rootCA.crt -CAkey ./certs/rabbitmq/rootCA.key -CAcreateserial -out ./certs/rabbitmq/server.crt -days 365 -sha256
openssl genrsa -out ./certs/rabbitmq/client.key 2048
openssl req -new -key ./certs/rabbitmq/client.key -out ./certs/rabbitmq/client.csr -subj "/C=RU/ST=Moscow/L=Moscow/O=postgres/OU=IT/CN=rabbitmq"
openssl x509 -req -in ./certs/rabbitmq/client.csr -CA ./certs/rabbitmq/rootCA.crt -CAkey ./certs/rabbitmq/rootCA.key -CAcreateserial -out ./certs/rabbitmq/client.crt -days 365
```

Генерация сертификатов для MinIO
```bash
openssl genrsa -out ./certs/minio/CAs/ca.key 4096
openssl req -x509 -new -nodes -key ./certs/minio/CAs/ca.key -sha256 -days 3650 -out ./certs/minio/CAs/ca.crt -subj "/C=RU/ST=Moscow/L=Moscow/O=rabbitmq/OU=CA/CN=minio"
openssl genrsa -out ./certs/minio/private.key 2048
openssl req -new -key ./certs/minio/private.key -out ./certs/minio/public.csr -subj "/C=RU/ST=Moscow/L=Moscow/O=rabbitmq/OU=CA/CN=minio"
openssl x509 -req -in ./certs/minio/public.csr -CA ./certs/minio/CAs/ca.crt -CAkey ./certs/minio/CAs/ca.key -CAcreateserial -out ./certs/minio/public.crt -days 3650 -sha256
```


Сертификаты рассчитаны на год и через год после генерации их нужно будет перегенерировать

Если же у вас есть свои сертификаты, то положите их в папки certs/postgres/ и certs/rabbitmq/, и они должны назваться также, как и автоматически генерируемые в этом репозитории

## Настройка .env
Также вам нужно создать и настроить **.env** файл, у вас есть .env.example который по факту служит шаблоном вашего .env файла
```bash
cp ./.env.example ./.env
```
В этом файле также есть коментарии которые описывают за что отвечает каждый параметр

# Запуск проекта
После предварительной настройки проекта для первого запуска(а также запуска после каких-либо изменений) нужно использовать
```bash
docker compose up --build
```
Последующие запуски можно делать с помощью
```bash
docker compose up
```
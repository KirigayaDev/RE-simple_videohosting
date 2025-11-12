# Что это за проект?
Переписанный с нуля проект [simple videohosting](https://github.com/Hexorcists/simple_videohosting) над которым я работал в рамках хакатона

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

Генерация сертификатов для Redis
```bash
openssl genrsa -out ./certs/redis/rootCA.key 4096
openssl req -x509 -new -nodes -key ./certs/redis/rootCA.key -sha256 -days 3650 -out ./certs/redis/rootCA.crt -subj "/C=RU/ST=Moscow/L=Moscow/O=postgres/OU=CA/CN=redis"
openssl genrsa -out ./certs/redis/server.key 2048
openssl req -new -key ./certs/redis/server.key -out ./certs/redis/server.csr -subj "/C=RU/ST=Moscow/L=Moscow/O=postgres/OU=IT/CN=redis"
openssl x509 -req -in ./certs/redis/server.csr -CA ./certs/redis/rootCA.crt -CAkey ./certs/redis/rootCA.key -CAcreateserial -out ./certs/redis/server.crt -days 365 -sha256
openssl genrsa -out ./certs/redis/client.key 2048
openssl req -new -key ./certs/redis/client.key -out ./certs/redis/client.csr -subj "/C=RU/ST=Moscow/L=Moscow/O=postgres/OU=IT/CN=redis"
openssl x509 -req -in ./certs/redis/client.csr -CA ./certs/redis/rootCA.crt -CAkey ./certs/redis/rootCA.key -CAcreateserial -out ./certs/redis/client.crt -days 365
```


Генерация сертификатов для auth_service
```bash
openssl genrsa -out ./certs/auth_service/rootCA.key 4096
openssl req -x509 -new -nodes -key ./certs/auth_service/rootCA.key -sha256 -days 3650 -out ./certs/auth_service/rootCA.crt -subj "/C=RU/ST=Moscow/L=Moscow/O=auth_service/OU=CA/CN=auth_service"
openssl genrsa -out ./certs/auth_service/server.key 2048
openssl req -new -key ./certs/auth_service/server.key -out ./certs/auth_service/server.csr -subj "/C=RU/ST=Moscow/L=Moscow/O=auth_service/OU=IT/CN=auth_service"
openssl x509 -req -in ./certs/auth_service/server.csr -CA ./certs/auth_service/rootCA.crt -CAkey ./certs/auth_service/rootCA.key -CAcreateserial -out ./certs/auth_service/server.crt -days 365 -sha256
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
Запуск компоуса для разработки
```bash
docker compose up
```
Запуск компоуса на проде
```bash
docker compose -f docker-compose-production.yml up
```

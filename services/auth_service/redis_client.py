import redis.asyncio as redis

from configurations import redis_settings

redis_client: redis.Redis = redis.Redis(password=redis_settings.password,
                                        port=6379,
                                        host='redis',
                                        decode_responses=True,
                                        ssl=True,
                                        ssl_cert_reqs="required",
                                        ssl_ca_certs="/auth_service/redis_certs/rootCA.crt",
                                        ssl_certfile="/auth_service/redis_certs/client.crt",
                                        ssl_keyfile="/auth_service/redis_certs/client.key",
                                        )

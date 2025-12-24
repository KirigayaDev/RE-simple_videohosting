from faststream.rabbit.fastapi import RabbitRouter

from configurations import rabbitmq_settings

from .security import security

_url = f"amqp://{rabbitmq_settings.user}:{rabbitmq_settings.password}@rabbitmq:5672/"

router = RabbitRouter(_url, reconnect_interval=10)

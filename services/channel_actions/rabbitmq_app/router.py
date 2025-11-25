from faststream.rabbit.fastapi import RabbitRouter

from configurations import rabbitmq_settings

from .security import security

_url = f"amqps://{rabbitmq_settings.user}:{rabbitmq_settings.password}@rabbitmq:5671/"

router = RabbitRouter(_url, security=security)

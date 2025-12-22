import ssl
from faststream.security import BaseSecurity

ssl_context = ssl.create_default_context(
    cafile="/channel_actions/certs/rabbitmq/rootCA.crt"
)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = True
ssl_context.load_cert_chain(
    certfile="/channel_actions/certs/rabbitmq/client.crt",
    keyfile="/channel_actions/certs/rabbitmq/client.key"
)

security = BaseSecurity(ssl_context)

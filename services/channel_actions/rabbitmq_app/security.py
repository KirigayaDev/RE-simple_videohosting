import ssl
from faststream.security import BaseSecurity

ssl_context = ssl.create_default_context(
    cafile="/channel_actions/rabbitmq_certs/rootCA.crt"
)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = True
ssl_context.load_cert_chain(
    certfile="/channel_actions/rabbitmq_certs/client.crt",
    keyfile="/channel_actions/rabbitmq_certs/client.key"
)

security = BaseSecurity(ssl_context)

import ssl
from faststream.security import BaseSecurity

ssl_context = ssl.create_default_context()

# ssl_context.load_cert_chain(
#     certfile="/file_upload/certs/rabbitmq/client.crt",
#     keyfile="/file_upload/certs/rabbitmq/client.key"
# )

ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
# ssl_context.load_verify_locations(cafile="/file_upload/certs/rabbitmq/rootCA.crt")

security = BaseSecurity(ssl_context)

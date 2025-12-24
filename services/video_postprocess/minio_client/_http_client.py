import ssl

import urllib3
from urllib3.util.ssl_ import create_urllib3_context
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

ctx = create_urllib3_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

http_client = urllib3.PoolManager(
    ca_certs="/video_postprocess/certs/minio/CAs/ca.crt",
    ssl_context=ctx
)

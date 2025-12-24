from minio import Minio

from configurations import minio_settings

from ._http_client import http_client


minio_client = Minio(
    endpoint="minio:9000",
    access_key=minio_settings.access_key,
    secret_key=minio_settings.access_secret,
    secure=True,
    cert_check=True,
    http_client=http_client,
)

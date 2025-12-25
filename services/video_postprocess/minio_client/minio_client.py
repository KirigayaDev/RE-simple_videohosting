import orjson
from minio import Minio

from configurations import minio_settings
from minio.error import S3Error

from ._http_client import http_client

minio_client = Minio(
    endpoint="minio:9000",
    access_key=minio_settings.access_key,
    secret_key=minio_settings.access_secret,
    secure=True,
    cert_check=True,
    http_client=http_client,
)

public_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::re-simple-videohosting/videos/*"]
        }
    ]
}

try:
    minio_client.set_bucket_policy(
        bucket_name="re-simple-videohosting",
        policy=orjson.dumps(public_policy)
    )
except S3Error as e:
    raise

from .minio_client import minio_client

bucket_name = "unprocessed-videos"

if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

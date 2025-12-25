import asyncio
import os
import shutil

from pathlib import Path

from faststream import AckPolicy
from faststream.rabbit import Channel, RabbitMessage

from minio.error import S3Error

from minio_client.minio_client import minio_client
from minio_client.bucket_info import bucket_name

from .schemas import ConvertVideoToHls, ConfirmVideoHlsConverting

from ._scan_video import scan_video

from .video_converter import convert_video_to_hls

from ..router import router

from ..queues import confirm_video_hls_converting_queue, convert_video_to_hls_queue


async def collect_all_files(local_dir: str) -> list[Path]:
    def _sync_walk():
        files = []
        for root, _, filenames in os.walk(local_dir):
            for filename in filenames:
                files.append(Path(root) / filename)
        return files

    return await asyncio.to_thread(_sync_walk)


async def _upload_folder(local_dir: str, uuid, prefix: str = "videos"):
    local_path = Path(local_dir)

    files = await collect_all_files(local_dir)

    await asyncio.gather(*[
        asyncio.to_thread(
            minio_client.fput_object,
            bucket_name,
            f"{prefix}/{uuid}/{f.relative_to(local_path)}",
            str(f)
        )
        for f in files])


async def _object_exists(object_name: str) -> bool:
    try:
        await asyncio.to_thread(minio_client.stat_object, bucket_name, object_name)
        return True
    except S3Error:
        return False


_video_converter_channel = Channel(prefetch_count=3)


@router.subscriber(convert_video_to_hls_queue, ack_policy=AckPolicy.NACK_ON_ERROR, channel=_video_converter_channel)
async def _convert_video_to_hls(info: ConvertVideoToHls) -> ConfirmVideoHlsConverting:
    try:
        unprocessed_video_path = f"./unprocessed_videos/{info.video_uuid}"
        converted_video_path = f"./converted_video/{info.video_uuid}"
        if not await _object_exists(info.video_path):
            return None

        await asyncio.to_thread(minio_client.fget_object, bucket_name, info.video_path, unprocessed_video_path)
        if not await scan_video(unprocessed_video_path):
            await asyncio.to_thread(minio_client.remove_object, bucket_name, info.video_path)
            return None

        await convert_video_to_hls(unprocessed_video_path, converted_video_path)
        await _upload_folder(converted_video_path, info.video_uuid)

        await asyncio.to_thread(minio_client.remove_object, bucket_name, info.video_path)

        await router.broker.publish(ConfirmVideoHlsConverting(uuid=info.video_uuid), confirm_video_hls_converting_queue)
    finally:
        if os.path.exists(unprocessed_video_path):
            os.remove(unprocessed_video_path)
        if os.path.exists(converted_video_path):
            shutil.rmtree(converted_video_path, ignore_errors=True)

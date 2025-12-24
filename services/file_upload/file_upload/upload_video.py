import os
import asyncio
import uuid

from pathlib import Path

from fastapi import UploadFile, File, Depends, HTTPException
from fastapi.responses import ORJSONResponse

from minio.error import S3Error

from schemas.user import UserSchema
from get_current_user.get_current_user import get_current_user

from minio_client.minio_client import minio_client
from minio_client.bucket_info import bucket_name

from rabbitmq_app.unprocessed_video_uploader import send_video_uploaded_message

from schemas.unprocessed_video_uploaded import UnprocessedVideoUploaded

from .router import router

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mkv'}
VIDEO_MIME_TYPES = {'video/mp4', 'video/avi', 'video/x-msvideo', 'video/x-matroska',
                    'video/quicktime', 'video/x-ms-wmv', 'video/x-flv', 'video/webm', 'video/x-m4v'}


def _is_valid_video_file(file: UploadFile) -> bool:
    # Проверка расширения
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in VIDEO_EXTENSIONS:
        return False

    # Проверка MIME типа
    if not file.content_type or file.content_type not in VIDEO_MIME_TYPES:
        return False

    return True


def _is_allowed_file_size(file: UploadFile) -> bool:
    return os.fstat(file.file.fileno()).st_size <= 2048 * 1024 * 1024


async def _object_exists(bucket, obj_name):
    try:
        await asyncio.to_thread(minio_client.stat_object, bucket, obj_name)
        return True
    except S3Error:
        return False


async def _try_upload_video(file: UploadFile, user: UserSchema) -> bool:
    file_ext = Path(file.filename).suffix.lower()
    new_filename = f"unprocessed-videos/{uuid.uuid4()}{file_ext}"
    while await _object_exists(bucket_name, new_filename):
        new_filename = f"{uuid.uuid4()}.{file_ext}"

    try:
        dup_fd = os.dup(file.file.fileno())
        result = await asyncio.to_thread(minio_client.fput_object,
                                         bucket_name,
                                         new_filename,
                                         dup_fd  # оптимизация Zero-copy которая была в старом проекте
                                         )
        # Отправка сообщения в брокер о том, что видео было выгружено
        await send_video_uploaded_message(UnprocessedVideoUploaded(user_uuid=user.uuid, video_path=new_filename))
    except S3Error as e:
        return False, e

    except Exception as e:
        try:
            if await _object_exists(bucket_name, new_filename):
                await asyncio.to_thread(minio_client.remove_object, bucket_name, new_filename)
        except Exception:
            pass
        return False, e

    return True, 0


@router.post("/upload_video")
async def upload_video(user: UserSchema = Depends(get_current_user), file: UploadFile = File(...)):
    if user is None:
        raise HTTPException(401, detail={"msg": "Unauthorized"})

    if not _is_valid_video_file(file):
        raise HTTPException(
            400,
            detail={
                "msg": "Not allowed file type",
                "allowed": list(VIDEO_EXTENSIONS),
                "received": {
                    "filename": file.filename,
                    "content_type": file.content_type
                }
            }
        )

    if not _is_allowed_file_size(file):
        raise HTTPException(413, detail={"msg": "File is bigger than 2GB"})
    res, e = await _try_upload_video(file, user)
    if not res:
        raise HTTPException(500, detail=f"Error while uploading video {e}")

    return ORJSONResponse(status_code=200, content={"msg": "successfully uploaded"})

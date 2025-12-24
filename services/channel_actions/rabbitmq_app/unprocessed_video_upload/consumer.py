import uuid

from faststream import AckPolicy

from database.session import async_session
from database.models.video_info import VideoInfo

from ._schemas import UnprocessedVideoUploaded, ConvertVideoToHls
from ..queues import unprocessed_video_uploaded_queue, convert_video_to_hls_queue

from ..router import router


@router.subscriber(unprocessed_video_uploaded_queue, ack_policy=AckPolicy.NACK_ON_ERROR)
@router.publisher(convert_video_to_hls_queue, persist=True)
async def handle_unprocessed_video_uploaded(info: UnprocessedVideoUploaded) -> bytes:
    async with async_session() as session:
        try:
            video_info_db = VideoInfo(author_uuid=info.user_uuid)
            session.add(video_info_db)
            await session.commit()
            video_uuid = video_info_db.uuid
        except Exception:
            await session.rollback()
            raise

    return ConvertVideoToHls(video_uuid=video_uuid, video_path=info.video_path)

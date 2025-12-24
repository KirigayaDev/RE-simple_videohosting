import uuid

import orjson

from faststream import AckPolicy

from database.session import async_session
from database.models.video_info import VideoInfo

from ._schema import UnprocessedVideoUploaded
from ..queues import unprocessed_video_uploaded_queue, convert_video_to_hls_queue

from ..router import router


@router.subscriber(unprocessed_video_uploaded_queue, ack_policy=AckPolicy.NACK_ON_ERROR)
@router.publisher(convert_video_to_hls_queue, persist=True)
async def handle_unprocessed_video_uploaded(info: UnprocessedVideoUploaded) -> bytes:
    video_uuid = uuid.uuid4()
    async with async_session() as session:
        video_info_db = VideoInfo(uuid=video_uuid, author_uuid=info.user_uuid)
        session.add(video_info_db)
        await session.commit()

    return orjson.dumps({"video_path": info.video_path, "uuid": video_uuid})

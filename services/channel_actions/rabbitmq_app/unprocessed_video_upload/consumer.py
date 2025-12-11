import uuid

import orjson

from faststream.rabbit import RabbitQueue

from database.session import async_session
from database.models.video_info import VideoInfo

from ._schema import UnprocessedVideoUploaded

from ..router import router

unprocessed_video_uploaded_queue = RabbitQueue("unprocessed_video_uploaded", durable=True, auto_delete=False,
                                               exclusive=False,
                                               arguments={"delivery_mode": 2})

convert_video_to_hls_queue = RabbitQueue("convert_video_to_hls", durable=True, auto_delete=False,
                                         exclusive=False,
                                         arguments={"delivery_mode": 2})


@router.publisher(convert_video_to_hls_queue, persist=True)
@router.subscriber(unprocessed_video_uploaded_queue, retry=True)
async def handle_unprocessed_video_uploaded(info: UnprocessedVideoUploaded) -> bytes:
    video_uuid = uuid.uuid4()
    async with async_session() as session:
        video_info_db = VideoInfo(uuid=video_uuid, author_uuid=info.user_uuid)
        session.add(video_info_db)
        await session.commit()

    return orjson.dumps({"video_path": info.video_path, "uuid": video_uuid})

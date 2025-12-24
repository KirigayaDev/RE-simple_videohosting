from faststream import AckPolicy

from sqlalchemy import update

from database.session import async_session
from database.models.video_info import VideoInfo

from ._schemas import ConfirmVideoHlsConverting
from ..queues import confirm_video_hls_converting_queue

from ..router import router


@router.subscriber(confirm_video_hls_converting_queue, ack_policy=AckPolicy.NACK_ON_ERROR)
async def confirm_video_hls_converting(info: ConfirmVideoHlsConverting):
    async with async_session() as session:
        await session.execute(
            update(VideoInfo).where(VideoInfo.uuid == info.uuid).values(is_complete=True)
        )
        await session.commit()

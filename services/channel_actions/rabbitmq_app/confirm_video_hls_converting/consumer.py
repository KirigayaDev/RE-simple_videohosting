from faststream.rabbit import RabbitQueue
from faststream import AckPolicy

from sqlalchemy import update

from database.session import async_session
from database.models.video_info import VideoInfo

from ._schema import ConfirmVideoHlsConverting

from ..router import router

confirm_video_hls_converting_queue = RabbitQueue("confirm_video_hls_converting", durable=True, auto_delete=False,
                                                 exclusive=False,
                                                 arguments={"delivery_mode": 2})


@router.subscriber(confirm_video_hls_converting_queue, ack_policy=AckPolicy.NACK_ON_ERROR)
async def confirm_video_hls_converting(info: ConfirmVideoHlsConverting):
    async with async_session() as session:
        await session.execute(
            update(VideoInfo).where(VideoInfo.uuid == info.uuid).values(is_complete=True)
        )
        await session.commit()

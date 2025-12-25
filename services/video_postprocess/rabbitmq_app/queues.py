import asyncio

from faststream.rabbit import RabbitQueue

from .router import router

convert_video_to_hls_queue = RabbitQueue("convert_video_to_hls", durable=True, auto_delete=False,
                                         exclusive=False,
                                         arguments={"delivery_mode": 2})
confirm_video_hls_converting_queue = RabbitQueue("confirm_video_hls_converting", durable=True, auto_delete=False,
                                                 exclusive=False,
                                                 arguments={"delivery_mode": 2})


@router.after_startup
async def declare_queues(broker):
    await asyncio.gather(router.broker.declare_queue(convert_video_to_hls_queue),
                         router.broker.declare_queue(confirm_video_hls_converting_queue))

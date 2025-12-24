import asyncio

from faststream.rabbit import RabbitQueue

from .router import router

unprocessed_video_uploaded_queue = RabbitQueue("unprocessed_video_uploaded", durable=True, auto_delete=False,
                                               exclusive=False,
                                               arguments={"delivery_mode": 2})
convert_video_to_hls_queue = RabbitQueue("convert_video_to_hls", durable=True, auto_delete=False,
                                         exclusive=False,
                                         arguments={"delivery_mode": 2})
confirm_video_hls_converting_queue = RabbitQueue("confirm_video_hls_converting", durable=True, auto_delete=False,
                                                 exclusive=False,
                                                 arguments={"delivery_mode": 2})


@router.after_startup
async def declare_queues(broker): # Крутой баг, в broker попадает FastAPI каким-то образом, а не RabbitBroker
    await asyncio.gather(router.broker.declare_queue(convert_video_to_hls_queue),
                         router.broker.declare_queue(unprocessed_video_uploaded_queue),
                         router.broker.declare_queue(confirm_video_hls_converting_queue))

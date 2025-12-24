from faststream.rabbit import RabbitQueue

from .router import router

from schemas.unprocessed_video_uploaded import UnprocessedVideoUploaded

unprocessed_video_uploaded_queue: RabbitQueue = RabbitQueue("unprocessed_video_uploaded",
                                                            durable=True,
                                                            auto_delete=False,
                                                            exclusive=False,
                                                            arguments={"x-delivery-mode": 2})

_publisher = router.publisher(unprocessed_video_uploaded_queue)


async def send_video_uploaded_message(info: UnprocessedVideoUploaded):
    await _publisher.publish(info)

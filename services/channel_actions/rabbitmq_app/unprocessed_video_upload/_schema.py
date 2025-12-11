from pydantic import BaseModel, UUID4


class UnprocessedVideoUploaded(BaseModel):
    user_uuid: UUID4
    video_path: str

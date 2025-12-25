from pydantic import BaseModel, UUID4


class ConvertVideoToHls(BaseModel):
    video_uuid: UUID4
    video_path: str


class ConfirmVideoHlsConverting(BaseModel):
    uuid: UUID4

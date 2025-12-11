from pydantic import BaseModel, UUID4

class ConfirmVideoHlsConverting(BaseModel):
    uuid: UUID4
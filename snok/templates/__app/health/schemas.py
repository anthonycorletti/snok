from datetime import datetime

from pydantic import BaseModel, StrictStr


class LivezResponse(BaseModel):
    message: StrictStr


class ReadyzResponse(BaseModel):
    message: StrictStr
    version: StrictStr
    time: datetime

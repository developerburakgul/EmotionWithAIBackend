from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_serializer

class Message(BaseModel):
    timestamp: datetime
    sender: str
    text: str
    translated_text: Optional[str] = None  # <-- DÜZELTİLDİ

    @field_serializer('timestamp')
    def serialize_datetime(self, dt: datetime, _info):
        return dt.isoformat()

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
from datetime import datetime
from pydantic import BaseModel, field_serializer
from Helpers.FormatDate import format_datetime

class GroupMessage(BaseModel):
    start_time: datetime
    end_time: datetime
    sender: str
    text: str
    count: int  # Grup içindeki mesaj sayısı
    translated_text: str = None  # <-- Bunu ekle!

    @field_serializer('start_time', 'end_time')
    def serialize_datetime(self, dt: datetime, _info):
        return format_datetime(dt)

    class Config:
        json_encoders = {
            datetime: format_datetime
        }
        from_attributes = True
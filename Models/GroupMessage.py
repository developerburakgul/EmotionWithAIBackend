from datetime import datetime
from pydantic import BaseModel, field_serializer

class GroupMessage(BaseModel):
    start_time: datetime
    end_time: datetime
    sender: str
    text: str

    @field_serializer('start_time', 'end_time')
    def serialize_datetime(self, dt: datetime, _info):
        return dt.isoformat()

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        from_attributes = True
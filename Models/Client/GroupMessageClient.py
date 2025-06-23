from dataclasses import dataclass
from datetime import datetime

from Helpers.FormatDate import format_datetime
from Models import Emotion

@dataclass
class GroupMessageClient:
    sender: str
    start_time: datetime
    end_time: datetime
    emotion: Emotion
    messageCount: int  # Grup içindeki mesaj sayısı
    
    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "start_time": format_datetime(self.start_time),
            "end_time":  format_datetime(self.end_time),
            "emotion": self.emotion.to_dict(),
            "count": self.messageCount
        }    


if __name__ == "__main__":
    print("✅ GroupMessageClient başarıyla çalıştı.")
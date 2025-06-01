from dataclasses import dataclass
from datetime import datetime

from Models import Emotion

@dataclass
class GroupMessageClient:
    sender: str
    start_time: datetime
    end_time: datetime
    emotion: Emotion
    
    def to_dict(self) -> dict:
        return {
            "sender": self.sender,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "emotion": self.emotion.to_dict()
        }    


if __name__ == "__main__":
    print("✅ GroupMessageClient başarıyla çalıştı.")
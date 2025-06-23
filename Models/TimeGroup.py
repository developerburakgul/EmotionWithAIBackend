from dataclasses import dataclass
import datetime
from Models import Emotion

@dataclass
class TimeGroup:
    start_time: datetime
    end_time: datetime
    emotion: Emotion
    total_messages: int
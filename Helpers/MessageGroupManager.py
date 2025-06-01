from Models.GroupMessage import GroupMessage
from Models.Message import Message


class MessageGroupManager:
    """Mesaj gruplama mantığını yöneten yardımcı sınıf"""
    def __init__(self, msg: Message):
        self.sender = msg.sender
        self.start_time = msg.timestamp
        self.end_time = msg.timestamp
        self.text = msg.text

    def can_append(self, msg: Message, time_threshold: int = 300) -> bool:
        """Yeni mesajın gruba eklenip eklenemeyeceğini kontrol eder"""
        return (
            msg.sender == self.sender
            and (msg.timestamp - self.end_time).total_seconds() <= time_threshold
        )

    def append_message(self, msg: Message) -> None:
        """Gruba yeni mesaj ekler"""
        self.text += f" {msg.text}"
        self.end_time = msg.timestamp

    def to_group_message(self) -> GroupMessage:
        """Grup mesajını GroupMessage nesnesine dönüştürür"""
        return GroupMessage(
            sender=self.sender,
            start_time=self.start_time,
            end_time=self.end_time,
            text=self.text
        )
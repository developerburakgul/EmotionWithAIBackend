from dataclasses import dataclass
from typing import List

@dataclass
class Emotion:
    sentiments: List[dict]
    
    def to_dict(self) -> dict:
        """Emotion nesnesini JSON uyumlu dictionary'e dönüştürür."""
        return {
            "sentiments": self.sentiments
        }








from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional
from datetime import datetime

class WhatsappTextRequest(BaseModel):
    text: str
    
    def to_dict(self) -> dict:
        return {"text": self.text}

class UserInfo(BaseModel):
    name: str
    
    def to_dict(self) -> dict:
        return {"name": self.name}

class AnalysisSummary(BaseModel):
    total_messages: int
    
    def to_dict(self) -> dict:
        return {"total_messages": self.total_messages}

class ParticipantData(BaseModel):
    user_info: UserInfo
    analysis_summary: AnalysisSummary
    messages: List
    
    def to_dict(self) -> dict:
        return {
            "user_info": self.user_info.to_dict(),
            "analysis_summary": self.analysis_summary.to_dict(),
            "messages": [msg.to_dict() if hasattr(msg, 'to_dict') else msg for msg in self.messages]
        }

class WhatsappAnalysisResponse(BaseModel):
    participants: Dict[str, ParticipantData]
    
    def to_dict(self) -> dict:
        return {
            "participants": {
                k: v.to_dict() for k, v in self.participants.items()
            }
        }
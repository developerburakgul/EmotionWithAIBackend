from datetime import datetime
from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel, Field, field_serializer
from Helpers.FormatDate import format_datetime  # <-- EKLE

T = TypeVar('T')


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Hata kodu")
    message: str = Field(..., description="Hata mesajı")
    details: Optional[Any] = Field(None, description="Detaylı hata bilgisi")


class ApiResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[ErrorDetail] = None
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_serializer('timestamp')
    def serialize_datetime(self, dt: datetime, _info):
        return format_datetime(dt)  # <-- GÜNCELLE

    class Config:
        json_encoders = {
            datetime: format_datetime  # <-- GÜNCELLE
        }

    @classmethod
    def success_response(cls, data: T, request_id: Optional[str] = None) -> "ApiResponse[T]":
        """Başarılı yanıt oluşturur"""
        return cls(
            success=True,
            data=data
        )

    @classmethod
    def error_response(cls,
                      code: str,
                      message: str,
                      details: Any = None) -> "ApiResponse[T]":
        """Hata yanıtı oluşturur"""
        error_detail = ErrorDetail(
            code=code,
            message=message,
            details=details
        )
        return cls(
            success=False,
            error=error_detail
        )
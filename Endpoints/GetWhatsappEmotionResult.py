from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from datetime import datetime
from typing import Dict, List, Optional
from Models.Client.ApiResponse import ApiResponse
from Models.Client.Response import AnalysisSummary, ParticipantData, UserInfo, WhatsappAnalysisResponse, WhatsappTextRequest
from Helpers.Parser import Parser
from Helpers.EmotionAnalyzer import EmotionAnalyzer
import logging

app = FastAPI()

# Swagger/OpenAPI dokümantasyonu için metadata
app.title = "WhatsApp Emotion Analysis API"
app.description = "WhatsApp sohbet metinleri için duygu analizi API'si"
app.version = "1.0.0"

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/v1/analyze/whatsapp", response_model=ApiResponse)
async def analyze_whatsapp_chat(request: WhatsappTextRequest):
    try:
        if not request.text or not request.text.strip():
            return JSONResponse(
                status_code=400,
                content=ApiResponse.error_response(
                    code="EMPTY_INPUT",
                    message="Boş metin gönderildi",
                    details="Analiz için WhatsApp mesaj metni gerekli"
                ).model_dump()
            )

        # 1. Mesajları ayrıştır
        try:
            messages = Parser.parse_messages(request.text)
        except ValueError as ve:
            return JSONResponse(
                status_code=400,
                content=ApiResponse.error_response(
                    code="INVALID_FORMAT",
                    message="WhatsApp mesaj formatı geçersiz",
                    details=str(ve)
                ).model_dump_json(),
                media_type="application/json"
            )

        if not messages:
            return JSONResponse(
                status_code=400,
                content=ApiResponse.error_response(
                    code="NO_VALID_MESSAGES",
                    message="Geçerli WhatsApp mesajı bulunamadı",
                    details="Mesaj listesi boş"
                ).model_dump()
            )

        # 2. Mesajları grupla
        try:
            grouped_messages = Parser.groupMessages(messages)
        except Exception as ge:
            return JSONResponse(
                status_code=400,
                content=ApiResponse.error_response(
                    code="GROUP_ERROR",
                    message="Mesajlar gruplanamadı",
                    details=str(ge)
                ).model_dump()
            )

        # 3. Duygu analizi yap
        try:
            analyzer = EmotionAnalyzer()
            participants_data: Dict[str, ParticipantData] = {}
            
            for sender, msgs in grouped_messages.items():
                group_message_client_list = analyzer.analyze_group_messages_parallel(msgs)
                participants_data[sender] = ParticipantData(
                    user_info=UserInfo(name=sender),
                    analysis_summary=AnalysisSummary(total_messages=len(group_message_client_list)),
                    messages=group_message_client_list
                )
            
            response_data = WhatsappAnalysisResponse(participants=participants_data)
            return Response(
                content=ApiResponse.success_response(
                    data=response_data.model_dump(exclude_none=True)
                ).model_dump_json(exclude_none=True),
                media_type="application/json",
                status_code=200
            )
            
        except Exception as ae:
            return Response(
                content=ApiResponse.error_response(
                    code="ANALYSIS_ERROR",
                    message="Duygu analizi sırasında hata oluştu",
                    details=str(ae)
                ).model_dump_json(),
                media_type="application/json",
                status_code=500
            )
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ApiResponse.error_response(
                code="UNEXPECTED_ERROR",
                message="Beklenmeyen bir hata oluştu",
                details=str(e)
            ).model_dump()
        )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {str(exc)}", exc_info=True)
    error_response = ApiResponse.error_response(
        code="INVALID_REQUEST",
        message="Geçersiz istek formatı",
        details=str(exc.errors())
    )
    return JSONResponse(
        status_code=400,
        content=error_response.model_dump()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error: {str(exc)}", exc_info=True)
    error_response = ApiResponse.error_response(
        code="UNEXPECTED_ERROR",
        message="Beklenmeyen bir hata oluştu",
        details=str(exc)
    )
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )
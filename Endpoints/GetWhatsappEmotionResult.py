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
        logger.info("Endpoint '/api/v1/analyze/whatsapp' called.")

        if not request.text or not request.text.strip():
            logger.warning("Empty input received.")
            return Response(
                content=ApiResponse.error_response(
                    code="EMPTY_INPUT",
                    message="Boş metin gönderildi",
                    details="Analiz için WhatsApp mesaj metni gerekli"
                ).model_dump_json(),
                media_type="application/json",
                status_code=200
            )

        # 1. Mesajları ayrıştır
        try:
            logger.info("Parsing WhatsApp messages.")
            messages = Parser.parse_messages(request.text)
        except ValueError as ve:
            logger.error(f"Parse error: {ve}", exc_info=True)
            return Response(
                content=ApiResponse.error_response(
                    code="INVALID_FORMAT",
                    message="WhatsApp mesaj formatı geçersiz",
                    details=str(ve)
                ).model_dump_json(),
                media_type="application/json",
                status_code=200
            )

        if not messages:
            logger.warning("No valid messages found after parsing.")
            return Response(
                content=ApiResponse.error_response(
                    code="NO_VALID_MESSAGES",
                    message="Geçerli WhatsApp mesajı bulunamadı",
                    details="Mesaj listesi boş"
                ).model_dump_json(),
                media_type="application/json",
                status_code=200
            )

        # 2. Mesajları grupla
        try:
            logger.info("Grouping messages by sender.")
            grouped_messages = Parser.groupMessages(messages)
        except Exception as ge:
            logger.error(f"Group error: {ge}", exc_info=True)
            return Response(
                content=ApiResponse.error_response(
                    code="GROUP_ERROR",
                    message="Mesajlar gruplanamadı",
                    details=str(ge)
                ).model_dump_json(),
                media_type="application/json",
                status_code=200
            )

        # 3. Duygu analizi yap
        try:
            logger.info("Starting emotion analysis for each participant.")
            analyzer = EmotionAnalyzer()
            participants_data: Dict[str, ParticipantData] = {}

            for sender, msgs in grouped_messages.items():
                logger.info(f"Analyzing messages for participant: {sender}")
                group_message_client_list = analyzer.analyze_group_messages_parallel(msgs)
                participants_data[sender] = ParticipantData(
                    user_info=UserInfo(name=sender),
                    analysis_summary=AnalysisSummary(total_messages=len(group_message_client_list)),
                    messages=group_message_client_list
                )

            response_data = WhatsappAnalysisResponse(participants=participants_data)
            logger.info("Emotion analysis completed successfully.")
            return Response(
                content=ApiResponse.success_response(
                    data=response_data.model_dump(exclude_none=True)
                ).model_dump_json(exclude_none=True),
                media_type="application/json",
                status_code=200
            )

        except Exception as ae:
            logger.error(f"Emotion analysis error: {ae}", exc_info=True)
            return Response(
                content=ApiResponse.error_response(
                    code="ANALYSIS_ERROR",
                    message="Duygu analizi sırasında hata oluştu",
                    details=str(ae)
                ).model_dump_json(),
                media_type="application/json",
                status_code=200
            )

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return Response(
            content=ApiResponse.error_response(
                code="UNEXPECTED_ERROR",
                message="Beklenmeyen bir hata oluştu",
                details=str(e)
            ).model_dump_json(),
            media_type="application/json",
            status_code=200
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
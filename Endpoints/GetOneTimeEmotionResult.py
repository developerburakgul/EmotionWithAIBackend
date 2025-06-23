from fastapi import APIRouter, Response
from Models.Client.ApiResponse import ApiResponse
from Models.Emotion import Emotion
from Helpers.EmotionAnalyzer import EmotionAnalyzer
from Helpers.Translator import TextTranslator

from pydantic import BaseModel

router = APIRouter()

class OneTimeEmotionRequest(BaseModel):
    text: str

@router.post("/api/v1/analyze/one-time", response_model=ApiResponse)
async def analyze_one_time_emotion(request: OneTimeEmotionRequest):
    if not request.text or not request.text.strip():
        return Response(
            content=ApiResponse.error_response(
                code="EMPTY_INPUT",
                message="Boş metin gönderildi",
                details="Analiz için mesaj metni gerekli"
            ).model_dump_json(),
            media_type="application/json",
            status_code=200
        )
    try:
        # Metni İngilizce'ye çevir
        translator = TextTranslator(source_lang='auto', target_lang='en')
        try:
            translated_text = translator.translate_to_english(request.text)
        except Exception as te:
            # Çeviri başarısızsa orijinal metni kullan
            translated_text = request.text

        analyzer = EmotionAnalyzer()
        emotion: Emotion = analyzer.analyze_message(translated_text)
        return Response(
            content=ApiResponse.success_response(
                data=emotion.to_dict()
            ).model_dump_json(exclude_none=True),
            media_type="application/json",
            status_code=200
        )
    except Exception as e:
        return Response(
            content=ApiResponse.error_response(
                code="ANALYSIS_ERROR",
                message="Duygu analizi sırasında hata oluştu",
                details=str(e)
            ).model_dump_json(),
            media_type="application/json",
            status_code=200
        )
from Models.Client.ApiResponse import ApiResponse
from fastapi import APIRouter, HTTPException, Response
from transformers import pipeline, AutoTokenizer

# Global model configurations
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

# Initialize model and tokenizer at startup
classifier = pipeline("sentiment-analysis", model=MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

router = APIRouter()

@router.get("/api/v1/model/max-input-size", response_model=ApiResponse)
async def get_max_input_size():
    """
    Duygu analizi modelinin alabileceği maksimum input boyutunu döndürür.
    """
    try:
        max_tokens = tokenizer.model_max_length
        approx_bytes = max_tokens * 4
        approx_kb = approx_bytes / 1024
        return ApiResponse(
            success=True,
            data={
                "model": MODEL_NAME,
                "task": "sentiment-analysis",
                "max_tokens": max_tokens,
                "approx_size_kb": round(approx_kb, 2),
                "approx_size_bytes": approx_bytes,
                "status": "success"
            }
        )
    except Exception as e:
        return Response(
            content=ApiResponse.error_response(
                code="MODEL_ERROR",
                message="Model bilgisi alınırken hata oluştu",
                details=str(e)
            ).model_dump_json(),
            media_type="application/json",
            status_code=200
        )
from Models.Client.ApiResponse import ApiResponse
from fastapi import FastAPI, HTTPException
from transformers import pipeline, AutoTokenizer
from pydantic import BaseModel
from typing import Dict, Any

# Global model configurations
MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

# Initialize model and tokenizer at startup
classifier = pipeline("sentiment-analysis", model=MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

app = FastAPI()


@app.get("/api/v1/model/max-input-size", response_model=ApiResponse)
async def get_max_input_size():
    """
    Duygu analizi modelinin alabileceği maksimum input boyutunu döndürür.
    
    Returns:
        ApiResponse: Başarı durumu ve maksimum input boyutu bilgisi
    """
    try:
        max_tokens = tokenizer.model_max_length
        # Yaklaşık hesaplama:
        # 1 token ≈ 4 karakter
        # 1 karakter = 1 byte (UTF-8 ASCII için)
        approx_bytes = max_tokens * 4
        
        # Byte'ı KB'a çevirme
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
        raise HTTPException(
            status_code=500,
            detail=ApiResponse(
                success=False,
                error={
                    "code": "MODEL_ERROR",
                    "message": "Model bilgisi alınırken hata oluştu",
                    "details": str(e)
                }
            ).dict()
        )

# Swagger/OpenAPI dokümantasyonu için metadata
app.title = "Emotion Analysis API"
app.description = "Duygu analizi modeli için API endpoints"
app.version = "1.0.0"
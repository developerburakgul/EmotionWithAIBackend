from fastapi import FastAPI
from Endpoints.GetMaxInputSize import router as max_input_router
from Endpoints.GetWhatsappEmotionResult import router as whatsapp_router
from Endpoints.GetOneTimeEmotionResult import router as one_time_emotion_router

app = FastAPI()
app.include_router(max_input_router)
app.include_router(whatsapp_router)
app.include_router(one_time_emotion_router)
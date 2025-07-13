from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentiment import analyze_sentiment
from tts import text_to_speech
import uuid

app = FastAPI()

class CallPayload(BaseModel):
    callerId: str
    transcript: str

@app.post("/call-hook")
async def call_hook(payload: CallPayload):
    if not payload.callerId or not payload.transcript:
        raise HTTPException(status_code=400, detail="Eksik parametre")

    sentiment = analyze_sentiment(payload.transcript)

    if sentiment == "negatif":
        response_text = "Üzgünüz, yaşadığınız deneyim beklentilerinizi karşılamadı. Sizi memnun edebilmek için buradayız."
    elif sentiment == "pozitif":
        response_text = "Görüşleriniz için teşekkür ederiz! Size yardımcı olabildiysek ne mutlu."
    else:
        response_text = "Geri bildiriminiz için teşekkür ederiz."

    filename = f"response_{uuid.uuid4()}.mp3"
    text_to_speech(response_text, filename)

    return {
        "sentiment": sentiment,
        "response_text": response_text,
        "audio_file": filename
    }

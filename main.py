from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_TOKEN = "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"  # paste your HuggingFace token

@app.get("/")
def home():
    return {"status": "Backend with HF working"}

@app.post("/ai-response")
def ai_response(payload: dict):
    user_text = payload.get("text", "")

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    url = "https://router.huggingface.co/models/google/flan-t5-small"

    response = requests.post(
        url,
        headers=headers,
        json={"inputs": user_text},
        timeout=30
    )

    # 🔐 SAFETY CHECK
    if response.status_code != 200:
        return {"reply": "AI is waking up, please try again"}

    try:
        data = response.json()
    except Exception:
        # HF returned non-JSON (loading / empty / HTML)
        return {"reply": "AI is loading, please speak again"}

    if isinstance(data, list) and len(data) > 0:
        reply = data[0].get("generated_text", "No response")
    else:
        reply = "AI could not understand"

    return {"reply": reply}


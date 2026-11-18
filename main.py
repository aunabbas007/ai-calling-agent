import os
import threading

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="AI Calling Agent API", version="0.1.0")

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_URL = "https://router.huggingface.co/hf-inference/models/google/flan-t5-base"


class AIRequest(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


@app.get("/")
def home():
    return {"status": "ok", "service": "AI Calling Agent API"}


@app.get("/health")
def health():
    return {"status": "healthy", "hf_token_configured": bool(HF_TOKEN)}


@app.post("/ai-response")
def ai_response(payload: AIRequest):
    if not HF_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="The AI service is not configured. Set the HF_TOKEN environment variable.",
        )

    try:
        response = requests.post(
            MODEL_URL,
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"inputs": payload.text},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail="The model provider request failed.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="The model provider returned invalid JSON.") from exc

    if isinstance(data, list) and data and isinstance(data[0], dict):
        reply = data[0].get("generated_text")
    elif isinstance(data, dict):
        reply = data.get("generated_text")
    else:
        reply = None

    if not isinstance(reply, str) or not reply.strip():
        raise HTTPException(status_code=502, detail="The model provider returned no generated text.")

    return {"reply": reply}


def warm_up():
    if not HF_TOKEN:
        return
    try:
        requests.post(
            MODEL_URL,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": "Hello"},
            timeout=30,
        )
    except requests.RequestException:
        pass


if HF_TOKEN:
    threading.Thread(target=warm_up, daemon=True).start()

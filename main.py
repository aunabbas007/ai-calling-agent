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

    # Model name (you can choose another free model)
    url = "https://router.huggingface.co/models/google/flan-t5-small"


    data = {"inputs": user_text}

    response = requests.post(url, headers=headers, json=data)

    # Some HF models return list of text
    if isinstance(response.json(), list):
        reply = response.json()[0]["generated_text"]
    else:
        # fallback
        reply = response.json().get("generated_text", str(response.json()))

    return {"reply": reply}

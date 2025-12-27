from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

# 🔑 PUT YOUR API KEY HERE
client = OpenAI(api_key="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")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "ChatGPT Voice Backend Running"}

@app.post("/ai-response")
def ai_response(payload: dict):
    user_text = payload.get("text", "")

    if not user_text:
        return {"reply": "I did not hear anything."}

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly AI assistant."},
            {"role": "user", "content": user_text}
        ]
    )

    ai_reply = response.choices[0].message.content
    return {"reply": ai_reply}

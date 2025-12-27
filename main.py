from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Browser Voice Demo Backend Running"}

@app.post("/ai-response")
def ai_response(payload: dict):
    user_text = payload.get("text", "")
    return {
        "reply": f"You said {user_text}. This is a browser based AI demo."
    }

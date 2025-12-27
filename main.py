from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# ✅ CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (safe for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Browser Voice Demo Backend Running"}

@app.post("/ai-response")
def ai_response(data: dict):
    user_text = data.get("text", "")
    reply = f"You said {user_text}. This is a browser based AI demo."
    return JSONResponse({"reply": reply})


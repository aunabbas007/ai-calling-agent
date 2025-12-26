from fastapi import FastAPI
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client

app = FastAPI()

# 🔴 REPLACE THESE WITH YOUR REAL VALUES
ACCOUNT_SID = "AC68ab81de9865cb7ea142eb358baf98e2"
AUTH_TOKEN = "1b54de2b21eae6cfc4626f9386092f0f"
TWILIO_NUMBER = "+17654357933"      # Twilio US number
YOUR_NUMBER = "+919945948706"       # Your Indian number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.get("/")
def home():
    return {"message": "AI Calling Agent backend is running"}

@app.post("/incoming-call")
def incoming_call():
    response = VoiceResponse()
    response.say(
        "Hello! This is your AI calling agent.How may I help you today?"
    )
    return str(response)

@app.get("/call-me")
def call_me():
    call = client.calls.create(
        to=YOUR_NUMBER,
        from_=TWILIO_NUMBER,
        url="https://ai-calling-agent-017m.onrender.com/incoming-call"
    )
    return {"status": "Calling your phone now"}

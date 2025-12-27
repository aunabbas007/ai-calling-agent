from fastapi import FastAPI
from twilio.twiml.voice_response import VoiceResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Calling Agent backend is running"}

@app.post("/incoming-call")
def incoming_call():
    response = VoiceResponse()
    response.say(
        "Hello. This is the incoming call test. Your AI calling agent is working."
    )
    return str(response)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Calling Agent backend is running"}

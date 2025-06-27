# filename: app.py
from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"

class SummaryRequest(BaseModel):
    content: str

@app.post("/summarize")
def summarize(data: SummaryRequest):
    prompt = f"Summarize the following text:\n\n{data.content.strip()}"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = httpx.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    return {"summary": response.json().get("response", "")}


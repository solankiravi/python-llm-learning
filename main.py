# filename: app.py
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from selectolax.lexbor import LexborHTMLParser

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"

class SummaryRequest(BaseModel):
    web_url: str

@app.post("/summarize")
async def summarize(data: SummaryRequest):
    data = requests.get(data.web_url)
    parser = LexborHTMLParser(data.content)
    
    text_content = parser.body.text(strip=True)
    if not text_content:
        return {"summary": "No text content found."}

    payload = {
        "model": MODEL_NAME,
        "prompt": f"provide the summary of text -  {text_content}",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    if response.status_code != 200:
        return {"summary": "Error generating summary."}

    return {"summary": response.json().get("response").strip()}


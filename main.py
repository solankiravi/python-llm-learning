from fastapi import FastAPI
import whisper
import requests
from selectolax.lexbor import LexborHTMLParser
from moviepy.video.io.VideoFileClip import VideoFileClip
from os import remove, path

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"


async def get_summary(text: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": f"provide the summary of text -  {text}",
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    if response.status_code != 200:
        return "Error generating summary."
    
    return response.json().get("response").strip()

async def get_audio_from_video(video_path: str, audio_path: str) -> None:
    
    if path.exists(audio_path):
        remove(audio_path)
    
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(audio_path)

async def summarize_audio(audio_path: str) -> str:
    whisper_model = whisper.load_model("base")
    
    if not path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    result = whisper_model.transcribe(audio_path, language='en', fp16=False)
    return result['text'].strip()

@app.post("/summarize_webpage")
async def summarize_webpage(web_url: str):
    data = requests.get(web_url)
    parser = LexborHTMLParser(data.content)
    
    text_content = parser.body.text(strip=True)
    if not text_content:
        return {"summary": "No text content found."}

    get_summary = await get_summary(text_content)
    return {"summary": get_summary}

@app.post("/summarize_video")
async def summarize_video(video_path: str):
    audio_path = "output_audio.wav"
    await get_audio_from_video(video_path, audio_path)
    transcription = await summarize_audio(audio_path)
    summary = await get_summary(transcription)
    return {"summary": summary}


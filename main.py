import base64
import tempfile
from typing import Final

from faster_whisper import WhisperModel
import whisper

import asyncio

from pydantic import BaseModel

# import logging
import numpy as np

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

SERVER_PORT: Final = 8000
MODEL_SIZE: Final = "tiny"
VAD_FILTER: Final = True
DOWNLOAD_ROOT: Final = "./models"
CORS_ORIGINS: Final = ["http://localhost:5173"]


model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8",
    cpu_threads=1,
    download_root=DOWNLOAD_ROOT,
)

app = FastAPI()

origins = CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def process_wav_bytes(
    webm_bytes: bytes, sample_rate: int = 16000, chunk_size: int = 48000
):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_file:
        temp_file.write(webm_bytes)
        temp_file.flush()
        waveform = whisper.load_audio(temp_file.name, sr=sample_rate)

        num_chunks = max(len(waveform) // chunk_size, 1)
        chunked_waveform = np.array_split(waveform, num_chunks)

        return chunked_waveform


def sync_transcription(audio: str) -> str:
    chunk_base64 = base64.b64decode(audio)
    chunks = process_wav_bytes(chunk_base64)

    full_transcription = ""
    for chunk in chunks:
        segments, _ = model.transcribe(
            chunk,
            language="pt",
            vad_filter=VAD_FILTER,
            condition_on_previous_text=True,
        )

        transcription = [segment.text for segment in segments]
        transcription = " ".join(transcription)

        full_transcription += transcription

    return full_transcription


@app.get("/")
async def health_check():
    return {"status": 1}


class TranscribeInput(BaseModel):
    audio: str


class TranscribeOutput(BaseModel):
    transcription: str


@app.post("/whisper", response_model=TranscribeOutput)
async def handle(
    input: TranscribeInput,
):
    # TODO: handle inputs has base64 (start with base64) [X]
    # TODO: Dockerize this
    # TODO: handle exceptions like vad
    # TODO: Log all process time to monitor performance (justificative)
    # TODO: Otimize this process to be faster and not need encode base64 (maybe this is slow) and remove
    # external depedency like whisper load audio from pip
    # TODO: maybe run transcription in a separate thread
    # TODO: maybe put a queue to process multiple requests

    loop = asyncio.get_event_loop()
    transcription = await loop.run_in_executor(None, sync_transcription, input.audio)

    return {"transcription": transcription}

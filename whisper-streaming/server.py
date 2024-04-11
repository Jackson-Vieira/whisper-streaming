from aiohttp import web
from typing import Final
from faster_whisper import WhisperModel
import aiohttp_cors
import whisper
import numpy as np
import logging
import tempfile
import base64

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SERVER_PORT: Final = 8000
MODEL_SIZE: Final = "small"

app = web.Application()
model = WhisperModel(MODEL_SIZE, device="cuda", compute_type="float16")


def process_wav_bytes(
    webm_bytes: bytes, sample_rate: int = 16000, chunk_size: int = 48000
):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as temp_file:
        temp_file.write(webm_bytes)
        temp_file.flush()
        waveform = whisper.load_audio(temp_file.name, sr=sample_rate)

        num_chunks = max(len(waveform) // chunk_size, 1)
        chunked_waveform = np.array_split(waveform, num_chunks)

        logger.info(f"Processing {len(chunked_waveform)} chunks")

        return chunked_waveform


def transcribe_chunk(chunk: bytes) -> str:
    # chunk is a base64 encoded string
    chunk_base64 = base64.b64decode(chunk)
    chunks = process_wav_bytes(chunk_base64)

    transcription = ""
    for chunk in chunks:
        # chunk = chunk.reshape(1, -1)
        # processed_chunk = whisper.pad_or_trim(chunk)
        segments, _ = model.transcribe(
            chunk, language="pt", condition_on_previous_text=False, vad_filter=True
        )
        for segment in segments:
            transcription += segment.text

    return transcription


# make a curl request to test this
# curl -X POST http://localhost:8000/whisper -H "Content-Type: application/json" -d '{"chunk": "base64"}'
async def hello(request):
    response = await request.json()
    chunk = response["chunk"]
    logging.info(f"Transcribing chunk: {chunk}")
    transcription = transcribe_chunk(chunk)
    return web.json_response({"transcription": transcription})


app.add_routes([web.post("/whisper", hello)])

cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True, expose_headers="*", allow_headers="*"
        )
    },
)

for route in list(app.router.routes()):
    cors.add(route)

if __name__ == "__main__":
    web.run_app(app, port=SERVER_PORT, host="0.0.0.0")

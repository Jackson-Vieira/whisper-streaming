from aiohttp import web
from typing import Final
from faster_whisper import WhisperModel
import aiohttp_cors
import logging
import numpy as np
from numpy import ndarray

logging.basicConfig()
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

SERVER_PORT: Final = 8000
MODEL_SIZE: Final = "medium"
VAD_FILTER: Final = False

app = web.Application()
model = WhisperModel(MODEL_SIZE, device="cuda", compute_type="float16")


def transcribe(array_data: ndarray) -> str:
    segments, _ = model.transcribe(
        array_data,
        language="pt",
        vad_filter=True,
        condition_on_previous_text=True,
    )

    transcription = [segment.text for segment in segments]
    transcription = " ".join(transcription)

    return transcription


# 1. Latencia
# 2. Disponibilidade
# 3. Escalabilidade


async def handle(request):
    buffer = await request.content.read()
    buffer_array = np.frombuffer(buffer, dtype=np.float32)

    transcription = transcribe(buffer_array)
    return web.json_response({"transcription": transcription})


app.add_routes([web.post("/whisper", handle)])

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

"""
tts_proxy.py — tiny local HTTP proxy in front of NVIDIA's hosted Magpie TTS.

WHY THIS EXISTS:
NVIDIA's hosted Magpie TTS (the free NIM endpoint) is a gRPC API at
grpc.nvcf.nvidia.com:443, authenticated with a `function-id` + Bearer token
via the Riva client. Browsers can't make raw gRPC calls, and the API key
shouldn't be shipped to client-side JS anyway — so anahita.html calls this
tiny local proxy over plain HTTP, and this proxy does the real gRPC call to
NVIDIA and returns a WAV file.

SETUP:
    pip install fastapi "uvicorn[standard]" nvidia-riva-client --break-system-packages
    export NVIDIA_API_KEY="nvapi-...."          # from build.nvidia.com/nvidia/magpie-tts-multilingual
    uvicorn tts_proxy:app --host 0.0.0.0 --port 8791

Then in anahita.html's config drawer, point "TTS proxy base URL" at
http://localhost:8791 (that's already the default).

NOTE ON THE RIVA CLIENT CALL: `function-id` below is the Magpie TTS
Multilingual function id shown on build.nvidia.com/nvidia/magpie-tts-multilingual/api
at the time this was written. If NVIDIA rotates it, or you're using a
different Magpie variant (zeroshot, flow), grab the current id + curl/python
snippet from that model's "API Reference" tab and swap FUNCTION_ID below.
"""

import io
import os
import wave
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

import riva.client

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tts_proxy")

NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
RIVA_SERVER = "grpc.nvcf.nvidia.com:443"
FUNCTION_ID = "877104f7-e885-42b9-8de8-f6e4c6303969"  # Magpie TTS Multilingual
DEFAULT_SAMPLE_RATE = 44100

app = FastAPI(title="Anahita TTS proxy")

# Local dev proxy — anahita.html is opened straight from disk / a plain
# static server, so keep CORS wide open here. Tighten this if you ever
# deploy the proxy somewhere less trusted than localhost.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SpeakRequest(BaseModel):
    text: str
    voice: str = "Magpie-Multilingual.EN-US.Aria"
    language_code: str = "en-US"
    sample_rate_hz: int = DEFAULT_SAMPLE_RATE


def _pcm_to_wav_bytes(pcm_bytes: bytes, sample_rate: int, channels: int = 1, sample_width: int = 2) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_bytes)
    return buf.getvalue()


_tts_service = None


def get_tts_service():
    global _tts_service
    if _tts_service is not None:
        return _tts_service
    if not NVIDIA_API_KEY:
        raise HTTPException(status_code=500, detail="NVIDIA_API_KEY env var is not set")
    auth = riva.client.Auth(
        uri=RIVA_SERVER,
        use_ssl=True,
        metadata_args=[
            ["function-id", FUNCTION_ID],
            ["authorization", f"Bearer {NVIDIA_API_KEY}"],
        ],
    )
    _tts_service = riva.client.SpeechSynthesisService(auth)
    return _tts_service


@app.get("/health")
def health():
    return {"ok": True, "has_api_key": bool(NVIDIA_API_KEY)}


@app.post("/speak")
def speak(req: SpeakRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="text is empty")

    service = get_tts_service()
    try:
        resp = service.synthesize(
            text=req.text,
            voice_name=req.voice,
            language_code=req.language_code,
            sample_rate_hz=req.sample_rate_hz,
        )
    except Exception as exc:  # noqa: BLE001 — surface the real gRPC error to the caller
        log.exception("Riva synthesize call failed")
        raise HTTPException(status_code=502, detail=f"NVIDIA TTS call failed: {exc}") from exc

    wav_bytes = _pcm_to_wav_bytes(resp.audio, req.sample_rate_hz)
    return Response(content=wav_bytes, media_type="audio/wav")

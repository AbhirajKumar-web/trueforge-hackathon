# Anahita voice frontend — setup

Two pieces:

1. **`anahita.html`** — the frontend. Open it directly in Chrome/Edge (Web
   Speech API needs a Chromium browser). No build step, no server required
   for the HTML itself.
2. **`tts_proxy.py`** — a tiny local proxy so the browser can reach NVIDIA's
   Magpie TTS. Required because NVIDIA's hosted TTS is a **gRPC** API
   (`grpc.nvcf.nvidia.com:443`), not a plain REST/CORS endpoint the browser
   can call directly — and the API key shouldn't sit in client-side JS anyway.

## Run order

```bash
pip install fastapi "uvicorn[standard]" nvidia-riva-client --break-system-packages
export NVIDIA_API_KEY="nvapi-...."        # from build.nvidia.com/nvidia/magpie-tts-multilingual
uvicorn tts_proxy:app --host 0.0.0.0 --port 8791
```

Then open `anahita.html`, click **⚙ config**, and confirm:
- **TrueForge base URL** → defaults to `http://localhost:8790/api/v1`
- **TTS proxy base URL** → defaults to `http://localhost:8791` (matches the
  proxy above)

## The one thing you still need to check

The `ENDPOINTS` object at the top of `anahita.html`'s `<script>` block —
session create, post-turn, SSE subscribe, approval, tool-response — is my
best guess at REST conventions from your description ("sessions, turns, SSE
subscribe, approval/tool-response events"). I couldn't reach your
`localhost:8790` from here to read the real OpenAPI schema. Two ways to
close that gap:

- Open `localhost:8790/api/v1/docs` yourself, and adjust the four path
  templates in `ENDPOINTS` if they differ (five-minute edit).
- Or paste me the schema JSON and I'll wire the exact paths + field names in.

Everything else — the SSE event handling, the approval modal, the mic input,
the TTS playback — is written to degrade gracefully: unrecognized SSE event
shapes get dumped into the log strip at the bottom instead of silently
failing, so you can see the real payload shapes the first time you run it
against your live server and adjust from there.

## Not yet wired

- Hindi-voice TTS: Magpie TTS Multilingual does support Hindi, but I don't
  know which exact voice IDs are enabled on your deployment — the config
  drawer has an `HI-IN` option marked "if deployed"; check
  `build.nvidia.com/nvidia/magpie-tts-multilingual` → API Reference for the
  current voice list if `EN-US` reading Hinglish text doesn't sound right.

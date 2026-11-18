# AI Calling Agent API

A minimal FastAPI service that accepts text and returns generated text from the Hugging Face Inference API. The current implementation uses Google's FLAN-T5 Base model through the Hugging Face router.

> **Scope note:** The repository currently contains a text-in/text-out inference API. It does not yet implement telephony, speech recognition, text-to-speech, call routing, or a complete voice-agent workflow.

## Features

- FastAPI endpoints for service status, health, and text generation.
- Hugging Face inference using an environment-based access token.
- Pydantic request validation.
- Configurable CORS origins through `ALLOWED_ORIGINS`.
- Provider timeouts and explicit HTTP error handling.

## Requirements

- Python 3.10+
- Hugging Face access token with permission to use the selected inference provider/model.

## Local setup

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Configure environment variables before starting the server.

**Windows PowerShell**
```powershell
$env:HF_TOKEN="your_hugging_face_token"
$env:ALLOWED_ORIGINS="http://localhost:3000"
```

**macOS/Linux**
```bash
export HF_TOKEN="your_hugging_face_token"
export ALLOWED_ORIGINS="http://localhost:3000"
```

Start the API:

```bash
uvicorn main:app --reload
```

- API root: http://127.0.0.1:8000/
- Health: http://127.0.0.1:8000/health
- Interactive API docs: http://127.0.0.1:8000/docs

## Example request

```bash
curl -X POST "http://127.0.0.1:8000/ai-response" \
  -H "Content-Type: application/json" \
  -d '{"text":"Explain machine learning in one sentence."}'
```

Example response shape:

```json
{"reply":"...generated text..."}
```

## Configuration

| Variable | Purpose |
| --- | --- |
| `HF_TOKEN` | Hugging Face access token; never commit this value |
| `ALLOWED_ORIGINS` | Comma-separated browser origins allowed by CORS |

## Security

- Store credentials in environment variables or a secret manager.
- Never commit `.env`, API tokens, or other credentials.
- Restrict `ALLOWED_ORIGINS` to the actual frontend origins in deployment.
- Rotate any token that has ever been committed to a public repository. Removing it from the latest version does not remove it from Git history.

## Current limitations

- This is a minimal inference API, not a production voice-calling system.
- Hugging Face provider/model availability and usage limits can change.
- Authentication, rate limiting, persistent conversation state, automated tests, and telephony integration are not implemented.
- Add tests and deployment configuration before treating the service as production-ready.

## Author

[Aun Abbas](https://github.com/aunabbas007) · [LinkedIn](https://www.linkedin.com/in/aunabbas07/)

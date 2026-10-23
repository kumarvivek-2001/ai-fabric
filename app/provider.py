import os

import httpx
from fastapi import HTTPException


async def create_chat_completion(payload: dict) -> dict:
    """Send a chat completion request to the configured AI provider."""

    base_url = os.getenv("AI_PROVIDER_BASE_URL", "").rstrip("/")
    api_key = os.getenv("AI_PROVIDER_API_KEY", "")
    default_model = os.getenv("AI_PROVIDER_MODEL", "")

    if not base_url or not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI provider is not configured.",
        )

    request_payload = dict(payload)
    request_payload["model"] = request_payload.get("model") or default_model

    if not request_payload["model"]:
        raise HTTPException(
            status_code=503,
            detail="AI provider model is not configured.",
        )

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{base_url}/chat/completions",
                json=request_payload,
                headers={"Authorization": f"Bearer {api_key}"},
            )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AI provider timed out.",
        )
    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="AI provider request failed.",
        )

    if response.is_error:
        raise HTTPException(
            status_code=502,
            detail="AI provider returned an error.",
        )

    return response.json()

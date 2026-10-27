import asyncio
import os

import httpx
from fastapi import HTTPException


async def _request_provider(
    base_url: str,
    api_key: str,
    model: str,
    payload: dict,
) -> dict:
    request_payload = dict(payload)
    request_payload["model"] = request_payload.get("model") or model

    if not request_payload["model"]:
        raise HTTPException(
            status_code=503,
            detail="AI provider model is not configured.",
        )

    last_error = None

    for attempt in range(2):
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{base_url.rstrip('/')}/chat/completions",
                    json=request_payload,
                    headers={"Authorization": f"Bearer {api_key}"},
                )

            status_code = response.status_code

            # Retry transient HTTP failures only when a real status code is available.
            if isinstance(status_code, int) and (
                status_code in (408, 429) or status_code >= 500
            ):
                last_error = HTTPException(
                    status_code=502,
                    detail="AI provider returned a temporary error.",
                )
                if attempt == 0:
                    await asyncio.sleep(0.25)
                    continue
                raise last_error

            if response.is_error:
                raise HTTPException(
                    status_code=502,
                    detail="AI provider returned an error.",
                )

            try:
                return response.json()
            except ValueError:
                raise HTTPException(
                    status_code=502,
                    detail="AI provider returned invalid JSON.",
                )

        except httpx.TimeoutException:
            last_error = HTTPException(
                status_code=504,
                detail="AI provider timed out.",
            )
            if attempt == 0:
                await asyncio.sleep(0.25)
                continue
            raise last_error
        except httpx.HTTPError:
            last_error = HTTPException(
                status_code=502,
                detail="AI provider request failed.",
            )
            if attempt == 0:
                await asyncio.sleep(0.25)
                continue
            raise last_error

    raise last_error or HTTPException(
        status_code=502,
        detail="AI provider request failed.",
    )


async def create_chat_completion(payload: dict) -> dict:
    """Send a chat completion request with one bounded retry for transient errors."""
    base_url = os.getenv("AI_PROVIDER_BASE_URL", "").rstrip("/")
    api_key = os.getenv("AI_PROVIDER_API_KEY", "")
    default_model = os.getenv("AI_PROVIDER_MODEL", "")

    if not base_url or not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI provider is not configured.",
        )

    model = payload.get("model") or default_model
    if not model:
        raise HTTPException(
            status_code=503,
            detail="AI provider model is not configured.",
        )

    return await _request_provider(base_url, api_key, model, payload)

import pytest
from fastapi import HTTPException

from app.provider import create_chat_completion


@pytest.mark.anyio
async def test_provider_requires_configuration(monkeypatch):
    monkeypatch.delenv("AI_PROVIDER_BASE_URL", raising=False)
    monkeypatch.delenv("AI_PROVIDER_API_KEY", raising=False)
    monkeypatch.delenv("AI_PROVIDER_MODEL", raising=False)

    with pytest.raises(HTTPException) as exc_info:
        await create_chat_completion(
            {"messages": [{"role": "user", "content": "Hello"}]}
        )

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "AI provider is not configured."


@pytest.mark.anyio
async def test_provider_requires_model(monkeypatch):
    monkeypatch.setenv(
        "AI_PROVIDER_BASE_URL",
        "https://api.tokenfactory.nebius.com/v1",
    )
    monkeypatch.setenv("AI_PROVIDER_API_KEY", "test-key")
    monkeypatch.delenv("AI_PROVIDER_MODEL", raising=False)

    with pytest.raises(HTTPException) as exc_info:
        await create_chat_completion(
            {"messages": [{"role": "user", "content": "Hello"}]}
        )

    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == "AI provider model is not configured."

from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.anyio
async def test_provider_returns_successful_response(monkeypatch):
    monkeypatch.setenv(
        "AI_PROVIDER_BASE_URL",
        "https://api.tokenfactory.nebius.com/v1",
    )
    monkeypatch.setenv("AI_PROVIDER_API_KEY", "test-key")
    monkeypatch.setenv("AI_PROVIDER_MODEL", "test-model")

    fake_response = MagicMock()
    fake_response.is_error = False
    fake_response.json.return_value = {
        "id": "test-response",
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Hello from fake provider",
                }
            }
        ],
    }

    fake_client = AsyncMock()
    fake_client.post.return_value = fake_response

    with patch("app.provider.httpx.AsyncClient") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = fake_client

        result = await create_chat_completion(
            {"messages": [{"role": "user", "content": "Hello"}]}
        )

    assert result["id"] == "test-response"
    assert result["choices"][0]["message"]["content"] == "Hello from fake provider"

    fake_client.post.assert_awaited_once()
    call_kwargs = fake_client.post.await_args.kwargs
    assert call_kwargs["json"]["model"] == "test-model"
    assert call_kwargs["headers"]["Authorization"] == "Bearer test-key"

@pytest.mark.anyio
async def test_provider_timeout_returns_504(monkeypatch):
    import httpx
    from fastapi import HTTPException

    monkeypatch.setenv(
        "AI_PROVIDER_BASE_URL",
        "https://api.tokenfactory.nebius.com/v1",
    )
    monkeypatch.setenv("AI_PROVIDER_API_KEY", "test-key")
    monkeypatch.setenv("AI_PROVIDER_MODEL", "test-model")

    fake_client = AsyncMock()
    fake_client.post.side_effect = httpx.TimeoutException("Request timed out")

    with patch("app.provider.httpx.AsyncClient") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = fake_client

        with pytest.raises(HTTPException) as exc_info:
            await create_chat_completion(
                {"messages": [{"role": "user", "content": "Hello"}]}
            )

    assert exc_info.value.status_code == 504
    assert exc_info.value.detail == "AI provider timed out."


@pytest.mark.anyio
async def test_provider_error_returns_502(monkeypatch):
    monkeypatch.setenv(
        "AI_PROVIDER_BASE_URL",
        "https://api.tokenfactory.nebius.com/v1",
    )
    monkeypatch.setenv("AI_PROVIDER_API_KEY", "test-key")
    monkeypatch.setenv("AI_PROVIDER_MODEL", "test-model")

    fake_response = MagicMock()
    fake_response.is_error = True

    fake_client = AsyncMock()
    fake_client.post.return_value = fake_response

    with patch("app.provider.httpx.AsyncClient") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = fake_client

        with pytest.raises(HTTPException) as exc_info:
            await create_chat_completion(
                {"messages": [{"role": "user", "content": "Hello"}]}
            )

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail == "AI provider returned an error."

@pytest.mark.anyio
async def test_provider_retries_temporary_error(monkeypatch):
    monkeypatch.setenv(
        "AI_PROVIDER_BASE_URL",
        "https://api.tokenfactory.nebius.com/v1",
    )
    monkeypatch.setenv("AI_PROVIDER_API_KEY", "test-key")
    monkeypatch.setenv("AI_PROVIDER_MODEL", "test-model")

    first_response = MagicMock()
    first_response.status_code = 503
    first_response.is_error = True

    second_response = MagicMock()
    second_response.status_code = 200
    second_response.is_error = False
    second_response.json.return_value = {"id": "recovered"}

    fake_client = AsyncMock()
    fake_client.post.side_effect = [first_response, second_response]

    with patch("app.provider.httpx.AsyncClient") as mock_client_class:
        mock_client_class.return_value.__aenter__.return_value = fake_client

        with patch("app.provider.asyncio.sleep", new_callable=AsyncMock):
            result = await create_chat_completion(
                {"messages": [{"role": "user", "content": "Hello"}]}
            )

    assert result == {"id": "recovered"}
    assert fake_client.post.await_count == 2

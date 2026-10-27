from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_chat_requires_provider_configuration(monkeypatch):
    monkeypatch.delenv("AI_PROVIDER_BASE_URL", raising=False)
    monkeypatch.delenv("AI_PROVIDER_API_KEY", raising=False)
    monkeypatch.delenv("AI_PROVIDER_MODEL", raising=False)

    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "Hello"}]
        },
    )

    assert response.status_code == 503
    assert response.json()["detail"] == "AI provider is not configured."


def test_chat_requires_at_least_one_message():
    response = client.post(
        "/v1/chat/completions",
        json={"messages": []},
    )

    assert response.status_code == 422


def test_streaming_is_not_supported_yet():
    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "stream": True,
        },
    )

    assert response.status_code == 501
def test_chat_rejects_private_execution_until_implemented():
    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "routing_mode": "PRIVACY_FIRST",
        },
    )

    assert response.status_code == 501
    detail = response.json()["detail"]
    assert detail["message"] == "Private execution is not implemented yet."
    assert detail["routing_decision"]["mode"] == "PRIVACY_FIRST"


def test_private_requirement_overrides_routing_mode():
    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "routing_mode": "LOW_COST",
            "private_required": True,
        },
    )

    assert response.status_code == 501
    detail = response.json()["detail"]
    assert detail["routing_decision"]["mode"] == "PRIVACY_FIRST"


def test_invalid_routing_mode_is_rejected():
    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "routing_mode": "MAGIC",
        },
    )

    assert response.status_code == 422
def test_chat_returns_mock_provider_response(monkeypatch):
    from app import main

    async def mock_create_chat_completion(payload):
        assert payload["messages"] == [
            {"role": "user", "content": "Hello"}
        ]
        return {
            "id": "mock-chat-123",
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "Hello from AI Fabric!",
                    }
                }
            ],
        }

    monkeypatch.setattr(
        main,
        "create_chat_completion",
        mock_create_chat_completion,
    )

    response = client.post(
        "/v1/chat/completions",
        json={
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "routing_mode": "BALANCED",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["choices"][0]["message"]["content"] == (
        "Hello from AI Fabric!"
    )
    assert body["ai_fabric_routing"]["mode"] == "BALANCED"
    assert isinstance(body["ai_fabric_metrics"]["latency_ms"], (int, float))
    assert body["ai_fabric_metrics"]["latency_ms"] >= 0

import time
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from app.provider import create_chat_completion
from app.router import RoutingMode, decide_route

app = FastAPI(
    title="AI Fabric",
    description="An intelligent AI gateway for reliable model access.",
    version="0.3.0",
)


class ChatCompletionRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str | None = None
    messages: list[dict[str, Any]] = Field(min_length=1)
    temperature: float | None = None
    max_tokens: int | None = None
    stream: bool = False
    routing_mode: RoutingMode = RoutingMode.BALANCED
    private_required: bool = False


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ai-fabric"}


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    start_time = time.perf_counter()
    if request.stream:
        raise HTTPException(
            status_code=501,
            detail="Streaming is not supported yet.",
        )

    decision = decide_route(
        request.routing_mode,
        private_required=request.private_required,
    )

    if decision.requires_private_execution:
        raise HTTPException(
            status_code=501,
            detail={
                "message": "Private execution is not implemented yet.",
                "routing_decision": {
                    "mode": decision.mode.value,
                    "reason": decision.reason,
                },
            },
        )

    payload = request.model_dump(
        exclude_none=True,
        exclude={"routing_mode", "private_required"},
    )

    result = await create_chat_completion(payload)

    result["ai_fabric_routing"] = {
        "mode": decision.mode.value,
        "reason": decision.reason,
    }
    result["ai_fabric_metrics"] = {
        "latency_ms": round((time.perf_counter() - start_time) * 1000, 2)
    }
    return result

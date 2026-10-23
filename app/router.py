from dataclasses import dataclass
from enum import Enum


class RoutingMode(str, Enum):
    LOW_COST = "LOW_COST"
    LOW_LATENCY = "LOW_LATENCY"
    HIGH_QUALITY = "HIGH_QUALITY"
    BALANCED = "BALANCED"
    PRIVACY_FIRST = "PRIVACY_FIRST"


@dataclass(frozen=True)
class RoutingDecision:
    mode: RoutingMode
    reason: str
    requires_private_execution: bool = False


def decide_route(
    mode: RoutingMode,
    *,
    private_required: bool = False,
) -> RoutingDecision:
    """Return an explainable routing decision without calling a provider."""

    if private_required or mode == RoutingMode.PRIVACY_FIRST:
        return RoutingDecision(
            mode=RoutingMode.PRIVACY_FIRST,
            reason="Privacy requirements take priority over other routing goals.",
            requires_private_execution=True,
        )

    reasons = {
        RoutingMode.LOW_COST: (
            "Prioritize the lowest estimated cost among eligible providers."
        ),
        RoutingMode.LOW_LATENCY: (
            "Prioritize the lowest estimated latency among eligible providers."
        ),
        RoutingMode.HIGH_QUALITY: (
            "Prioritize the best expected response quality among eligible models."
        ),
        RoutingMode.BALANCED: (
            "Balance estimated cost, latency, and response quality."
        ),
    }

    return RoutingDecision(
        mode=mode,
        reason=reasons[mode],
    )

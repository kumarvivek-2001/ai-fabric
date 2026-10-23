import pytest

from app.router import RoutingMode, decide_route


@pytest.mark.parametrize(
    "mode",
    [
        RoutingMode.LOW_COST,
        RoutingMode.LOW_LATENCY,
        RoutingMode.HIGH_QUALITY,
        RoutingMode.BALANCED,
    ],
)
def test_routing_modes_return_explainable_decisions(mode):
    decision = decide_route(mode)

    assert decision.mode == mode
    assert decision.reason
    assert decision.requires_private_execution is False


def test_privacy_first_mode_requires_private_execution():
    decision = decide_route(RoutingMode.PRIVACY_FIRST)

    assert decision.mode == RoutingMode.PRIVACY_FIRST
    assert decision.requires_private_execution is True
    assert decision.reason


def test_private_requirement_overrides_other_modes():
    decision = decide_route(
        RoutingMode.LOW_COST,
        private_required=True,
    )

    assert decision.mode == RoutingMode.PRIVACY_FIRST
    assert decision.requires_private_execution is True

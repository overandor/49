from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


class LDVState(str, Enum):
    ILLIQUID_SHELL = "illiquid_shell"
    FRAGILE_LIQUIDITY = "fragile_liquidity"
    OPERATIONAL_LIQUIDITY = "operational_liquidity"
    DENSE_LIQUID_VALUE = "dense_liquid_value"
    HIGH_DENSITY_SETTLEMENT = "high_density_settlement_layer"


@dataclass
class LiquidValueDensityInput:
    depth_1pct_usd: float
    target_depth_1pct_usd: float
    executable_notional_usd: float
    target_executable_notional_usd: float
    mobile_collateral_usd: float
    required_mobile_collateral_usd: float
    largest_venue_share: float
    observed_rebalance_seconds: float
    target_rebalance_seconds: float
    usable_liquidity_under_stress_usd: float
    required_stress_liquidity_usd: float
    aggregate_liquidation_distance_bps: float
    target_liquidation_distance_bps: float


@dataclass
class LiquidValueDensityResult:
    score: float
    state: LDVState
    liquid_depth: float
    execution_readiness: float
    collateral_mobility: float
    venue_distribution: float
    rebalance_latency: float
    stress_usability: float
    liquidation_resistance: float
    weakest_component: str
    reason: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["state"] = self.state.value
        return data


def classify_ldv(score: float) -> LDVState:
    if score < 0.20:
        return LDVState.ILLIQUID_SHELL
    if score < 0.40:
        return LDVState.FRAGILE_LIQUIDITY
    if score < 0.60:
        return LDVState.OPERATIONAL_LIQUIDITY
    if score < 0.80:
        return LDVState.DENSE_LIQUID_VALUE
    return LDVState.HIGH_DENSITY_SETTLEMENT


def score_liquid_value_density(inp: LiquidValueDensityInput) -> LiquidValueDensityResult:
    liquid_depth = clamp01(inp.depth_1pct_usd / max(inp.target_depth_1pct_usd, 1e-9))
    execution_readiness = clamp01(inp.executable_notional_usd / max(inp.target_executable_notional_usd, 1e-9))
    collateral_mobility = clamp01(inp.mobile_collateral_usd / max(inp.required_mobile_collateral_usd, 1e-9))
    venue_distribution = clamp01(1.0 - inp.largest_venue_share)
    rebalance_latency = clamp01(inp.target_rebalance_seconds / max(inp.observed_rebalance_seconds, 1.0))
    stress_usability = clamp01(inp.usable_liquidity_under_stress_usd / max(inp.required_stress_liquidity_usd, 1e-9))
    liquidation_resistance = clamp01(inp.aggregate_liquidation_distance_bps / max(inp.target_liquidation_distance_bps, 1e-9))

    components = {
        "liquid_depth": liquid_depth,
        "execution_readiness": execution_readiness,
        "collateral_mobility": collateral_mobility,
        "venue_distribution": venue_distribution,
        "rebalance_latency": rebalance_latency,
        "stress_usability": stress_usability,
        "liquidation_resistance": liquidation_resistance,
    }
    weakest = min(components, key=components.get)
    score = min(components.values())
    state = classify_ldv(score)
    reason = f"LDV={score:.2f}, state={state.value}, weakest_component={weakest}:{components[weakest]:.2f}"

    return LiquidValueDensityResult(
        score=round(score, 4),
        state=state,
        liquid_depth=round(liquid_depth, 4),
        execution_readiness=round(execution_readiness, 4),
        collateral_mobility=round(collateral_mobility, 4),
        venue_distribution=round(venue_distribution, 4),
        rebalance_latency=round(rebalance_latency, 4),
        stress_usability=round(stress_usability, 4),
        liquidation_resistance=round(liquidation_resistance, 4),
        weakest_component=weakest,
        reason=reason,
    )

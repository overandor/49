from overworker.research.liquid_value_density import LiquidValueDensityInput, score_liquid_value_density


def test_ldv_uses_weakest_link():
    inp = LiquidValueDensityInput(
        depth_1pct_usd=1_000_000,
        target_depth_1pct_usd=1_000_000,
        executable_notional_usd=1_000_000,
        target_executable_notional_usd=1_000_000,
        mobile_collateral_usd=1_000_000,
        required_mobile_collateral_usd=1_000_000,
        largest_venue_share=0.75,
        observed_rebalance_seconds=60,
        target_rebalance_seconds=60,
        usable_liquidity_under_stress_usd=1_000_000,
        required_stress_liquidity_usd=1_000_000,
        aggregate_liquidation_distance_bps=2000,
        target_liquidation_distance_bps=2000,
    )
    result = score_liquid_value_density(inp)
    assert result.score == 0.25
    assert result.weakest_component == "venue_distribution"


def test_ldv_classifies_dense_state():
    inp = LiquidValueDensityInput(
        depth_1pct_usd=800_000,
        target_depth_1pct_usd=1_000_000,
        executable_notional_usd=900_000,
        target_executable_notional_usd=1_000_000,
        mobile_collateral_usd=850_000,
        required_mobile_collateral_usd=1_000_000,
        largest_venue_share=0.25,
        observed_rebalance_seconds=80,
        target_rebalance_seconds=60,
        usable_liquidity_under_stress_usd=850_000,
        required_stress_liquidity_usd=1_000_000,
        aggregate_liquidation_distance_bps=1800,
        target_liquidation_distance_bps=2000,
    )
    result = score_liquid_value_density(inp)
    assert 0.60 <= result.score < 0.80
    assert result.state.value == "dense_liquid_value"

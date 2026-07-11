from strategy_factory.promotion import evaluate_promotion


def test_promotion_requires_all_hard_gates():
    decision = evaluate_promotion(
        strategy_id="S",
        from_state="dataset_ready",
        requested_state="baseline_tested",
        evidence={"expectancy": 0.1, "audit_pass": True},
        requirements={"expectancy": {"operator": ">=", "value": 0.0}, "audit_pass": True},
    )
    assert decision.approved

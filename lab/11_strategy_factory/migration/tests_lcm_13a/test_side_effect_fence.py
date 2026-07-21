def test_submission_remains_disabled(results):
    for row in results:
        fence = row["side_effect_fence"]
        assert fence["broker_submission_enabled"] is False
        assert fence["paper_submission_enabled"] is False
        assert fence["live_order_enabled"] is False
        assert fence["capital_activation_enabled"] is False
        assert fence["submission_attempt_count"] == 0
        assert fence["live_order_count"] == 0
        assert fence["capital_activation_count"] == 0

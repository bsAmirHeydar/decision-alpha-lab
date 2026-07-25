def test_negative_controls_pass(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_NEGATIVE_CONTROL_AUDIT.JSON')['all_passed']
def test_environment_permutation_preserves_marginals(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_ENVIRONMENT_PERMUTATION.JSON')['marginals_preserved']
def test_hidden_confounder_never_identifies(load):assert not any(r['identification_survives'] for r in load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_HIDDEN_CONFOUNDER_SENSITIVITY.JSON')['rows'])
def test_edge_reversal_fail_closed(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_EDGE_REVERSAL_STRESS.JSON')['all_future_reversals_fail_closed']
def test_future_suffix_pass(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_FUTURE_SUFFIX_AUDITS.JSON')['all_passed']
def test_fail_closed_matrix_pass(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_FAIL_CLOSED_AUDITS.JSON')['all_passed']
def test_transport_not_claimed(load):assert not load('releases/history/strategy_factory/artifacts/saed_v4_17/GOLDEN_TRANSPORT_SUPPORT_REPORT.JSON')['transport_claim_allowed']

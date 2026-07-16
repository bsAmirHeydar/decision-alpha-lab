def test_structural_equations_reference_only(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_STRUCTURAL_EQUATIONS.JSON');assert x['equation_count']>0 and not x['causal_interpretation_allowed']
def test_residual_audit_finite(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_RESIDUAL_INDEPENDENCE_AUDIT.JSON');assert x['row_count']>0 and x['maximum_absolute_residual_parent_correlation']>=0
def test_invariance_has_multiple_mechanisms(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_INVARIANT_MECHANISM_REPORT.JSON');assert x['mechanism_count']>=3
def test_conditional_tests_recorded(load):
 x=load('lab/11_strategy_factory/artifacts/saed_v4_17/GOLDEN_CONDITIONAL_INDEPENDENCE_AUDIT.JSON');assert x['test_count']>20

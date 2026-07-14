import pytest
from fp_i14_diagnostic import *
@pytest.mark.parametrize('kind', [ScenarioKind.BASELINE,ScenarioKind.DUPLICATE_DELIVERY,ScenarioKind.RECONNECT,ScenarioKind.RESTART,ScenarioKind.SYMBOL_STAGGER,ScenarioKind.LATE_REVISION,ScenarioKind.TIMEFRAME_SWITCH])
def test_stress_deterministic(kind,runs):
    r=runs[ProductKind.INDICATOR];s=StressScenario('SC-'+kind.value,kind,14,duplicate_every=3,disconnect_after=8,reconnect_skip=2,restart_after=9);assert run_stress(r,s).status==DifferentialStatus.PASS
def test_truncation_detected(runs):
    r=runs[ProductKind.INDICATOR];s=StressScenario('SC-TRUNC',ScenarioKind.TRACE_TRUNCATION,14);assert run_stress(r,s).status==DifferentialStatus.FAIL

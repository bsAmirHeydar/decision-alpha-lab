from strategy_factory_integration import PilotPipelineGate, map_candidate, reference_candidates, reference_config
from strategy_factory_integration.enums import StageStatus

def test_pipeline_binds_layers_but_fails_closed_without_model():
    e,_=map_candidate(reference_candidates()[0],reference_config(),1783795000000)
    rows=PilotPipelineGate().route(e,1783795000000,"ctx_1",("cand_1",))
    status={r.stage:r.status for r in rows}
    assert status["anatomy"]==StageStatus.PASSED
    assert status["context"]==StageStatus.PASSED
    assert status["candidate"]==StageStatus.PASSED
    assert status["inference"]==StageStatus.GATED
    assert status["decision"]==StageStatus.GATED
    assert status["live"]==StageStatus.GATED

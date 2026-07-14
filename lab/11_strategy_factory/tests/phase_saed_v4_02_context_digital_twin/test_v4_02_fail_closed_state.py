from saed_v4_context_twin.compiler import compile_twin
from saed_v4_context_twin.models import Contradiction,EvidenceDebtItem,SupportEvaluation
from saed_v4_context_twin.enums import ContradictionSeverity,DebtSeverity,SupportStatus,TwinState
from saed_v4_context_twin.state import build_snapshot
H='a'*64

def test_material_contradiction_conflicts(context_spec,seed):
    m=compile_twin(context_spec,seed);c=Contradiction(m.twin_id,'k',H,'b'*64,ContradictionSeverity.MATERIAL,'2026-01-01T00:00:00Z','d')
    s=build_snapshot(m,'2026-01-01T00:00:00Z','initialized',(),(),None,(c,),(),(),1);assert s.twin_state==TwinState.CONFLICTED

def test_blocking_debt_quarantines(context_spec,seed):
    m=compile_twin(context_spec,seed);d=EvidenceDebtItem(m.twin_id,'k','d',DebtSeverity.BLOCKING,'s','2026-01-01T00:00:00Z')
    s=build_snapshot(m,'2026-01-01T00:00:00Z','initialized',(),(),None,(),(d,),(),1);assert s.twin_state==TwinState.QUARANTINED

def test_unsupported_support_degrades(context_spec,seed):
    m=compile_twin(context_spec,seed);e=SupportEvaluation(m.twin_id,m.support_geometry.geometry_id,'2026-01-01T00:00:00Z',SupportStatus.UNSUPPORTED,0.0,(),('x',),('missing',))
    s=build_snapshot(m,'2026-01-01T00:00:00Z','initialized',(),(),e,(),(),(),1);assert s.twin_state==TwinState.DEGRADED

def test_warning_does_not_conflict(context_spec,seed):
    m=compile_twin(context_spec,seed);c=Contradiction(m.twin_id,'k',H,'b'*64,ContradictionSeverity.WARNING,'2026-01-01T00:00:00Z','d')
    s=build_snapshot(m,'2026-01-01T00:00:00Z','initialized',(),(),None,(c,),(),(),1);assert s.twin_state==TwinState.OBSERVING

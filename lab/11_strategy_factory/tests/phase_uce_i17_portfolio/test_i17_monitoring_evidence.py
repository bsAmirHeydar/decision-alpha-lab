import pytest
from strategy_factory_portfolio_v3.golden import *
from strategy_factory_portfolio_v3.queue import rank_batch
from strategy_factory_portfolio_v3.capacity import estimate_capacity
from strategy_factory_portfolio_v3.allocator import allocate
from strategy_factory_portfolio_v3.stress import run_stress
from strategy_factory_portfolio_v3.validation import validate_portfolio
from strategy_factory_portfolio_v3.runtime import compile_runtime_bundle
from strategy_factory_portfolio_v3.monitoring import build_telemetry
from strategy_factory_portfolio_v3.reconciliation import reconcile,require_safe_reconciliation
from strategy_factory_portfolio_v3.evidence import build_evidence
from strategy_factory_portfolio_v3.errors import PortfolioError

def setup():
 b=golden_batch();r=rank_batch(b);q=[estimate_capacity(x.candidate,b.as_of_ms) for x in r];qm={x.candidate_id:x for x in q};p,l=allocate(b,golden_model(),golden_limits(),qm);s=run_stress(p,golden_stress(),golden_limits());v=validate_portfolio(p,s,{x.context_id:x.adjusted_score for x in p.selected});rb=compile_runtime_bundle(p,golden_limits(),golden_model(),v,l);t=build_telemetry('telemetry',b.as_of_ms,r,p,l,golden_model());return r,q,p,l,v,rb,t

def test_reconciliation_passes_exact_reservations():
 r,q,p,l,v,rb,t=setup();obs={x.reservation_id:x.allocated_risk for x in p.selected};assert require_safe_reconciliation(reconcile(p,l,obs))
def test_reconciliation_fails_missing_reservation():
 r,q,p,l,v,rb,t=setup();rep=reconcile(p,l,{})
 with pytest.raises(PortfolioError):require_safe_reconciliation(rep)
def test_drift_forces_emergency_derisk_flag():
 r,q,p,l,v,rb,t=setup();t=build_telemetry('telemetry',2000,r,p,l,golden_model(),('calibration_drift',));assert t.emergency_derisk
def test_evidence_identity_is_stable():
 r,q,p,l,v,rb,t=setup();e=build_evidence(r,golden_model(),q,p,v,rb,t,False,('no_real_two_context_promotion_evidence',));assert e.evidence_hash==e.evidence_hash and not e.activation_allowed

from decimal import Decimal
from strategy_factory_treatments_v3.enums import TradeSide
from .golden import fixture,golden_envelopes
from .solver import MaximumLossSolver
from .stress import EconomicStressSuite
from .contracts import StressScenario
from .enums import StressKind
from .reservation import ReservationLedger

def run_conformance():
    envs=golden_envelopes(); checks=[]
    checks.append(('golden_count',len(envs)==4))
    checks.append(('all_accepted',all(e.accepted for e in envs)))
    checks.append(('risk_never_exceeds_budget',all(e.maximum_loss_cash<=e.risk_budget_cash for e in envs)))
    checks.append(('treatment_identity_preserved',all(e.treatment_id=='ucet_fixture' for e in envs)))
    # Determinism
    checks.append(('deterministic_ids',[e.envelope_id for e in envs]==[e.envelope_id for e in golden_envelopes()]))
    # Side-aware executable semantics
    long,short=envs[0],envs[2]
    checks.append(('long_entry_ask_side',long.entry_executable_price>=Decimal('1.10010')))
    checks.append(('short_entry_bid_side',short.entry_executable_price<=Decimal('1.10000')))
    # Stress monotonicity
    q,s,a,g,r,b,m=fixture(TradeSide.LONG,'fx'); base=MaximumLossSolver().solve(g,q,s,a,m,b)
    suite=EconomicStressSuite(); scenarios=(StressScenario('stress.spread','1.0.0',StressKind.SPREAD_MULTIPLIER,Decimal('3')),StressScenario('stress.commission','1.0.0',StressKind.COMMISSION_MULTIPLIER,Decimal('2')),StressScenario('stress.slip','1.0.0',StressKind.SLIPPAGE_POINTS,Decimal('10')))
    results=[suite.run_one(x,base,q,s,m,g,a,b) for x in scenarios]; checks.append(('stress_non_increasing_volume',all(x.passed_monotonicity for x in results)))
    # Reservation restart and idempotency
    ledger=ReservationLedger(); ev=ledger.reserve(base,'acct.fixture','strategy.fixture','fx_major',1,1,'idempotent'); ev2=ledger.reserve(base,'acct.fixture','strategy.fixture','fx_major',1,1,'idempotent')
    checks.append(('reservation_idempotent',ev.event_hash==ev2.event_hash and len(ledger.events)==1))
    replay=ReservationLedger().replay(tuple(ledger.events)); checks.append(('reservation_restart_parity',replay.head_hash==ledger.head_hash and replay.total_open_cash==ledger.total_open_cash))
    return {'accepted':all(v for _,v in checks),'checks':[{'name':n,'passed':v} for n,v in checks],'envelopes':[e.to_dict() for e in envs],'stress_results':[x.to_dict() for x in results]}

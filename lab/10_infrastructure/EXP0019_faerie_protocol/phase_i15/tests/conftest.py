from pathlib import Path
import sys,hashlib,pytest
PH=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PH/'python'))
from fp_i15_paper import *
def h(x): return hashlib.sha256(str(x).encode()).hexdigest()
@pytest.fixture
def proof(): return DiagnosticAcceptanceProof("ACC-I14","PASS","FP-CONTEXT-001","PAIR-ES-NQ",h('cfg'),"REV-1",h('consensus'),1_700_000_000_000)
@pytest.fixture
def buy_winner(): return WinnerSignalInput("SIG-BUY",h('sig-buy'),"CAN-BUY","AL",TradeDirection.BUY,"NQ","ES","NYDAY-2026-07-13:N","FP-EPOCH|NYDAY|PAIR-ES-NQ|N","I09-RES-BUY",ReservationFinality.FINAL,1_700_000_000_000,1_700_000_060_000,99.0,"REV-1",h('cfg'),(1,"AL","BUY"))
@pytest.fixture
def sell_winner(): return WinnerSignalInput("SIG-SELL",h('sig-sell'),"CAN-SELL","WW",TradeDirection.SELL,"ES","NQ","NYDAY-2026-07-13:N","FP-EPOCH|NYDAY|PAIR-ES-NQ|N","I09-RES-SELL",ReservationFinality.FINAL,1_700_000_000_000,1_700_000_060_000,201.0,"REV-1",h('cfg'),(1,"WW","SELL"))
@pytest.fixture
def readiness(): return CausalReadiness(1_700_000_120_000,True,True,0,True,False)
@pytest.fixture
def buy_quote(): return QuoteSnapshot("Q-BUY","ES",100.0,100.25,1_700_000_120_000,"REV-1")
@pytest.fixture
def sell_quote(): return QuoteSnapshot("Q-SELL","NQ",199.75,200.0,1_700_000_120_000,"REV-1")
@pytest.fixture
def buy_spec(): return SymbolSpec("ES",0.25,12.5,0.01,100.0,0.01,0.25,0.0)
@pytest.fixture
def sell_spec(): return SymbolSpec("NQ",0.25,5.0,0.01,100.0,0.01,0.25,0.0)
@pytest.fixture
def risk(): return RiskConfig(100.0,2.0,0.25,0.0)
@pytest.fixture
def buy_plan(proof,buy_winner,readiness,buy_quote,buy_spec,risk): return build_plan(proof,buy_winner,readiness,buy_quote,buy_spec,risk,1_700_000_120_000)
@pytest.fixture
def sell_plan(proof,sell_winner,readiness,sell_quote,sell_spec,risk): return build_plan(proof,sell_winner,readiness,sell_quote,sell_spec,risk,1_700_000_120_000)

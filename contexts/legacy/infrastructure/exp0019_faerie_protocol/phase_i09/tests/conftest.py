import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
for p in [
 ROOT/'phase_i02/python',ROOT/'phase_i03/python',ROOT/'phase_i04/python',ROOT/'phase_i05/python',ROOT/'phase_i06/python',ROOT/'phase_i07/python',ROOT/'phase_i08/python',ROOT/'phase_i09/python'
]: sys.path.insert(0,str(p))
import pytest
from fp_i02_kernel.enums import RelationCode,Direction,PriceSide
from fp_i07_confirmation.contracts import ConfirmedSignal
from fp_i07_confirmation.enums import HostTimeframe
from fp_i08_weekly.contracts import DirectionGateDecision
from fp_i08_weekly.enums import GateEligibility
from fp_i09_ledger.canonical import canonical_sha256,stable_id
from fp_i09_ledger.contracts import LedgerConfig
from fp_i09_ledger.identity import build_quota_key,build_eligibility
from fp_i09_ledger.enums import PrecheckState

BASE=1_789_000_000_000//60_000*60_000

def signal(i=0,relation=RelationCode.AL,direction=Direction.BULLISH,hunt=None,confirm=None,session='NYDAY-2026-09-08:N',hunter='ES',protected='NQ'):
    hunt=BASE+i*60_000 if hunt is None else hunt; confirm=hunt+5*60_000 if confirm is None else confirm
    p={"i":i,"relation":relation.value,"direction":direction.value,"hunt":hunt,"confirm":confirm,"session":session,"hunter":hunter,"protected":protected}
    sid=stable_id('FPSIG',p); h=canonical_sha256(p)
    return ConfirmedSignal(sid,stable_id('FPCAN',p),stable_id('FPRI',p),relation,direction,PriceSide.LOW if direction is Direction.BULLISH else PriceSide.HIGH,hunter,protected,hunt,stable_id('FPBAR',p),confirm-5*60_000,confirm,hunter,HostTimeframe.M5,session,'REV-1','0'*64,h,h)

def gate(sig,elig=GateEligibility.ALLOWED,active_dir=None):
    p={"sid":sig.signal_id,"elig":elig.value,"active":active_dir.value if active_dir else ''}
    h=canonical_sha256(p); return DirectionGateDecision(stable_id('FPGD',p),sig.signal_id,sig.relation,sig.direction,elig,'WWCTX' if active_dir else '',active_dir,sig.confirmation_close_utc_ms,'FP_WRC_TEST','1'*64,h)

@pytest.fixture
def config(): return LedgerConfig('FP-CONTEXT-001','PAIR-ES-NQ','EPOCH-1','2'*64)
@pytest.fixture
def qkey(): return build_quota_key('EPOCH-1','NYDAY-2026-09-08','PAIR-ES-NQ','NYDAY-2026-09-08:N','N')

def eligible(sig,g=None,**kw):
    g=g or gate(sig); return build_eligibility(sig,g,**kw)

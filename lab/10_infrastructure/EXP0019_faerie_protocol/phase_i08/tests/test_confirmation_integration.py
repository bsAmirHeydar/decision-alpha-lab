from fp_i02_kernel.enums import PriceSide,Direction
from fp_i07_confirmation.contracts import ConfirmationConfig
from fp_i07_confirmation.enums import HostTimeframe,ClosePairState,ConfirmationOutcome
from fp_i07_confirmation.golden import host_bar
from fp_i07_confirmation.observation import observe_close
from fp_i08_weekly.confirmation import confirm_ww
from fp_i08_weekly.contracts import WWRelationInstance,WWSidePlan
from fp_i08_weekly.enums import WWDataState,WWLifecycleState
from fp_i08_weekly.canonical import canonical_sha256
from helpers import config,ww_candidate_and_scan

def objects(state=ClosePairState.HUNTER_ONLY):
 cand,scan=ww_candidate_and_scan();plan=WWSidePlan('WW-PLAN','WW-REL','PAIR.A.B',PriceSide.LOW,'RA','AAA',90.0,'RB','BBB',190.0,cand.first_hunt_minute_utc_ms-60000,cand.check_end_utc_ms,tuple(sorted(('1'*64,'2'*64))),WWDataState.COMPLETE,('OK',),canonical_sha256({'plan':'WW'}))
 inst=WWRelationInstance('WW-REL','PAIR.A.B','W-PREV','W-CUR','PW-PREV','PW-CUR',plan.check_start_utc_ms,plan.check_end_utc_ms,'1'*64,'REV-1',WWDataState.COMPLETE,('OK',),canonical_sha256({'inst':'WW'}))
 cc=ConfirmationConfig('FP-CONTEXT-001','PAIR.A.B','ES',HostTimeframe.M5,300)
 bar=host_bar(cand,HostTimeframe.M5,300000);obs=observe_close(cand,bar,state,bar.close_utc_ms,'REV-1')
 return cand,scan,plan,inst,cc,bar,obs

def test_confirmed_ww_creates_context():
 cand,scan,plan,inst,cc,bar,obs=objects();r,c,e=confirm_ww(scan,plan,inst,(bar,),obs,cc,config(),cand.first_hunt_minute_utc_ms);assert r.outcome is ConfirmationOutcome.CONFIRMED and c.state is WWLifecycleState.CONFIRMED and c.protected_reference_id=='RB'
def test_nonconfirmed_ww_creates_no_context():
 cand,scan,plan,inst,cc,bar,obs=objects(ClosePairState.BOTH);r,c,e=confirm_ww(scan,plan,inst,(bar,),obs,cc,config(),cand.first_hunt_minute_utc_ms);assert r.outcome is ConfirmationOutcome.INVALIDATED_DOUBLE_HUNT and c is None
def test_ww_context_preserves_week_lineage():
 cand,scan,plan,inst,cc,bar,obs=objects();_,c,_=confirm_ww(scan,plan,inst,(bar,),obs,cc,config(),cand.first_hunt_minute_utc_ms);assert (c.previous_week_id,c.current_week_id)==('W-PREV','W-CUR')

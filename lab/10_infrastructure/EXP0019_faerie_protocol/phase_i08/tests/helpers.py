from fp_i02_kernel.enums import RelationCode,PriceSide,Direction
from fp_i07_confirmation.enums import HostTimeframe
from fp_i07_confirmation.contracts import ConfirmedSignal
from fp_i08_weekly.canonical import canonical_sha256,stable_id
from fp_i08_weekly.contracts import WWConfig,WWContext,WWNeutralizationObservation
from fp_i08_weekly.enums import WWLifecycleState,WWDataState

def config(): return WWConfig('FP-CONTEXT-001','PAIR.A.B','1'*64,'2'*64)
def signal(n=1,direction=Direction.BULLISH,side=PriceSide.LOW,confirmed=1_000_020_000):
    mat={'n':n,'direction':direction,'side':side,'confirmed':confirmed}
    return ConfirmedSignal(stable_id('FPSIGNAL',mat,40),f'CAND-{n}',f'REL-{n}',RelationCode.WW,direction,side,'AAA','BBB',confirmed-60000,f'BAR-{n}',confirmed-300000,confirmed,'AAA',HostTimeframe.M5,'WW-SESSION','REV-1','2'*64,canonical_sha256(mat),canonical_sha256({'sig':mat}))
def context(n=1,direction=Direction.BULLISH,side=PriceSide.LOW,confirmed=1_000_020_000,state=WWLifecycleState.CONFIRMED,week_end=1_010_040_000):
    s=signal(n,direction,side,confirmed);mat={'s':s.signal_id,'n':n}
    return WWContext(stable_id('FPWWCTX',mat,36),s,f'RES-{n}',f'PLAN-{n}',direction,side,'AAA','BBB',f'RA-{n}',100.0,f'RB-{n}',200.0,'W-PREV','W-CUR',week_end,state,confirmed,confirmed+60000 if state is WWLifecycleState.NEUTRALIZED else 0,f'OBS-{n}' if state is WWLifecycleState.NEUTRALIZED else '',week_end if state is WWLifecycleState.EXPIRED else 0,'FP_WRC_WW_CONFIRMED_ACTIVE','REV-1',config().config_hash,canonical_sha256(mat))
def observation(c,minute=None,symbol=None,side=None,extreme=None,complete=True):
    minute=minute or c.confirmed_utc_ms+60000;symbol=symbol or c.protected_symbol;side=side or c.side;extreme=extreme if extreme is not None else (c.protected_reference_price+1 if side is PriceSide.HIGH else c.protected_reference_price-1)
    mat={'c':c.ww_context_id,'m':minute,'s':symbol,'side':side,'e':extreme}
    return WWNeutralizationObservation(stable_id('FPWWOBS',mat,32),c.ww_context_id,symbol,side,minute,extreme,c.protected_reference_id,c.protected_reference_price,complete,'REV-2',canonical_sha256(mat))

def weekly_store(previous_complete=True,current_blocked=False,consume_high=False):
    from fp_i02_kernel.enums import WindowKind,PriceSide,ReferenceState
    from fp_i05_reference.contracts import WindowStoreConfig,WindowDescriptor,SymbolWindowAggregate,PairWindowAggregate,ReferenceLevel
    from fp_i05_reference.enums import WindowBuildState,PairWindowHealth
    from fp_i05_reference.store import build_store_snapshot
    base=1_700_006_400_000
    prev_start=base;prev_end=base+5*24*60*60*1000
    cur_start=prev_end+2*24*60*60*1000;cur_end=cur_start+5*24*60*60*1000
    cfg=WindowStoreConfig('FP-CONTEXT-001','PAIR.A.B','a'*64,'b'*64)
    def pair_window(tag,week,start,end,complete=True,blocked=False):
        desc=WindowDescriptor(f'DESC-{tag}','PAIR.A.B',WindowKind.W,tag,f'NYDAY-{tag}',week,start,end,1,'a'*64,f'CAL-{tag}')
        state=WindowBuildState.COMPLETE if complete else WindowBuildState.ACTIVE
        def agg(sym,baseprice):
            mat={'sym':sym,'tag':tag,'state':state.value}
            return SymbolWindowAggregate(f'AGG-{tag}-{sym}',desc.descriptor_id,sym,state,baseprice,baseprice+10,baseprice-10,baseprice+1,start,start,1,1,1,0,0,0,'REV-1',(canonical_sha256(mat),),('OK',),canonical_sha256({'agg':mat}))
        left=agg('AAA',100.0);right=agg('BBB',200.0)
        health=PairWindowHealth.BLOCKED if blocked else PairWindowHealth.READY
        mat={'tag':tag,'left':left.semantic_hash,'right':right.semantic_hash,'health':health.value}
        return PairWindowAggregate(f'PAIRWIN-{tag}',desc,left,right,health,'REV-1',('OK',),canonical_sha256(mat))
    previous=pair_window('2026-07-05','NYWEEK-2026-07-05',prev_start,prev_end,previous_complete,False)
    current=pair_window('2026-07-12','NYWEEK-2026-07-12',cur_start,cur_end,False,current_blocked)
    refs=[]
    for sym,high,low in [('AAA',110.0,90.0),('BBB',210.0,190.0)]:
        for side,price in [(PriceSide.HIGH,high),(PriceSide.LOW,low)]:
            state=ReferenceState.CONSUMED_BY_PROTECTED_TOUCH if consume_high and side is PriceSide.HIGH and sym=='AAA' else ReferenceState.FRESH
            mat={'sym':sym,'side':side.value,'price':price,'state':state.value}
            refs.append(ReferenceLevel(f'REF-{sym}-{side.value}','PAIR.A.B',sym,side,price,prev_start,previous.pair_window_id,previous.descriptor.descriptor_id,WindowKind.W,previous.descriptor.trading_date,previous.descriptor.week_id,'REV-1',state,0,prev_end,prev_end,'OK',canonical_sha256(mat)))
    snap=build_store_snapshot(cfg,'DATASET','REV-1',(previous,current),tuple(refs),cur_start)
    return snap,previous,current

def ww_candidate_and_scan(side=PriceSide.LOW,direction=Direction.BULLISH):
    from fp_i06_relations.contracts import RawDivergenceCandidate,FirstSweepClassification,RelationScanResult
    from fp_i06_relations.enums import CandidateState,SweepOutcome,ScanMode
    first=1_700_100_000_000;first-=first%60_000;end=first+3_600_000
    cm={'side':side.value,'first':first}
    cand=RawDivergenceCandidate(stable_id('FPCAND',cm,32),'WW-PLAN','WW-REL',RelationCode.WW,direction,side,'AAA','BBB',first,'HUNT-AAA',CandidateState.RAW_ACTIVE,0,None,'',end,'REV-1','FP_HRC_RAW_CANDIDATE_CREATED',canonical_sha256(cm))
    clm={'plan':'WW-PLAN','outcome':'LEFT_FIRST','first':first}
    cl=FirstSweepClassification(stable_id('FPSWEEP',clm,32),'WW-PLAN','WW-REL',SweepOutcome.LEFT_FIRST,first,'AAA','BBB','HUNT-AAA',(),None,'FP_HRC_CLASSIFICATION_ASYMMETRIC_FIRST_SWEEP',canonical_sha256(clm))
    sm={'candidate':cand.semantic_hash}
    scan=RelationScanResult(stable_id('FPRELSCAN',sm,32),'WW-PLAN',ScanMode.BATCH,first,first+60_000,(),(),cl,cand,(),1,'REV-1',canonical_sha256(('ROW',)),canonical_sha256(sm))
    from fp_i08_weekly.contracts import WWScanRecord
    rec=WWScanRecord(stable_id('FPWWSCAN',sm,32),'WW-PLAN',scan,'REV-1',canonical_sha256({'ww':sm}))
    return cand,rec

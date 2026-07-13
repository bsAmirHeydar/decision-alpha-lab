from __future__ import annotations
from dataclasses import replace
from fp_i02_kernel.enums import RelationCode,PriceSide
from fp_i04_data.contracts import M1Bar,MinuteCell,AlignedMinute
from fp_i04_data.enums import BarFinality,MinuteCellState
from .golden import golden_store_and_report
from .engine import scan_side_plan
from .canonical import canonical_sha256

def _row(plan,minute,left_high,left_low,right_high,right_low,seq=1,blocked=False):
    def cell(symbol,high,low,n):
        if blocked:return MinuteCell(symbol,minute,MinuteCellState.MISSING,None,'FP_DRC_MISSING_INSIDE_COVERAGE','a'*64)
        bar=M1Bar(symbol,minute,(high+low)/2,high,low,(high+low)/2,1,0,1,BarFinality.CLOSED,'fixture',n,'r1',minute+60_000)
        return MinuteCell(symbol,minute,MinuteCellState.PRESENT,bar,'FP_DRC_PRESENT','a'*64)
    left=cell(plan.left_symbol,left_high,left_low,seq);right=cell(plan.right_symbol,right_high,right_low,seq+1)
    return AlignedMinute('ES_NQ',minute,left,right,'N','b'*64)

def run_conformance():
    _,_,_,_,_,_,report,_=golden_store_and_report(2)
    plan=next(p for p in report.side_plans if p.relation is RelationCode.AL and p.side is PriceSide.HIGH)
    m=plan.check_start_utc_ms
    no=_row(plan,m,plan.left_reference_price-1,plan.left_reference_price-2,plan.right_reference_price-1,plan.right_reference_price-2)
    left=_row(plan,m+60_000,plan.left_reference_price+1,plan.left_reference_price-2,plan.right_reference_price-1,plan.right_reference_price-2)
    result=scan_side_plan(plan,(no,left),'REV-GOLDEN')
    same=_row(plan,m+120_000,plan.left_reference_price+1,plan.left_reference_price-2,plan.right_reference_price+1,plan.right_reference_price-2)
    symmetric=scan_side_plan(plan,(same,),'REV-GOLDEN')
    return {'phase':'FP-I06','version':'1.0.0','checks':{'compiled_relation_count':len(report.compiled_instances),'compiled_side_plan_count':len(report.side_plans),'candidate_direction':result.candidate.direction.value,'candidate_hunter':result.candidate.hunter_symbol,'candidate_state':result.candidate.state.value,'same_m1_outcome':symmetric.classification.outcome.value,'ww_compiled':any(i.relation is RelationCode.WW for i in report.compiled_instances)},'evidence_hash':canonical_sha256((report.evidence_hash,result.evidence_hash,symmetric.evidence_hash))}

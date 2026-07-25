from __future__ import annotations
from fp_i06_relations.engine import scan_side_plan
from fp_i06_relations.enums import ScanMode
from .canonical import canonical_sha256,stable_id
from .contracts import WWScanRecord
from .enums import WWDataState
from .errors import FPI08Error

def scan_ww_side_plan(plan,rows,source_revision_id,scan_mode=ScanMode.BATCH,scan_end_utc_ms=None):
    if plan.data_state is not WWDataState.COMPLETE: raise FPI08Error("FP_WRC_SIDE_PLAN_DATA_BLOCKED","cannot scan blocked WW side plan")
    result=scan_side_plan(plan.to_i06_plan(),rows,source_revision_id,scan_mode,scan_end_utc_ms,False)
    material={"plan":plan.semantic_hash,"scan":result.evidence_hash,"revision":source_revision_id}
    return WWScanRecord(stable_id("FPWWSCAN",material,32),plan.side_plan_id,result,source_revision_id,canonical_sha256(material))

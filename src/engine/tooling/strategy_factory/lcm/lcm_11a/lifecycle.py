from __future__ import annotations
from pathlib import Path
from .canonical import stable_id
from .constants import CANONICAL_LIFECYCLE
from .models import LifecycleContract, VisualSite

def build_lifecycle_contract(repo_root: Path, site: VisualSite, delete_sites: list[dict]) -> LifecycleContract:
    text=(repo_root/site.source_path).read_text(encoding="utf-8",errors="replace")
    relevant=[x for x in delete_sites if x["source_path"]==site.source_path]
    blockers=[]
    if site.surface_kind=="REPORT_PROJECTION":
        init="CREATE_OUTPUT_ON_EXPLICIT_REPORT_RUN"; backfill="INPUT_DATASET_BOUND"; incremental="NOT_APPLICABLE_OR_EXPLICIT_RERUN"; restart="DETERMINISTIC_REWRITE_BY_OUTPUT_ID"; tf="NOT_APPLICABLE"; sym="NOT_APPLICABLE"; deinit="NO_RUNTIME_OBJECT"; cleanup="OUTPUT_PATH_OWNED"; observed="OUTPUT_FILE_WRITE"
    else:
        init="ON_INIT_OR_FIRST_ENSURE" if ("OnInit" in text or "ObjectFind" in text) else "FIRST_RENDER_CALL"
        backfill="ON_CALCULATE_HISTORY_OR_EXPLICIT_REPLAY" if ("OnCalculate" in text or "history" in text.lower() or "backfill" in text.lower()) else "UNKNOWN_REQUIRES_LCM11B_FIXTURE"
        incremental="ON_TICK_TIMER_CALCULATE_OR_RENDER_CALL" if any(x in text for x in ("OnTick","OnTimer","OnCalculate","Update","Render","Draw")) else "CALLER_DRIVEN_UNKNOWN"
        restart="IDEMPOTENT_ENSURE_BY_CANONICAL_ID"
        tf="RECONCILE_ON_CHART_CHANGE_WITH_CANONICAL_SCOPE"
        sym="RECONCILE_ON_CHART_CHANGE_WITH_CANONICAL_SCOPE"
        if relevant:
            scopes={x["scope_classification"] for x in relevant}
            if "BROAD_CHART_DELETE_BLOCKING" in scopes:
                observed="BROAD_CHART_DELETE_BLOCKING"; blockers.append(stable_id("VISBLOCK",site.visual_object_id,"BROAD_DELETE"))
            elif "PREFIX_SCOPED_DELETE_REVIEW_REQUIRED" in scopes:
                observed="PREFIX_SCOPED_DELETE"
            else: observed="INDIVIDUAL_OBJECT_DELETE"
            deinit="DELETE_ONLY_CANONICAL_INSTANCE_NAMESPACE"; cleanup="CANONICAL_INSTANCE_PREFIX_ONLY"
        else:
            observed="NO_DELETE_EVIDENCE"; deinit="CANONICAL_OWNED_CLEANUP_REQUIRED"; cleanup="CANONICAL_INSTANCE_PREFIX_ONLY"; blockers.append(stable_id("VISBLOCK",site.visual_object_id,"MISSING_CLEANUP_EVIDENCE"))
    status="BLOCKED" if blockers else "PASS"
    return LifecycleContract(stable_id("VISLIFE",site.visual_object_id,observed,cleanup),site.visual_object_id,init,backfill,incremental,restart,tf,sym,deinit,cleanup,observed,CANONICAL_LIFECYCLE,status,tuple(blockers))

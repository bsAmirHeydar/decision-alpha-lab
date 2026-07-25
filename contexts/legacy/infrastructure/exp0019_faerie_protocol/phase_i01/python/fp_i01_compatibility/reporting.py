from __future__ import annotations
from pathlib import Path
import csv,json
from .canonical import canonical_sha256
from .differential import run_all_fixtures
from .duplicate_scan import scan_paths
from .enums import CompatibilityStatus
from .hash_guard import verify_dependency
from .models import CompatibilityReport
from .policy import load_dependency_pins

def build_report(repo:Path):
    policy,pins=load_dependency_pins(repo)
    deps=tuple(verify_dependency(repo,p) for p in pins)
    adapters=run_all_fixtures()
    findings=scan_paths(repo,policy['phase_owned_roots'])
    prev=[]
    with (repo/policy['previous_context_test_inventory']).open(encoding='utf-8') as f:
        for row in csv.DictReader(f):
            row=dict(row);row['exists_now']=(repo/row['relative_path']).is_file();prev.append(row)
    blockers=[];warnings=[]
    blockers += [f'DEPENDENCY:{d.dependency_id}:{d.reason_code}' for d in deps if d.status is CompatibilityStatus.FAIL]
    blockers += [f'ADAPTER:{a.fixture_id}:{b}' for a in adapters for b in a.blockers]
    blockers += [f"DUPLICATE:{x['code']}:{x['path']}" for x in findings]
    blockers += [f"MISSING_PREVIOUS_TEST:{x['test_id']}" for x in prev if not x['exists_now']]
    status=CompatibilityStatus.FAIL if blockers else CompatibilityStatus.PASS
    report=CompatibilityReport('FP-I01-COMPATIBILITY-REPORT-V1','FP-I01',deps,adapters,findings,tuple(prev),status,tuple(blockers),tuple(warnings),'pending_local_windows')
    return report

def write_report(repo:Path,report):
    from dataclasses import asdict
    out=repo/'contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i01/artifacts/FP_I01_COMPATIBILITY_REPORT.json'
    out.write_text(json.dumps({**asdict(report),'report_hash':report.report_hash},indent=2,sort_keys=True,default=lambda x:x.value if hasattr(x,'value') else x)+'\n',encoding='utf-8')
    return out

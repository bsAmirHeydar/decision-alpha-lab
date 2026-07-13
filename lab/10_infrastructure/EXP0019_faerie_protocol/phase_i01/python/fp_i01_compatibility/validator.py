from __future__ import annotations
from pathlib import Path
from .enums import CompatibilityStatus
from .reporting import build_report,write_report

def validate(repo:Path):
    report=build_report(repo);write_report(repo,report)
    checks=[]
    for d in report.dependency_results:checks.append({'check_id':f'DEP::{d.dependency_id}','passed':d.status is CompatibilityStatus.PASS,'reason':d.reason_code})
    for a in report.adapter_results:
        checks.append({'check_id':f'ADAPTER::{a.fixture_id}::READ_ONLY','passed':a.source_unchanged,'reason':'SOURCE_UNCHANGED' if a.source_unchanged else 'SOURCE_MUTATED'})
        checks.append({'check_id':f'ADAPTER::{a.fixture_id}::DETERMINISTIC','passed':a.deterministic,'reason':'OUTPUT_STABLE' if a.deterministic else 'OUTPUT_CHANGED'})
    checks.append({'check_id':'DUPLICATE_IMPLEMENTATION_SCAN','passed':not report.duplicate_findings,'reason':'NO_DUPLICATE_CORE_OR_AUTHORITY' if not report.duplicate_findings else 'FORBIDDEN_PATTERN_FOUND'})
    checks.append({'check_id':'PREVIOUS_TEST_DISCOVERY','passed':all(x['exists_now'] for x in report.previous_context_tests),'reason':'ALL_DISCOVERABLE'})
    return report,checks

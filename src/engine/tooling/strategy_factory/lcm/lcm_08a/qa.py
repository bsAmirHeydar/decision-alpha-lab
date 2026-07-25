from __future__ import annotations
from pathlib import Path
from .verify import verify_package
from .io import load_json, load_jsonl


def run(repo_root: Path, portfolio_root: Path) -> dict:
    result=verify_package(portfolio_root)
    records=load_jsonl(portfolio_root/'portfolio/context_portfolio_registry.jsonl')
    selection=load_json(portfolio_root/'pilot/pilot_selection_decision.json')
    pilot=next(r for r in records if r['identity_id']==selection['selected_pilot_identity_id'])
    source=repo_root/pilot['source_artifact_path']
    checks={
      'source_exists':source.is_file(),
      'source_digest_preserved':pilot['source_artifact_sha256'].endswith(__import__('hashlib').sha256(source.read_bytes()).hexdigest()),
      'candidate_count_321':len(records)==321,
      'critical_dimensions_non_compensatory':all(r['risk_class']=='CRITICAL' for r in records if r['critical_dimensions']),
      'pilot_no_order_api':not pilot['static_profile']['capabilities'].get('order_api'),
      'pilot_no_collision':not pilot['identity_collision'],
      'pilot_package_context':pilot['granularity_class']=='PACKAGE_CONTEXT',
      'no_source_move':source.as_posix().endswith(pilot['source_artifact_path']),
    }
    return {**result,'qa_passed':all(checks.values()),'checks':checks}

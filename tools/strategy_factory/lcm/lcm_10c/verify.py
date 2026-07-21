from __future__ import annotations
from pathlib import Path
from .io import load_json,load_jsonl
from .canonical import verify_embedded_digest
class ClosureVerifier:
    def verify(self,root:Path)->dict:
        required=['dry_run/dry_run_golden_requests.jsonl','dry_run/dry_run_replay_results.jsonl','parity/execution_parity_report.json','safety/safety_control_test_report.json','authority_negative/authority_negative_test_report.json','authority_negative/forbidden_api_scan.json','closure/treatment_execution_disposition_registry.json','handoff/lcm10c_to_lcm11a_handoff.json','output_manifest.json']
        missing=[x for x in required if not (root/x).is_file()]
        cases=load_jsonl(root/'dry_run/dry_run_golden_requests.jsonl') if not missing else []
        replays=load_jsonl(root/'dry_run/dry_run_replay_results.jsonl') if not missing else []
        parity=load_json(root/'parity/execution_parity_report.json') if not missing else {}
        auth=load_json(root/'authority_negative/authority_negative_test_report.json') if not missing else {}
        safety=load_json(root/'safety/safety_control_test_report.json') if not missing else {}
        errors=[]
        if len(cases)!=422:errors.append(f'expected 422 cases, got {len(cases)}')
        if len(replays)!=422:errors.append(f'expected 422 replays, got {len(replays)}')
        if parity.get('failed_count')!=0:errors.append('parity failures')
        if auth.get('failed_count')!=0:errors.append('authority failures')
        if safety.get('failed_count')!=0:errors.append('safety failures')
        if sum(x.get('submission_attempt_count',0) for x in replays)!=0:errors.append('submission attempts nonzero')
        return {'result':'PASS' if not missing and not errors else 'FAIL','missing':missing,'errors':errors,'case_count':len(cases),'replay_count':len(replays)}

from __future__ import annotations
from pathlib import Path
from .io import load_json,dump_json,dump_jsonl
from .fixtures import build_request_case
from .lifecycle import DryRunLifecycleSimulator
from .parity import compare_case
from .authority import AuthorityNegativeVerifier
from .canonical import digest_object,stable_id
class LCM10CClosureService:
    def __init__(self,repo_root:Path,upstream_root:Path,output_root:Path):self.repo_root=repo_root;self.upstream_root=upstream_root;self.output_root=output_root
    def build(self)->dict:
        packages=[load_json(p) for p in sorted((self.upstream_root/'canonical_treatment_packages').glob('*.json'))]
        adapters=[load_json(p) for p in sorted((self.upstream_root/'execution_adapter_contracts').glob('*.json'))]
        sim=DryRunLifecycleSimulator();auth=AuthorityNegativeVerifier();cases=[];replays=[];parity=[];auth_results=[]
        for pkg in packages:
            case=build_request_case(pkg);replay=sim.replay(case);par=compare_case(case,replay);cases.append(case);replays.append(replay);parity.append(par)
        for adapter in adapters:auth_results.append(auth.verify_adapter(adapter))
        dump_jsonl(self.output_root/'dry_run/dry_run_golden_requests.jsonl',cases)
        dump_jsonl(self.output_root/'dry_run/dry_run_replay_results.jsonl',replays)
        dump_jsonl(self.output_root/'parity/execution_parity_results.jsonl',parity)
        dump_jsonl(self.output_root/'authority_negative/adapter_authority_negative_results.jsonl',auth_results)
        summary={"package_count":len(packages),"adapter_count":len(adapters),"parity_pass_count":sum(x['result']=='PASS' for x in parity),"authority_pass_count":sum(x['result']=='PASS' for x in auth_results),"submission_attempt_count":sum(x['submission_attempt_count'] for x in replays),"live_order_count":sum(x['live_order_count'] for x in replays),"paper_order_count":sum(x['paper_order_count'] for x in replays),"capital_activation_count":sum(x['capital_activation_count'] for x in replays)}
        summary['summary_digest']=digest_object(summary,'summary_digest');return summary

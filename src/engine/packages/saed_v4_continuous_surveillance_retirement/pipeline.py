from __future__ import annotations
from copy import deepcopy
from .upstream import verify_upstream
from .constitution import freeze_constitution,authority_boundary
from .policy import freeze_policy
from .observations import compile_observations
from .detectors import run_detectors
from .fusion import fuse_alerts
from .incidents import build_incidents
from .actions import compile_actions
from .dependencies import build_dependency_graph,impact_for_cells
from .retirement import compile_retirements
from .archive import archive_retirements
from .verification import verify_post_retirement
from .surveillance import build_surveillance_dashboard
from .evidence import build_evidence
from .governance import review_bundle
from .release import compile_release,compile_certificate,compile_operations_handoff

def run_reference(v:dict)->dict:
 upstream=verify_upstream(v["upstream_certificate"],v["upstream_handoff"])
 constitution=freeze_constitution(v["constitution"]);authority=authority_boundary();policy=freeze_policy(v["policy"])
 registry=deepcopy(v["registry"]);routes=deepcopy(v["routes"])
 ledger=compile_observations(v["observations"],registry,policy,v["cutoff"])
 detection=run_detectors(ledger,policy);fusion=fuse_alerts(detection,registry,policy);incidents=build_incidents(fusion,v["cutoff"]);actions=compile_actions(fusion,registry,v["cutoff"])
 dependencies=build_dependency_graph(registry,routes);candidate_ids=[x["cell_id"] for x in fusion["rows"] if x["action"]=="RETIRE_CANDIDATE"];impact=impact_for_cells(dependencies,candidate_ids)
 retirement=compile_retirements(fusion,registry,policy,v["retirement_approvals"],v["replacement_map"],impact,v["cutoff"])
 archive=archive_retirements(retirement,dependencies,ledger,detection,incidents,actions);verification=verify_post_retirement(retirement,archive,actions,registry)
 dashboard=build_surveillance_dashboard(registry,policy,ledger,detection,fusion,incidents,retirement)
 parts={"upstream":upstream,"constitution":constitution,"authority":authority,"policy":policy,"registry":registry,"routes":routes,"ledger":ledger,"detection":detection,"fusion":fusion,"incidents":incidents,"actions":actions,"dependencies":dependencies,"impact":impact,"retirement":retirement,"archive":archive,"verification":verification,"dashboard":dashboard}
 evidence=build_evidence(parts);review=review_bundle({**v["governance_review"],"reviews":[{**x,"evidence_hash":evidence["evidence_bundle_hash"]} for x in v["governance_review"]["reviews"]]},evidence["evidence_bundle_hash"])
 release=compile_release(evidence,review,verification,dashboard);certificate=compile_certificate(release,evidence);handoff=compile_operations_handoff(certificate,release)
 return {**parts,"evidence_bundle":evidence,"review_bundle":review,"release":release,"certificate":certificate,"handoff":handoff}

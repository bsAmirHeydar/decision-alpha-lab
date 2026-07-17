from __future__ import annotations
import copy, pytest
from saed_v4_mechanistic_interpretability import run
from saed_v4_mechanistic_interpretability.errors import SecurityBoundaryError, UpstreamVerificationError

def test_authority_zero(outputs): assert not any(outputs["authority_boundary"]["authority"].values())
def test_certificate_claim_ceiling(outputs):
 c=outputs["certificate"]; assert c["accepted_for_mechanistic_interpretability_research"]
 for f in ["decision_authority","promotion_authority","runtime_executable","risk_allocation_authority","execution_authority","production_authority","online_learning_authority","real_alpha_claim","prospective_success_claim","runtime_parity_claim"]: assert c[f] is False
def test_upstream_hash_mutation_rejected(config,upstream,records):
 m=copy.deepcopy(upstream); m["handoff"]["handoff_hash"]="0"*64
 with pytest.raises(UpstreamVerificationError): run(config,m,records)
def test_security_token_rejected(config,upstream,records):
 m=copy.deepcopy(records); m[0]["context_id"]="broker_token"
 with pytest.raises(SecurityBoundaryError): run(config,upstream,m)

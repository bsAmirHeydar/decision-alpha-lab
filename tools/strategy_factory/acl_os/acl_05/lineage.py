from __future__ import annotations
from typing import Any
from .canonical import digest_object

def build_provenance(*,batch_id: str,handoff: dict[str,Any],binding: dict[str,Any],candidate_freeze: dict[str,Any],search_freeze: dict[str,Any],datasets: dict[str,Any],labels: dict[str,Any],split: dict[str,Any],environment: dict[str,Any],budget: dict[str,Any],object_index: dict[str,Any]) -> dict[str,Any]:
    nodes=[
      {"node_id":"ACL03_HANDOFF","artifact_type":"ACL03_TO_ACL04","digest":handoff["upstream_acl03_handoff_digest"]},
      {"node_id":"ACL04_HANDOFF","artifact_type":"ACL04_TO_ACL05","digest":handoff["handoff_digest"]},
      {"node_id":"ACL04_BINDING","artifact_type":"ACL04_BINDING","digest":binding["binding_digest"]},
      {"node_id":"CANDIDATE_FREEZE","artifact_type":"CANDIDATE_FREEZE_SET","digest":candidate_freeze["candidate_freeze_digest"]},
      {"node_id":"SEARCH_FREEZE","artifact_type":"SEARCH_SPACE_FREEZE","digest":search_freeze["search_space_freeze_digest"]},
      {"node_id":"DATASET_SET","artifact_type":"DATASET_SNAPSHOT_SET","digest":datasets["dataset_snapshot_set_digest"]},
      {"node_id":"LABEL_SET","artifact_type":"LABEL_CONTRACT_SET","digest":labels["label_contract_set_digest"]},
      {"node_id":"SPLIT","artifact_type":"SPLIT_CONTRACT","digest":split["split_digest"]},
      {"node_id":"ENVIRONMENT","artifact_type":"ENVIRONMENT_LOCK","digest":environment["environment_digest"]},
      {"node_id":"BUDGET","artifact_type":"COMPUTE_BUDGET","digest":budget["budget_digest"]},
      {"node_id":"OBJECT_INDEX","artifact_type":"CAS_OBJECT_INDEX","digest":object_index["object_index_digest"]},
      {"node_id":"BATCH","artifact_type":"IMMUTABLE_RESEARCH_BATCH","digest":batch_id},
    ]
    edges=[
      {"from":"ACL03_HANDOFF","to":"ACL04_HANDOFF","relation":"CONTEXT_COMPILED_INTO_SETUP_FACTORY"},
      {"from":"ACL04_HANDOFF","to":"ACL04_BINDING","relation":"VERIFIED_AND_BOUND"},
      {"from":"ACL04_BINDING","to":"CANDIDATE_FREEZE","relation":"FREEZES_CANONICAL_SETUPS"},
      {"from":"CANDIDATE_FREEZE","to":"SEARCH_FREEZE","relation":"CLOSES_SEARCH_SPACE"},
    ]
    for node in ("SEARCH_FREEZE","DATASET_SET","LABEL_SET","SPLIT","ENVIRONMENT","BUDGET","OBJECT_INDEX"):
        edges.append({"from":node,"to":"BATCH","relation":"MATERIAL_IDENTITY_INPUT"})
    body={"schema_version":"1.0.0","batch_id":batch_id,"nodes":nodes,"edges":edges,"reaches_acl03":True,"all_material_inputs_bound":True}
    return {**body,"graph_digest":digest_object(body)}

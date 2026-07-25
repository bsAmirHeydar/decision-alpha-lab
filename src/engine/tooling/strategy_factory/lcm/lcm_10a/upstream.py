from __future__ import annotations
from pathlib import Path
from .canonical import digest_object, file_digest
from .constants import LCM01_SURVEY_ROOT, LCM02_CLASSIFICATION_ROOT, LCM07_SHARED_ENGINE_ROOT, UPSTREAM_HANDOFF_DIGEST, UPSTREAM_SETUP_ROOT
from .errors import UpstreamBindingError
from .io import load_csv, load_json, load_jsonl

def load_upstream(repo_root: Path) -> dict:
    setup=repo_root/UPSTREAM_SETUP_ROOT; survey=repo_root/LCM01_SURVEY_ROOT; cls=repo_root/LCM02_CLASSIFICATION_ROOT; eng=repo_root/LCM07_SHARED_ENGINE_ROOT
    handoff=load_json(setup/'handoff/lcm09b_to_lcm10a_handoff.json')
    if handoff.get('handoff_digest') != UPSTREAM_HANDOFF_DIGEST: raise UpstreamBindingError('LCM10A_UPSTREAM_HANDOFF_DIGEST_MISMATCH')
    if handoff.get('allowed_next_actions') is None or 'INVENTORY_TREATMENT_AND_EXECUTION_CAPABILITIES' not in handoff['allowed_next_actions']: raise UpstreamBindingError('LCM10A_UPSTREAM_ACTION_NOT_ALLOWED')
    seeds=load_jsonl(setup/'dependencies/treatment_dependency_inventory_seed.jsonl')
    if len(seeds)!=60: raise UpstreamBindingError('LCM10A_SETUP_DEPENDENCY_SEED_COUNT_MISMATCH')
    cap_rows=load_csv(survey/'capabilities/capability_findings.csv')
    entry_rows=load_csv(survey/'dependencies/entry_points.csv')
    classification_rows=load_jsonl(cls/'artifacts/artifact_classification_records.jsonl')
    security_rows=load_csv(cls/'authority/security_sensitive_paths.csv')
    engine_handoff=load_json(eng/'handoff/lcm07_to_lcm08_handoff.json')
    return {"setup_handoff":handoff,"setup_seeds":seeds,"lcm01_capabilities":cap_rows,"lcm01_entries":entry_rows,"classifications":classification_rows,"security_rows":security_rows,"engine_handoff":engine_handoff,"roots":{"setup":setup,"survey":survey,"classification":cls,"shared_engine":eng}}

def source_binding_doc(upstream: dict) -> dict:
    h=upstream['setup_handoff']; roots=upstream['roots']
    body={"schema_version":"1.0.0","lcm09b_handoff_digest":h['handoff_digest'],"lcm09b_treatment_dependency_seed_digest":h['treatment_dependency_seed_digest'],"lcm01_survey_manifest_digest":load_json(roots['survey']/'output_manifest.json')['output_manifest_digest'],"lcm02_classification_manifest_digest":load_json(roots['classification']/'output_manifest.json')['output_manifest_digest'],"lcm07_shared_engine_manifest_digest":load_json(roots['shared_engine']/'output_manifest.json')['output_manifest_digest'],"setup_dependency_seed_count":len(upstream['setup_seeds']),"lcm01_capability_finding_count":len(upstream['lcm01_capabilities']),"lcm01_entry_point_count":len(upstream['lcm01_entries']),"lcm02_classification_count":len(upstream['classifications']),"lcm02_security_sensitive_path_count":len(upstream['security_rows'])}
    return {**body,"binding_digest":digest_object(body)}

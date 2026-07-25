from __future__ import annotations
from pathlib import Path
from typing import Any, Iterable
from .handoff_input import load_acl03_bundle
from .authority import validate_authority
from .atom_registry import build_default_registry, validate_registry
from .search_authority import validate_search_authority
from .treatment import validate_treatment_envelope
from .human_dsl import compile_human_setup
from .ai_generator import generate_ai_setups
from .baseline import compile_baselines
from .constraints import evaluate_policy
from .candidate import build_candidate
from .deduplication import deduplicate
from .provenance import build_provenance
from .security import evaluate_security
from .handoff import build_acl05_handoff
from .artifact_manifest import build_manifest
from .generator import prepare_output, emit
from .canonical import digest_object
from .io import dump_json
from .schema_validation import validate_instance

FACTORY_VERSION="1.0.0"
CLAIM_CEILING="SETUP_DEFINITION_REFERENCE_ONLY"

class ACL04DualSetupFactoryService:
    def build(self, *, compiled_root: Path, output_root: Path, authority_permit: dict[str, Any], search_authority: dict[str, Any], treatment_envelope: dict[str, Any], human_setups: Iterable[dict[str, Any]]=(), ai_requests: Iterable[dict[str, Any]]=(), atom_registry: dict[str, Any]|None=None, include_baselines: bool=True) -> dict[str, Any]:
        bundle=load_acl03_bundle(compiled_root); handoff=bundle["handoff"]
        authority_report=validate_authority(authority_permit,handoff)
        registry=validate_registry(atom_registry or build_default_registry())
        search=validate_search_authority(search_authority,handoff,registry)
        envelope=validate_treatment_envelope(treatment_envelope,handoff)
        if not set(search["allowed_actions"]).issubset(set(envelope["allowed_actions"])):
            raise ValueError("ACL04_SEARCH_ACTIONS_EXCEED_TREATMENT_ENVELOPE")
        source_irs=[]; exposures=[]
        for doc in human_setups:
            validate_instance("human_setup_dsl",doc)
            source_irs.append((doc["setup_key"],digest_object(doc),compile_human_setup(doc,context_id=handoff["context_id"],context_version=handoff["context_version"])))
        for req in ai_requests:
            generated, exposure=generate_ai_setups(req,search,context_id=handoff["context_id"],context_version=handoff["context_version"])
            exposures.append(exposure)
            for index,ir in enumerate(generated): source_irs.append((f"{req['request_id']}:{index:04d}",digest_object(req),ir))
        if include_baselines:
            for name,ir in compile_baselines(handoff["context_id"],handoff["context_version"]): source_irs.append((name,digest_object({"baseline":name,"version":"1.0.0"}),ir))
        if len(source_irs)>search["max_candidates"]+5:
            raise ValueError("ACL04_TOTAL_CANDIDATE_BUDGET_EXCEEDED")
        candidates=[]
        for source_id,source_digest,ir in source_irs:
            findings=evaluate_policy(ir,registry,search,envelope)
            candidates.append(build_candidate(ir,source_id=source_id,source_digest=source_digest,authority_digest=search["authority_digest"],envelope_digest=envelope["envelope_digest"],findings=findings))
        canonical,dedup=deduplicate(candidates)
        exposure_body={"schema_version":"1.0.0","authority_id":search["authority_id"],"authority_digest":search["authority_digest"],"human_definition_count":sum(1 for c in candidates if c["origin"]=="HUMAN"),"ai_exposures":exposures,"baseline_count":sum(1 for c in candidates if c["origin"]=="BASELINE"),"total_materialized":len(candidates),"complete_search_exposure_recorded":True}
        exposure_ledger={**exposure_body,"ledger_digest":digest_object(exposure_body)}
        provenance=build_provenance(candidates,handoff)
        security=evaluate_security(Path(__file__).parent)
        if not security["passed"]: raise RuntimeError("ACL04_SECURITY_BOUNDARY_FAILED")
        acl05=build_acl05_handoff(context_id=handoff["context_id"],context_version=handoff["context_version"],upstream_handoff_digest=handoff["handoff_digest"],candidates=canonical,dedup_report=dedup,exposure_ledger=exposure_ledger,provenance=provenance)
        binding_body={"schema_version":"1.0.0","context_id":handoff["context_id"],"context_version":handoff["context_version"],"upstream_handoff_digest":handoff["handoff_digest"],"upstream_bundle_digest":bundle["bundle_digest"],"detector_ir_digest":handoff["detector_ir_digest"],"occurrence_ir_digest":handoff["occurrence_ir_digest"],"feature_binding_ir_digest":handoff["feature_binding_ir_digest"],"known_time_policy":"INHERIT_AND_NEVER_BYPASS","context_semantics_mutable":False}
        binding={**binding_body,"binding_digest":digest_object(binding_body)}
        prepare_output(output_root)
        summary={"context_id":handoff["context_id"],"context_version":handoff["context_version"],"upstream_handoff_digest":handoff["handoff_digest"],"source_candidate_count":len(candidates),"canonical_candidate_count":len(canonical),"invalid_candidate_count":sum(c["status"]=="INVALID" for c in candidates),"diagnostic_candidate_count":sum(c["status"]=="DIAGNOSTIC_ONLY" for c in candidates)}
        emit(output_root,binding=binding,authority_report=authority_report,search_authority=search,envelope=envelope,registry=registry,all_candidates=candidates,canonical_candidates=canonical,dedup_report=dedup,exposure_ledger=exposure_ledger,provenance=provenance,security=security,handoff=acl05,result_summary=summary)
        manifest=build_manifest(output_root,handoff["context_id"],handoff["context_version"]); dump_json(output_root/"output_manifest.json",manifest)
        receipt_body={"schema_version":"1.0.0","factory_version":FACTORY_VERSION,"context_id":handoff["context_id"],"context_version":handoff["context_version"],"upstream_handoff_digest":handoff["handoff_digest"],"binding_digest":binding["binding_digest"],"search_authority_digest":search["authority_digest"],"treatment_envelope_digest":envelope["envelope_digest"],"output_manifest_digest":manifest["manifest_digest"],"acl05_handoff_digest":acl05["handoff_digest"],"source_candidate_count":len(candidates),"canonical_candidate_count":len(canonical),"claim_ceiling":CLAIM_CEILING,"live_order_submission_allowed":False,"capital_activation_allowed":False}
        receipt={**receipt_body,"receipt_digest":digest_object(receipt_body)}; validate_instance("factory_receipt",receipt); dump_json(output_root/"factory_receipt.json",receipt)
        return {"passed":True,**summary,"candidates":candidates,"canonical_candidates":canonical,"deduplication":dedup,"exposure_ledger":exposure_ledger,"provenance":provenance,"security":security,"handoff":acl05,"binding":binding,"output_manifest":manifest,"receipt":receipt,"output_root":str(output_root)}

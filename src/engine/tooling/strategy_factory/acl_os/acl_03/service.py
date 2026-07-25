from __future__ import annotations
from pathlib import Path
from typing import Any
from ..acl_02.loader import ContextPackageLoader
from ..acl_02.service import ACL02ContextIntakeService
from .source_snapshot import build_source_snapshot
from .prerequisites import validate_prerequisites
from .compiler_plan import build_compiler_plan
from .detector_ir import compile_detector_ir
from .occurrence_ir import compile_occurrence_ir
from .known_time_ir import compile_known_time_ir
from .feature_binding_ir import compile_feature_binding_ir
from .adapters import compile_adapter_contracts
from .golden_replay import compile_golden_cases,run_golden_replay
from .generator import prepare_output,emit_all
from .artifact_manifest import build_output_manifest
from .onboarding import build_onboarding_report
from .handoff import build_acl04_handoff
from .canonical import digest_object
from .compatibility import validate_compatibility
from .extensions import resolve_extensions
from .lineage import build_lineage_graph
from .security import evaluate_security_boundary
from .schema_emitter import generated_schemas
from .io import dump_json
from .errors import PrerequisiteError,CompilationError

COMPILER_VERSION="1.0.0"

class ACL03ContextCompilerService:
    def compile(self,context_root:Path,output_root:Path,authority_permit:dict,semantic_approval:dict,acl02_readiness:dict|None=None)->dict[str,Any]:
        context_root=context_root.resolve(); output_root=output_root.resolve()
        package=ContextPackageLoader(context_root).load(); package.pop("_paths",None)
        snapshot=build_source_snapshot(context_root,package,COMPILER_VERSION)
        if acl02_readiness is None:
            intake_permit={"decision":"ALLOW","action":"ACL02_EVALUATE_CONTEXT","subject_artifact_id":package["manifest"]["artifact_id"],"live_order_submission_allowed":False,"capital_activation_allowed":False}
            acl02_readiness=ACL02ContextIntakeService().evaluate(context_root,intake_permit)["readiness"]
        prereq=validate_prerequisites(package,snapshot,authority_permit,semantic_approval,acl02_readiness)
        if not prereq["passed"]: raise PrerequisiteError("ACL-03 prerequisites failed: "+",".join(f["code"] for f in prereq["findings"]))
        compatibility=validate_compatibility(package,COMPILER_VERSION); extensions=resolve_extensions(package)
        if not compatibility["compatible"] or not extensions["passed"]: raise CompilationError("ACL-03 compatibility or extension resolution failed")
        plan=build_compiler_plan(package["manifest"]["context_id"],package["manifest"]["context_version"],snapshot["snapshot_digest"],COMPILER_VERSION)
        detector,fd=compile_detector_ir(package); occurrence,fo=compile_occurrence_ir(package); known,fk=compile_known_time_ir(package); feature,ff=compile_feature_binding_ir(package)
        findings=prereq["findings"]+compatibility["findings"]+extensions["findings"]+fd+fo+fk+ff
        if any(x["severity"] in {"BLOCKER","ERROR"} for x in findings): raise CompilationError("ACL-03 compilation blockers: "+",".join(x["code"] for x in findings))
        adapters=compile_adapter_contracts(package,known,feature); cases=compile_golden_cases(context_root,package,detector); replay=run_golden_replay(detector,known,cases)
        artifact_count=24+len(adapters)+len(generated_schemas(package["manifest"]["context_id"]))
        onboarding=build_onboarding_report(package,prereq,findings,replay,adapters,artifact_count)
        handoff=build_acl04_handoff(package,snapshot,detector,occurrence,feature,onboarding)
        lineage=build_lineage_graph(package,snapshot,plan,detector,occurrence,known,feature,replay,onboarding,handoff)
        security_report=evaluate_security_boundary(context_root,package,detector,adapters)
        if not security_report["passed"]: raise CompilationError("ACL-03 security boundary failed")
        prepare_output(output_root);emit_all(output_root,COMPILER_VERSION,snapshot,plan,detector,occurrence,known,feature,adapters,cases,replay,onboarding,handoff,findings,compatibility,extensions,lineage,security_report)
        manifest=build_output_manifest(output_root,package["manifest"]["context_id"],package["manifest"]["context_version"],snapshot["snapshot_digest"]);dump_json(output_root/"output_manifest.json",manifest)
        receipt_body={"schema_version":"1.0.0","context_id":package["manifest"]["context_id"],"context_version":package["manifest"]["context_version"],"compiler_version":COMPILER_VERSION,"source_digest":snapshot["snapshot_digest"],"plan_digest":plan["plan_digest"],"output_manifest_digest":manifest["manifest_digest"],"onboarding_report_digest":onboarding["report_digest"],"acl04_handoff_digest":handoff["handoff_digest"],"claim_ceiling":"CONTEXT_COMPILATION_REFERENCE_ONLY","live_order_submission_allowed":False,"capital_activation_allowed":False}
        receipt={**receipt_body,"receipt_digest":digest_object(receipt_body)};dump_json(output_root/"compilation_receipt.json",receipt)
        return {"passed":onboarding["decision"]=="COMPILED_WITH_OBLIGATIONS","source_snapshot":snapshot,"plan":plan,"detector_ir":detector,"occurrence_ir":occurrence,"known_time_ir":known,"feature_binding_ir":feature,"adapters":adapters,"replay":replay,"onboarding":onboarding,"handoff":handoff,"compatibility":compatibility,"extensions":extensions,"lineage":lineage,"security_report":security_report,"output_manifest":manifest,"receipt":receipt,"output_root":str(output_root)}

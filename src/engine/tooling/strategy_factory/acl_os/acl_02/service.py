from __future__ import annotations
from pathlib import Path
from typing import Any
from .loader import ContextPackageLoader
from .schema_validation import validate_schemas
from .completeness import evaluate_completeness
from .ambiguity import AmbiguityAnalyzer
from .clocks import validate_causal_clock
from .semantics import validate_semantics
from .security import classify_security
from .authority_binding import validate_authority_binding
from .readiness import build_readiness
from .io import dump_json
from .projection import write_projection

class ACL02ContextIntakeService:
    def evaluate(self,context_root:Path,authority_permit:dict|None=None,output_dir:Path|None=None)->dict[str,Any]:
        package=ContextPackageLoader(context_root).load();paths=package.pop("_paths")
        schema=[f.to_dict() for f in validate_schemas(package,paths)]
        completeness=evaluate_completeness(package);ambiguity=AmbiguityAnalyzer().analyze(package)
        clock=validate_causal_clock(package["causal_clock"]);semantic=validate_semantics(package);security=classify_security(package);authority=validate_authority_binding(package["manifest"],authority_permit)
        report=build_readiness(package["manifest"]["context_id"],completeness,ambiguity,clock,semantic,security,schema,authority)
        result={"package_digest":__import__('src.engine.tooling.strategy_factory.acl_os.acl_02.canonical',fromlist=['digest_object']).digest_object(package),"readiness":report,"components":{"schema_findings":schema,"completeness":completeness,"ambiguity":ambiguity,"causal_clock":clock,"semantics":semantic,"security":security,"authority":authority}}
        if output_dir:
            dump_json(output_dir/"context_intake_result.json",result);write_projection(output_dir/"CONTEXT_INTAKE_READINESS.md",report)
        return result

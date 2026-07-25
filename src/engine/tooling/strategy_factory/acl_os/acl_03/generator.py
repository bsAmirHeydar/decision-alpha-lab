from __future__ import annotations
import shutil
from pathlib import Path
from .io import dump_json,atomic_write,generated_header
from .schema_emitter import generated_schemas
from .projection import write_projection

def prepare_output(output_root:Path)->None:
    output_root=output_root.resolve()
    if output_root.exists():
        marker=output_root/".acl03_generated_root"
        if not marker.is_file(): raise ValueError("refusing to replace output without ACL-03 marker")
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    atomic_write(output_root/".acl03_generated_root",b"ACL03_GENERATED_ROOT_V1\n")

def emit_all(output_root:Path,compiler_version:str,source_snapshot:dict,plan:dict,detector_ir:dict,occurrence_ir:dict,known_time_ir:dict,feature_ir:dict,adapters:list,cases:list,replay:dict,onboarding:dict,handoff:dict,findings:list,compatibility:dict,extensions:dict,lineage:dict,security_report:dict)->None:
    source=source_snapshot["snapshot_digest"]
    docs={
      "source/source_snapshot.json":source_snapshot,
      "plan/compiler_plan.json":plan,
      "ir/detector_ir.json":detector_ir,
      "ir/occurrence_ir.json":occurrence_ir,
      "ir/known_time_ir.json":known_time_ir,
      "ir/feature_binding_ir.json":feature_ir,
      "replay/golden_cases.json":{"schema_version":"1.0.0","cases":cases},
      "replay/golden_replay_result.json":replay,
      "reports/onboarding_report.json":onboarding,
      "handoff/acl04_handoff.json":handoff,
      "reports/compilation_findings.json":{"schema_version":"1.0.0","findings":findings},
      "reports/compatibility_report.json":compatibility,
      "reports/extension_resolution.json":extensions,
      "reports/security_boundary_report.json":security_report,
      "lineage/lineage_graph.json":lineage,
    }
    for rel,obj in docs.items(): dump_json(output_root/rel,obj)
    for adapter in adapters: dump_json(output_root/"adapters"/f"{adapter['adapter_id']}.json",adapter)
    for name,schema in generated_schemas(onboarding["context_id"]).items(): dump_json(output_root/"schemas"/name,schema)
    write_projection(output_root/"docs"/"ACL03_ONBOARDING_REPORT.md",onboarding)
    text=generated_header(source,compiler_version)+"\nAll files in this directory are projections of machine-readable ACL-03 artifacts.\n"
    atomic_write(output_root/"docs"/"GENERATED_FILES.md",text.encode("utf-8"))

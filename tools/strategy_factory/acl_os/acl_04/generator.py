from __future__ import annotations
import shutil
from pathlib import Path
from typing import Any
from .io import dump_json, dump_text
from .projection import candidate_markdown, factory_summary_markdown

MARKER=".acl04_generated_root"

def prepare_output(output_root: Path) -> None:
    if output_root.exists():
        marker=output_root/MARKER
        if not marker.is_file(): raise RuntimeError("ACL04_OUTPUT_ROOT_NOT_OWNED")
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True)
    dump_text(output_root/MARKER, "ACL-04 generated output; safe to replace only through ACL-04.\n")


def emit(output_root: Path, *, binding: dict[str, Any], authority_report: dict[str, Any], search_authority: dict[str, Any], envelope: dict[str, Any], registry: dict[str, Any], all_candidates: list[dict[str, Any]], canonical_candidates: list[dict[str, Any]], dedup_report: dict[str, Any], exposure_ledger: dict[str, Any], provenance: dict[str, Any], security: dict[str, Any], handoff: dict[str, Any], result_summary: dict[str, Any]) -> None:
    dump_json(output_root/"binding"/"acl03_binding.json",binding)
    dump_json(output_root/"authority"/"authority_report.json",authority_report)
    dump_json(output_root/"authority"/"search_authority.json",search_authority)
    dump_json(output_root/"authority"/"treatment_envelope.json",envelope)
    dump_json(output_root/"registry"/"setup_atom_registry.json",registry)
    for c in all_candidates:
        dump_json(output_root/"candidates"/"all"/f"{c['candidate_id']}.json",c)
    for c in canonical_candidates:
        dump_json(output_root/"candidates"/"canonical"/f"{c['setup_id']}.json",c)
        dump_text(output_root/"docs"/"setups"/f"{c['setup_id']}.md",candidate_markdown(c))
    dump_json(output_root/"reports"/"deduplication_report.json",dedup_report)
    dump_json(output_root/"reports"/"search_exposure_ledger.json",exposure_ledger)
    dump_json(output_root/"lineage"/"provenance_graph.json",provenance)
    dump_json(output_root/"reports"/"security_boundary_report.json",security)
    dump_json(output_root/"handoff"/"acl05_handoff.json",handoff)
    dump_text(output_root/"docs"/"ACL04_FACTORY_SUMMARY.md",factory_summary_markdown(result_summary))

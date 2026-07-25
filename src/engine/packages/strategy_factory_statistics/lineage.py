from __future__ import annotations
from .models import StatisticalReportManifest

def validate_report_lineage(manifest: StatisticalReportManifest,
                            source_run_id: str, source_manifest_hash: str,
                            source_artifact_hash: str) -> None:
    manifest.validate()
    if manifest.source_run_id != source_run_id: raise ValueError("source run mismatch")
    if manifest.source_manifest_hash != source_manifest_hash: raise ValueError("source manifest mismatch")
    if manifest.source_artifact_hash != source_artifact_hash: raise ValueError("source artifact mismatch")

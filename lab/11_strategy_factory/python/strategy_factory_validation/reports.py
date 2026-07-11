from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import hashlib, json
from .models import AntiOverfitReportManifest, PromotionDecision

def write_report_bundle(directory: str | Path,
                        manifest: AntiOverfitReportManifest,
                        decision: PromotionDecision,
                        diagnostics: dict) -> dict[str,str]:
    out=Path(directory); out.mkdir(parents=True,exist_ok=True)
    manifest=manifest.with_hash() if not manifest.manifest_hash else manifest
    files={
      "manifest.json": json.dumps(asdict(manifest),indent=2,sort_keys=True,default=int)+"\n",
      "promotion_decision.json": json.dumps(asdict(decision),indent=2,sort_keys=True,default=int)+"\n",
      "diagnostics.json": json.dumps(diagnostics,indent=2,sort_keys=True,default=int)+"\n",
      "README.md": _markdown(manifest,decision),
    }
    hashes={}
    for name,text in files.items():
        (out/name).write_text(text,encoding="utf-8",newline="\n")
        hashes[name]=hashlib.sha256(text.encode("utf-8")).hexdigest()
    index={"schema":"alpha_lab.strategy_factory/anti_overfit_artifact_index@1.0.0",
           "report_id":manifest.report_id,"manifest_hash":manifest.manifest_hash,
           "artifacts":[{"path":k,"sha256":v} for k,v in sorted(hashes.items())]}
    index_text=json.dumps(index,indent=2,sort_keys=True)+"\n"
    (out/"artifact_index.json").write_text(index_text,encoding="utf-8",newline="\n")
    hashes["artifact_index.json"]=hashlib.sha256(index_text.encode()).hexdigest()
    return hashes

def _markdown(manifest,decision):
    lines=["# Anti-Overfit Validation Report","",
           f"- Report: `{manifest.report_id}`",
           f"- Plan: `{manifest.plan_hash}`",
           f"- Selected trial: `{decision.selected_trial_id}`",
           f"- Status: **{decision.status.name}**","",
           "## Gate ledger","",
           "| Gate | Status | Observed | Threshold | Reason |",
           "|---|---:|---:|---:|---|"]
    for g in decision.gate_results:
        lines.append(f"| `{g.gate_id}` | {g.status.name} | {g.observed_value:.6g} | {g.comparison} {g.threshold_value:.6g} | `{g.reason_code}` |")
    lines += ["", "## Authority boundary", "",
              "This report may permit dataset-review progression only. It does not authorize paper or live orders.", ""]
    return "\n".join(lines)

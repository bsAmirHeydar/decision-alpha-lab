from __future__ import annotations
from pathlib import Path
from .io import load_json
class VisualizerMigrationVerifier:
    REQUIRED=("canonical_visualizer_registry.json","golden_fixture_registry.json","visual_parity_report.json","multi_chart_test_report.json","restart_backfill_test_report.json","visual_cutover_manifest.json","visual_rollback_manifest.json","blockers/blocker_resolution_registry.json","reports/acceptance_report.json","reports/hostile_review.json","reports/authority_negative_report.json","LCM11B_TO_LCM12A_HANDOFF.json","output_manifest.json")
    def verify(self,root:Path)->dict:
        missing=[x for x in self.REQUIRED if not (root/x).is_file()];errors=[]
        if missing:return {"result":"FAIL","missing":missing,"errors":errors}
        reg=load_json(root/"canonical_visualizer_registry.json");par=load_json(root/"visual_parity_report.json");iso=load_json(root/"multi_chart_test_report.json");rb=load_json(root/"restart_backfill_test_report.json");cut=load_json(root/"visual_cutover_manifest.json");acc=load_json(root/"reports/acceptance_report.json");hand=load_json(root/"LCM11B_TO_LCM12A_HANDOFF.json")
        if len(reg.get("visualizers",[]))!=128:errors.append("visualizer count mismatch")
        if par.get("semantic_mismatch_count")!=0:errors.append("semantic mismatch")
        if iso.get("canonical_collision_count")!=0:errors.append("canonical collision")
        if rb.get("domain_state_mutation_count")!=0:errors.append("domain mutation")
        if cut.get("production_source_mutation_count")!=0:errors.append("production source mutation")
        if not acc.get("passed"):errors.append("acceptance not passed")
        if hand.get("runtime_authority_created") or hand.get("live_order_authority_created") or hand.get("capital_authority_created"):errors.append("authority created")
        count=len(list((root/"canonical_visualizers").glob("*.json")))
        if count!=128:errors.append("per-visualizer artifact count mismatch")
        return {"result":"PASS" if not errors else "FAIL","missing":missing,"errors":errors,"visualizer_count":count,"eligible_count":cut.get("reference_cutover_count"),"blocked_count":cut.get("blocked_count")}

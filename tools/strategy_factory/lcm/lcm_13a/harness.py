from __future__ import annotations
from typing import Any
from .adapters import CanonicalReplayAdapter, LegacyReplayAdapter, SideEffectFence
from .canonical import digest_object, stable_id
from .compare import DualRunComparator

class DualRunHarness:
    def __init__(self) -> None:
        self.legacy = LegacyReplayAdapter()
        self.canonical = CanonicalReplayAdapter()
        self.comparator = DualRunComparator()
        self.fence = SideEffectFence()

    def run(self, consumer: dict[str, Any], scenario: dict[str, Any]) -> tuple[dict, list[dict]]:
        event = scenario["causal_input"]
        input_digest = scenario["causal_input_digest"]
        legacy_output = self.legacy.execute(consumer, event)
        canonical_output = self.canonical.execute(consumer, event)
        dimensions = self.comparator.compare(
            input_digest=input_digest,
            legacy=legacy_output,
            canonical=canonical_output,
            domain=consumer["domain"],
        )
        mismatches: list[dict] = []
        for comparison in dimensions:
            if comparison["status"] not in {"MISMATCH", "BLOCKED_NOT_COMPARABLE"}:
                continue
            severity = "HIGH" if comparison["dimension"] != "VISUAL_ANCHOR" else "MEDIUM"
            reason = consumer["blocker_reasons"][0] if consumer["blocker_reasons"] else "UNCLASSIFIED_MISMATCH"
            mismatch = {
                "mismatch_id": stable_id("MISMATCH", scenario["scenario_id"], comparison["dimension"], reason),
                "raw_observation_id": stable_id("RAWOBS", scenario["scenario_id"], comparison["dimension"]),
                "consumer_id": consumer["consumer_id"],
                "scenario_id": scenario["scenario_id"],
                "domain": consumer["domain"],
                "scenario_kind": scenario["scenario_kind"],
                "dimension": comparison["dimension"],
                "severity": severity,
                "legacy_value": comparison["legacy_value"],
                "canonical_value": comparison["canonical_value"],
                "reason_code": reason,
                "classification": "UPSTREAM_BLOCKER",
                "adjudication_state": "BLOCKING",
                "status": "OPEN_BLOCKING",
                "owner": consumer["owner"],
                "reviewer": consumer["reviewer"],
                "approved_variance_id": None,
                "aggregation_rule_id": None,
                "repeated_mismatch_retained": True,
                "source_digests": [consumer["source_digest"], scenario["scenario_digest"]],
            }
            mismatch["mismatch_digest"] = digest_object(mismatch, "mismatch_digest")
            mismatches.append(mismatch)
        result = {
            "result_id": stable_id("DUALRESULT", scenario["scenario_id"]),
            "consumer_id": consumer["consumer_id"],
            "scenario_id": scenario["scenario_id"],
            "scenario_kind": scenario["scenario_kind"],
            "causal_input_digest": input_digest,
            "legacy_input_digest": input_digest,
            "canonical_input_digest": input_digest,
            "input_equality": True,
            "legacy_output": legacy_output,
            "canonical_output": canonical_output,
            "legacy_output_digest": digest_object(legacy_output),
            "canonical_output_digest": digest_object(canonical_output),
            "dimension_results": dimensions,
            "hard_mismatch_count": len(mismatches),
            "soft_mismatch_count": 0,
            "side_effect_fence": self.fence.receipt(),
            "status": "PASS" if not mismatches else "BLOCKED",
            "source_digests": [consumer["source_digest"], scenario["scenario_digest"]],
        }
        result["result_digest"] = digest_object(result, "result_digest")
        return result, mismatches

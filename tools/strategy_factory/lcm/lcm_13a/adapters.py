from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class SideEffectFence:
    broker_submission_enabled: bool = False
    paper_submission_enabled: bool = False
    live_order_enabled: bool = False
    capital_activation_enabled: bool = False

    def receipt(self) -> dict[str, Any]:
        return {
            "broker_submission_enabled": self.broker_submission_enabled,
            "paper_submission_enabled": self.paper_submission_enabled,
            "live_order_enabled": self.live_order_enabled,
            "capital_activation_enabled": self.capital_activation_enabled,
            "submission_attempt_count": 0,
            "paper_order_count": 0,
            "live_order_count": 0,
            "capital_activation_count": 0,
        }

class LegacyReplayAdapter:
    def execute(self, consumer: dict, event: dict) -> dict:
        return {
            "availability": "AVAILABLE",
            "known_time": event["known_time"],
            "state": "REFERENCE_READY" if consumer["readiness_state"] == "TECHNICALLY_ELIGIBLE" else "LEGACY_ACTIVE_BLOCKED_CANONICAL",
            "event": "DUAL_RUN_OBSERVATION",
            "decision": "REFERENCE_PARITY_PASS" if consumer["readiness_state"] == "TECHNICALLY_ELIGIBLE" else "REMAIN_ON_LEGACY",
            "request": "NO_EXTERNAL_SIDE_EFFECT",
            "visual_anchor": consumer.get("visual_anchor"),
            "reason_codes": ["PARITY_PASS"] if consumer["readiness_state"] == "TECHNICALLY_ELIGIBLE" else list(consumer["blocker_reasons"]),
            "resolved_locator": consumer["canonical_locator"] or consumer["legacy_locator"],
            "side_effect_authority": False,
        }

class CanonicalReplayAdapter:
    def execute(self, consumer: dict, event: dict) -> dict:
        if consumer["readiness_state"] != "TECHNICALLY_ELIGIBLE":
            return {
                "availability": "BLOCKED",
                "known_time": None,
                "state": "CANONICAL_PATH_BLOCKED",
                "event": None,
                "decision": "BLOCKED",
                "request": None,
                "visual_anchor": None,
                "reason_codes": list(consumer["blocker_reasons"]),
                "resolved_locator": consumer.get("canonical_locator"),
                "side_effect_authority": False,
            }
        return {
            "availability": "AVAILABLE",
            "known_time": event["known_time"],
            "state": "REFERENCE_READY",
            "event": "DUAL_RUN_OBSERVATION",
            "decision": "REFERENCE_PARITY_PASS",
            "request": "NO_EXTERNAL_SIDE_EFFECT",
            "visual_anchor": consumer.get("visual_anchor"),
            "reason_codes": ["PARITY_PASS"],
            "resolved_locator": consumer["canonical_locator"],
            "side_effect_authority": False,
        }

from __future__ import annotations
from collections import defaultdict
from typing import Iterable

from .canonical import digest_object, stable_id
from .constants import BLAST_RADIUS, DOMAIN_ORDER, ROLLBACK_TRIGGERS, WAVE_SIZE_LIMITS


def dependency_family(consumer: dict) -> str:
    locator = str(consumer.get("legacy_locator") or "").split("::", 1)[0].replace("\\", "/")
    parts = [part for part in locator.split("/") if part]
    if len(parts) <= 1:
        base = "ROOT_FILES"
    elif parts[0] in {"mql5", "lab", "docs", "tools", "registry", "research", "product_lab"}:
        depth = 3 if len(parts) >= 3 else len(parts)
        base = "/".join(parts[:depth])
    else:
        base = parts[0]
    return f"{consumer['domain']}::{base}"


class ConsumerWavePlanner:
    def plan(self, consumers: Iterable[dict], common: dict) -> list[dict]:
        by_domain_family: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
        for consumer in consumers:
            by_domain_family[consumer["domain"]][dependency_family(consumer)].append(consumer)

        plans: list[dict] = []
        wave_sequence = 0
        for domain in DOMAIN_ORDER:
            families = by_domain_family.get(domain, {})
            limit = WAVE_SIZE_LIMITS[domain]
            current: list[dict] = []
            current_families: list[str] = []

            def flush() -> None:
                nonlocal wave_sequence, current, current_families
                if not current:
                    return
                wave_sequence += 1
                consumer_ids = sorted(item["consumer_id"] for item in current)
                wave_id = stable_id("CUTOVERWAVE", domain, wave_sequence, *consumer_ids)
                record = {
                    **common,
                    "wave_id": wave_id,
                    "wave_sequence": wave_sequence,
                    "domain": domain,
                    "blast_radius": BLAST_RADIUS[domain],
                    "consumer_count": len(consumer_ids),
                    "consumer_ids": consumer_ids,
                    "dependency_families": sorted(set(current_families)),
                    "max_consumer_count": limit,
                    "switch_mechanism": "REFERENCE_LOCATOR_BINDING_CANONICAL_PRIMARY_LEGACY_FALLBACK",
                    "observation_window": "THREE_BOUND_DUAL_RUN_SCENARIOS_PLUS_POST_SWITCH_RESOLUTION_CHECK",
                    "preconditions": [
                        "UPSTREAM_HANDOFF_DIGEST_MATCH",
                        "ELIGIBILITY_STATE_APPROVED",
                        "REFERENCE_OWNER_APPROVAL_PRESENT",
                        "ROLLBACK_PACKAGE_PREVERIFIED",
                        "FRESH_IMMUTABLE_DUAL_RUN_EVIDENCE",
                        "CANONICAL_TARGET_EXISTS",
                        "WORKING_TREE_EXACT_OR_RECORDED",
                    ],
                    "health_signals": [
                        "CANONICAL_RESOLUTION_PASS",
                        "LEGACY_FALLBACK_RETAINED",
                        "ZERO_POST_SWITCH_HIGH_CRITICAL_MISMATCH",
                        "ZERO_SIDE_EFFECT_FENCE_BREACH",
                    ],
                    "rollback_triggers": list(ROLLBACK_TRIGGERS),
                    "partial_wave_allowed": False,
                    "source_deletion_authorized": False,
                    "runtime_authority": False,
                    "live_order_authority": False,
                    "capital_authority": False,
                }
                record["wave_plan_digest"] = digest_object(record, "wave_plan_digest")
                plans.append(record)
                current = []
                current_families = []

            for family in sorted(families):
                family_consumers = sorted(families[family], key=lambda item: item["consumer_id"])
                while family_consumers:
                    available = limit - len(current)
                    if available == 0:
                        flush()
                        available = limit
                    take = min(available, len(family_consumers))
                    current.extend(family_consumers[:take])
                    current_families.append(family)
                    family_consumers = family_consumers[take:]
                    if len(current) == limit:
                        flush()
            flush()
        return plans

from __future__ import annotations

from .canonical import digest_object
from .errors import PolicyError
from .registries import ADAPTER_TYPES

DENIED = (
    "source_mutation_allowed",
    "semantic_expansion_allowed",
    "execution_authority",
    "runtime_authority",
    "live_order_authority",
    "capital_authority",
)


def build(adapter_id, adapter_type, source_identity_id, target_identity_id):
    if adapter_type not in ADAPTER_TYPES:
        raise PolicyError("unknown adapter type")
    if not all(isinstance(value, str) and value for value in (adapter_id, source_identity_id, target_identity_id)):
        raise PolicyError("adapter identities must be non-empty")
    out = {
        "schema_version": "1.0.0",
        "phase_id": "LCM-06",
        "claim_ceiling": "MIGRATION_FRAMEWORK_REFERENCE_ONLY",
        "adapter_id": adapter_id,
        "adapter_type": adapter_type,
        "source_identity_id": source_identity_id,
        "target_identity_id": target_identity_id,
        "input_contract": "LEGACY_OBSERVATION",
        "output_contract": "CANONICAL_OBSERVATION",
        "known_time_preserved": True,
        "reason_codes_preserved": True,
        "state_order_preserved": True,
        **{key: False for key in DENIED},
        "adapter_digest": None,
    }
    out["adapter_digest"] = digest_object(out, "adapter_digest")
    return out


def verify(adapter):
    if adapter.get("schema_version") != "1.0.0" or adapter.get("phase_id") != "LCM-06":
        raise PolicyError("adapter phase binding invalid")
    if adapter.get("claim_ceiling") != "MIGRATION_FRAMEWORK_REFERENCE_ONLY":
        raise PolicyError("adapter claim ceiling invalid")
    if adapter.get("adapter_type") not in ADAPTER_TYPES:
        raise PolicyError("unknown adapter type")
    for key in DENIED:
        if adapter.get(key) is not False:
            raise PolicyError(f"adapter authority escalation: {key}")
    for key in ("known_time_preserved", "reason_codes_preserved", "state_order_preserved"):
        if adapter.get(key) is not True:
            raise PolicyError(f"adapter preservation declaration missing: {key}")
    if adapter.get("input_contract") != "LEGACY_OBSERVATION" or adapter.get("output_contract") != "CANONICAL_OBSERVATION":
        raise PolicyError("adapter contract binding invalid")
    if digest_object(adapter, "adapter_digest") != adapter.get("adapter_digest"):
        raise PolicyError("adapter digest invalid")
    return True

from datetime import datetime, timedelta, timezone

from .canonical import content_id, digest_object
from .errors import PolicyError

ACTION = "LCM06_BUILD_MIGRATION_FRAMEWORK"
DENIAL_FIELDS = (
    "source_move_allowed",
    "source_delete_allowed",
    "target_materialization_allowed",
    "semantic_refactor_allowed",
    "merge_allowed",
    "cutover_allowed",
    "runtime_authority",
    "live_order_authority",
    "capital_authority",
)


def _parse_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise PolicyError("invalid permit timestamp") from exc
    if parsed.tzinfo is None:
        raise PolicyError("naive permit timestamp forbidden")
    return parsed.astimezone(timezone.utc)


def build_permit(handoff_digest, topology_run_id, issued_at):
    issued = _parse_timestamp(issued_at)
    expires = (issued + timedelta(days=7)).isoformat().replace("+00:00", "Z")
    obj = {
        "schema_version": "1.0.0",
        "phase_id": "LCM-06",
        "action": ACTION,
        "permit_id": content_id("PERMIT", [handoff_digest, topology_run_id, issued_at]),
        "source_handoff_digest": handoff_digest,
        "topology_run_id": topology_run_id,
        "issuer": "ALPHA_LAB_MIGRATION_CONTROL_PLANE",
        "issued_at": issued_at,
        "expires_at": expires,
        **{key: False for key in DENIAL_FIELDS},
        "permit_digest": None,
    }
    obj["permit_digest"] = digest_object(obj, "permit_digest")
    return obj


def verify_permit(permit, expected_handoff, expected_topology_run_id=None):
    if permit.get("schema_version") != "1.0.0" or permit.get("phase_id") != "LCM-06":
        raise PolicyError("permit phase binding invalid")
    if permit.get("action") != ACTION or permit.get("source_handoff_digest") != expected_handoff:
        raise PolicyError("permit source binding invalid")
    if expected_topology_run_id is not None and permit.get("topology_run_id") != expected_topology_run_id:
        raise PolicyError("permit topology binding invalid")
    issued = _parse_timestamp(permit.get("issued_at"))
    expires = _parse_timestamp(permit.get("expires_at"))
    if expires <= issued:
        raise PolicyError("permit expiry invalid")
    expected_id = content_id("PERMIT", [permit.get("source_handoff_digest"), permit.get("topology_run_id"), permit.get("issued_at")])
    if permit.get("permit_id") != expected_id:
        raise PolicyError("permit identity invalid")
    for key in DENIAL_FIELDS:
        if permit.get(key) is not False:
            raise PolicyError(f"authority escalation: {key}")
    if digest_object(permit, "permit_digest") != permit.get("permit_digest"):
        raise PolicyError("permit digest invalid")
    return True

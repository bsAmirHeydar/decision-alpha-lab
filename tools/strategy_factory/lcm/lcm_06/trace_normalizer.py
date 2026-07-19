from __future__ import annotations

from datetime import datetime, timezone

from .canonical import digest_object
from .errors import PolicyError
from .registries import HARD_DIMENSIONS, SOFT_DIMENSIONS


def _time(value):
    if value in (None, ""):
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError as exc:
        raise PolicyError(f"invalid trace timestamp: {value}") from exc
    if dt.tzinfo is None:
        raise PolicyError(f"naive trace timestamp forbidden: {value}")
    return dt.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def normalize_event(event):
    if not isinstance(event, dict):
        raise PolicyError("trace event must be an object")
    out = {key: event.get(key) for key in HARD_DIMENSIONS + SOFT_DIMENSIONS}
    missing_keys = {key for key in HARD_DIMENSIONS if key not in event}
    for key in ("event_time", "available_at", "expiry", "drawing_anchor_time"):
        if out.get(key) is not None:
            out[key] = _time(out[key])
    if isinstance(out.get("reason_codes"), list):
        out["reason_codes"] = sorted(set(out["reason_codes"]))
    if isinstance(out.get("drawing_anchor_price"), float):
        out["drawing_anchor_price"] = round(out["drawing_anchor_price"], 10)
    out["missing_hard_dimensions"] = sorted(missing_keys)
    out["normalized_event_digest"] = digest_object(out)
    return out


def normalize_trace(trace):
    if not isinstance(trace, dict):
        raise PolicyError("trace must be an object")
    events_value = trace.get("events")
    if not isinstance(events_value, list):
        raise PolicyError("trace events must be a list")
    events = [normalize_event(item) for item in events_value]
    out = {
        "schema_version": "1.0.0",
        "trace_id": trace.get("trace_id"),
        "events": events,
        "event_count": len(events),
        "trace_digest": None,
    }
    out["trace_digest"] = digest_object(out, "trace_digest")
    return out

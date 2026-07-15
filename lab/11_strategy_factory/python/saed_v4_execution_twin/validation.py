from __future__ import annotations
from .authority import OUTPUT_AUTHORITY
from .canonical import content_hash
from .errors import AuthorityError, IntegrityError


def validate_twin(twin: dict) -> None:
    if twin.get("phase") != "SAED_V4_09" or twin.get("authority") != OUTPUT_AUTHORITY:
        raise AuthorityError("execution twin authority or phase mismatch")
    if twin.get("shadow_replacement") is not False or twin["authority"].get("send_order") is not False:
        raise AuthorityError("shadow replacement or order authority is prohibited")
    if not twin.get("complete_exposure") or not twin.get("exposure_ledger", {}).get("complete"):
        raise IntegrityError("incomplete execution twin exposure")
    if twin.get("twin_row_count") != len(twin.get("rows", [])):
        raise IntegrityError("twin row count mismatch")
    for row in twin["rows"]:
        expected = content_hash({k: v for k, v in row.items() if k != "twin_row_hash"})
        if row.get("twin_row_hash") != expected:
            raise IntegrityError("twin row hash mismatch")
        if row["incremental_execution_cost_points"] < 0 or row["incremental_execution_cost_r"] < 0:
            raise IntegrityError("negative incremental execution cost")

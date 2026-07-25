from __future__ import annotations
from pathlib import Path
from .admission import build_wave_receipts
from .canonical import content_id
from .closure import build_closure
from .packet import build_packet
from .registries import build_registries
from .upstream import load_upstream, PORTFOLIO_ID

def build_reference_closure(repo_root: Path) -> dict:
    upstream = load_upstream(repo_root)
    seed = {"phase_id":"LCM-08C","portfolio_id":PORTFOLIO_ID,"pilot_migration_id":"PILOTMIG_344455420C8CA68E865FD54135E891D7","lcm08b_handoff_digest":upstream["handoff"]["handoff_digest"],"portfolio_summary_digest":upstream["summary"]["summary_digest"],"wave_assignment_digest":upstream["wave_assignment"]["assignment_digest"]}
    closure_id = content_id("CTXWAVECLOSE", seed)
    packets = [build_packet(row, closure_id, upstream["handoff"]) for row in sorted(upstream["portfolio_rows"], key=lambda x:x["identity_id"])]
    registries = build_registries(packets, upstream["handoff"])
    wave_receipts = build_wave_receipts(packets, closure_id)
    closure_report = build_closure(packets, registries, wave_receipts, closure_id, PORTFOLIO_ID)
    return {"closure_id":closure_id,"packets":packets,"registries":registries,"wave_receipts":wave_receipts,"closure_report":closure_report}

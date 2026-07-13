from __future__ import annotations
from dataclasses import dataclass,asdict
from .canonical import canonical_sha256
@dataclass(frozen=True,slots=True)
class PortfolioTelemetry:
    telemetry_id:str;as_of_ms:int;queue_count:int;eligible_count:int;selected_count:int;reserved_risk:float;capacity_utilization:float;context_count:int;fallback_dependence_count:int;drift_flags:tuple[str,...];emergency_derisk:bool
    @property
    def telemetry_hash(self):return canonical_sha256(asdict(self))
def build_telemetry(telemetry_id,as_of_ms,ranked,plan,ledger,model,drift_flags=()):
    eligible=sum(x.status.value=='eligible' for x in ranked);fallback=sum(e.source.value=='fallback' for e in model.edges)
    utilization=ledger.total()/max(plan.gross_exposure,1e-12) if plan.gross_exposure else 0.0
    emergency=bool(drift_flags) or not all(plan.checks.values())
    return PortfolioTelemetry(telemetry_id,as_of_ms,len(ranked),eligible,len(plan.selected),ledger.total(),utilization,plan.context_count,fallback,tuple(sorted(set(drift_flags))),emergency)

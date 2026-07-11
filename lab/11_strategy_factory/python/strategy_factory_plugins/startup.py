from dataclasses import dataclass
from .enums import RequirementKind,RequirementStrength
@dataclass(frozen=True,slots=True)
class StartupValidationReport: ready:bool;requirement_count:int;prepared_count:int;optional_failures:int;required_failures:int;requirements_hash:str;details:tuple[str,...]
def validate_requirements(requirements,probe):
    prepared=optional=required=0;details=[]
    for r in requirements.items:
        try:
            probe.ensure_symbol(r.symbol)
            if r.kind is RequirementKind.TICK: probe.refresh_tick(r.symbol)
            elif r.kind is RequirementKind.SYMBOL_SPEC: probe.refresh_symbol_spec(r.symbol)
            else:
                if probe.refresh_closed_bars(r.symbol,r.timeframe_seconds,r.lookback_bars)<=0: raise RuntimeError("no bars")
                if r.max_staleness_msc and probe.now_utc_msc()-probe.latest_closed_bar_time_msc(r.symbol,r.timeframe_seconds)>r.max_staleness_msc: raise RuntimeError("stale bars")
            prepared+=1
        except Exception as exc:
            details.append(f"{r.requirement_id}: {exc}")
            if r.strength is RequirementStrength.REQUIRED: required+=1
            else: optional+=1
    return StartupValidationReport(required==0,len(requirements.items),prepared,optional,required,requirements.requirements_hash,tuple(details))

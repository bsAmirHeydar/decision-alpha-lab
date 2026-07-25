from .contracts import *
from .canonical import *

def size_fixed_risk(geometry:RiskGeometry,spec:SymbolSpec,risk:RiskConfig)->SizingResult:
    reasons=[]
    if geometry.status!=GeometryStatus.READY: reasons.append("FP_PAPER_GEOMETRY_NOT_READY")
    ticks=geometry.stop_distance/spec.tick_size if spec.tick_size>0 else 0
    loss_per_lot=ticks*spec.tick_value_loss_per_lot+risk.round_trip_cost_per_lot
    if loss_per_lot<=0: reasons.append("FP_PAPER_LOSS_PER_LOT_NONPOSITIVE")
    raw=risk.fixed_risk_amount/loss_per_lot if loss_per_lot>0 else 0.0
    vol=floor_step(min(raw,spec.volume_max),spec.volume_step) if raw>0 else 0.0
    if vol+1e-12<spec.volume_min: reasons.append("FP_PAPER_MIN_VOLUME_EXCEEDS_RISK_CAP")
    if vol>spec.volume_max+1e-12: reasons.append("FP_PAPER_MAX_VOLUME_EXCEEDED")
    estimated=vol*loss_per_lot
    if estimated>risk.fixed_risk_amount+risk.risk_tolerance: reasons.append("FP_PAPER_RISK_CAP_EXCEEDED")
    status=GeometryStatus.READY if not reasons else GeometryStatus.BLOCKED
    payload={"geometry":geometry.geometry_hash,"spec":spec,"risk":risk.config_hash,"loss_per_lot":loss_per_lot,"raw":raw,"volume":vol,"estimated":estimated,"reasons":sorted(reasons)}
    return SizingResult(stable_id("FPSIZE",payload),status,risk.fixed_risk_amount,loss_per_lot,raw,vol,estimated,(estimated/risk.fixed_risk_amount if risk.fixed_risk_amount else 0.0),tuple(sorted(reasons)),sha256(payload))

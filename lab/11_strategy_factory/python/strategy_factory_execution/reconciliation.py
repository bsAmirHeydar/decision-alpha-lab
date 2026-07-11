from __future__ import annotations
from .models import *
from .enums import *
from .hashing import stable_id, cfloat


def reconcile_positions(expected: list[PositionRecord], observed: list[ObservedPosition], now_utc_msc: int,
                        *, volume_tolerance: float = 1e-9, price_tolerance: float = 1e-6) -> ReconciliationReport:
    exp={(x.symbol,x.direction):x for x in expected if x.state == PositionState.OPEN}
    obs={(x.symbol,x.direction):x for x in observed}
    items=[]
    for key in sorted(set(exp)|set(obs)):
        e=exp.get(key); o=obs.get(key)
        if e is None:
            status=ReconciliationStatus.UNEXPECTED_OBSERVED; msg="observed position has no paper counterpart"
        elif o is None:
            status=ReconciliationStatus.MISSING_EXPECTED; msg="paper position missing from observed snapshot"
        elif abs(e.volume-o.volume)>volume_tolerance:
            status=ReconciliationStatus.VOLUME_MISMATCH; msg="position volume differs"
        elif abs(e.average_entry_price-o.average_price)>price_tolerance:
            status=ReconciliationStatus.PRICE_DRIFT; msg="average entry price differs"
        else:
            status=ReconciliationStatus.MATCHED; msg="position matched"
        items.append(ReconciliationItem(f"{key[0]}:{key[1]}",status,e.position_id if e else "",
            o.external_position_id if o else "",e.volume if e else 0.0,o.volume if o else 0.0,
            e.average_entry_price if e else 0.0,o.average_price if o else 0.0,msg))
    canonical="|".join(f"{x.key}:{int(x.status)}:{cfloat(x.expected_volume)}:{cfloat(x.observed_volume)}" for x in items)
    rh=stable_id("xrec",f"{now_utc_msc}|{canonical}")
    matched=sum(x.status==ReconciliationStatus.MATCHED for x in items)
    return ReconciliationReport(rh,now_utc_msc,matched,len(items)-matched,tuple(items),rh)

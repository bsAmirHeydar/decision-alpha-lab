from __future__ import annotations
from .models import ShadowComparison
from .hashing import stable_id, cfloat


def compare_shadow_execution(*, intent_id: str, paper_order_id: str, observed_external_order_id: str,
        paper_fill_price: float, observed_fill_price: float, paper_fill_time_utc_msc: int,
        observed_fill_time_utc_msc: int, paper_volume: float, observed_volume: float,
        price_tolerance: float, latency_tolerance_milliseconds: int, volume_tolerance: float) -> ShadowComparison:
    price_delta=observed_fill_price-paper_fill_price
    latency_delta=observed_fill_time_utc_msc-paper_fill_time_utc_msc
    volume_delta=observed_volume-paper_volume
    matched=(abs(price_delta)<=price_tolerance and abs(latency_delta)<=latency_tolerance_milliseconds
             and abs(volume_delta)<=volume_tolerance)
    canonical="|".join((intent_id,paper_order_id,observed_external_order_id,cfloat(paper_fill_price),
        cfloat(observed_fill_price),str(paper_fill_time_utc_msc),str(observed_fill_time_utc_msc),
        cfloat(price_delta),str(latency_delta),cfloat(volume_delta),"1" if matched else "0"))
    cid=stable_id("xshd",canonical)
    return ShadowComparison(cid,intent_id,paper_order_id,observed_external_order_id,paper_fill_price,
        observed_fill_price,paper_fill_time_utc_msc,observed_fill_time_utc_msc,price_delta,
        latency_delta,volume_delta,matched,cid)

from __future__ import annotations
from .contracts import M1Bar, SymbolSpec
from .enums import BarFinality, SourceQuality
from .errors import FPI04Error

def validate_bar(bar:M1Bar,spec:SymbolSpec,closed_only:bool=True)->SourceQuality:
    if bar.canonical_symbol!=spec.canonical_symbol: raise FPI04Error('FP_DRC_BAR_SYMBOL_MISMATCH','bar symbol differs from spec')
    if closed_only and bar.finality is not BarFinality.CLOSED: raise FPI04Error('FP_DRC_PROVISIONAL_BAR_FORBIDDEN','only closed M1 bars are canonical')
    prices=(bar.open,bar.high,bar.low,bar.close)
    for value in prices:
        units=value/spec.tick_size
        if abs(units-round(units))>1e-7: raise FPI04Error('FP_DRC_PRICE_OFF_TICK_GRID','price is off tick grid',{'value':value,'tick_size':spec.tick_size})
    if bar.tick_volume==0 and bar.real_volume==0:return SourceQuality.SUSPECT
    return SourceQuality.CANONICAL

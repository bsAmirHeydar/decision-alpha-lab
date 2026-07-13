from __future__ import annotations
from collections import defaultdict
from .canonical import canonical_sha256
from .contracts import DuplicateResolution,M1Bar,SymbolPairSpec
from .enums import DuplicateDisposition
from .errors import FPI04Error
from .bar_validation import validate_bar

def normalize_bars(pair:SymbolPairSpec,bars:list[M1Bar]|tuple[M1Bar,...],closed_only:bool=True)->tuple[tuple[M1Bar,...],tuple[DuplicateResolution,...]]:
    specs={pair.left.canonical_symbol:pair.left,pair.right.canonical_symbol:pair.right}
    grouped=defaultdict(list)
    for bar in bars:
        if bar.canonical_symbol not in specs: raise FPI04Error('FP_DRC_BAR_OUTSIDE_PAIR','bar symbol outside pair')
        validate_bar(bar,specs[bar.canonical_symbol],closed_only)
        grouped[(bar.canonical_symbol,bar.open_utc_ms)].append(bar)
    selected=[]; resolutions=[]
    for (symbol,minute),items in sorted(grouped.items()):
        hashes=tuple(sorted({b.bar_hash for b in items}))
        if len(hashes)==1:
            chosen=sorted(items,key=lambda b:(b.source_sequence,b.received_utc_ms,b.source_id))[-1]
            disposition=DuplicateDisposition.UNIQUE if len(items)==1 else DuplicateDisposition.IDENTICAL_DEDUPLICATED
            reason='FP_DRC_BAR_UNIQUE' if len(items)==1 else 'FP_DRC_DUPLICATE_IDENTICAL_DEDUPLICATED'
            selected.append(chosen)
        else:
            chosen=None; disposition=DuplicateDisposition.CONFLICT; reason='FP_DRC_DUPLICATE_CONFLICT'
        material={'symbol':symbol,'minute':minute,'disposition':disposition,'input_hashes':hashes,'selected':chosen.bar_hash if chosen else ''}
        resolutions.append(DuplicateResolution(symbol,minute,disposition,chosen,hashes,reason,canonical_sha256(material)))
    return tuple(sorted(selected,key=lambda b:(b.open_utc_ms,b.canonical_symbol))),tuple(resolutions)

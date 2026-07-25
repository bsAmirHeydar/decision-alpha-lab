from __future__ import annotations
from .contracts import SymbolPairSpec, SymbolSpec
from .errors import FPI04Error

class SymbolResolver:
    def __init__(self,pair:SymbolPairSpec):
        self.pair=pair
        self._map={}
        for spec in (pair.left,pair.right):
            for alias in (spec.canonical_symbol,*spec.aliases):
                key=alias.upper()
                if key in self._map and self._map[key]!=spec.canonical_symbol:
                    raise FPI04Error('FP_DRC_ALIAS_COLLISION','alias maps to multiple symbols',{'alias':alias})
                self._map[key]=spec.canonical_symbol
    def resolve(self,raw_symbol:str)->str:
        key=(raw_symbol or '').strip().upper()
        if key not in self._map: raise FPI04Error('FP_DRC_SYMBOL_UNRESOLVED','symbol alias not registered',{'symbol':raw_symbol})
        return self._map[key]
    def spec(self,raw_symbol:str)->SymbolSpec:
        canonical=self.resolve(raw_symbol)
        return self.pair.left if canonical==self.pair.left.canonical_symbol else self.pair.right

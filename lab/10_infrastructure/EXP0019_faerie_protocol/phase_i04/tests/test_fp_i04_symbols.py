import pytest
from fp_i04_data.contracts import SymbolPairSpec,SymbolSpec
from fp_i04_data.errors import FPI04Error
from fp_i04_data.golden import golden_pair
from fp_i04_data.symbol_resolver import SymbolResolver

def test_aliases_resolve_case_insensitively():
    r=SymbolResolver(golden_pair())
    assert r.resolve('us500')=='ES' and r.resolve('USTEC')=='NQ'

def test_unknown_alias_is_blocked():
    with pytest.raises(FPI04Error,match='not registered'):SymbolResolver(golden_pair()).resolve('YM')

def test_alias_collision_is_blocked():
    pair=SymbolPairSpec('FP-CONTEXT-001','FP-PAIR-X',SymbolSpec('ES',('X',),0.25,2),SymbolSpec('NQ',('x',),0.25,2))
    with pytest.raises(FPI04Error,match='multiple symbols'):SymbolResolver(pair)

def test_resolver_returns_matching_spec():
    assert SymbolResolver(golden_pair()).spec('US500').canonical_symbol=='ES'

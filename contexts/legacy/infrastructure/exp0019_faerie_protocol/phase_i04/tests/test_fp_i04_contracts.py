import pytest
from fp_i04_data.contracts import *
from fp_i04_data.enums import *
from fp_i04_data.errors import FPI04Error
from fp_i04_data.golden import golden_pair,bar

def test_symbol_spec_hash_is_deterministic():
    assert golden_pair().left.spec_hash==golden_pair().left.spec_hash

def test_pair_rejects_same_symbols():
    s=SymbolSpec('ES',('ES',),0.25,2)
    with pytest.raises(FPI04Error,match='pair symbols'):
        SymbolPairSpec('FP-CONTEXT-001','FP-PAIR-X',s,s)

def test_bar_requires_minute_alignment():
    with pytest.raises(FPI04Error,match='minute open'):
        bar('ES',60_001,5000)

def test_bar_rejects_invalid_envelope():
    with pytest.raises(FPI04Error,match='OHLC envelope'):
        M1Bar('ES',60_000,10,9,8,10,1,0,1,BarFinality.CLOSED,'S',1,'R',120_000)

def test_coverage_reconciles_calendar_exclusions():
    c=CoverageInterval('ES',0,300_000,3,3,2,CoverageState.COMPLETE,'0'*64,'OK')
    assert c.coverage_ratio==1.0

def test_minute_cell_state_controls_bar_presence():
    b=bar('ES',60_000,5000)
    with pytest.raises(FPI04Error): MinuteCell('ES',60_000,MinuteCellState.MISSING,b,'X','0'*64)

def test_alignment_rejects_cell_time_mismatch():
    b=bar('ES',60_000,5000); l=MinuteCell('ES',60_000,MinuteCellState.PRESENT,b,'X','0'*64); r=MinuteCell('NQ',120_000,MinuteCellState.MISSING,None,'X','0'*64)
    with pytest.raises(FPI04Error):AlignedMinute('FP-PAIR-X',60_000,l,r,'A','0'*64)

def test_config_hash_changes_with_policy():
    a=SynchronizerConfig(calendar_config_hash='0'*64)
    b=SynchronizerConfig(expected_minute_policy=ExpectedMinutePolicy.ALL_REQUESTED_MINUTES,calendar_config_hash='0'*64)
    assert a.config_hash!=b.config_hash

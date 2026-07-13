from dataclasses import replace
import pytest
from fp_i04_data.enums import DuplicateDisposition
from fp_i04_data.errors import FPI04Error
from fp_i04_data.golden import bar,golden_pair
from fp_i04_data.normalization import normalize_bars

def test_unique_bar_is_selected():
    bars,res=normalize_bars(golden_pair(),(bar('ES',60_000,5000),))
    assert len(bars)==1 and res[0].disposition is DuplicateDisposition.UNIQUE

def test_identical_duplicates_are_deduplicated_deterministically():
    first=bar('ES',60_000,5000,1); second=replace(first,source_sequence=2,received_utc_ms=180_000)
    bars,res=normalize_bars(golden_pair(),(first,second))
    assert len(bars)==1 and bars[0].source_sequence==2 and res[0].disposition is DuplicateDisposition.IDENTICAL_DEDUPLICATED

def test_conflicting_duplicates_block_minute():
    first=bar('ES',60_000,5000,1); second=bar('ES',60_000,5001,2)
    bars,res=normalize_bars(golden_pair(),(first,second))
    assert not bars and res[0].disposition is DuplicateDisposition.CONFLICT

def test_bar_outside_pair_is_rejected():
    with pytest.raises(FPI04Error,match='outside pair'):normalize_bars(golden_pair(),(bar('YM',60_000,40000),))

def test_input_order_does_not_change_output():
    a=bar('ES',60_000,5000,1);b=bar('NQ',60_000,20000,2)
    assert normalize_bars(golden_pair(),(a,b))==normalize_bars(golden_pair(),(b,a))

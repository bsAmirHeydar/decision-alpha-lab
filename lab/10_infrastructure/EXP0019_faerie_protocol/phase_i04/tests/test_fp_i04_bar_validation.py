import pytest
from fp_i04_data.bar_validation import validate_bar
from fp_i04_data.enums import BarFinality,SourceQuality
from fp_i04_data.errors import FPI04Error
from fp_i04_data.golden import bar,golden_pair

def test_closed_tick_aligned_bar_is_canonical():
    assert validate_bar(bar('ES',60_000,5000),golden_pair().left) is SourceQuality.CANONICAL

def test_zero_volume_is_suspect_not_silently_complete():
    b=bar('ES',60_000,5000)
    b=type(b)(**{**{f:getattr(b,f) for f in b.__dataclass_fields__},'tick_volume':0})
    assert validate_bar(b,golden_pair().left) is SourceQuality.SUSPECT

def test_provisional_bar_is_forbidden_by_default():
    with pytest.raises(FPI04Error,match='closed M1'):validate_bar(bar('ES',60_000,5000,finality=BarFinality.PROVISIONAL),golden_pair().left)

def test_off_tick_grid_is_forbidden():
    b=bar('ES',60_000,5000.1)
    with pytest.raises(FPI04Error,match='tick grid'):validate_bar(b,golden_pair().left)

def test_wrong_symbol_spec_is_forbidden():
    with pytest.raises(FPI04Error,match='differs'):validate_bar(bar('ES',60_000,5000),golden_pair().right)

from strategy_factory_statistics.models import StatisticalReportManifest,MatchedNullSpec
from strategy_factory_statistics.enums import NullMethod
from strategy_factory_statistics.lineage import validate_report_lineage
import pytest

def manifest():
    return StatisticalReportManifest('r','p','1','run','mh','ah','st','1','cm','sp','cr','gs','mr','nr',17,100,'abc').with_hash()
def test_manifest_hash_and_lineage():
    m=manifest();m.validate();validate_report_lineage(m,'run','mh','ah')
def test_lineage_mismatch_rejected():
    with pytest.raises(ValueError):validate_report_lineage(manifest(),'bad','mh','ah')
def test_null_hash_deterministic():
    a=MatchedNullSpec('n','1',NullMethod.EXACT_STRATIFIED_CYCLIC,1,2,1,True,('x',)).with_hash()
    b=MatchedNullSpec('n','1',NullMethod.EXACT_STRATIFIED_CYCLIC,1,2,1,True,('x',)).with_hash()
    assert a.null_hash==b.null_hash

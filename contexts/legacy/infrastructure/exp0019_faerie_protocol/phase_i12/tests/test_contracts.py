from fp_i12_operator import *
import pytest
def test_snapshot_hash(snapshot):assert len(snapshot.computed_hash)==64
def test_config_hash(config):assert len(config.config_hash)==64
def test_invalid_relation():
 with pytest.raises(FPI12Error):OperatorItem('S','O','K','BAD',semantic_hash=sha256('x'))
def test_noncanonical_reasons():
 with pytest.raises(FPI12Error):OperatorItem('S','O','K',reason_codes=('B','A'),semantic_hash=sha256('x'))
def test_page_limit():
 with pytest.raises(FPI12Error):PanelConfig(page_size=0)

from decimal import Decimal as D
import pytest
from strategy_factory_dataset_v3.golden import golden_anchors
from strategy_factory_dataset_v3.contracts import PathObservation
from strategy_factory_dataset_v3.errors import ContractError,CausalityError

def test_anchor_identity_deterministic():
    a=golden_anchors(1)[0]; assert a.opportunity_id==golden_anchors(1)[0].opportunity_id; assert len(a.anchor_hash)==64

def test_anchor_source_causality():
    a=golden_anchors(1)[0]; assert all(s.available_time_ms<=a.known_time_ms for s in a.source_inventory)

def test_crossed_quote_rejected():
    with pytest.raises(ContractError): PathObservation(0,1,1,D('2'),D('1'))

def test_path_known_time_rejected():
    with pytest.raises(CausalityError): PathObservation(0,2,1,D('1'),D('1.1'))

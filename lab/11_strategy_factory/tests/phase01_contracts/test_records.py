import pytest
from strategy_factory_contracts import *
from strategy_factory_contracts.records import FeatureValue, FeatureSnapshot
from strategy_factory_contracts.validation import ContractValidationError

ET=MarketTimestamp(1783771200000,"America/New_York",-240,"broker",TimestampPrecision.MILLISECONDS)
KT=MarketTimestamp(1783771260000,"America/New_York",-240,"broker",TimestampPrecision.MILLISECONDS)
CT=MarketTimestamp(1783771320000,"America/New_York",-240,"broker",TimestampPrecision.MILLISECONDS)

def make_event(**changes):
    data=dict(event_id="",strategy_id="exp0017_temporal_divergence",strategy_version="1.0.0",
      producer_id="mql5.exp0017.adapter",producer_version="1.0.0",symbol="NQ",reference_symbol="ES",
      direction=Direction.LONG,event_time=ET,known_time=KT,confirmation_time=CT,
      reference_price=22500.25,invalidation_price=22480.0,timeframe_seconds=60,
      session_id="new_york_am",parent_event_id="none",market_event_cluster_id="cluster_20260711_001",
      source_hash="sha256_deadbeef",anatomy_state="confirmed")
    data.update(changes)
    return AnatomyEvent(**data)

def test_event_id_matches_mql_vector():
    assert make_event().derived_event_id == 'evt_cd79492563408d2b'

def test_future_known_time_rejected():
    with pytest.raises(ContractValidationError):
        make_event(known_time=MarketTimestamp(CT.utc_epoch_milliseconds+1))

def test_bar_geometry_rejected():
    with pytest.raises(ContractValidationError):
        BarRecord("NQ",60,ET,CT,100,99,95,98,1,1,98,99,1,"broker","bar1")

def test_feature_snapshot_duplicate_rejected():
    evt=make_event().with_derived_id()
    f=FeatureValue("x","1.0.0",FeatureType.DOUBLE,FeatureQuality.VALID,KT,evt.event_id,"hash",1.0)
    with pytest.raises(ContractValidationError):
        FeatureSnapshot("",evt.event_id,evt.strategy_id,CT,"p","1.0.0","hash",0,(f,f))

def test_snapshot_id_matches_mql_vector():
    evt=make_event().with_derived_id()
    f=FeatureValue("divergence_strength","1.0.0",FeatureType.DOUBLE,FeatureQuality.VALID,KT,evt.event_id,"sha256_feature",0.75)
    snap=FeatureSnapshot("",evt.event_id,evt.strategy_id,CT,"mql5.context.exp0017","1.0.0","sha256_context",7,(f,))
    assert snap.derived_snapshot_id == 'snap_a1483fb0aa370dc5'

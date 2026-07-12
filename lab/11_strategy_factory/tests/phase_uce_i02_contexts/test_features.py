from __future__ import annotations
import pytest
from dataclasses import replace
from strategy_factory_contexts_v3 import *
from strategy_factory_contexts_v3.fixtures import synthetic_records

def base():
    p=SyntheticBreakContextPackage(); o=p.observe(synthetic_records()[0])[0]; return p,o,p.build_feature_frame(o,{})

def test_frame_is_ordered_and_stable():
    p,o,f=base()
    assert [d.feature_id for d in f.descriptors]==sorted(d.feature_id for d in f.descriptors)
    assert f.frame_hash==p.build_feature_frame(o,{}).frame_hash
    assert f.frame_id==p.build_feature_frame(o,{}).frame_id

def test_missing_spread_is_explicit_not_zero():
    p=SyntheticBreakContextPackage(); src=dict(synthetic_records()[0]); src["spread_points"]=None
    o=p.observe(src)[0]; f=p.build_feature_frame(o,{})
    assert f.freshness("market.spread_points")==FreshnessState.MISSING
    value=next(v for v in f.values if v.feature_id=="market.spread_points")
    assert value.is_missing and value.value is None

def test_future_feature_rejected():
    p,o,f=base(); values=list(f.values)
    values[0]=replace(values[0],known_time=UtcInstant(f.observation_cut.epoch_ms+1))
    with pytest.raises(FeatureError): FeatureFrame(f.context_observation_id,f.context_package_id,f.context_package_version,f.observation_cut,f.descriptors,tuple(values))

def test_stale_reject_policy():
    p,o,f=base(); descriptors=list(f.descriptors); values=list(f.values)
    i=next(i for i,d in enumerate(descriptors) if d.feature_id=="break.distance_atr")
    values[i]=replace(values[i],known_time=UtcInstant(f.observation_cut.epoch_ms-1),source_time=UtcInstant(f.observation_cut.epoch_ms-1))
    with pytest.raises(FeatureError): FeatureFrame(f.context_observation_id,f.context_package_id,f.context_package_version,f.observation_cut,tuple(descriptors),tuple(values))

def test_descriptor_value_order_mismatch_rejected():
    p,o,f=base()
    with pytest.raises(FeatureError): FeatureFrame(f.context_observation_id,f.context_package_id,f.context_package_version,f.observation_cut,tuple(reversed(f.descriptors)),f.values)

def test_category_requires_domain():
    with pytest.raises(FeatureError): FeatureDescriptor("x","1.0.0","owner",FeatureDataType.CATEGORY,"unit",(),MissingnessPolicy.REJECT,StalenessPolicy.REJECT,0,(),AvailabilityMode.RESEARCH,True,())

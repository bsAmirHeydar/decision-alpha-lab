from copy import deepcopy
from strategy_factory_rthp_context_v1 import RTHPContextPackage, build_auxiliary_payload, validate_source_record
from strategy_factory_contexts_v3 import ContextPackageRegistry
from .helpers import records

def test_package_contract_counts_and_registry():
 p=RTHPContextPackage(); r=ContextPackageRegistry(); r.register(p)
 assert r.resolve(p.manifest.package_id,p.manifest.version) is p
 assert len(p.feature_descriptors())==31
 assert len(p.view_descriptors())==5
 assert len(p.cluster_rules())==4
 assert len(p.manifest.tasks)==30

def test_package_is_context_only():
 p=RTHPContextPackage(); text=str(p.manifest.material()).lower()
 for forbidden in ('order_send','position_size','stop_loss','take_profit','capital_activation'):
  assert forbidden not in text
 assert p.manifest.metadata['entry_treatment_execution']=='OUT_OF_SCOPE'

def test_source_records_validate_and_observe():
 p=RTHPContextPackage()
 for row in records():
  assert validate_source_record(row)==()
  obs=p.observe(row)
  assert len(obs)==1 and obs[0].time_chain.observation_cut.epoch_ms==row['observation_cut_ms']

def test_auxiliary_projection_is_exact_and_fail_closed():
 p=RTHPContextPackage(); row=records()[0]
 assert row['auxiliary']==build_auxiliary_payload(row)
 bad=deepcopy(row); bad['auxiliary']['graph']['nodes'].append('tampered')
 assert 'auxiliary_projection_mismatch' in validate_source_record(bad)
 assert p.observe(bad)==()

def test_invalid_unconfirmed_and_future_prefixed_inputs_are_rejected():
 p=RTHPContextPackage(); row=records()[0]
 a=deepcopy(row); a['confirmed_context_event']=False
 b=deepcopy(row); b['future_price']=1
 assert p.observe(a)==() and p.observe(b)==()

def test_polarity_level_side_contract_is_enforced():
 row=deepcopy(records()[0]); row['polarity']='BEARISH_DIVERGENCE'
 assert 'polarity_level_side_mismatch' in validate_source_record(row)

def test_deterministic_observation_and_feature_frame_identity():
 p=RTHPContextPackage(); row=records()[0]
 a=p.observe(row)[0]; b=p.observe(deepcopy(row))[0]
 fa=p.build_feature_frame(a,row); fb=p.build_feature_frame(b,deepcopy(row))
 assert a.observation_id==b.observation_id and a.observation_hash==b.observation_hash
 assert fa.frame_id==fb.frame_id and fa.frame_hash==fb.frame_hash

def test_future_only_suffix_does_not_change_past_outputs():
 p=RTHPContextPackage(); row=records()[0]; changed=deepcopy(row)
 changed['post_cut_diagnostics']={'future_path':'ignored'}
 a=p.observe(row)[0]; b=p.observe(changed)[0]
 assert a.observation_hash==b.observation_hash
 assert p.build_feature_frame(a,row).frame_hash==p.build_feature_frame(b,changed).frame_hash

def test_raw_symbol_identity_is_not_a_training_feature():
 p=RTHPContextPackage(); row=records()[0]; obs=p.observe(row)[0]; frame=p.build_feature_frame(obs,row)
 feature_ids={d.feature_id for d in frame.descriptors}
 assert not any('symbol' in x for x in feature_ids)
 values={v.value for v in frame.values if isinstance(v.value,str)}
 assert row['primary_symbol'] not in values and row['secondary_symbol'] not in values
 assert {'PRIMARY','SECONDARY'} & values

def test_optional_geometry_is_explicit_missing_not_imputed():
 p=RTHPContextPackage(); row=records()[1]; obs=p.observe(row)[0]; frame=p.build_feature_frame(obs,row)
 by_id={v.feature_id:v for v in frame.values}
 for fid in ('rthp.hunter_touch_overrun_ticks','rthp.protected_distance_to_level_ticks','rthp.reference_range_ticks','rthp.active_range_ticks'):
  if row.get(fid.split('rthp.',1)[1]) is None:
   assert by_id[fid].is_missing and by_id[fid].value is None

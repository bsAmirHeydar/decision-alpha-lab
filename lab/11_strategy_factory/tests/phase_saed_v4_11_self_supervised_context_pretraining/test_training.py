from saed_v4_self_supervised_pretraining.service import build_reference_bundle

def build(records,config,upstream,load):return build_reference_bundle(records,upstream[0],upstream[1],config,load('lab/11_strategy_factory/examples/saed_v4_11/reference_split_policy.json'),load('lab/11_strategy_factory/examples/saed_v4_11/membership_canaries.json')['tokens'])
def test_training_completes(records,config,upstream,load):
 b,_=build(records,config,upstream,load);assert b['training_receipt']['status']=='completed_reference_synthetic'
def test_exposure_complete(records,config,upstream,load):
 b,_=build(records,config,upstream,load);assert b['exposure']['complete'];assert b['exposure']['total_pairs']==b['training_receipt']['total_pairs']
def test_checkpoint_learned(records,config,upstream,load):
 b,_=build(records,config,upstream,load);assert b['checkpoint']['metadata']['training_receipt_hash']==b['training_receipt']['receipt_hash']
def test_full_bundle_deterministic(records,config,upstream,load):
 a,sa=build(records,config,upstream,load);b,sb=build(records,config,upstream,load);assert a['checkpoint']['checkpoint_hash']==b['checkpoint']['checkpoint_hash'];assert a['training_receipt']['receipt_hash']==b['training_receipt']['receipt_hash'];assert sa==sb
def test_no_runtime_authority(records,config,upstream,load):
 b,_=build(records,config,upstream,load);assert not b['checkpoint']['runtime_authority'] and not b['checkpoint']['execution_authority']

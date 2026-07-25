from .canonical import content_hash,stable_id

def claim_ledger(registry,tournament):
    claims={'deep_sequence_reference_implemented':True,'state_space_reference_implemented':True,'streaming_batch_parity_reference':True,'restart_snapshot_reference':True,'synthetic_self_supervised_readout':True,'real_corpus_training':False,'real_alpha':False,'outcome_prediction_authority':False,'treatment_ranking':False,'treatment_selection':False,'runtime_parity':False,'production_authorization':False,'live_trading':False}
    material={'phase':'SAED_V4_12','claims':claims,'admitted_reference_count':registry['admitted_count'],'reference_champion_id':tournament['reference_champion_id']}
    return {**material,'ledger_id':stable_id('seqclaims',material),'ledger_hash':content_hash(material)}

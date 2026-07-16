from .canonical import content_hash,stable_id

def make(candidate,feature,evaluation,calibration,domain,intake_decision,attestation,seq):
    doc={'phase':'SAED_V4_14','candidate_id':candidate.candidate_id,'intake_id':candidate.intake_id,'family':candidate.family,'adapter_mode':candidate.adapter_mode,'seed':candidate.seed,'source_token_sequence_hash':seq['token_sequence_hash'],'feature_hash':feature['feature_hash'],'evaluation_hash':evaluation['evaluation_hash'],'calibration_hash':calibration['calibration_hash'],'domain_shift_hash':domain['domain_shift_hash'],'intake_decision_hash':intake_decision['decision_hash'],'supply_chain_attestation_hash':attestation['attestation_hash'],'composite_score':evaluation['composite_score'],'external_weights_loaded':False,'production_eligible':False,'runtime_authority':False}
    doc['checkpoint_hash']=content_hash(doc);doc['checkpoint_id']=stable_id('fmckpt',doc);return doc

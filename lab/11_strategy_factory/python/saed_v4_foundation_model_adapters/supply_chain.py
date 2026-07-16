from .canonical import content_hash,stable_id

def attest(intake,decision):
    doc={'phase':'SAED_V4_14','intake_id':intake.intake_id,'family':intake.family,'release':intake.release,'weight_digest':intake.weight_digest,'code_digest':intake.code_digest,'tokenizer_digest':intake.tokenizer_digest,'license_id':intake.license_id,'license_permitted':intake.license_permitted,'local_execution_only':intake.local_execution_only,'remote_inference_forbidden':intake.remote_inference_forbidden,'external_network_calls':False,'external_weights_loaded':False,'decision':decision['decision'],'signature_status':'synthetic_reference_digest_verified','vulnerability_scan':'reference_no_external_dependencies','production_eligible':False}
    doc['attestation_hash']=content_hash(doc);doc['attestation_id']=stable_id('fmattest',doc);return doc

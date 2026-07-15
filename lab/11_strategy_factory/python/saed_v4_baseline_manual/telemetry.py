from .canonical import content_hash, stable_id

def build_telemetry(registry,benchmark,exposure,corpus):
    payload={"phase":"SAED_V4_10","baseline_count":registry['entry_count'],"benchmark_result_count":benchmark['baseline_count'],"complete_exposure":exposure['complete'],"pretraining_artifact_count":len(corpus['included_artifacts']),"prohibited_artifact_class_count":len(corpus['prohibited_input_artifact_classes']),"synthetic_watermark":benchmark['synthetic_watermark'],"authority_violations":0,"leakage_violations":0}
    payload['telemetry_id']=stable_id('v410telemetry',payload);payload['telemetry_hash']=content_hash(payload);return payload

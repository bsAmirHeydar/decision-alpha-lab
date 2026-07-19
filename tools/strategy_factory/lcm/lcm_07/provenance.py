from .canonical import digest_object

def build(run_id,source_handoff_digest,summary_digest):
    o={"schema_version":"1.0.0","shared_engine_run_id":run_id,"nodes":[{"node_id":"LCM06_HANDOFF","digest":source_handoff_digest},{"node_id":"LCM07_SHARED_ENGINE_STUDY","digest":summary_digest}],"edges":[{"from":"LCM06_HANDOFF","to":"LCM07_SHARED_ENGINE_STUDY"}],"reaches_lcm06_framework":True,"source_semantics_mutated":False,"shared_engine_materialized":False,"source_moved":False,"source_deleted":False,"merge_performed":False,"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False,"provenance_digest":None};o["provenance_digest"]=digest_object(o,"provenance_digest");return o

from .canonical import digest_object
def build(run_id,source_handoff_digest,summary_digest):
    out={"schema_version":"1.0.0","framework_run_id":run_id,"nodes":[{"node_id":"LCM05_HANDOFF","digest":source_handoff_digest},{"node_id":"LCM06_FRAMEWORK","digest":summary_digest}],"edges":[{"from":"LCM05_HANDOFF","to":"LCM06_FRAMEWORK"}],"reaches_lcm05_topology":True,"source_semantics_mutated":False,"target_paths_materialized":False,"source_moved":False,"source_deleted":False,"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False,"provenance_digest":None}
    out['provenance_digest']=digest_object(out,'provenance_digest');return out

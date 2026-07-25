from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id

def build_lineage_graph(package:dict[str,Any],source_snapshot:dict[str,Any],plan:dict[str,Any],detector:dict[str,Any],occurrence:dict[str,Any],known:dict[str,Any],feature:dict[str,Any],replay:dict[str,Any],onboarding:dict[str,Any],handoff:dict[str,Any])->dict[str,Any]:
    cid=package['manifest']['context_id'];nodes=[
      {'node_id':'SOURCE','kind':'SOURCE_SNAPSHOT','digest':source_snapshot['snapshot_digest']},
      {'node_id':'PLAN','kind':'COMPILER_PLAN','digest':plan['plan_digest']},
      {'node_id':'DETECTOR','kind':'DETECTOR_IR','digest':detector['detector_ir_digest']},
      {'node_id':'OCCURRENCE','kind':'OCCURRENCE_IR','digest':occurrence['occurrence_ir_digest']},
      {'node_id':'KNOWN_TIME','kind':'KNOWN_TIME_IR','digest':known['known_time_ir_digest']},
      {'node_id':'FEATURE','kind':'FEATURE_BINDING_IR','digest':feature['feature_binding_ir_digest']},
      {'node_id':'REPLAY','kind':'GOLDEN_REPLAY','digest':replay['replay_digest']},
      {'node_id':'ONBOARDING','kind':'ONBOARDING_REPORT','digest':onboarding['report_digest']},
      {'node_id':'HANDOFF','kind':'ACL04_HANDOFF','digest':handoff['handoff_digest']},
    ]
    edges=[]
    def edge(a,b,rel):edges.append({'edge_id':stable_id('EDGE',cid,a,b,rel),'from_node':a,'to_node':b,'relation':rel})
    edge('SOURCE','PLAN','PLANS');
    for n in ('DETECTOR','OCCURRENCE','KNOWN_TIME','FEATURE'):edge('SOURCE',n,'COMPILES_TO')
    for n in ('DETECTOR','OCCURRENCE','KNOWN_TIME'):edge(n,'REPLAY','VALIDATED_BY')
    for n in ('REPLAY','FEATURE'):edge(n,'ONBOARDING','EVIDENCES')
    edge('ONBOARDING','HANDOFF','BOUNDS')
    body={'schema_version':'1.0.0','context_id':cid,'nodes':nodes,'edges':edges,'acyclic_required':True}
    return {**body,'lineage_digest':digest_object(body)}

from __future__ import annotations
from .canonical import stable_id,with_digest

def build_provenance(bundle,dag,result_bundle,object_index,event_ledger):
    nodes=[
      {'node_id':bundle['batch']['batch_id'],'kind':'FROZEN_BATCH','digest':bundle['batch']['batch_definition_digest']},
      {'node_id':dag['plan_id'],'kind':'RESEARCH_DAG','digest':dag['dag_digest']},
      {'node_id':result_bundle['result_bundle_id'],'kind':'RESEARCH_RESULT_BUNDLE','digest':result_bundle['result_bundle_digest']},
      {'node_id':'ACL06_RUN_OBJECT_INDEX','kind':'RUN_OBJECT_INDEX','digest':object_index['object_index_digest']},
      {'node_id':'ACL06_EVENT_LEDGER','kind':'EVENT_LEDGER','digest':event_ledger['ledger_digest']},]
    edges=[{'from':bundle['batch']['batch_id'],'to':dag['plan_id'],'relation':'PLANNED_FROM'},{'from':dag['plan_id'],'to':result_bundle['result_bundle_id'],'relation':'EXECUTED_AS'},{'from':result_bundle['result_bundle_id'],'to':'ACL06_RUN_OBJECT_INDEX','relation':'MATERIALIZED_IN'},{'from':result_bundle['result_bundle_id'],'to':'ACL06_EVENT_LEDGER','relation':'EVIDENCED_BY'}]
    return with_digest({'schema_version':'1.0.0','graph_id':stable_id('PROV',result_bundle['result_bundle_digest'],length=24),'nodes':nodes,'edges':edges,'reaches_frozen_batch':True,'candidate_behavior_mutated':False},'graph_digest')

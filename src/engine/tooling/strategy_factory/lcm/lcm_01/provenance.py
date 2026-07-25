from __future__ import annotations
from .canonical import content_id, digest_object

def build(baseline_id: str, baseline_digest: str, handoff_digest: str, survey_id: str, output_digests: dict[str,str]) -> dict:
    nodes=[
      {'node_id':'LCM00_BASELINE','artifact_type':'BASELINE_MANIFEST','artifact_id':baseline_id,'digest':baseline_digest},
      {'node_id':'LCM00_HANDOFF','artifact_type':'LCM00_TO_LCM01','artifact_id':'LCM00_TO_LCM01','digest':handoff_digest},
      {'node_id':'LCM01_SURVEY','artifact_type':'FORENSIC_SURVEY','artifact_id':survey_id,'digest':output_digests['survey_digest']},
      {'node_id':'LCM01_HANDOFF','artifact_type':'LCM01_TO_LCM02','artifact_id':'LCM01_TO_LCM02','digest':output_digests['handoff_digest']},
    ]
    edges=[{'from_node':'LCM00_BASELINE','to_node':'LCM01_SURVEY','relation':'SURVEYED_WITHOUT_MUTATION'},{'from_node':'LCM00_HANDOFF','to_node':'LCM01_SURVEY','relation':'AUTHORIZED_NON_DESTRUCTIVE_ACTION'},{'from_node':'LCM01_SURVEY','to_node':'LCM01_HANDOFF','relation':'PRODUCED'}]
    g={'schema_version':'1.0.0','graph_id':content_id('LCM01PROV',{'baseline':baseline_digest,'survey':survey_id}),'nodes':nodes,'edges':edges,'reaches_lcm00_baseline':True,'baseline_artifact_mutated':False,'source_file_moved':False,'source_file_deleted':False,'semantic_refactor_performed':False,'live_authority_inferred_from_pattern_hits':False,'graph_digest':''}
    g['graph_digest']=digest_object(g,'graph_digest'); return g

from __future__ import annotations
from .canonical import content_id, digest_object


def build(portfolio_id: str, input_digests: dict, output_digests: dict):
    nodes=[];edges=[]
    for name,digest in sorted(input_digests.items()):
        nid=content_id("PROVNODE",["INPUT",name,digest]);nodes.append({"node_id":nid,"node_type":"INPUT_ARTIFACT","name":name,"digest":digest});edges.append({"from_node":nid,"to_node":portfolio_id,"relation":"CONSUMED_BY"})
    for name,digest in sorted(output_digests.items()):
        nid=content_id("PROVNODE",["OUTPUT",name,digest]);nodes.append({"node_id":nid,"node_type":"OUTPUT_ARTIFACT","name":name,"digest":digest});edges.append({"from_node":portfolio_id,"to_node":nid,"relation":"PRODUCED"})
    obj={"schema_version":"1.0.0","graph_id":content_id("LCM08APROV",portfolio_id),"portfolio_id":portfolio_id,"nodes":nodes,"edges":edges,"semantic_reinterpretation_performed":False,"graph_digest":None};obj["graph_digest"]=digest_object(obj,"graph_digest");return obj

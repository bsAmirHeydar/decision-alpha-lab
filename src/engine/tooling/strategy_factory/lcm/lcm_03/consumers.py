from __future__ import annotations
from collections import Counter
from .canonical import content_id,digest_object

def build_consumer_census(edges: list[dict], identity_by_path: dict):
    rows=[]
    for e in edges:
        target=e.get('resolved_path','')
        if e.get('resolution_status')!='RESOLVED_INTERNAL' or target not in identity_by_path: continue
        iid=identity_by_path.get(target)
        row={'consumer_record_id':content_id('CONSUMER',{'source':e.get('source_path'),'target':target,'raw':e.get('raw_target'),'line':e.get('line_number'),'type':e.get('edge_type')},24),'target_identity_id':iid,'target_artifact_path':target,'consumer_artifact_path':e.get('source_path',''),'edge_type':e.get('edge_type',''),'raw_target':e.get('raw_target',''),'line_number':int(e.get('line_number') or 0),'resolution_status':'IDENTITY_BOUND' if iid else 'TARGET_IDENTITY_AMBIGUOUS','semantic_reachability_claimed':False,'consumer_digest':None}
        row['consumer_digest']=digest_object(row,'consumer_digest'); rows.append(row)
    unique={x['consumer_record_id']:x for x in rows}
    return sorted(unique.values(),key=lambda x:(x['target_artifact_path'],x['consumer_artifact_path'],x['edge_type'],x['line_number']))

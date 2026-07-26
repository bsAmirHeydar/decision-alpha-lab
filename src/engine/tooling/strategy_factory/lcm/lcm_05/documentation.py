from .canonical import content_id,digest_object
def build_successors(exact,namespace_rows):
    records=[]
    for g in exact.get('groups',[]):
        ns=g['namespaces']
        if len(ns)<2 or g.get('member_count',0)==0:continue
        canonical=next((x for x in ns if x.startswith('docs/architecture/master/')),sorted(ns)[0])
        for source in ns:
            status='CANONICAL_MASTER_SELECTED' if source==canonical else 'EXACT_DUPLICATE_SUCCESSOR_PROPOSED';obj={"schema_version":"1.0.0","successor_record_id":content_id('DOCSUCCESSOR',[source,canonical]),"source_namespace":source,"canonical_successor":canonical,"relationship":"SELF" if source==canonical else 'EXACT_BYTE_DUPLICATE_TREE',"status":status,"redirect_materialized":False,"deletion_authorized":False,"semantic_equivalence_claimed":False,"tree_fingerprint":g['tree_fingerprint'],"record_digest":None};obj['record_digest']=digest_object(obj,'record_digest');records.append(obj)
    known={r['source_namespace'] for r in records}
    for row in namespace_rows:
        ns=row['namespace']
        if ns in known:continue
        obj={"schema_version":"1.0.0","successor_record_id":content_id('DOCSUCCESSOR',[ns,ns]),"source_namespace":ns,"canonical_successor":ns,"relationship":"RETAIN_PENDING_SEMANTIC_RECONCILIATION","status":"RETAIN_CURRENT_REFERENCE","redirect_materialized":False,"deletion_authorized":False,"semantic_equivalence_claimed":False,"tree_fingerprint":row['tree_fingerprint'],"record_digest":None};obj['record_digest']=digest_object(obj,'record_digest');records.append(obj)
    return sorted(records,key=lambda x:x['source_namespace'])

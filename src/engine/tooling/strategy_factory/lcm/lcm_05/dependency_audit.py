from collections import Counter
from .canonical import content_id,digest_object
from .layering import layer_for,allowed
def audit(edges,class_by_path):
    violations=[];evaluated=0;unresolved=0;counts=Counter()
    for e in edges:
        src=class_by_path.get(e['source_path']);dst=class_by_path.get(e.get('resolved_path') or '')
        if not src or not dst:unresolved+=1;continue
        evaluated+=1;sl=layer_for(src['artifact_role'],src['artifact_path']);tl=layer_for(dst['artifact_role'],dst['artifact_path']);ok=allowed(sl,tl);counts['ALLOWED' if ok else 'PROHIBITED']+=1
        if not ok:
            obj={"schema_version":"1.0.0","violation_id":content_id('DEPVIOL',[e['source_path'],e['edge_type'],e.get('resolved_path'),e.get('line_number')]),"source_path":e['source_path'],"target_path":e.get('resolved_path'),"edge_type":e['edge_type'],"line_number":int(e.get('line_number') or 0),"source_layer":sl,"target_layer":tl,"status":"LEGACY_DIRECTION_VIOLATION_REQUIRES_MIGRATION","waiver_allowed":False,"violation_digest":None};obj['violation_digest']=digest_object(obj,'violation_digest');violations.append(obj)
    summary={"schema_version":"1.0.0","evaluated_edge_count":evaluated,"unresolved_or_unclassified_edge_count":unresolved,"allowed_edge_count":counts['ALLOWED'],"prohibited_edge_count":counts['PROHIBITED'],"current_legacy_violations_are_target_topology_approval":False,"violation_count":len(violations),"audit_digest":None};summary['audit_digest']=digest_object(summary,'audit_digest');return summary,violations

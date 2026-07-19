from __future__ import annotations
from collections import Counter,defaultdict
from .canonical import digest_object
from .naming import propose_identity
from .registries import ACTIVE_STATUSES

def build_identity_candidates(records: list[dict]):
    identities=[]; ambiguities=[]; by_path={}
    for record in records:
        if record['activity_status'] not in ACTIVE_STATUSES: continue
        candidate=propose_identity(record)
        if candidate is None:
            ambiguity={'ambiguity_id':'IDAMB_'+record['classification_id'].split('_')[-1],'artifact_path':record['artifact_path'],'classification_id':record['classification_id'],'family_candidate':record['family_candidate'],'artifact_role':record['artifact_role'],'activity_status':record['activity_status'],'reason_codes':['UNKNOWN_OR_NON_DOMAIN_ROLE','HUMAN_SEMANTIC_CLASSIFICATION_REQUIRED'],'resolution_status':'AMBIGUOUS_ROLE_BLOCKED','source_classification_digest':record['classification_digest'],'ambiguity_digest':None}
            ambiguity['ambiguity_digest']=digest_object(ambiguity,'ambiguity_digest'); ambiguities.append(ambiguity); by_path[record['artifact_path']]=None; continue
        candidate['identity_digest']=digest_object(candidate,'identity_digest'); identities.append(candidate); by_path[record['artifact_path']]=candidate['identity_id']
    if len({x['identity_id'] for x in identities})!=len(identities): raise ValueError('identity collision')
    return identities,ambiguities,by_path

def family_map(identities: list[dict], ambiguities: list[dict]):
    rows=[]; groups=defaultdict(list)
    for x in identities: groups[(x['family_candidate'],x['identity_kind'])].append(x)
    amb=Counter(x['family_candidate'] for x in ambiguities)
    for (family,kind),items in sorted(groups.items()):
        row={'family_candidate':family,'identity_kind':kind,'identity_candidate_count':len(items),'protected_platform_count':sum(x['protected_platform_asset'] for x in items),'security_review_blocked_count':sum(x['security_sensitive'] for x in items),'human_semantic_approval_complete':False,'automatic_merge_allowed':False,'family_identity_status':'PROVISIONAL_UNMERGED','family_identity_digest':None}
        row['family_identity_digest']=digest_object(row,'family_identity_digest'); rows.append(row)
    return rows,amb

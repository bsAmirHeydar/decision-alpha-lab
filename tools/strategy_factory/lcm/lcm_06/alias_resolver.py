from __future__ import annotations
from collections import defaultdict
from .canonical import digest_object
class AliasResolver:
    def __init__(self,records):
        self.by_alias=defaultdict(list)
        for r in records:self.by_alias[r['alias'].casefold()].append(r)
    def resolve(self,alias):
        matches=self.by_alias.get(alias.casefold(),[])
        if len(matches)==1:status='RESOLVED';reason='ALIAS_RESOLVED';identity=matches[0]['identity_id'];target=matches[0].get('target_path')
        elif len(matches)>1:status='AMBIGUOUS';reason='ALIAS_AMBIGUOUS';identity=None;target=None
        else:status='NOT_FOUND';reason='ALIAS_NOT_FOUND';identity=None;target=None
        out={"schema_version":"1.0.0","alias":alias,"resolution_status":status,"reason_code":reason,"identity_id":identity,"target_path":target,"candidate_count":len(matches),"resolver_digest":None}
        out['resolver_digest']=digest_object(out,'resolver_digest');return out

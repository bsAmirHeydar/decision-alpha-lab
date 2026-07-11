from __future__ import annotations
from collections import defaultdict
import math
from .models import StatisticalSample, MatchedNullSpec, NullAssignment, NullComparison
from .enums import NullMethod, ReportStatus
from .hashing import fnv1a64_utf16le, stable_id

class MatchedNullEngine:
    def __init__(self, spec: MatchedNullSpec) -> None:
        self.spec=spec.with_hash() if not spec.null_hash else spec
        if self.spec.minimum_pool_size < 1 or self.spec.maximum_reuse < 1:
            raise ValueError("invalid null matching limits")
        if self.spec.method not in (NullMethod.EXACT_STRATIFIED_CYCLIC, NullMethod.EXACT_STRATIFIED_HASHED):
            raise ValueError("null method is not available in Phase 11 matching engine")
    def assign(self, observed: list[StatisticalSample], controls: list[StatisticalSample]) -> list[NullAssignment]:
        pools=defaultdict(list)
        for c in controls: c.validate(); pools[c.stratum_key].append(c)
        for key in pools: pools[key].sort(key=lambda x:x.sample_id)
        reuse=defaultdict(int); out=[]
        for o in sorted(observed,key=lambda x:x.sample_id):
            o.validate(); pool=pools.get(o.stratum_key,[])
            if len(pool)<self.spec.minimum_pool_size: continue
            start=fnv1a64_utf16le(f"{o.sample_id}|{self.spec.seed}")%len(pool)
            selected=None
            for offset in range(len(pool)):
                c=pool[(start+offset)%len(pool)]
                if self.spec.require_different_cluster and c.cluster_id==o.cluster_id: continue
                if reuse[c.sample_id]>=self.spec.maximum_reuse: continue
                selected=c; break
            if selected is None: continue
            reuse[selected.sample_id]+=1
            payload=f"{self.spec.null_hash}|{o.sample_id}|{selected.sample_id}|{reuse[selected.sample_id]}"
            out.append(NullAssignment(stable_id("nasn",payload),self.spec.null_hash,o.sample_id,
                                      selected.sample_id,o.stratum_key,o.cluster_id,
                                      selected.cluster_id,reuse[selected.sample_id]))
        return out

def compare_matched_pairs(observed: list[StatisticalSample], controls: list[StatisticalSample],
                          assignments: list[NullAssignment], null_hash: str,
                          group_key: str="all=all") -> NullComparison:
    om={x.sample_id:x for x in observed}; cm={x.sample_id:x for x in controls}; diffs=[]; obs=[]; ctl=[]
    for a in assignments:
        if a.observed_sample_id not in om or a.control_sample_id not in cm: raise ValueError("assignment references missing sample")
        ov=om[a.observed_sample_id].net_r; cv=cm[a.control_sample_id].net_r
        obs.append(ov); ctl.append(cv); diffs.append(ov-cv)
    if not diffs:
        return NullComparison(null_hash,group_key,0,0,0,0,0,0,0,ReportStatus.UNMATCHED).with_hash()
    mean_diff=sum(diffs)/len(diffs); mean_obs=sum(obs)/len(obs); mean_ctl=sum(ctl)/len(ctl)
    sd=(sum((x-mean_diff)**2 for x in diffs)/(len(diffs)-1))**.5 if len(diffs)>1 else 0.0
    se=sd/math.sqrt(len(diffs)) if len(diffs)>1 else 0.0
    z=mean_diff/se if se>0 else (1e9 if mean_diff>0 else (-1e9 if mean_diff<0 else 0.0))
    rate=len(diffs)/len(observed) if observed else 0.0
    status=ReportStatus.VALID if rate>=.8 else ReportStatus.PARTIAL_MATCH
    return NullComparison(null_hash,group_key,len(diffs),mean_obs,mean_ctl,mean_diff,se,z,rate,status).with_hash()

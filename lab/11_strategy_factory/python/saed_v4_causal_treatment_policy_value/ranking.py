from __future__ import annotations
from .canonical import content_hash

def rank_treatments(ate_report):
    rows=sorted(ate_report['effects'],key=lambda x:(x['lower_95'],x['estimate'],x['treatment_id']),reverse=True)
    ranked=[{'rank':i+1,'treatment_id':r['treatment_id'],'estimate':r['estimate'],'lower_95':r['lower_95'],'research_only':True} for i,r in enumerate(rows)]
    out={'phase':'SAED_V4_18','ranking_basis':'synthetic_cross_fitted_aipw_lower_95','ranking':ranked,'production_ranking_authority':False};out['report_hash']=content_hash(out);return out

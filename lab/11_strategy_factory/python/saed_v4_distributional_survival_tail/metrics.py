from __future__ import annotations
from .canonical import content_hash
from .numerics import mean,pinball,safe_div,l1

def evaluate(candidates,dataset,dist,surv,tail_cal,config):
    actual={r['row_id']:r for r in dataset['rows'] if r['split']=='selection_validation'};dby={};sby={}
    for p in dist['items']:dby.setdefault(p['candidate_id'],[]).append(p)
    for p in surv['items']:sby.setdefault(p['candidate_id'],[]).append(p)
    tcby={}
    for r in tail_cal['rows']:tcby.setdefault(r['candidate_id'],[]).append(r)
    rows=[]
    for c in candidates:
        if not c.enabled:continue
        dp=dby[c.candidate_id];sp=sby[c.candidate_id];pins=[];cover=[];width=[]
        for p in dp:
            r=actual[p['row_id']]
            if not r['outcome_observed']:continue
            pins.extend(pinball(r['net_r'],qh,q) for qh,q in zip(p['monotone_quantiles'],config.quantiles))
            lo=p['monotone_quantiles'][1];hi=p['monotone_quantiles'][-2];cover.append(lo<=r['net_r']<=hi);width.append(hi-lo)
        briers=[];cindex_pairs=0;cindex_correct=0
        for p in sp:
            r=actual[p['row_id']]
            for h,sprob in zip(p['horizons_seconds'],p['survival_probability']):
                y=1.0 if r['event_duration_seconds']>h else 0.0;briers.append((y-sprob)**2)
        for i,a in enumerate(sp):
            ra=actual[a['row_id']]
            for b in sp[i+1:]:
                rb=actual[b['row_id']]
                if ra['event_duration_seconds']==rb['event_duration_seconds']:continue
                cindex_pairs+=1;pa=a['expected_remaining_opportunity_seconds'];pb=b['expected_remaining_opportunity_seconds'];cindex_correct+=((pa-pb)*(ra['event_duration_seconds']-rb['event_duration_seconds'])>0)
        tail_err=mean([x['exceedance_error'] for x in tcby[c.candidate_id]]);pin=mean(pins);brier=mean(briers);coverage=mean(cover);cindex=safe_div(cindex_correct,cindex_pairs,.5);cross=sum(p['quantile_crossing_after_projection'] for p in dp)
        score=1/(1+pin+brier+tail_err+abs(coverage-.8)+(1-cindex)+cross)
        rows.append({'candidate_id':c.candidate_id,'algorithm':c.algorithm,'pinball_loss':pin,'integrated_brier_score':brier,'central_interval_coverage':coverage,'central_interval_width':mean(width),'concordance_index':cindex,'tail_exceedance_error':tail_err,'quantile_crossing_count':cross,'reference_score':score,'evaluation_rows':len(dp),'production_eligible':False})
    out={'phase':'SAED_V4_16','row_count':len(rows),'rows':rows};out['report_hash']=content_hash(out);return out

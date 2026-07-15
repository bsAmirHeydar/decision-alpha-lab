from __future__ import annotations
from .canonical import content_hash,stable_id

def run_tournament(metric_docs,parity_docs,probe_docs):
    parity_by={x['candidate_id']:x for x in parity_docs};probe_by={x['candidate_id']:x for x in probe_docs};rows=[]
    for m in metric_docs:
        val=m['summary']['validation']['mean_mse'];par=parity_by[m['candidate_id']]['passed'];collapse=probe_by[m['candidate_id']]['collapsed'];eligible=par and not collapse and val is not None
        rows.append({'candidate_id':m['candidate_id'],'architecture':m['architecture'],'validation_mse':val,'test_mse':m['summary']['test']['mean_mse'],'streaming_parity':par,'state_collapsed':collapse,'research_eligible':eligible})
    rows.sort(key=lambda r:(not r['research_eligible'],float('inf') if r['validation_mse'] is None else r['validation_mse'],r['candidate_id']))
    champion=rows[0]['candidate_id'] if rows and rows[0]['research_eligible'] else None
    material={'rows':rows,'reference_champion_id':champion,'decision':'research_reference_only' if champion else 'reject','production_promotion':False,'treatment_authority':False,'baseline_preserved':any(r['architecture']=='ema_recurrent' for r in rows)}
    return {**material,'tournament_id':stable_id('seqtournament',material),'tournament_hash':content_hash(material)}

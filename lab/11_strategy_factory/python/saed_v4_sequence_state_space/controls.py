from __future__ import annotations
from .canonical import content_hash,stable_id

def baseline_control(tournament):
    base=next(r for r in tournament['rows'] if r['architecture']=='ema_recurrent');champ=next((r for r in tournament['rows'] if r['candidate_id']==tournament['reference_champion_id']),None)
    material={'baseline_candidate_id':base['candidate_id'],'baseline_validation_mse':base['validation_mse'],'champion_candidate_id':None if champ is None else champ['candidate_id'],'champion_validation_mse':None if champ is None else champ['validation_mse'],'baseline_preserved':True,'advanced_model_required':False,'promotion_inference_forbidden':True}
    return {**material,'control_id':stable_id('baselinecontrol',material),'control_hash':content_hash(material)}

from .canonical import content_hash,stable_id
from .numerics import l2,clamp

def evaluate(seq,features,calibration,domain,candidate,config):
    tokens=seq['tokens'];rep=features['embedding'];target=[sum(t['feature'][j] for t in tokens[-min(4,len(tokens)):])/min(4,len(tokens)) for j in range(config.feature_dim)]
    target=(target*((len(rep)+len(target)-1)//len(target)))[:len(rep)]
    recon=clamp(1-l2(rep,target)/(1+l2([0]*len(rep),target)),0,1)
    temporal=clamp(1-features['uncertainty_scale']/(1+abs(features['quantile_forecast'][len(features['quantile_forecast'])//2]['value'])),0,1)
    graph_alignment=clamp(.5+.5*sum(abs(x) for x in rep)/len(rep),0,1)
    calibration_score=calibration['calibration_score'];robust=domain['robustness_score'];complexity=clamp(1-candidate.trainable_parameter_budget/max(1,250000)-.02*max(0,candidate.expert_count-1),0,1)
    composite=.24*recon+.18*temporal+.18*graph_alignment+.18*calibration_score+.14*robust+.08*complexity
    doc={'phase':'SAED_V4_14','candidate_id':candidate.candidate_id,'family':candidate.family,'adapter_mode':candidate.adapter_mode,'masked_latent_reconstruction':recon,'temporal_consistency':temporal,'graph_alignment':graph_alignment,'calibration_score':calibration_score,'domain_shift_robustness':robust,'complexity_score':complexity,'composite_score':composite,'outcome_labels_used':False,'economic_uplift_claimed':False,'production_authority':False}
    doc['evaluation_hash']=content_hash(doc);doc['evaluation_id']=stable_id('fmeval',doc);return doc

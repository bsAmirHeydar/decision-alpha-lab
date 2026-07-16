from .encoding import encode_domain_view,encode_foundation_feature
from .canonical import content_hash,stable_id

def build(v404_package,v414_features,v414_domain,v414_calibration,config):
    cutoff=v404_package['known_as_of'];domain=[encode_domain_view(v,config,cutoff) for v in sorted(v404_package['views'],key=lambda x:x['view_name'])]
    domain_rows={r['candidate_id']:r for r in v414_domain['rows']};cal_rows={r['candidate_id']:r for r in v414_calibration['rows']}
    foundation=[encode_foundation_feature(f,config,domain_rows,cal_rows) for f in sorted(v414_features['items'],key=lambda x:x['candidate_id'])]
    allv=domain+foundation
    doc={'phase':'SAED_V4_15','known_as_of':cutoff,'common_dim':config.common_dim,'domain_views':domain,'foundation_views':foundation,'ordered_envelope_ids':[x['envelope_id'] for x in allv],'ordered_envelope_hashes':[x['envelope_hash'] for x in allv],'domain_view_count':len(domain),'foundation_view_count':len(foundation),'future_suffix_accessed':False,'outcome_labels_accessed':False,'production_eligible':False}
    doc['aligned_set_hash']=content_hash(doc);doc['aligned_set_id']=stable_id('v415aligned',doc);return doc

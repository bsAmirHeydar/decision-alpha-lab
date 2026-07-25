from .canonical import content_hash,stable_id
from .numerics import quantile,clamp

def calibrate(features,token_sequence,candidate):
    hist=[sum(t['feature'])/len(t['feature']) for t in token_sequence['tokens']]
    target=hist[-1]
    qs=features['quantile_forecast'];values=[x['value'] for x in qs];monotone=all(a<=b for a,b in zip(values,values[1:]));lo,hi=values[0],values[-1]
    covered=lo<=target<=hi;median=min(qs,key=lambda x:abs(x['q']-.5))['value'];abs_error=abs(median-target)
    raw_coverage=1.0 if covered else 0.0;expected=qs[-1]['q']-qs[0]['q'];gap=abs(raw_coverage-expected)
    score=clamp(1.0-abs_error/(1.0+abs(target))-0.25*gap,0.0,1.0)
    doc={'phase':'SAED_V4_14','candidate_id':candidate.candidate_id,'calibration_method':candidate.calibration_method,'quantile_monotonic':monotone,'reference_target':target,'interval_covered':covered,'expected_interval_mass':expected,'coverage_gap':gap,'median_absolute_error':abs_error,'calibration_score':score,'selection_evidence':False,'production_evidence':False}
    doc['calibration_hash']=content_hash(doc);doc['calibration_id']=stable_id('fmcal',doc);return doc

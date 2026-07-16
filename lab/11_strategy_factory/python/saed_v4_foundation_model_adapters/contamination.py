from .canonical import content_hash,stable_id

def audit(intakes,disclosures,decisions,as_of):
    by_d={d.intake_id:d for d in disclosures}; by_dec={d['intake_id']:d for d in decisions}; rows=[]
    for i in intakes:
        d=by_d[i.intake_id]
        risk='none' if i.synthetic_reference_adapter and i.source_kind=='reference_emulation' else i.overlap_risk
        passed=by_dec[i.intake_id]['decision']=='admit_reference' and risk not in {'high','unknown'}
        rows.append({'intake_id':i.intake_id,'family':i.family,'training_cutoff':d.training_cutoff,'evaluation_period_overlap_possible':d.evaluation_period_overlap_possible,'exact_corpus_disclosed':d.exact_corpus_disclosed,'effective_overlap_risk':risk,'synthetic_reference_adapter':i.synthetic_reference_adapter,'passed':passed,'action':'admit_reference' if passed else 'quarantine'})
    doc={'phase':'SAED_V4_14','known_as_of':as_of,'rows':rows,'all_admitted_rows_safe':all(r['passed'] for r in rows if by_dec[r['intake_id']]['decision']=='admit_reference'),'outcome_labels_accessed':False,'protected_evidence_accessed':False}
    doc['audit_hash']=content_hash(doc);doc['audit_id']=stable_id('fmcontamination',doc);return doc

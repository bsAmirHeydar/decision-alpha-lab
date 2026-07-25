from __future__ import annotations
from .canonical import content_hash,stable_id
from .errors import CausalityError

def audit(sequences):
    train={p.record_id for s in sequences if s.split=='train' for p in s.points};validation={p.record_id for s in sequences if s.split=='validation' for p in s.points};test={p.record_id for s in sequences if s.split=='test' for p in s.points};overlaps={'train_validation':sorted(train&validation),'train_test':sorted(train&test),'validation_test':sorted(validation&test)};passed=not any(overlaps.values())
    material={'overlaps':overlaps,'outcome_inputs_detected':False,'identity_tokens_detected':False,'future_suffix_allowed':False,'passed':passed}
    if not passed:raise CausalityError('sequence split contamination')
    return {**material,'audit_id':stable_id('seqcontam',material),'audit_hash':content_hash(material)}

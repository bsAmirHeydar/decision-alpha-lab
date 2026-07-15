from __future__ import annotations
from .canonical import content_hash,stable_id
from .initialization import matrix
from .numerics import matvec,max_abs_diff
from .errors import DistillationError

def distill_state(candidate_id,state_dim,runtime_dim):
    if runtime_dim<2 or runtime_dim>state_dim:raise DistillationError('invalid runtime dimension')
    projection=[list(row) for row in matrix(f'{candidate_id}:distill',runtime_dim,state_dim,0.15)]
    material={'candidate_id':candidate_id,'source_state_dim':state_dim,'runtime_state_dim':runtime_dim,'projection':projection,'method':'deterministic_linear_projection','runtime_authority':False}
    return {**material,'distillation_id':stable_id('distill',material),'distillation_hash':content_hash(material)}
def project(report,state):return tuple(matvec(report['projection'],state))
def distillation_report(model,sequences,distilled):
    from .streaming import _dts
    rows=[]
    for seq in sequences:
        hs,_=model.batch([p.vector for p in seq.points],_dts(seq.points));
        for i,h in enumerate(hs):
            z=project(distilled,h);rows.append({'sequence_id':seq.sequence_id,'step':i,'source_norm':sum(x*x for x in h)**0.5,'runtime_norm':sum(x*x for x in z)**0.5})
    material={'distillation_hash':distilled['distillation_hash'],'row_count':len(rows),'rows':rows,'bounded_runtime_representation':True,'mql5_export_claimed':False}
    return {**material,'report_id':stable_id('distillreport',material),'report_hash':content_hash(material)}

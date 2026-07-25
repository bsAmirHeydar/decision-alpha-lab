from __future__ import annotations
from .errors import BaselineError

def baseline_report(ranked,baseline_id,skip_id,decision):
    by={r['treatment_id']:r for r in ranked}
    if baseline_id not in by or skip_id not in by:raise BaselineError('baseline treatment absent')
    best=ranked[0];base=by[baseline_id];skip=by[skip_id]
    return {'canonical_baseline':baseline_id,'skip_treatment':skip_id,'best_candidate':best['treatment_id'],'best_minus_baseline':best['objective_score']-base['objective_score'],'best_minus_skip':best['objective_score']-skip['objective_score'],'baseline_preserved':True,'decision_abstained':decision['abstain'],'fallback':decision['fallback']}

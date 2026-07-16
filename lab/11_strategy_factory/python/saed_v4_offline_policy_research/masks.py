from __future__ import annotations
from collections import defaultdict
from .trajectory import transitions
from .canonical import content_hash

def compile_masks(dataset,actions,safe_action='skip'):
    observed=defaultdict(set)
    for tr in transitions(dataset): observed[tr['state']].update(tr['allowed_actions'])
    masks={s:{a:(a in observed[s]) for a in actions} for s in sorted(observed)}
    for s in masks:masks[s][safe_action]=True
    out={'states':masks,'actions':list(actions),'safe_action':safe_action,'all_states_have_safe_action':all(m[safe_action] for m in masks.values()),'unknown_action_rejected':True}
    out['mask_hash']=content_hash(out);return out

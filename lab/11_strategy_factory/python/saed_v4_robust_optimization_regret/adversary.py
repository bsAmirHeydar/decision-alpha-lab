from __future__ import annotations
from .canonical import content_hash

def bounded_adversary(optimization_report,scenario_set,steps,shock_bound,ledger=None):
    selected=optimization_report['decision']['selected_allocation_id'];row=next(r for r in optimization_report['rows'] if r['allocation_id']==selected)
    ordered=sorted(row['scenario_utilities'].items(),key=lambda kv:(kv[1],kv[0]))
    trace=[];current=float(row['distributionally_robust_utility'])
    for k in range(int(steps)):
        sid,val=ordered[k%len(ordered)];delta=min(float(shock_bound),(k+1)*float(shock_bound)/max(1,int(steps)))
        current=min(current,float(val)-delta)
        trace.append({'step':k+1,'scenario_id':sid,'bounded_shift':delta,'adversarial_value':current})
        if ledger:ledger.consume('adversarial_steps',1)
    out={'selected_allocation_id':selected,'bounded':True,'shock_bound':float(shock_bound),'trace':trace,'worst_adversarial_value':min([x['adversarial_value'] for x in trace],default=current),'research_only':True}
    out['adversary_report_hash']=content_hash(out);return out

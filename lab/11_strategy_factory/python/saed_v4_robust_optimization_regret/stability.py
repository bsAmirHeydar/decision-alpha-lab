from __future__ import annotations
from .canonical import content_hash

def leave_one_scenario_out(optimization_report,scenario_set,ledger=None):
    selected=optimization_report['decision']['selected_allocation_id'];row=next(r for r in optimization_report['rows'] if r['allocation_id']==selected)
    vals=row['scenario_utilities'];ids=sorted(vals);rows=[]
    for sid in ids:
        remain=[float(vals[x]) for x in ids if x!=sid]
        rows.append({'excluded_scenario_id':sid,'worst_case_utility':min(remain) if remain else 0.0,'mean_utility':sum(remain)/len(remain) if remain else 0.0})
        if ledger:ledger.consume('stability_resamples',1)
    spread=max((x['worst_case_utility'] for x in rows),default=0)-min((x['worst_case_utility'] for x in rows),default=0)
    out={'selected_allocation_id':selected,'rows':rows,'worst_case_spread':spread,'stable_under_leave_one_out':spread<=0.25,'research_only':True}
    out['stability_report_hash']=content_hash(out);return out

def radius_sensitivity(base_report,radii):
    selected=base_report['decision']['selected_allocation_id'];row=next(r for r in base_report['rows'] if r['allocation_id']==selected)
    rows=[{'radius':float(r),'conservative_value':float(row['distributionally_robust_utility'])-float(r)*float(row['utility_std'])} for r in sorted(map(float,radii))]
    out={'selected_allocation_id':selected,'rows':rows,'monotone_nonincreasing':all(rows[i]['conservative_value']>=rows[i+1]['conservative_value'] for i in range(len(rows)-1))}
    out['radius_sensitivity_hash']=content_hash(out);return out

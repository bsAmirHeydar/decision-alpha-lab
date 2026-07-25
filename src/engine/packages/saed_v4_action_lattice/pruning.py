def failed_constraint_names(evaluations:list[dict])->list[str]:
    return sorted(e['constraint_name'] for e in evaluations if e['status']=='violated')

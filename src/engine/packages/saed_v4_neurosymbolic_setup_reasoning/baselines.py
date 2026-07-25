from __future__ import annotations
from .canonical import content_hash

def preserve(approved_treatments,skip_id='skip',manual_id='manual_baseline'):
    ok=skip_id in approved_treatments and manual_id in approved_treatments
    rows=[{'baseline_id':'skip_all','treatment_id':skip_id,'preserved':skip_id in approved_treatments},{'baseline_id':'manual_doctrine','treatment_id':manual_id,'preserved':manual_id in approved_treatments}]
    return {'baselines':rows,'all_preserved':ok,'runtime_replaced':False,'report_hash':content_hash(rows)}

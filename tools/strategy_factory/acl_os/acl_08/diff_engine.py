from __future__ import annotations
from pathlib import Path
from .canonical import with_digest
from .io import load_json
def build_diff(report_id:str,current:dict,previous_root:Path|None)->dict:
    if previous_root is None:
        return with_digest({'schema_version':'1.0.0','report_id':report_id,'comparison_status':'FIRST_REPORT','previous_report_id':None,'material_change':False,'changed_dimensions':[],'reason_codes':['NO_PREVIOUS_REPORT']},'diff_digest')
    previous=load_json(previous_root/'reports/batch_report.json')
    dimensions=[]
    for k in ['validation_id','decision_counts','gate_status_counts','unknown_gate_frequency','reporting_eligible_count']:
        if previous.get(k)!=current.get(k): dimensions.append(k)
    return with_digest({'schema_version':'1.0.0','report_id':report_id,'comparison_status':'MATERIAL_CHANGE' if dimensions else 'NO_MATERIAL_CHANGE','previous_report_id':previous.get('report_id'),'previous_batch_report_digest':previous.get('batch_report_digest'),'material_change':bool(dimensions),'changed_dimensions':dimensions,'reason_codes':['MATERIAL_CHANGE_DETECTED' if dimensions else 'NO_MATERIAL_CHANGE']},'diff_digest')

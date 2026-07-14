from .contracts import *
from .canonical import sha256,stable_id

def diagnostic_summary(full_run,incremental_run,restart_report,timeframe_report,isolation_report,performance_report,acceptance_report):
    body={'full':full_run.run_id,'incremental':incremental_run.run_id,'restart':restart_report.report_id,'timeframe':timeframe_report.report_id,'isolation':isolation_report.report_id,'performance':performance_report.report_id,'acceptance':acceptance_report.report_id}
    return {'diagnostic_id':stable_id('FPREL-DIAG',body),'phase_id':'FP-I13','summary':body,'diagnostic_hash':sha256(body)}

from .contracts import CrossProductReport,HealthSnapshot

def dashboard_rows(report:CrossProductReport,health:HealthSnapshot):
    rows=[('overall_status',report.status.value),('health',health.state.value),('mismatch_count',str(report.mismatch_count)),('product_count',str(len(report.products)))]
    for pair in report.pairwise_reports:rows.append((f'pair:{pair.left_run_id[:12]}:{pair.right_run_id[:12]}',pair.status.value))
    return tuple(rows)

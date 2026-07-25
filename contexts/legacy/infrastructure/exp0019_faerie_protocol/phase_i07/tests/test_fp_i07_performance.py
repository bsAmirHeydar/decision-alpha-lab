from fp_i07_confirmation.benchmark import benchmark_store
def test_no_full_history_scan_claim(): assert benchmark_store(1000)['full_history_scan'] is False
def test_operations_scale_linearly(): assert benchmark_store(2000)['operations']==2*benchmark_store(1000)['operations']

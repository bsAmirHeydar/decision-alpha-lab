from fp_i09_ledger.identity import build_contender
from fp_i09_ledger.benchmark import benchmark_rank
from conftest import signal,eligible

def test_rank_benchmark_is_bounded(qkey):
    cs=[build_contender(signal(i),qkey,eligible(signal(i))) for i in range(200)]
    r=benchmark_rank(cs,20); assert r['contenders']==200 and r['elapsed_ms']<2000

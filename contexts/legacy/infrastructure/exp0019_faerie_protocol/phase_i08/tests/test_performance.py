from fp_i08_weekly.benchmark import benchmark_stack
from fp_i08_weekly.enums import WWDataState
from helpers import config,context
def test_stack_benchmark_runs():
 r=benchmark_stack(config(),tuple(context(i+1,confirmed=1_000_020_000+i*60_000) for i in range(25)),WWDataState.COMPLETE,1_005_000_000,100);assert r['ops_per_second']>0

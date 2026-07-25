from __future__ import annotations
import argparse, json
from dataclasses import asdict
from pathlib import Path
from .io import read_samples_csv
from .grouped import GroupedStatisticsEngine
from .confidence import normal_mean_interval, wilson_interval
from .bootstrap import cluster_bootstrap_mean_interval

def main(argv=None):
    p=argparse.ArgumentParser(prog='strategy-factory-statistics')
    p.add_argument('samples');p.add_argument('--group-by',default='all');p.add_argument('--output',required=True)
    args=p.parse_args(argv);samples=read_samples_csv(args.samples);dims=tuple(args.group_by.split(','))
    summaries=GroupedStatisticsEngine().summarize(samples,dims)
    out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps([asdict(x) for x in summaries],indent=2,sort_keys=True,default=int),encoding='utf-8')
    return 0
if __name__=='__main__': raise SystemExit(main())

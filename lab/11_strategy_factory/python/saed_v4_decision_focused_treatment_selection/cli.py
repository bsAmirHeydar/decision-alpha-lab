from pathlib import Path
import argparse,json
from .service import select_treatments

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--context',required=True);p.add_argument('--outcomes',required=True);p.add_argument('--proofs',required=True);p.add_argument('--upstream-hashes',required=True);p.add_argument('--output',required=True);a=p.parse_args(argv)
    load=lambda x:json.loads(Path(x).read_text(encoding='utf-8'))
    result=select_treatments(load(a.config),load(a.context),load(a.outcomes),load(a.proofs),load(a.upstream_hashes));Path(a.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8');return 0
if __name__=='__main__':raise SystemExit(main())
